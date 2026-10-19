# 영역 3: 컨테이너 오케스트레이션 (Container Orchestration - 22%)

> 컨테이너의 생명주기 관리, 자가 치유(Self-healing), 스케일링, 그리고 쿠버네티스의 3대 표준 인터페이스(CRI, CNI, CSI) 및 리눅스 컨테이너 격리 기술의 핵심 원리

---

## 1. 컨테이너 오케스트레이션이란?

단일 호스트에서 수십 개의 컨테이너를 실행할 때는 도커(Docker) 명령어로 충분하지만, 수백~수천 대의 서버(클러스터)에서 대규모 분산 컨테이너를 안정적으로 운영하려면 다음과 같은 자동화 메커니즘이 필요합니다:

```
┌────────────────────────────────────────────────────────────────────────┐
│               Core Features of Container Orchestration                 │
├────────────────────────────────────────────────────────────────────────┤
│ 1. 스케줄링 (Scheduling)   : 적절한 리소스를 가진 최적의 노드에 배치    │
│ 2. 자가 치유 (Self-Healing) : 컨테이너나 노드 장애 시 자동 재시작/재배치 │
│ 3. 수평 확장 (Auto-scaling) : 트래픽 부하에 따라 인스턴스 수 증감      │
│ 4. 서비스 디스커버리       : 동적으로 변하는 파드 IP를 단일 엔드포인트로 노출│
│ 5. 무중단 롤링 업데이트    : 서비스 중단 없이 신규 버전 점진 배포/롤백 │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 쿠버네티스 3대 표준 인터페이스 (CRI, CNI, CSI)

쿠버네티스는 특정 벤더에 종속되지 않도록 **플러그인 아키텍처**를 지향하며, 세 가지 핵심 표준 인터페이스 규격을 정의합니다:

```
                  ┌──────────────────────┐
                  │       kubelet        │
                  └──────────┬───────────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  CRI 플러그인 │      │  CNI 플러그인 │      │  CSI 플러그인 │
│ (컨테이너 실행)│      │  (네트워크 구성)│     │  (스토리지 연결)│
└──────┬───────┘      └──────┬───────┘      └──────┬───────┘
       ▼                     ▼                     ▼
 containerd / CRI-O   Calico / Cilium / Flannel AWS EBS / Ceph / NFS
```

### 1) CRI (Container Runtime Interface)
- `kubelet`이 다양한 컨테이너 런타임과 gRPC 통신을 통해 상호 작용할 수 있도록 하는 API 규격.
- **역할**: 이미지 다운로드, 컨테이너 생성/시작/중지/삭제.
- **대표 구현체**: `containerd` (CNCF Graduated), `CRI-O` (RedHat 주도 CNCF Graduated).
- **OCI (Open Container Initiative)**:
  - 이미지 규격(Image Spec) 및 런타임 규격(Runtime Spec)을 정의하는 오픈 표준.
  - 최하위 레벨 실행 도구: `runc` (OCI 런타임 표준 구현체).

### 2) CNI (Container Network Interface)
- 파드가 생성될 때 네트워크 인터페이스를 연결하고 IP 주소를 할당(IPAM)하는 플러그인 규격.
- **대표 구현체**:
  - `Flannel`: 간단한 오버레이 네트워크(VXLAN) 제공, 설정이 단순함.
  - `Calico`: BGP 라우팅 기반 고성능 네트워킹 및 정교한 **NetworkPolicy(보안 방화벽)** 지원.
  - `Cilium`: 리눅스 커널 **eBPF** 기술 기반으로 iptables 병목 없이 초고성능 라우팅 및 L7 보안 제공.

### 3) CSI (Container Storage Interface)
- 서드파티 스토리지 벤더가 쿠버네티스 코어 소스코드를 변경하지 않고도 자사의 스토리지를 볼륨 플러그인으로 연동할 수 있게 해주는 인터페이스.
- **동작 방식**: Volume 프로비저닝, 노드에 Attach, 파일시스템 Format 및 Mount.

---

## 3. 리눅스 커널의 컨테이너 격리 기술

컨테이너는 별도의 가상 머신(VM)이 아니라 **호스트 OS 커널을 공유하는 격리된 리눅스 프로세스**입니다. 다음 핵심 기술로 격리가 이루어집니다:

1. **Namespaces (이름공간 - 자원의 뷰 격리)**:
   - `PID Namespace`: 프로세스 ID 트리 격리 (컨테이너 내부에서 프로세스는 PID 1로 동작).
   - `NET Namespace`: 네트워크 인터페이스, IP, 라우팅 테이블 격리.
   - `MNT Namespace`: 파일시스템 마운트 포인트 격리.
   - `IPC Namespace`: 프로세스 간 통신(공유 메모리, 메시지 큐) 격리.
   - `UTS Namespace`: 호스트명(Hostname) 및 도메인명 격리.
   - `USER Namespace`: 호스트와 컨테이너 간 UID/GID 매핑 격리.

2. **Control Groups (cgroups - 자원 사용량 제한)**:
   - 특정 프로세스 그룹이 사용할 수 있는 시스템 리소스(CPU, Memory, Disk I/O, Network 대역폭)의 **상한선(Limit)**을 강제.
   - 쿠버네티스 `resources.limits.cpu`, `resources.limits.memory`가 바로 cgroups로 변환됨.

3. **보안 제어 기술**:
   - `Capabilities`: root 권한을 세분화하여 불필요한 시스템 콜 권한 박탈 (예: `CAP_NET_ADMIN`, `CAP_SYS_ADMIN`).
   - `seccomp (Secure Computing Mode)`: 프로세스가 호출할 수 있는 시스템 콜을 필터링하여 커널 공격 방지.
   - `AppArmor / SELinux`: MAC(Mandatory Access Control) 기반 파일 및 디바이스 접근 제어.

---

## 4. 고가용성(HA)과 자가 치유(Self-Healing) 메커니즘

- **Liveness Probe**: 컨테이너가 정상 작동 중인지 감지. 실패 시 컨테이너를 **재시작(Restart)**.
- **Readiness Probe**: 트래픽을 받을 준비가 되었는지 감지. 실패 시 Service의 **EndpointSlice에서 해당 파드 IP를 일시 제외**.
- **Startup Probe**: 부팅 시간이 오래 걸리는 레거시 애플리케이션의 초기화 동안 Liveness/Readiness의 실패 카운트를 일시 정지.
- **Pod Disruption Budget (PDB)**: 노드 업그레이드나 유지보수(Drain) 시 동시에 다운될 수 있는 파드의 최대 허용 수량을 지정하여 서비스 가용성 보장.

## 3.6 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)

이 섹션은 CBT 문제 은행(**questions_kcna_domain3.json 50문항**)의 모든 핵심 개념(`key_concept`), 정답 해설 및 빈출 함정 키워드와 1:1로 일치하도록 정리된 요약본입니다.

| 출제 핵심 개념 (Key Concept) | 공식 출제 의도 및 표준 인터페이스 정의 | CBT 대표 오답 함정 & 판별 포인트 |
| :--- | :--- | :--- |
| **CRI (Container Runtime Interface)** | kubelet과 컨테이너 런타임(containerd, CRI-O) 간의 gRPC 통신 사양 | • 쿠버네티스 1.24에서 레거시 dockershim이 완전히 제거되어 containerd 직접 통신 표준화. |
| **OCI (Open Container Initiative)** | 컨테이너 런타임 표준(runtime-spec, runc) 및 이미지 포맷 표준(image-spec) | • 특정 벤더(Docker)에 종속되지 않고 어떤 OCI 호환 런타임에서도 동일하게 컨테이너 실행 보장. |
| **CNI (Container Network Interface)** | 파드에 IP 주소를 할당하고 파드 간 오버레이 네트워크 통신을 구성하는 플러그인 사양 (Calico, Flannel, Cilium) | • CNI 플러그인이 미설치되면 클러스터의 모든 워커 노드는 `NotReady` 상태로 유지됨. |
| **CSI (Container Storage Interface)** | 서드파티 스토리지 벤더가 쿠버네티스 코어 코드 수정 없이 플러그인 형태로 볼륨을 연동할 수 있게 해주는 외부(Out-of-tree) 사양 | • In-tree 스토리지 플러그인 방식의 유지보수 한계를 극복하기 위해 제정됨. |
| **Namespaces vs cgroups (Linux)** | • **Namespaces**: 프로세스 간 격리 (PID, Mount, Network, IPC, UTS, User)<br>• **cgroups**: CPU, Memory, I/O 등 시스템 자원 사용량 제한 및 계측 | • 격리(Isolation)는 Namespaces가 담당하고, 자원 제한(Resource Limits)은 cgroups가 담당함 (혼동 금지). |
| **3대 컨테이너 프로브** | • **StartupProbe**: 애플리케이션 초기 기동 완료 대기<br>• **LivenessProbe**: 컨테이너 멈춤(Hang) 감지 시 강제 재시작<br>• **ReadinessProbe**: 준비 미완료 시 서비스 엔드포인트에서 트래픽만 격리 | • Liveness 실패는 파드를 재시작시키지만, Readiness 실패는 파드를 죽이지 않고 트래픽 인입만 차단함. |
