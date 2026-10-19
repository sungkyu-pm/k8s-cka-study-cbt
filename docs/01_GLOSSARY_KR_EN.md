# CKA 필수 한·영 쿠버네티스 대백과 사전 (Kubernetes Deep Glossary)

> **쿠버네티스 엔지니어 및 CKA 수험자를 위한 필수 핵심 전문 용어 사전**  
> 공식 영문 문서 및 에러 로그 완벽 대응 | 7대 영역 65+ 핵심 용어 총망라

---

## 1. 제어 평면 및 클러스터 아키텍처 (Control Plane & Architecture)

| 영문 용어 (English) | 한국어 명칭 | 심층 기술 설명 및 시험 포인트 |
| :--- | :--- | :--- |
| **Control Plane (Master Node)** | 컨트롤 플레인 (마스터 노드) | 클러스터 전체 상태를 관리, 스케줄링 결정, 이벤트를 감지 및 처리하는 핵심 제어 계층. apiserver, etcd, scheduler, controller-manager로 구성됨. |
| **kube-apiserver** | API 서버 | 제어 평면의 관문(Frontend) 역할을 하는 핵심 프로세스. 모든 외부 CLI(`kubectl`) 및 내부 에이전트의 REST API 요청을 인증, 인가, 어드미션 제어 후 etcd에 반영함. 수평 확장 가능(Stateless). |
| **etcd** | 분산 키-값 저장소 | 쿠버네티스의 모든 오브젝트 상태 및 구성 데이터를 영구 보관하는 일관성(Consistency) 있는 고가용성 Key-Value 저장소. Raft 합의 알고리즘 기반. CKA 시험 백업/복원 1순위. |
| **Raft Consensus & Quorum** | 래프트 합의 및 쿼럼 | etcd 노드 간 데이터 일관성을 유지하기 위한 과반수 합의 메커니즘. 쿼럼 공식 $Q = \lfloor N/2 \rfloor + 1$. 3대(쿼럼 2, 허용 1), 5대(쿼럼 3, 허용 2). 짝수 노드는 결함 허용도 증가 없이 오버헤드만 가중되므로 반드시 홀수로 구축. |
| **kube-scheduler** | 큐브 스케줄러 | 노드가 지정되지 않은 새로 생성된 파드를 감지하고, 리소스 요청량(requests), 노드 어피니티, 테인트/톨러레이션, 데이터 지역성을 평가하여 실행할 최적의 워커 노드를 결정(바인딩). |
| **kube-controller-manager** | 컨트롤러 매니저 | 노드 컨트롤러, 디플로이먼트 컨트롤러, 잡 컨트롤러 등 다양한 제어 루프(Control Loop)를 단일 프로세스로 실행하여 클러스터의 '현재 상태'를 '원하는 상태(Desired State)'로 지속 수렴시킴. |
| **cloud-controller-manager** | 클라우드 컨트롤러 매니저 | AWS, GCP, Azure 등 클라우드 제공업체의 인프라 API(로드밸런서 생성, 노드 라우팅, 볼륨 어태치 등)와 쿠버네티스 클러스터를 연동해주는 전용 컨트롤러. |
| **kubelet** | 큐브릿 | 각 워커 노드에서 systemd 데몬으로 실행되는 핵심 에이전트. API 서버로부터 전달받은 PodSpec을 기반으로 로컬 컨테이너 런타임에 지시하여 컨테이너를 구동, 헬스체크 및 리포팅 수행. |
| **kube-proxy** | 큐브 프록시 | 각 노드에서 실행되며 쿠버네티스 서비스(Service) 가상 IP(VIP)로 향하는 트래픽을 실제 백엔드 파드 IP로 포워딩하기 위해 호스트의 iptables 또는 IPVS 규칙을 실시간 관리. |
| **Container Runtime (CRI)** | 컨테이너 런타임 인터페이스 | kubelet이 컨테이너 런타임(containerd, CRI-O)과 통신하기 위한 gRPC 표준 사양. k8s 1.24부터 dockershim이 완전히 제거되어 containerd 직접 연동이 표준화됨. |
| **Container Network Interface (CNI)**| 컨테이너 네트워크 인터페이스| 파드 간 IP 할당 및 오버레이(VXLAN, IP-in-IP) 네트워크 통신을 구성하는 플러그인 사양 (Calico, Flannel, Cilium). CNI 미설치 시 노드가 `NotReady` 상태로 유지됨. |
| **Container Storage Interface (CSI)**| 컨테이너 스토리지 인터페이스| 서드파티 스토리지 벤더가 쿠버네티스 코어 코드를 수정하지 않고 외부(Out-of-tree) 플러그인 형태로 볼륨 드라이버를 연동할 수 있게 해주는 표준 인터페이스. |
| **Static Pods** | 스태틱 파드 | API 서버의 스케줄링 없이 특정 노드의 kubelet이 로컬 디렉토리(`/etc/kubernetes/manifests`)에 있는 매니페스트 파일을 직접 감시하여 실행하는 특별한 파드 (apiserver, etcd 등 제어 평면 구동용). |
| **Kubeconfig & Context** | 쿠브컨피그 및 컨텍스트 | 클러스터 접속 정보(clusters), 사용자 인증서(users), 작업 공간(contexts)을 기술하는 설정 파일(기본 경로: `~/.kube/config`). `kubectl config use-context`로 컨텍스트 전환. |

---

## 2. 워크로드 및 오케스트레이션 (Workloads & Orchestration)

| 영문 용어 (English) | 한국어 명칭 | 심층 기술 설명 및 시험 포인트 |
| :--- | :--- | :--- |
| **Pod** | 파드 | 쿠버네티스에서 생성 및 배포할 수 있는 가장 작은 컴퓨팅 단위. 하나 이상의 컨테이너가 동일한 네트워크 네임스페이스(IP, 포트)와 스토리지 볼륨을 공유함. |
| **Deployment** | 디플로이먼트 | 무상태(Stateless) 애플리케이션의 선언적 배포와 버전 관리를 담당. ReplicaSet을 하위에서 제어하여 무중단 롤링 업데이트 및 간편한 롤백(`rollout undo`) 지원. |
| **RollingUpdate Strategy** | 롤링 업데이트 전략 | 구버전 파드를 단계적으로 종료하면서 신버전 파드를 생성하는 무중단 배포 기법. `maxSurge`(동시 초과 생성 허용 비율)와 `maxUnavailable`(동시 불능 허용 비율)로 속도 제어. |
| **ReplicaSet** | 레플리카셋 | 명시된 수량(replicas)만큼의 파드가 클러스터 내에서 항상 정상 동작하도록 보장하는 컨트롤러. 라벨 셀렉터로 파드를 관리함. |
| **DaemonSet** | 데몬셋 | 클러스터의 모든(또는 특정 라벨을 가진) 노드에 파드를 정확히 1개씩 실행하도록 보장하는 컨트롤러. 모니터링 에이전트, 로그 수집기, CNI 네트워크 데몬 배포에 활용. |
| **StatefulSet** | 스테이트풀셋 | 데이터베이스(MySQL, Redis)처럼 상태 유지가 필요한 워크로드 관리. 예측 가능한 고유 서수 인덱스(web-0, web-1), 순차적 배포/삭제, Headless Service DNS 연계, 영구 볼륨(`volumeClaimTemplates`) 보장. |
| **Job & CronJob** | 잡 & 크론잡 | Job은 1회성 또는 병렬 배치 작업을 실행하고 완료 시 성공(0) 상태로 종료. CronJob은 지정된 스케줄 표현식에 따라 주기적으로 Job을 자동 생성. `concurrencyPolicy: Forbid`로 중복 실행 방지. |
| **Init Container** | 초기화 컨테이너 | 메인 컨테이너들이 기동되기 전에 순차적으로 먼저 실행되어 선행 준비 작업(DB 기동 대기, 설정 파일 다운로드 등)을 수행하는 컨테이너. 실패 시 메인 컨테이너는 실행되지 않음. |
| **Sidecar Container** | 사이드카 컨테이너 | 메인 컨테이너와 동일한 파드 내부에서 로깅, 프록시, 메트릭 수집 등의 보조 기능을 수행하는 컨테이너. `emptyDir` 볼륨을 통해 메인 컨테이너와 로그 파일 공유. |

---

## 3. 고급 스케줄링 및 노드 제어 (Scheduling & Node Management)

| 영문 용어 (English) | 한국어 명칭 | 심층 기술 설명 및 시험 포인트 |
| :--- | :--- | :--- |
| **NodeSelector** | 노드 셀렉터 | 파드를 특정 노드 라벨(`key: value`)에 배치하는 가장 단순한 1:1 매칭 스케줄링 방식. |
| **NodeAffinity** | 노드 선호도 | 파드가 특정 노드 라벨을 만족하는 노드에 배치되도록 표현식을 사용하는 고급 규칙. `required...`(조건 미일치 시 배정 불가 Hard Rule)과 `preferred...`(가능한 우선 배정 Soft Rule)로 나뉨. |
| **PodAffinity / PodAntiAffinity** | 파드 어피니티 / 안티어피니티 | 이미 실행 중인 다른 파드의 라벨을 기준으로 동일 노드/존에 모으거나(Affinity), 장애 격리를 위해 서로 다른 노드/존으로 분산 배치(AntiAffinity)하는 규칙. `topologyKey` 기준. |
| **Taint & Toleration** | 테인트와 톨러레이션 | **Taint**: 노드가 특정 파드를 밀어내도록 설정(`key=value:effect`).<br>**Toleration**: 파드가 노드의 Taint를 견디고 해당 노드에 스케줄될 수 있도록 허용.<br>Effect 3종: `NoSchedule`, `PreferNoSchedule`, `NoExecute`. |
| **Cordon & Uncordon** | 노드 스케줄링 격리/해제 | `cordon`: 노드를 `SchedulingDisabled` 상태로 변경하여 신규 파드 유입 차단.<br>`uncordon`: 노드를 다시 정상 스케줄링 가능 상태로 복귀. |
| **Drain** | 노드 파드 퇴거 | 노드 유지보수를 위해 노드 상의 기존 파드들을 안전하게 축출(Evict)하여 다른 노드로 이주시킴. 플래그: `--ignore-daemonsets`, `--delete-emptydir-data`. |
| **QoS Class** | 서비스 품질 클래스 | 리소스 경합 시 파드 퇴거 우선순위를 결정하는 3가지 등급: **Guaranteed**(requests=limits 완전 일치), **Burstable**(requests < limits), **BestEffort**(requests/limits 미설정, 퇴거 1순위). |

---

## 4. 서비스 및 네트워킹 (Services & Networking)

| 영문 용어 (English) | 한국어 명칭 | 심층 기술 설명 및 시험 포인트 |
| :--- | :--- | :--- |
| **ClusterIP Service** | 클러스터IP 서비스 | 쿠버네티스의 기본 서비스 타입. 클러스터 내부에서만 접근 가능한 가상 IP(VIP)를 할당하여 동적으로 변하는 파드들에 대한 단일 진입점과 L4 로드밸런싱 제공. |
| **NodePort Service** | 노드포트 서비스 | 모든 워커 노드의 특정 고정 포트(30000~32767)를 열어 `<NodeIP>:<NodePort>`로 외부 트래픽을 인입받아 백엔드 파드로 전달하는 서비스. |
| **LoadBalancer Service** | 로드밸런서 서비스 | AWS NLB/ALB, GCP LB 등 클라우드 공급자의 외부 로드밸런서를 자동 프로비저닝하여 퍼블릭 IP를 통해 서비스를 인터넷에 노출. |
| **ExternalName Service** | 익스터널네임 서비스 | 셀렉터나 VIP 없이 CoreDNS가 외부 CNAME 레코드(예: `my-db.company.com`)를 직접 반환하도록 설정하는 서비스 타입. |
| **Headless Service** | 헤드리스 서비스 | `spec.clusterIP: None`으로 설정하여 단일 VIP를 할당하지 않고, DNS 질의 시 백엔드 파드들의 실제 개별 IP 목록을 직접 반환하는 서비스. StatefulSet과 필수 결합. |
| **Endpoints & EndpointSlice** | 엔드포인트 / 엔드포인트 슬라이스 | 서비스의 셀렉터와 일치하는 정상(Ready) 상태 백엔드 파드 IP/포트 목록. 대규모 클러스터 성능 향상을 위해 100개 단위 분할 관리 구조인 EndpointSlice가 도입됨. |
| **Ingress** | 인그레스 | 클러스터 외부의 HTTP/HTTPS 트래픽을 내부 서비스로 라우팅하는 L7 규칙 리소스. 호스트 기반, 경로 기반(`pathType: Prefix/Exact`), SSL/TLS 종료 지원. |
| **Ingress Controller** | 인그레스 컨트롤러 | Ingress 리소스 규칙을 감시하여 실제 리버스 프록시(Nginx, Traefik 등) 프로세스를 동작시키고 트래픽을 라우팅하는 구현체. 컨트롤러가 없으면 Ingress는 동작하지 않음. |
| **CoreDNS** | 코어DNS | 클러스터 내부의 서비스 및 파드 도메인 해석을 담당하는 DNS 서버. 표준 FQDN: `<service>.<namespace>.svc.cluster.local`. |
| **NetworkPolicy** | 네트워크 정책 | 파드 간 인입(Ingress) 및 송출(Egress) 트래픽을 허용/차단하는 방화벽 규칙. CNI(Calico 등) 지원 필수. 기본 차단(Default Deny), `podSelector`, `namespaceSelector`, `ipBlock`. |

---

## 5. 스토리지 (Storage)

| 영문 용어 (English) | 한국어 명칭 | 심층 기술 설명 및 시험 포인트 |
| :--- | :--- | :--- |
| **PersistentVolume (PV)** | 영구 볼륨 | 관리자가 프로비저닝하거나 StorageClass에 의해 동적 생성된 실제 물리 스토리지 객체 (클러스터 전역 리소스). 파드 수명 주기와 완전히 독립적으로 데이터 유지. |
| **PersistentVolumeClaim (PVC)** | 영구 볼륨 요청서 | 사용자가 필요한 용량(storage)과 접근 모드(AccessModes)를 명시하여 PV를 요청하는 바인딩 티켓 (네임스페이스 단위 리소스). 파드는 PVC를 볼륨으로 마운트함. |
| **StorageClass (SC)** | 스토리지 클래스 | 관리자가 스토리지의 프로비저너(`provisioner`)와 속성을 정의하여, PVC 생성 시 백엔드 클라우드 볼륨을 실시간 자동 생성해주는 동적 프로비저닝(Dynamic Provisioning) 템플릿. |
| **AccessModes** | 접근 모드 | • **RWO (ReadWriteOnce)**: 단일 노드에서만 읽기/쓰기 마운트 허용 (EBS 등).<br>• **ROX (ReadOnlyMany)**: 여러 노드에서 읽기 전용 마운트 허용.<br>• **RWX (ReadWriteMany)**: 여러 노드에서 읽기/쓰기 동시 마운트 허용 (NFS, EFS 등). |
| **ReclaimPolicy** | 볼륨 반환 정책 | PVC가 삭제되었을 때 PV와 실제 스토리지를 어떻게 처리할지 결정 (`Retain`: 데이터 보존 후 Released 상태 대기, `Delete`: 실제 스토리지 에셋까지 즉시 영구 삭제). |
| **WaitForFirstConsumer** | 첫 사용자 대기 바인딩 | `StorageClass`의 `volumeBindingMode: WaitForFirstConsumer`. PVC 생성 즉시 볼륨을 만들지 않고, 파드가 어느 노드에 스케줄링될지 확정된 후에 볼륨을 프로비저닝하여 토폴로지 불일치 스케줄링 실패를 방지. |
| **subPath** | 서브패스 마운트 | 볼륨 내의 특정 단일 파일이나 하위 디렉토리만 컨테이너 경로에 마운트하여, 대상 디렉토리의 다른 기존 파일들을 덮어쓰지 않고 보존할 수 있게 해주는 속성. |

---

## 6. 보안 및 접근 제어 (Security & RBAC)

| 영문 용어 (English) | 한국어 명칭 | 심층 기술 설명 및 시험 포인트 |
| :--- | :--- | :--- |
| **RBAC** | 역할 기반 접근 제어 | Role-Based Access Control. 사용자가 수행할 수 있는 작업(verbs: get, list, watch, create, delete, update)을 리소스(resources: pods, deployments 등)별로 제한하는 인가 메커니즘. |
| **Role vs ClusterRole** | 롤 vs 클러스터롤 | **Role**: 특정 단일 네임스페이스 내에서만 유효한 권한 정의.<br>**ClusterRole**: 클러스터 전체 범위(nodes, namespaces 등 비네임스페이스 리소스 포함)의 권한 정의. |
| **RoleBinding vs ClusterRoleBinding** | 롤바인딩 vs 클러스터롤바인딩 | Role 또는 ClusterRole에서 정의한 권한을 사용자(User), 그룹(Group), 서비스어카운트(ServiceAccount)에 실제로 연결(바인딩)하는 리소스. |
| **ServiceAccount (SA)** | 서비스 어카운트 | 파드 내부에서 실행되는 프로세스가 쿠버네티스 API 서버와 통신할 때 인증(Authentication)을 위해 사용하는 전용 계정. |
| **CSR (CertificateSigningRequest)** | 인증서 서명 요청 | 신규 사용자나 컴포넌트가 클러스터 인증을 받기 위해 제출하는 인증서 서명 요청. 관리자가 `kubectl certificate approve`로 승인하면 x509 클라이언트 인증서가 발급됨. |
| **SecurityContext** | 보안 컨텍스트 | 파드 또는 컨테이너 수준에서 실행 권한(UID/GID, `runAsNonRoot: true`, `readOnlyRootFilesystem`, 리눅스 Capabilities 추가/제거)을 설정하여 보안을 강화. |

---

## 7. 문제 해결 및 모니터링 (Troubleshooting & Diagnostics)

| 영문 용어 (English) | 한국어 명칭 | 심층 기술 설명 및 시험 포인트 |
| :--- | :--- | :--- |
| **CrashLoopBackOff** | 크래시 루프 백오프 | 컨테이너가 기동 직후 비정상 종료(Exit Code 1, 2 등)되어 kubelet이 지수적 백오프 시간 간격으로 재시작을 반복하는 상태. 직전 로그(`kubectl logs -p`) 및 Exit Code 분석 필수. |
| **ImagePullBackOff / ErrImagePull** | 이미지 풀 실패 | 컨테이너 이미지를 다운로드하지 못해 파드가 기동되지 못하는 상태. 이미지 이름 오탈자, 태그 불일치, 프라이빗 레지스트리 인증 시크릿(`imagePullSecrets`) 누락이 주원인. |
| **OOMKilled (Exit Code 137)** | 메모리 부족 강제 종료 | 컨테이너가 지정된 `resources.limits.memory` 한도를 초과하여 리눅스 커널 OOM 킬러에 의해 강제 종료(SIGKILL)된 상태. Memory limit 상향 조정 필요. |
| **Pending** | 스케줄링 대기 상태 | 파드가 실행할 노드를 배정받지 못한 상태. 노드 리소스 부족(CPU/Memory requests 미충족), 노드 테인트 불일치, nodeSelector 오탈자가 주원인. `kubectl describe pod`의 Events 확인. |
| **Node NotReady** | 노드 불능 상태 | 워커 노드가 컨트롤 플레인에 정상 하트비트를 보고하지 못하는 상태. `kubelet` 서비스 중단, 인증서 만료, CNI 플러그인 장애, 디스크 풀(`DiskPressure`) 등이 원인. |
| **ReadinessProbe vs LivenessProbe** | 준비성 프로브 vs 활성 프로브 | **ReadinessProbe**: 실패 시 파드를 종료하지 않고 서비스 엔드포인트에서만 파드 IP를 격리하여 트래픽 인입 차단.<br>**LivenessProbe**: 실패 시 파드가 행(hang)에 빠진 것으로 간주하고 kubelet이 컨테이너를 강제 재시작. |
| **crictl** | 컨테이너 런타임 CLI | API 서버가 다운되었거나 kubelet 수준에서 직접 컨테이너를 점검할 때 사용하는 저수준 CRI 디버깅 도구 (`crictl ps -a`, `crictl logs <id>`). |
