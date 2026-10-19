# CKA (Certified Kubernetes Administrator) 종합 학습 가이드 & 실전 로드맵

> **Linux Foundation & CNCF 공식 커리큘럼 기준 5대 도메인 심층 분석**  
> 실전 핸즈온 시험 대비 | 시험장 원격 환경 최적화 | 도메인별 세부 출제 영역 & 학습 체크리스트

---

## 🔗 공식 시험 및 접수 링크 (Official Resources)

| 구분 | 주요 내용 및 공식 링크 |
| :--- | :--- |
| **🌐 Linux Foundation 공식 포털** | [Linux Foundation CKA Certification ↗](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/) |
| **📝 CNCF 공식 CKA 안내 페이지** | [CNCF CKA Overview ↗](https://www.cncf.io/certification/cka/) |
| **📖 쿠버네티스 공식 문서 (시험 중 열람 가능)** | [Kubernetes Official Documentation ↗](https://kubernetes.io/docs/) |
| **📄 공식 CKA 커리큘럼 GitHub** | [CNCF Curriculum Repository ↗](https://github.com/cncf/curriculum) |
| **🖥️ PSI 시험 예약 및 관리 대시보드** | [Linux Foundation Candidate Portal ↗](https://trainingportal.linuxfoundation.org/) |

---

## 1. 시험 개요 및 최신 출제 경향 (Exam Overview)

* **시험 형태**: 100% 실기(Performance-based / Hands-on) 문제 해결형 시험
* **시험 플랫폼**: PSI Secure Browser 기반 원격 데스크톱(XFCE GUI) 가상 머신 터미널
* **시험 시간**: **120분 (2시간)**
* **문항 수**: **15 ~ 17문항** (각 문항마다 배점이 4% ~ 9%로 상이)
* **합격 기준**: **66% 이상** 득점 시 합격
* **재응시 정책**: 시험 구매 시 **12개월 내 무료 1회 재응시(Free Retake)** 기본 제공
* **인증 유효 기간**: 취득일로부터 **2년**
* **열람 가능 리소스**: 시험 중 브라우저 탭 1개로 공식 문서 사이트 검색 가능
  - 허용 도메인: `https://kubernetes.io/docs/`, `https://kubernetes.io/blog/`, `https://github.com/kubernetes/`

---

## 2. 5대 도메인 세부 출제 요소 (Curriculum Breakdown)

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CKA 5대 도메인 출제 비중                        │
├───────────────────────────────┬────────────────────────────────────────┤
│ 1. Cluster Architecture (25%) │ kubeadm, etcd 백업/복구, RBAC, 업그레이드 │
│ 2. Workloads & Scheduling (15%)│ Deployment, DaemonSet, Affinity, Taints│
│ 3. Services & Networking (20%)│ Ingress, CoreDNS, NetworkPolicy, Services│
│ 4. Storage (10%)              │ PV, PVC, StorageClass, VolumeMounts   │
│ 5. Troubleshooting (30%)      │ Node NotReady, kubelet, Pod 장애, 로그 │
└───────────────────────────────┴────────────────────────────────────────┘
```

### 2.1 도메인 1: 클러스터 아키텍처, 설치 및 구성 (25%)
* **1.1 RBAC 기반 권한 제어**:
  - `Role`과 `RoleBinding`을 통한 네임스페이스 격리 권한 부여
  - `ClusterRole`과 `ClusterRoleBinding`을 통한 비네임스페이스 리소스(nodes, PV 등) 접근 제어
  - `ServiceAccount` 생성 및 토큰 바인딩
  - `kubectl auth can-i`를 활용한 권한 시뮬레이션 및 검증
* **1.2 kubeadm 클러스터 설치 및 노드 조인**:
  - `kubeadm init` 파라미터(`--pod-network-cidr`, `--apiserver-advertise-address`)
  - `kubeadm token create --print-join-command`로 신규 워커 노드 조인
  - CNI 플러그인(Calico, Flannel) 배포 및 인터페이스 상태 확인
* **1.3 etcd 데이터베이스 백업 및 복원**:
  - `etcdctl snapshot save`와 필수 TLS 플래그(`--cacert`, `--cert`, `--key`, `--endpoints`)
  - `etcdctl snapshot restore --data-dir=...` 복구 후 Static Pod 매니페스트 볼륨 경로 갱신
* **1.4 클러스터 버전 업그레이드**:
  - 컨트롤 플레인: `drain` ➔ `kubeadm upgrade plan/apply` ➔ `kubelet/kubectl` 업그레이드 ➔ `uncordon`
  - 워커 노드: `drain` ➔ `kubeadm upgrade node` ➔ `kubelet/kubectl` 업그레이드 ➔ `uncordon`
* **1.5 제어 평면 고가용성(HA) 아키텍처**:
  - etcd 쿼럼 원칙 ($Q = \lfloor N/2 \rfloor + 1$) 및 홀수 노드 구성 이유
  - Static Pod 매니페스트 경로(`/etc/kubernetes/manifests`)와 kubelet의 inotify 감시 메커니즘

### 2.2 도메인 2: 워크로드 및 스케줄링 (15%)
* **2.1 무상태/상태유지 애플리케이션 수명주기**:
  - `Deployment` 롤링 업데이트 전략(`maxSurge`, `maxUnavailable`), 롤백(`rollout undo`), 히스토리 관리
  - `DaemonSet`: 모든 노드 또는 특정 라벨 노드에 파드 1개씩 보장, 마스터 노드 toleration 적용
  - `StatefulSet`: 고유 서수 인덱스(web-0, web-1), Headless Service 연계, `volumeClaimTemplates`
* **2.2 배치 워크로드 관리**:
  - `Job`: `completions`, `parallelism`, `backoffLimit`(실패 재시도 횟수)
  - `CronJob`: cron 시간 표현식(`*/5 * * * *`), `concurrencyPolicy`(Allow, Forbid, Replace)
* **2.3 멀티 컨테이너 파드 패턴**:
  - 사이드카(Sidecar): 로그 수집 에이전트, 로컬 프록시
  - 어댑터(Adapter) & 앰배서더(Ambassador) 패턴
  - `emptyDir` 볼륨을 통한 컨테이너 간 디렉토리 실시간 공유
  - `initContainers`: 메인 애플리케이션 기동 전 순차 실행 및 선행 조건 대기
* **2.4 고급 파드 스케줄링 제어**:
  - `nodeSelector`: 단순 키-값 매칭
  - `nodeAffinity`: `requiredDuringSchedulingIgnoredDuringExecution`(Hard Rule) vs `preferred...`(Soft Rule)
  - `podAffinity` & `podAntiAffinity`: 고가용성 분산 배치 및 토폴로지 도메인(`topologyKey`)
  - `Taints & Tolerations`: 노드의 파드 기피(NoSchedule, PreferNoSchedule, NoExecute)
  - 스케줄러 우회 수동 스케줄링(`spec.nodeName`)
* **2.5 리소스 관리 및 보안 제약**:
  - `resources.requests` & `limits`: CPU(millicores), Memory(Mi/Gi)
  - QoS 클래스: `Guaranteed`, `Burstable`, `BestEffort`
  - `securityContext`: `runAsNonRoot: true`, `readOnlyRootFilesystem`, `capabilities`

### 2.3 도메인 3: 서비스 및 네트워킹 (20%)
* **3.1 서비스(Service) 핵심 아키텍처**:
  - 4대 서비스 타입: `ClusterIP`, `NodePort`(30000~32767), `LoadBalancer`, `ExternalName`(CNAME)
  - 3단계 포트 체계: `port`(서비스 VIP 포트), `targetPort`(파드 컨테이너 포트), `nodePort`(노드 물리 포트)
  - `Endpoints`와 `EndpointSlice`: 셀렉터 기반 자동 생성 vs 셀렉터 없는 수동 엔드포인트 구성
  - `Headless Service`(`clusterIP: None`): 단일 VIP 없이 파드 직접 IP A-레코드 반환
* **3.2 Ingress 라우팅 및 L7 트래픽 제어**:
  - Ingress 컨트롤러와 Ingress 리소스 명세의 역할 분담
  - 경로 기반(Path-based) 및 호스트 기반(Host-based) 라우팅 규칙
  - `pathType`: `Prefix` vs `Exact`
  - Nginx Ingress 어노테이션: `nginx.ingress.kubernetes.io/rewrite-target: /`
  - TLS/SSL 인증서 종료: `spec.tls` 및 Secret 매핑
* **3.3 클러스터 내부 DNS(CoreDNS) 서비스 디스커버리**:
  - FQDN 명명 규칙: `<service-name>.<namespace>.svc.cluster.local`
  - 파드 DNS 주소: `<pod-ip-with-hyphens>.<namespace>.pod.cluster.local`
  - `kube-system` 네임스페이스의 CoreDNS ConfigMap(`Corefile`) 구성
* **3.4 네트워크 정책(NetworkPolicy) 트래픽 격리**:
  - CNI 플러그인의 NetworkPolicy 지원 전제 조건 (Calico, Cilium 등)
  - 기본 완전 차단 정책(Default Deny All Ingress / Egress)
  - 소스/목적지 필터: `podSelector`, `namespaceSelector`, `ipBlock`(CIDR 및 `except` 예외 대역)
  - 단일 블록(AND) vs 복수 배열(OR) 문법 구별

### 2.4 도메인 4: 스토리지 (10%)
* **4.1 PV & PVC 바인딩 메커니즘**:
  - `PersistentVolume`(PV): 클러스터 전역 스토리지 리소스, 생명주기(Available, Bound, Released, Failed)
  - `PersistentVolumeClaim`(PVC): 사용자의 스토리지 요청서 (네임스페이스 단위)
  - 바인딩 3대 일치 조건: StorageClass, AccessModes, 용량(Capacity $\ge$ 요청량)
* **4.2 AccessModes 및 ReclaimPolicy**:
  - 접근 모드: `ReadWriteOnce`(RWO), `ReadOnlyMany`(ROX), `ReadWriteMany`(RWX), `ReadWriteOncePod`(RWOP)
  - 반환 정책: `Retain`(데이터 보존), `Delete`(스토리지 자동 삭제)
* **4.3 StorageClass와 동적 프로비저닝**:
  - 프로비저너(`provisioner`) 설정 및 기본 스토리지 클래스 어노테이션(`is-default-class: "true"`)
  - `volumeBindingMode: WaitForFirstConsumer`의 필요성 (토폴로지/노드 스케줄링 후 볼륨 생성)
  - 볼륨 온라인 확장: `allowVolumeExpansion: true` 설정 후 PVC 편집
* **4.4 파드 볼륨 마운트 기법**:
  - `volumes.persistentVolumeClaim.claimName`과 `volumeMounts.mountPath`
  - `subPath`를 활용한 기존 디렉토리 파일 보존 및 단일 파일 덮어쓰기
  - ConfigMap/Secret 볼륨 마운트 및 `defaultMode: 0400` 파일 권한 설정
  - Storage Object in Use Protection (`kubernetes.io/pvc-protection` finalizer)

### 2.5 도메인 5: 문제 해결 (30% - 최대 비중!)
* **5.1 노드 수준 장애 진단**:
  - 노드 `NotReady` 상태 원인 분석 (`kubectl describe node <node>`)
  - `systemctl status kubelet`, `journalctl -u kubelet -n 100 --no-pager` 로그 분석
  - `/var/lib/kubelet/config.yaml` 설정 오탈자 및 x509 인증서 만료 진단
* **5.2 제어 평면(Control Plane) 컴포넌트 디버깅**:
  - Static Pod 매니페스트(`/etc/kubernetes/manifests`) 오탈자 검사
  - API 서버 다운 시 컨테이너 런타임 CLI 활용: `crictl ps -a`, `crictl logs <id>`
  - etcd 디스크 부하 및 리더 선출 타임아웃 진단
* **5.3 애플리케이션 및 파드 장애 복구**:
  - `CrashLoopBackOff`: 애플리케이션 비정상 종료, 직전 로그(`kubectl logs -p`), Exit Code 확인
  - `ImagePullBackOff` / `ErrImagePull`: 이미지 태그 오탈자, `imagePullSecrets` 누락
  - `Pending`: 노드 CPU/메모리 부족, Taint 불일치, NodeSelector 오탈자 분석
  - `OOMKilled` (Exit Code 137): 메모리 한도 초과 분석 및 `limits.memory` 상향
* **5.4 서비스 및 네트워크 장애 디버깅**:
  - 서비스 타임아웃 시 `kubectl get ep <svc>`로 백엔드 엔드포인트 누락 확인
  - `readinessProbe` 실패로 인한 서비스 트래픽 격리 상태 감지
  - CoreDNS 파드 루프 에러(`Loop ... loop detected`) 해결
  - 임시 디버그 파드(`busybox:1.28`)를 통한 DNS/네트워크 핑 테스트
  - 파드 강제 삭제: `kubectl delete pod <name> --force --grace-period=0`

---

## 3. 시험장 실전 터미널 최적화 설정 (Speed Setup)

시험이 시작되면 가장 먼저 아래 4가지 환경 설정을 터미널에 적용하여 문제 풀이 속도를 2배 이상 높이세요:

```bash
# 1. kubectl 단축 별칭 설정
alias k=kubectl

# 2. 명령형 커맨드 YAML 추출 단축 환경변수 설정
export do="--dry-run=client -o yaml"
export now="--force --grace-period=0"

# 3. bash 자동완성 및 alias 연동
source <(kubectl completion bash)
complete -o default -F __start_kubectl k

# 4. vim YAML 들여쓰기 2칸 자동화 (~/.vimrc)
cat <<EOF > ~/.vimrc
set tabstop=2
set shiftwidth=2
set expandtab
set number
set paste
EOF
```

---

## 4. 합격을 위한 3단계 전략

```
[1단계: 개념 및 아키텍처 완전 이해]
  - docs/01_GLOSSARY_KR_EN.md 로 필수 한/영 용어 100% 매핑
  - docs/02 ~ 06 도메인별 세부 가이드로 매니페스트 구조와 아키텍처 학습

[2단계: 명령형 커맨드(Imperative CLI) 숙달]
  - docs/07_KUBECTL_CHEAT_SHEET.md 의 모든 명령어 암기
  - YAML 매니페스트를 손으로 타이핑하지 않고 'k run', 'k create' + $do 로 5초 만에 생성

[3단계: 1,250문항 무작위 문제은행 & 실전 CBT 반복]
  - [CBT 가상 실습] 탭에서 무작위 셔플 실전 모의고사 반복 풀이
  - 1회차: [학습 모드] 즉시 해설과 영/한 번역 토글로 오답 개념 보완
  - 2회차: [실전 모드] 120분 타이머를 켜고 66% 이상 고득점 달성
  - 오답노트 복습 기능으로 취약 도메인 완벽 정복
```
