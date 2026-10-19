# CKA 필수 한·영 쿠버네티스 용어사전 (Kubernetes Glossary)

> **시험 공략 팁**: CKA 및 쿠버네티스 실무에서는 영문 공식 문서와 에러 로그를 빠르고 정확하게 해석하는 능력이 필수적입니다. 본 용어사전을 통해 핵심 용어의 한·영 매핑과 개념을 마스터하세요.

---

## 1. 클러스터 아키텍처 & 제어 평면 (Control Plane & Architecture)

| 영문 용어 (English) | 한국어 명칭 | 핵심 설명 및 시험 출제 포인트 |
| :--- | :--- | :--- |
| **Control Plane (Master Node)** | 컨트롤 플레인 (마스터 노드) | 클러스터의 상태를 유지, 결정(스케줄링 등), 이벤트를 감지 및 반응하는 전사 제어 계층. |
| **kube-apiserver** | API 서버 | 쿠버네티스 제어 평면의 프론트엔드로 모든 REST 요청의 진입점. 수평 확장이 가능하도록 상태를 저장하지 않음(Stateless). |
| **etcd** | 분산 키-값 저장소 | 쿠버네티스의 모든 클러스터 데이터(상태 및 사양)를 보관하는 일관성 있는 고가용성 Key-Value 저장소. CKA 백업/복원 필수 출제. |
| **kube-scheduler** | 스케줄러 | 노드가 배정되지 않은 새로 생성된 파드를 감지하고, 리소스 요구사항과 제약조건(Affinity, Taint)에 맞춰 실행할 최적의 노드를 선택. |
| **kube-controller-manager** | 컨트롤러 매니저 | 노드 컨트롤러, 디플로이먼트 컨트롤러 등 여러 제어 루프를 단일 프로세스로 실행하여 클러스터 상태를 원하는 상태(Desired State)로 유지. |
| **kubelet** | 큐브릿 | 각 워커 노드에서 실행되는 핵심 에이전트. PodSpec을 전달받아 컨테이너가 정상적으로 실행되고 헬스체크를 통과하도록 보장. systemd 서비스로 동작. |
| **kube-proxy** | 큐브 프록시 | 각 노드에서 실행되는 네트워크 프록시. 노드의 네트워크 규칙(iptables 또는 IPVS)을 관리하여 Service IP로의 트래픽을 파드로 포워딩. |
| **Container Runtime (CRI)** | 컨테이너 런타임 인터페이스 | 컨테이너를 실제로 실행하는 소프트웨어 인터페이스 (예: containerd, CRI-O). Docker Shim은 v1.24부터 제거됨. |
| **Container Network Interface (CNI)**| 컨테이너 네트워크 인터페이스| 파드 간 오버레이 네트워크 통신을 구성하는 플러그인 인터페이스 (예: Calico, Flannel, Cilium). CKA에서 클러스터 초기화 시 CNI 미설치로 인한 NotReady 해결 단골 출제. |
| **Container Storage Interface (CSI)**| 컨테이너 스토리지 인터페이스| 서드파티 스토리지 벤더가 쿠버네티스에 블록 및 파일 스토리지를 플러그인 형태로 연결할 수 있게 해주는 표준 사양. |

---

## 2. 워크로드 & 오브젝트 (Workloads & Objects)

| 영문 용어 (English) | 한국어 명칭 | 핵심 설명 및 시험 출제 포인트 |
| :--- | :--- | :--- |
| **Pod** | 파드 | 쿠버네티스에서 생성하고 관리할 수 있는 배포의 가장 작은 단위. 하나 이상의 컨테이너가 스토리지와 네트워크 IP를 공유. |
| **Deployment** | 디플로이먼트 | 무상태(Stateless) 애플리케이션의 선언적 업데이트를 제공. ReplicaSet을 관리하여 롤링 업데이트 및 즉각적인 롤백 지원. |
| **ReplicaSet** | 레플리카셋 | 지정된 수의 파드 복제본(Replicas)이 항상 실행되도록 보장하는 컨트롤러. 보통 직접 생성하지 않고 Deployment를 통해 제어. |
| **DaemonSet** | 데몬셋 | 클러스터의 모든(또는 특정 레이블의) 노드마다 파드를 정확히 1개씩 실행하도록 보장. 모니터링 에이전트(Prometheus Node Exporter)나 로그 수집기(Fluentd)에 활용. |
| **StatefulSet** | 스테이트풀셋 | 고유한 네트워크 식별자, 순차적인 배포/스케일링, 안정적인 영구 스토리지를 필요로 하는 상태 유지형 워크로드(DB, Redis 클러스터 등) 관리. |
| **Job & CronJob** | 잡 & 크론잡 | Job은 1회성 또는 병렬 배치 작업을 실행하고 완료(Completed)되면 종료. CronJob은 cron 시간 표현식에 따라 주기적으로 Job을 생성. |
| **Init Container** | 초기화 컨테이너 | 메인 애플리케이션 컨테이너가 기동되기 전에 순차적으로 먼저 실행되어 사전 준비 작업(DB 대기, 설정 파일 다운로드 등)을 완료하는 컨테이너. |
| **Sidecar Container** | 사이드카 컨테이너 | 메인 컨테이너와 동일 파드 내에서 보조 역할(로그 수집, 프록시, 동기화 등)을 수행하는 컨테이너. k8s 1.28+부터 네이티브 사이드카 지원. |

---

## 3. 서비스 & 네트워킹 (Services & Networking)

| 영문 용어 (English) | 한국어 명칭 | 핵심 설명 및 시험 출제 포인트 |
| :--- | :--- | :--- |
| **Service (ClusterIP)** | 클러스터 내부 서비스 | 클러스터 내부에서만 접근 가능한 가상 IP(VIP)를 할당하여 동적으로 변경되는 파드들에 대해 단일 엔드포인트와 L4 로드밸런싱 제공 (기본 서비스 타입). |
| **NodePort** | 노드포트 서비스 | 모든 워커 노드의 특정 고정 포트(기본 30000~32767)를 열어 외부에서 `<NodeIP>:<NodePort>`로 접근할 수 있게 노출하는 서비스. |
| **LoadBalancer** | 로드밸런서 서비스 | 클라우드 공급자(AWS NLB/ALB, GCP LB 등)의 외부 로드밸런서를 자동 프로비저닝하여 퍼블릭 트래픽을 인입. |
| **Headless Service** | 헤드리스 서비스 | `clusterIP: None`으로 설정하여 단일 VIP 없이 DNS 조회를 통해 개별 파드들의 IP 목록을 직접 반환받는 서비스 (StatefulSet과 주로 결합). |
| **Ingress** | 인그레스 | 클러스터 외부에서 내부 서비스로의 HTTP/HTTPS 경로 기반(Path-based) 및 호스트 기반(Host-based) 라우팅, SSL/TLS 종료를 제공하는 L7 규칙 리소스. |
| **Ingress Controller** | 인그레스 컨트롤러 | Ingress 리소스 규칙을 실제로 읽어 트래픽을 프록시해주는 구현체 (예: ingress-nginx, Traefik). 컨트롤러가 없으면 Ingress 규칙은 동작하지 않음. |
| **CoreDNS** | 코어DNS | 클러스터 내부의 서비스 이름과 IP를 상호 조회해주는 내부 DNS 서버. `<service-name>.<namespace>.svc.cluster.local` 형식의 FQDN 해석. |
| **NetworkPolicy** | 네트워크 정책 | 파드 간의 인그레스(Ingress: 인입) 및 이그레스(Egress: 송출) 네트워크 트래픽을 라벨 셀렉터, 네임스페이스, IP 블록(CIDR) 기준으로 격리 및 허용하는 방화벽 규칙. CNI(Calico 등) 지원 필수. |

---

## 4. 스토리지 (Storage)

| 영문 용어 (English) | 한국어 명칭 | 핵심 설명 및 시험 출제 포인트 |
| :--- | :--- | :--- |
| **PersistentVolume (PV)** | 영구 볼륨 | 관리자가 프로비저닝하거나 StorageClass에 의해 동적으로 생성된 실제 스토리지 조각. 파드의 수명 주기와 완전히 독립적으로 데이터 유지. |
| **PersistentVolumeClaim (PVC)** | 영구 볼륨 요청 | 사용자가 특정 용량(Storage Size) 및 접근 모드(AccessModes)를 요청하는 바인딩 요청서. 파드는 PVC를 볼륨으로 마운트함. |
| **StorageClass (SC)** | 스토리지 클래스 | 관리자가 스토리지의 프로비저너(provisioner)와 파라미터를 정의하여, 사용자가 PVC를 생성할 때 백엔드 스토리지를 실시간 자동 생성(동적 프로비저닝)하게 해주는 템플릿. |
| **AccessModes** | 접근 모드 | • **RWO (ReadWriteOnce)**: 단일 노드에서만 읽기/쓰기 마운트 가능.<br>• **ROX (ReadOnlyMany)**: 여러 노드에서 읽기 전용으로 동시 마운트 가능.<br>• **RWX (ReadWriteMany)**: 여러 노드에서 읽기/쓰기로 동시 마운트 가능(NFS 등). |
| **ReclaimPolicy** | 볼륨 반환 정책 | PVC가 삭제되었을 때 PV와 실제 스토리지를 어떻게 처리할지 결정 (`Retain`: 데이터 보존, `Delete`: 실제 볼륨 즉시 삭제). |

---

## 5. 보안 및 접근 제어 (Security & RBAC)

| 영문 용어 (English) | 한국어 명칭 | 핵심 설명 및 시험 출제 포인트 |
| :--- | :--- | :--- |
| **RBAC** | 역할 기반 접근 제어 | Role-Based Access Control. 사용자가 수행할 수 있는 작업(verbs: get, list, watch, create, delete)을 리소스(resources: pods, deployments 등)별로 제한. |
| **Role vs ClusterRole** | 롤 vs 클러스터롤 | **Role**: 특정 단일 네임스페이스 내에서만 유효한 권한 정의.<br>**ClusterRole**: 클러스터 전체 범위(노드, PV, 네임스페이스 등 비네임스페이스 리소스 포함)의 권한 정의. |
| **RoleBinding vs ClusterRoleBinding** | 롤바인딩 vs 클러스터롤바인딩 | Role 또는 ClusterRole에서 정의한 권한을 특정 사용자(User), 그룹(Group), 서비스어카운트(ServiceAccount)에 실제로 부여(연결). |
| **ServiceAccount** | 서비스 어카운트 | 파드 내부에서 실행되는 프로세스가 쿠버네티스 API 서버와 통신할 때 인증(Authentication)을 위해 사용하는 계정. |
| **SecurityContext** | 보안 컨텍스트 | 파드 또는 컨테이너의 권한(UID/GID 실행, Privileged 모드, 읽기 전용 루트 파일시스템, Linux Capabilities 추가/제거)을 설정. |

---

## 6. 스케줄링 & 노드 유지보수 (Scheduling & Node Maintenance)

| 영문 용어 (English) | 한국어 명칭 | 핵심 설명 및 시험 출제 포인트 |
| :--- | :--- | :--- |
| **Taint & Toleration** | 테인트와 톨러레이션 | **Taint**: 노드가 특정 파드를 밀어내도록 설정 (`Key=Value:Effect`).<br>**Toleration**: 파드가 노드의 Taint를 견디고(용인하고) 해당 노드에 스케줄될 수 있도록 허용. |
| **NodeAffinity** | 노드 선호도 | 파드가 특정 라벨을 가진 노드에 우선적(Preferred) 또는 필수적(Required)으로 스케줄링되도록 지정하는 규칙. |
| **Cordon / Drain / Uncordon** | 노드 격리 및 배출 | • `cordon`: 노드를 신규 파드 스케줄링 금지(SchedulingDisabled)로 설정.<br>• `drain`: 노드 위의 기존 파드들을 안전하게 축출(Evict)하여 다른 노드로 이주.<br>• `uncordon`: 노드를 다시 정상 스케줄링 가능 상태로 복귀. |
| **Static Pod** | 스태틱 파드 | API 서버의 관여 없이 특정 노드의 kubelet이 로컬 디렉토리(`/etc/kubernetes/manifests`)의 매니페스트를 직접 감시하여 실행하는 제어 평면 파드(apiserver, etcd 등). |
