# 영역 2: 쿠버네티스 핵심 원리 (Kubernetes Fundamentals - 46%)

> KCNA 시험에서 가장 높은 비중(46%, 약 28문항)을 차지하는 핵심 영역. 쿠버네티스 아키텍처와 기본 리소스 모델, 네트워크, 스토리지, 보안의 동작 원리를 정확히 이해해야 합니다.

---

## 1. 쿠버네티스 클러스터 아키텍처 (Control Plane vs Worker Node)

```
                     ┌─────────────────────────────────────────────────────────┐
                     │                      CONTROL PLANE                      │
                     │  ┌─────────────────┐   ┌──────────────────────────────┐ │
                     │  │ kube-apiserver  │◄──┤      etcd (Distributed       │ │
                     │  │ (REST Gateway)  │   │      Key-Value Store)        │ │
                     │  └────────┬────────┘   └──────────────────────────────┘ │
                     │           │                                             │
                     │  ┌────────┴────────┐   ┌──────────────────────────────┐ │
                     │  │  kube-scheduler │   │   kube-controller-manager    │ │
                     │  │(Node Placement) │   │     (Reconcile Loops)        │ │
                     │  └─────────────────┘   └──────────────────────────────┘ │
                     └───────────┬─────────────────────────────────────────────┘
                                 │ TLS / HTTPS 통신
                                 ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                                 WORKER NODES                                 │
│  ┌─────────────────────────────────────┐  ┌────────────────────────────────┐ │
│  │ Node 1                              │  │ Node 2                         │ │
│  │ ┌───────────────┐ ┌───────────────┐ │  │ ┌───────────────┐ ┌──────────┐ │ │
│  │ │ kubelet       │ │ kube-proxy    │ │  │ │ kubelet       │ │kube-proxy│ │ │
│  │ └───────┬───────┘ └───────┬───────┘ │  │ └───────┬───────┘ └────┬─────┘ │ │
│  │         │ (CRI)           │(iptables)│  │         │              │      │ │
│  │ ┌───────▼───────┐ ┌───────▼───────┐ │  │ ┌───────▼───────┐ ┌────▼─────┐│ │
│  │ │ Container     │ │ Linux Kernel  │ │  │ │ Container     │ │Linux Net ││ │
│  │ │ Runtime (CRI) │ │ Network Rules │ │  │ │ Runtime (CRI) │ │Rules     ││ │
│  │ └───────┬───────┘ └───────────────┘ │  │ └───────┬───────┘ └──────────┘│ │
│  │         ▼                           │  │         ▼                      │ │
│  │ [ Pod A ]   [ Pod B ]               │  │ [ Pod C ]   [ Pod D ]          │ │
│  └─────────────────────────────────────┘  └────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 1) Control Plane 핵심 구성 요소
1. **`kube-apiserver`**:
   - 클러스터의 두뇌이자 모든 내부/외부 요청의 유일한 진입점.
   - RESTful API를 노출하며, 인증(Authentication), 인가(Authorization), Admission Control을 수행.
   - **유일하게 `etcd`와 직접 통신**하는 컴포넌트 (다른 컴포넌트는 반드시 apiserver를 경유).
2. **`etcd`**:
   - Raft 합의 알고리즘 기반의 분산 고가용성 키-값(Key-Value) 데이터베이스.
   - 클러스터의 모든 상태 정보(Desired State vs Actual State)가 영구 저장됨.
3. **`kube-scheduler`**:
   - 새로 생성된 파드 중 아직 노드가 배정되지 않은 파드를 감지.
   - 노드의 리소스 가용량(CPU/Mem), Taints/Tolerations, NodeAffinity 등을 평가(Filtering & Scoring)하여 가장 적합한 노드를 결정.
4. **`kube-controller-manager`**:
   - 지속적인 제어 루프(Reconciliation Loop)를 실행하여 현재 상태(Actual)를 원하는 상태(Desired)로 일치시킴.
   - Node Controller, Deployment/ReplicaSet Controller, EndpointSlice Controller, ServiceAccount Controller 등을 포함.

### 2) Worker Node 핵심 구성 요소
1. **`kubelet`**:
   - 각 노드에서 에이전트로 실행되는 필수 데몬.
   - apiserver로부터 PodSpec을 전달받아 컨테이너 런타임(CRI)에 컨테이너 생성을 요청하고, 헬스체크(Liveness/Readiness Probe) 수행 및 상태 보고.
2. **`kube-proxy`**:
   - 각 노드에서 실행되며 쿠버네티스 서비스(Service)의 가상 IP(ClusterIP)를 실제 파드 IP로 라우팅하기 위해 호스트의 iptables 또는 IPVS 규칙을 유지 관리.
3. **`Container Runtime` (CRI)**:
   - 실제 컨테이너의 라이프사이클(다운로드, 실행, 중지)을 담당하는 엔진 (예: `containerd`, `CRI-O`).

---

## 2. 쿠버네티스 핵심 워크로드 리소스 (Workload Resources)

| 리소스 | 주요 목적 및 특징 | 상태 보존 여부 |
| :--- | :--- | :---: |
| **Pod** | 쿠버네티스에서 생성 및 배포할 수 있는 가장 작은 컴퓨팅 단위. 하나 이상의 컨테이너(네트워크 IP 및 스토리지 볼륨 공유)로 구성. | 일회성(Ephemeral) |
| **ReplicaSet** | 명시된 수(`replicas`)의 동일한 파드가 항상 실행되도록 보장하는 저수준 컨트롤러. | 무상태(Stateless) |
| **Deployment** | 선언적 방식으로 파드와 ReplicaSet을 관리. 무중단 롤링 업데이트, 롤백, 일시 정지 및 재개 기능 제공. | 무상태(Stateless) |
| **StatefulSet** | 고유한 식별자(순차 번호 `web-0`, `web-1`), 안정적인 네트워크 식별자, 전용 PersistentVolume이 필요한 워크로드(DB, 카프카 등). | 유상태(Stateful) |
| **DaemonSet** | 클러스터의 모든 노드(또는 특정 노드들)에 파드를 정확히 하나씩 실행하도록 보장 (로그 수집기, 노드 모니터링 데몬). | 호스트 종속 |
| **Job** | 하나 이상의 파드를 실행하고, 지정된 개수의 파드가 정상 종료(Exit 0)될 때까지 대기하는 일회성 배치 작업. | 완료 후 종료 |
| **CronJob** | 크론 표현식(`*/5 * * * *`)에 따라 주기적인 시간에 Job을 예약 실행. | 주기적 완료 |

---

## 3. 서비스(Service) 및 네트워킹 핵심 원리

### 1) 쿠버네티스 기본 네트워킹 3대 원칙
1. 모든 파드는 NAT(Network Address Translation) 없이 다른 모든 파드와 고유 IP로 통신 가능.
2. 노드의 에이전트(kubelet 등)는 동일 노드의 모든 파드와 통신 가능.
3. 파드의 IP는 외부와 내부에서 동일하게 인식됨.

### 2) 서비스 유형 (Service Types)
- **ClusterIP** (기본값):
  - 클러스터 내부에서만 접근 가능한 가상 IP(Virtual VIP)를 할당.
  - 마이크로서비스 간 내부 통신용.
- **NodePort**:
  - 클러스터의 모든 노드에 동일한 고정 포트(범위: `30000-32767`)를 열어 외부 트래픽을 허용.
  - `<NodeIP>:<NodePort>` 형태로 접근 가능.
- **LoadBalancer**:
  - 클라우드 공급자(AWS, GCP, Azure 등)의 외부 로드 밸런서를 자동으로 프로비저닝.
- **ExternalName**:
  - CNAME DNS 레코드를 반환하여 클러스터 외부의 도메인(예: `my-db.example.com`)으로 트래픽을 직접 매핑.
- **Headless Service (`clusterIP: None`)**:
  - 가상 VIP를 할당하지 않고, DNS 쿼리 시 백엔드 파드들의 개별 IP 목록을 직접 반환 (StatefulSet의 피어 디스커버리에 필수).

### 3) Ingress (인그레스)
- 클러스터 외부에서 내부 서비스로의 HTTP/HTTPS 경로 기반(Path-based) 및 호스트 기반(Host-based) 라우팅 규칙을 제공하는 L7(Application Layer) 리소스.
- 실제 동작을 위해서는 **Ingress Controller** (예: Ingress-NGINX, Traefik, Envoy)가 반드시 설치되어 있어야 함.

---

## 4. 스토리지 추상화 모델 (Storage Abstraction)

```
[ Developer / Application ]
         │
         ▼ 요청 (Request)
┌──────────────────┐               ┌───────────────────────┐
│ PersistentVolume │   자동 바인딩  │    PersistentVolume   │
│   Claim (PVC)    ├──────────────►│         (PV)          │
└──────────────────┘               └───────────┬───────────┘
         │                                     │ 실제 볼륨 프로비저닝
         ▼ StorageClass 지정                   ▼
┌──────────────────┐               ┌───────────────────────┐
│   StorageClass   ├──────────────►│ AWS EBS / NFS / Ceph  │
│  (Dynamic Prov)  │               │   (Cloud Storage)     │
└──────────────────┘               └───────────────────────┘
```

1. **PersistentVolume (PV)**: 관리자가 프로비저닝하거나 StorageClass에 의해 동적으로 생성된 실제 클러스터 스토리지 리소스.
2. **PersistentVolumeClaim (PVC)**: 사용자가 특정 용량(`storage: 10Gi`)과 접근 모드(`accessModes`)를 지정하여 스토리지를 요청하는 티켓.
3. **StorageClass**: 스토리지의 종류(SSD, HDD, 네트워크 파일시스템)와 **동적 프로비저닝(Dynamic Provisioning)**을 위한 CSI 플러그인을 정의.
4. **접근 모드 (Access Modes)**:
   - `ReadWriteOnce` (RWO): 단일 노드에서 읽기/쓰기로 마운트 가능.
   - `ReadOnlyMany` (ROX): 여러 노드에서 읽기 전용으로 동시 마운트 가능.
   - `ReadWriteMany` (RWX): 여러 노드에서 읽기/쓰기로 동시 마운트 가능 (NFS, CephFS 등).

---

## 5. 보안 및 접근 제어 (RBAC & Security)

### 1) 인증(Authentication) vs 인가(Authorization)
- **인증 (Authentication)**: 요청자가 "누구인지(Who are you?)"를 확인 (X.509 인증서, OIDC 토큰, ServiceAccount 토큰).
- **인가 (Authorization)**: 인증된 주체가 "해당 리소스에 대해 특정 액션을 수행할 권한이 있는지(Can you do this?)"를 확인 (RBAC, ABAC, Webhook).

### 2) RBAC 리소스 구조
- **Role vs ClusterRole**:
  - `Role`: 특정 **네임스페이스(Namespace)** 내의 리소스에 대한 권한 정의.
  - `ClusterRole`: 클러스터 전체 범위의 리소스(Node, PV, Namespace) 또는 모든 네임스페이스에 적용되는 권한 정의.
- **RoleBinding vs ClusterRoleBinding**:
  - `RoleBinding`: 정의된 Role(또는 ClusterRole)을 특정 네임스페이스 내의 사용자/그룹/ServiceAccount에 바인딩.
  - `ClusterRoleBinding`: ClusterRole을 클러스터 전체 범위에서 바인딩.

## 2.6 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)

이 섹션은 CBT 문제 은행(**questions_kcna_domain2.json 100문항**)의 모든 핵심 개념(`key_concept`), 정답 해설 및 빈출 함정 키워드와 1:1로 일치하도록 정리된 요약본입니다.

| 출제 핵심 개념 (Key Concept) | 공식 출제 의도 및 쿠버네티스 원리 | CBT 대표 오답 함정 & 판별 포인트 |
| :--- | :--- | :--- |
| **Control Plane 컴포넌트 분담** | • **kube-apiserver**: 유일하게 etcd와 직접 통신하는 관문 REST API<br>• **etcd**: 분산 합의(Raft) 기반 고가용성 키-값 저장소<br>• **kube-scheduler**: 노드 리소스 평가 후 파드 배치 결정<br>• **kube-controller-manager**: Desired State 수렴 제어 루프 | • kube-scheduler는 파드를 직접 실행하는 프로세스가 아님 (실행은 워커 노드의 kubelet이 담당).<br>• etcd와 직접 통신할 수 있는 컴포넌트는 오직 apiserver뿐임. |
| **Worker Node 에이전트** | • **kubelet**: 노드 데몬, PodSpec 기반 컨테이너 구동/상태 보고<br>• **kube-proxy**: 서비스 가상 IP 포워딩 (iptables/IPVS)<br>• **CRI**: 컨테이너 런타임(containerd) | • kubelet은 쿠버네티스 파드로 뜨지 않고 노드 OS의 systemd 데몬으로 직접 실행됨. |
| **워크로드 컨트롤러 5종 비교** | • **Deployment**: 무상태 롤링 업데이트<br>• **DaemonSet**: 모든 노드 1개씩 실행 (로깅/모니터링)<br>• **StatefulSet**: 고유 식별자, 순차 배포, Headless 연계, DB<br>• **Job**: 1회성 완료 작업<br>• **CronJob**: 주기적 스케줄링 | • 모니터링 데몬 배포에 Deployment를 쓰면 특정 노드에 몰릴 수 있으므로 반드시 DaemonSet 사용. |
| **서비스 4대 타입** | `ClusterIP`(내부), `NodePort`(외부 30000~32767), `LoadBalancer`(클라우드 LB), `ExternalName`(CNAME) | • Headless 서비스는 `spec.clusterIP: None`으로 설정하여 DNS 직접 질의 지원. |
| **RBAC 인가 체계** | `Role` & `RoleBinding` (네임스페이스 단위) vs `ClusterRole` & `ClusterRoleBinding` (클러스터 전역) | • 노드(`nodes`)나 네임스페이스 자체는 비네임스페이스 리소스이므로 RoleBinding이 아닌 ClusterRoleBinding 필요. |
