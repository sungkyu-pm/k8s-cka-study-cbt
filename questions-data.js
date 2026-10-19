// Kubernetes Certification (CKA / CKAD) Full Question Bank
const EXAM_DATA = {
  "domain1": [
    {
      "id": "D1-Q01",
      "domain": "Domain 1",
      "domain_name": "클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration)",
      "question_en": "You need to create a snapshot backup of an existing etcd instance running as a static pod. The etcd client certificates are located at /etc/kubernetes/pki/etcd/server.crt and /etc/kubernetes/pki/etcd/server.key, and the CA certificate is at /etc/kubernetes/pki/etcd/ca.crt. Which command correctly creates the snapshot at /var/lib/etcd-snapshot.db?",
      "question_kr": "스태틱 파드로 실행 중인 기존 etcd 인스턴스의 스냅샷 백업을 생성해야 합니다. etcd 클라이언트 인증서는 /etc/kubernetes/pki/etcd/server.crt 및 server.key에 위치하고, CA 인증서는 ca.crt에 위치합니다. /var/lib/etcd-snapshot.db 경로에 스냅샷을 올바르게 생성하는 명령어는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "etcdctl backup save --endpoints=https://127.0.0.1:2379 /var/lib/etcd-snapshot.db",
          "text_kr": "etcdctl backup save --endpoints=https://127.0.0.1:2379 /var/lib/etcd-snapshot.db"
        },
        {
          "key": "B",
          "text_en": "ETCDCTL_API=3 etcdctl snapshot save /var/lib/etcd-snapshot.db --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key",
          "text_kr": "ETCDCTL_API=3 etcdctl snapshot save /var/lib/etcd-snapshot.db --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key"
        },
        {
          "key": "C",
          "text_en": "kubectl snapshot etcd /var/lib/etcd-snapshot.db --all-certificates",
          "text_kr": "kubectl snapshot etcd /var/lib/etcd-snapshot.db --all-certificates"
        },
        {
          "key": "D",
          "text_en": "kubeadm backup etcd --output=/var/lib/etcd-snapshot.db",
          "text_kr": "kubeadm backup etcd --output=/var/lib/etcd-snapshot.db"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• etcd v3 API를 사용할 때는 환경변수 `ETCDCTL_API=3`을 지정해야 하며, `snapshot save <경로>` 명령어를 사용합니다.\n• 보안이 활성화된 etcd 클러스터 통신을 위해 `--cacert`, `--cert`, `--key` 옵션으로 유효한 인증서와 키를 반드시 함께 전달해야 합니다.\n• A는 인증서 플래그와 snapshot save 문법이 누락되었습니다.\n• C와 D는 존재하지 않는 명령어입니다.",
      "key_concept": "etcdctl snapshot save, TLS Authentication Flags (--cacert, --cert, --key)"
    },
    {
      "id": "D1-Q02",
      "domain": "Domain 1",
      "domain_name": "클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration)",
      "question_en": "You are tasked with upgrading the control plane node of a Kubernetes cluster using kubeadm from version 1.30.0 to 1.31.0. Before performing the package upgrade, what is the recommended procedure to ensure running workloads on the control plane node are safely evicted or ignored?",
      "question_kr": "kubeadm을 사용하여 쿠버네티스 컨트롤 플레인 노드를 버전 1.30.0에서 1.31.0으로 업그레이드해야 합니다. 패키지 업그레이드를 수행하기 전에 컨트롤 플레인 노드에서 실행 중인 워크로드를 안전하게 퇴거하거나 무시하도록 조치하는 권장 절차는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "kubectl delete node controlplane --force",
          "text_kr": "kubectl delete node controlplane --force"
        },
        {
          "key": "B",
          "text_en": "kubectl drain controlplane --ignore-daemonsets",
          "text_kr": "kubectl drain controlplane --ignore-daemonsets"
        },
        {
          "key": "C",
          "text_en": "kubectl cordon controlplane --delete-emptydir-data",
          "text_kr": "kubectl cordon controlplane --delete-emptydir-data"
        },
        {
          "key": "D",
          "text_en": "kubeadm upgrade prepare controlplane",
          "text_kr": "kubeadm upgrade prepare controlplane"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• 노드 유지보수 및 업그레이드 전에는 `kubectl drain <노드이름> --ignore-daemonsets`를 실행하여 노드를 스케줄링 불능(cordon) 상태로 만들고 기존 파드들을 안전하게 다른 노드로 축출(evict)해야 합니다.\n• DaemonSet 파드는 노드에서 배출될 수 없으므로 `--ignore-daemonsets` 플래그를 붙여야 drain 명령이 정상 완료됩니다.\n• 업그레이드가 완료된 후에는 `kubectl uncordon <노드이름>`으로 복구합니다.",
      "key_concept": "kubectl drain, Node Maintenance, Cluster Upgrade Procedure"
    },
    {
      "id": "D1-Q03",
      "domain": "Domain 1",
      "domain_name": "클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration)",
      "question_en": "A junior administrator needs read-only access to view and list Pods only within the 'development' namespace. Which set of RBAC resources must be created to achieve this without granting cluster-wide permissions?",
      "question_kr": "주니어 관리자가 'development' 네임스페이스 내에서만 파드를 조회(get)하고 목록화(list)할 수 있는 읽기 전용 권한이 필요합니다. 클러스터 전체 권한을 부여하지 않고 이를 달성하기 위해 생성해야 하는 RBAC 리소스 조합은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "A ClusterRole in the development namespace and a ClusterRoleBinding",
          "text_kr": "development 네임스페이스의 ClusterRole 및 ClusterRoleBinding"
        },
        {
          "key": "B",
          "text_en": "A Role defined in the development namespace and a RoleBinding in the development namespace",
          "text_kr": "development 네임스페이스에 정의된 Role과 development 네임스페이스의 RoleBinding"
        },
        {
          "key": "C",
          "text_en": "A ServiceAccount bound directly to the PodSpec without RBAC",
          "text_kr": "RBAC 없이 PodSpec에 직접 바인딩된 ServiceAccount"
        },
        {
          "key": "D",
          "text_en": "A ClusterRoleBinding scoped with a namespace filter flag",
          "text_kr": "네임스페이스 필터 플래그가 지정된 ClusterRoleBinding"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• 특정 네임스페이스로 범위를 제한할 때는 반드시 네임스페이스 리소스인 `Role`과 `RoleBinding`을 해당 네임스페이스(`development`) 내에 생성해야 합니다.\n• ClusterRole은 클러스터 전역 범위이며, ClusterRoleBinding을 사용하면 모든 네임스페이스에 권한이 전파되므로 최소 권한 원칙(Principle of Least Privilege)에 위배됩니다.",
      "key_concept": "RBAC Role vs ClusterRole, RoleBinding Scope"
    },
    {
      "id": "D1-Q04",
      "domain": "Domain 1",
      "domain_name": "클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration)",
      "question_en": "How does kubelet know to start and manage static pods such as kube-apiserver and kube-controller-manager on a control plane node?",
      "question_kr": "kubelet은 컨트롤 플레인 노드에서 kube-apiserver 및 kube-controller-manager와 같은 스태틱 파드(Static Pods)를 어떻게 인식하고 시작 및 관리합니까?",
      "options": [
        {
          "key": "A",
          "text_en": "The API server sends a webhook request to kubelet on boot.",
          "text_kr": "API 서버가 부팅 시 kubelet에 웹훅 요청을 보냅니다."
        },
        {
          "key": "B",
          "text_en": "kubelet watches the staticPodPath directory (default: /etc/kubernetes/manifests) defined in its configuration file.",
          "text_kr": "kubelet이 설정 파일에 정의된 staticPodPath 디렉토리(기본값: /etc/kubernetes/manifests)를 직접 감시합니다."
        },
        {
          "key": "C",
          "text_en": "systemd launches static pods using docker run commands directly.",
          "text_kr": "systemd가 docker run 명령어로 스태틱 파드를 직접 실행합니다."
        },
        {
          "key": "D",
          "text_en": "kube-scheduler assigns static pods to node-0 based on affinity.",
          "text_kr": "kube-scheduler가 어피니티에 따라 스태틱 파드를 node-0에 할당합니다."
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• 스태틱 파드는 API 서버의 개입 없이 노드의 `kubelet` 데몬이 특정 로컬 디렉토리(기본: `/etc/kubernetes/manifests`)에 위치한 YAML 매니페스트 파일을 주기적으로 스캔하여 직접 띄우고 라이프사이클을 관리합니다.\n• 컨트롤 플레인의 핵심 컴포넌트(apiserver, etcd, scheduler, controller-manager)는 모두 스태틱 파드로 구동됩니다.",
      "key_concept": "Static Pods, kubelet staticPodPath, Control Plane Bootstrap"
    },
    {
      "id": "D1-Q05",
      "domain": "Domain 1",
      "domain_name": "클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration)",
      "question_en": "An etcd cluster consists of 5 members. According to the Raft consensus algorithm, what is the minimum quorum required, and how many node failures can this cluster tolerate while remaining operational?",
      "question_kr": "5개의 멤버로 구성된 etcd 클러스터가 있습니다. Raft 분산 합의 알고리즘에 따를 때, 필요한 최소 쿼럼(Quorum) 수와 정상 작동을 유지하면서 허용할 수 있는 최대 노드 장애 대수는 각각 얼마입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "Quorum: 2, Tolerated Failures: 3",
          "text_kr": "쿼럼: 2, 허용 장애 대수: 3"
        },
        {
          "key": "B",
          "text_en": "Quorum: 3, Tolerated Failures: 2",
          "text_kr": "쿼럼: 3, 허용 장애 대수: 2"
        },
        {
          "key": "C",
          "text_en": "Quorum: 4, Tolerated Failures: 1",
          "text_kr": "쿼럼: 4, 허용 장애 대수: 1"
        },
        {
          "key": "D",
          "text_en": "Quorum: 5, Tolerated Failures: 0",
          "text_kr": "쿼럼: 5, 허용 장애 대수: 0"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• etcd의 쿼럼 공식은 $(N/2) + 1$ (과반수)입니다.\n• 5개 노드의 경우 과반수는 3개 노드입니다.\n• 따라서 $5 - 3 = 2$대의 노드가 다운되더라도 3대가 살아있으므로 정상적으로 쓰기 및 합의 작업이 가능합니다.",
      "key_concept": "etcd Quorum, Raft Consensus, High Availability"
    },
    {
      "id": "D1-Q06",
      "domain": "Domain 1",
      "domain_name": "클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration)",
      "question_en": "Which command allows an administrator to verify if user 'developer-jane' has permission to delete deployments in the 'staging' namespace?",
      "question_kr": "관리자가 'staging' 네임스페이스에서 'developer-jane' 사용자가 디플로이먼트를 삭제(delete)할 수 있는 권한이 있는지 신속하게 검증할 수 있는 명령어는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "kubectl auth can-i delete deployments --as=developer-jane -n staging",
          "text_kr": "kubectl auth can-i delete deployments --as=developer-jane -n staging"
        },
        {
          "key": "B",
          "text_en": "kubectl get permissions --user=developer-jane --namespace=staging",
          "text_kr": "kubectl get permissions --user=developer-jane --namespace=staging"
        },
        {
          "key": "C",
          "text_en": "kubectl describe rbac --user=developer-jane -n staging",
          "text_kr": "kubectl describe rbac --user=developer-jane -n staging"
        },
        {
          "key": "D",
          "text_en": "kubectl check-access delete deployments -u developer-jane",
          "text_kr": "kubectl check-access delete deployments -u developer-jane"
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• `kubectl auth can-i <동사> <리소스> [--as=<사용자>] [-n <네임스페이스>]` 명령어를 사용하면 특정 사용자나 서비스어카운트의 권한 여부를 `yes` 또는 `no`로 즉시 테스트할 수 있어 CKA 시험에서 권한 부여 후 셀프 검증 시 필수적입니다.",
      "key_concept": "kubectl auth can-i, Impersonation (--as), RBAC Verification"
    },
    {
      "id": "D1-Q07",
      "domain": "Domain 1",
      "domain_name": "클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration)",
      "question_en": "After initializing a single-node control plane using `kubeadm init`, what is the critical component that must be deployed before worker nodes can join and CoreDNS pods can transition from Pending to Running?",
      "question_kr": "`kubeadm init`을 사용하여 싱글 노드 컨트롤 플레인을 초기화한 직후, 워커 노드가 조인하고 CoreDNS 파드가 Pending에서 Running 상태로 전환되기 위해 반드시 배포해야 하는 핵심 컴포넌트는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "Metrics Server",
          "text_kr": "Metrics Server"
        },
        {
          "key": "B",
          "text_en": "A Container Network Interface (CNI) plugin (e.g., Calico, Flannel, Cilium)",
          "text_kr": "컨테이너 네트워크 인터페이스(CNI) 플러그인 (예: Calico, Flannel, Cilium)"
        },
        {
          "key": "C",
          "text_en": "Ingress Controller",
          "text_kr": "인그레스 컨트롤러 (Ingress Controller)"
        },
        {
          "key": "D",
          "text_en": "MetalLB LoadBalancer",
          "text_kr": "MetalLB 로드밸런서"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• kubeadm으로 클러스터를 초기화하면 기본적으로 네트워크 플러그인이 설치되지 않은 상태입니다.\n• CNI 플러그인(Calico, Flannel 등)이 설치되어 노드에 IP 대역이 할당되고 파드 간 통신 오버레이가 설정되어야 노드가 Ready 상태가 되고 CoreDNS 파드가 구동됩니다.",
      "key_concept": "CNI Plugin Installation, Cluster Bootstrap, CoreDNS Pending State"
    },
    {
      "id": "D1-Q08",
      "domain": "Domain 1",
      "domain_name": "클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration)",
      "question_en": "You need to restore etcd from a backup snapshot to a new data directory /var/lib/etcd-new. After running `etcdctl snapshot restore /tmp/backup.db --data-dir=/var/lib/etcd-new`, what final step is required to make the etcd static pod use the new data?",
      "question_kr": "백업 스냅샷으로부터 새로운 데이터 디렉토리 /var/lib/etcd-new로 etcd를 복원해야 합니다. `etcdctl snapshot restore /tmp/backup.db --data-dir=/var/lib/etcd-new`를 실행한 후, etcd 스태틱 파드가 새 데이터를 사용하도록 만들기 위해 수행해야 하는 마지막 필수 작업은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "Update the hostPath volume in /etc/kubernetes/manifests/etcd.yaml to point to /var/lib/etcd-new.",
          "text_kr": "/etc/kubernetes/manifests/etcd.yaml 파일의 hostPath 볼륨 경로를 /var/lib/etcd-new로 수정합니다."
        },
        {
          "key": "B",
          "text_en": "Run `kubectl rollout restart pod etcd -n kube-system`.",
          "text_kr": "`kubectl rollout restart pod etcd -n kube-system`을 실행합니다."
        },
        {
          "key": "C",
          "text_en": "Restart docker using `systemctl restart docker`.",
          "text_kr": "`systemctl restart docker`로 도커를 재시작합니다."
        },
        {
          "key": "D",
          "text_en": "Re-run `kubeadm init phase etcd local`.",
          "text_kr": "`kubeadm init phase etcd local`을 다시 실행합니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• etcdctl로 스냅샷을 새 디렉토리에 복원한 후에는 etcd 스태틱 파드 매니페스트(`/etc/kubernetes/manifests/etcd.yaml`)에서 hostPath 볼륨의 `path`를 기존 `/var/lib/etcd`에서 복원된 새 디렉토리(`/var/lib/etcd-new`)로 변경해야 합니다.\n• kubelet이 파일 수정을 감지하고 자동으로 etcd 파드를 새 볼륨으로 재시작합니다.",
      "key_concept": "etcd Snapshot Restore, Static Pod Manifest HostPath Modification"
    },
    {
      "id": "D1-Q09",
      "domain": "Domain 1",
      "domain_name": "클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration)",
      "question_en": "Which command safely removes the cordon restriction from 'node-2' after scheduled hardware maintenance is completed, allowing new pods to be scheduled onto it again?",
      "question_kr": "예정된 하드웨어 유지보수가 완료된 후 'node-2' 노드에 적용된 스케줄링 제한(cordon)을 안전하게 해제하여 신규 파드가 다시 스케줄될 수 있도록 허용하는 명령어는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "kubectl uncordon node-2",
          "text_kr": "kubectl uncordon node-2"
        },
        {
          "key": "B",
          "text_en": "kubectl resume node node-2",
          "text_kr": "kubectl resume node node-2"
        },
        {
          "key": "C",
          "text_en": "kubectl enable node-2",
          "text_kr": "kubectl enable node-2"
        },
        {
          "key": "D",
          "text_en": "kubectl undrain node-2",
          "text_kr": "kubectl undrain node-2"
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• `kubectl cordon <node>`는 노드를 SchedulingDisabled 상태로 만들고,\n• `kubectl uncordon <node>`는 노드를 다시 정상 스케줄링 가능 상태로 복귀시킵니다.\n• undrain이나 resume 명령어는 존재하지 않습니다.",
      "key_concept": "kubectl uncordon, Node Maintenance Lifecycle"
    },
    {
      "id": "D1-Q10",
      "domain": "Domain 1",
      "domain_name": "클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration)",
      "question_en": "When upgrading a worker node with kubeadm, what is the correct command executed on the worker node to perform the upgrade planning and configuration step?",
      "question_kr": "kubeadm으로 워커 노드를 업그레이드할 때, 워커 노드에 직접 접속하여 업그레이드 설정 및 구성을 적용하기 위해 실행하는 올바른 명령어는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "kubeadm upgrade apply v1.31.0",
          "text_kr": "kubeadm upgrade apply v1.31.0"
        },
        {
          "key": "B",
          "text_en": "kubeadm upgrade node",
          "text_kr": "kubeadm upgrade node"
        },
        {
          "key": "C",
          "text_en": "kubeadm worker update",
          "text_kr": "kubeadm worker update"
        },
        {
          "key": "D",
          "text_en": "kubectl upgrade worker-node",
          "text_kr": "kubectl upgrade worker-node"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• 컨트롤 플레인(마스터) 노드에서는 `kubeadm upgrade apply v<버전>` 명령을 사용하지만,\n• 워커 노드에서는 컨트롤 플레인 설정을 건드리지 않고 로컬 kubelet 구성을 갱신하기 위해 `kubeadm upgrade node` 명령어를 사용합니다. (CKA 시험 필수 구분 포인트!)",
      "key_concept": "kubeadm upgrade node vs kubeadm upgrade apply"
    }
  ],
  "domain2": [
    {
      "id": "D2-Q01",
      "domain": "Domain 2",
      "domain_name": "워크로드 및 스케줄링 (Workloads & Scheduling)",
      "question_en": "A deployment named 'frontend-deploy' was updated to an unstable image version, causing pods to crash. You need to immediately roll back this deployment to its immediately preceding revision. Which command should you run?",
      "question_kr": "'frontend-deploy'라는 이름의 디플로이먼트가 불안정한 이미지 버전으로 업데이트되어 파드들이 비정상 종료되고 있습니다. 이 디플로이먼트를 직전 리비전으로 즉시 롤백해야 합니다. 실행해야 하는 명령어는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "kubectl rollout undo deployment frontend-deploy",
          "text_kr": "kubectl rollout undo deployment frontend-deploy"
        },
        {
          "key": "B",
          "text_en": "kubectl revert deployment frontend-deploy --step=1",
          "text_kr": "kubectl revert deployment frontend-deploy --step=1"
        },
        {
          "key": "C",
          "text_en": "kubectl rollout restart deployment frontend-deploy",
          "text_kr": "kubectl rollout restart deployment frontend-deploy"
        },
        {
          "key": "D",
          "text_en": "kubectl set image deployment/frontend-deploy --previous",
          "text_kr": "kubectl set image deployment/frontend-deploy --previous"
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• `kubectl rollout undo deployment <이름>`은 추가 옵션이 없을 때 직전 리비전(Revision)으로 즉시 롤백합니다.\n• 특정 리비전으로 롤백하려면 `--to-revision=<번호>` 옵션을 지정할 수 있습니다.",
      "key_concept": "kubectl rollout undo, Deployment Rollback"
    },
    {
      "id": "D2-Q02",
      "domain": "Domain 2",
      "domain_name": "워크로드 및 스케줄링 (Workloads & Scheduling)",
      "question_en": "You are creating a multi-container Pod where a logging container needs to read log files generated by the primary application container. What type of volume should be defined in the Pod spec so that both containers can share this directory without persisting data to a remote storage system?",
      "question_kr": "로깅 컨테이너가 기본 애플리케이션 컨테이너에서 생성된 로그 파일을 읽어야 하는 멀티 컨테이너 파드를 생성하고 있습니다. 원격 스토리지 시스템에 데이터를 영구 저장하지 않고 두 컨테이너가 이 디렉토리를 공유할 수 있도록 Pod spec에 정의해야 하는 볼륨 유형은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "persistentVolumeClaim",
          "text_kr": "persistentVolumeClaim"
        },
        {
          "key": "B",
          "text_en": "emptyDir",
          "text_kr": "emptyDir"
        },
        {
          "key": "C",
          "text_en": "hostPath with type Socket",
          "text_kr": "hostPath with type Socket"
        },
        {
          "key": "D",
          "text_en": "configMap",
          "text_kr": "configMap"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• `emptyDir` 볼륨은 파드가 노드에 할당될 때 처음 생성되며, 해당 파드 내의 모든 컨테이너가 동일한 디렉토리를 읽고 쓸 수 있는 임시 공유 볼륨입니다.\n• 파드가 삭제되면 데이터도 함께 삭제되므로 사이드카 로깅 패턴이나 임시 작업 디렉토리에 가장 적합합니다.",
      "key_concept": "emptyDir Volume, Multi-container Shared Storage"
    },
    {
      "id": "D2-Q03",
      "domain": "Domain 2",
      "domain_name": "워크로드 및 스케줄링 (Workloads & Scheduling)",
      "question_en": "A node named 'node-dedicated' has been tainted with `dedicated=analytics:NoSchedule`. You need to ensure a new pod can be scheduled on this node while other pods avoid it. What must be included in the Pod's specification?",
      "question_kr": "'node-dedicated'라는 노드에 `dedicated=analytics:NoSchedule` 테인트가 적용되었습니다. 다른 일반 파드는 이 노드를 피하고, 특정 신규 파드만 이 노드에 스케줄링될 수 있도록 보장해야 합니다. 해당 파드의 Pod spec에 포함되어야 하는 설정은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "spec.nodeSelector with dedicated: analytics only",
          "text_kr": "dedicated: analytics 가 지정된 spec.nodeSelector 만 포함"
        },
        {
          "key": "B",
          "text_en": "spec.tolerations with key 'dedicated', operator 'Equal', value 'analytics', and effect 'NoSchedule'",
          "text_kr": "key 'dedicated', operator 'Equal', value 'analytics', effect 'NoSchedule' 이 정의된 spec.tolerations"
        },
        {
          "key": "C",
          "text_en": "spec.securityContext with privileged: true",
          "text_kr": "privileged: true 로 설정된 spec.securityContext"
        },
        {
          "key": "D",
          "text_en": "metadata.annotations with taint.ignore=true",
          "text_kr": "taint.ignore=true 가 정의된 metadata.annotations"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• 노드에 설정된 Taint(`NoSchedule`)는 기본적으로 파드가 스케줄링되는 것을 차단합니다.\n• 파드가 이 테인트를 무시하고 배정되려면 파드 스펙에 일치하는 `tolerations` 블록(key, value, effect)을 정의해야 합니다.",
      "key_concept": "Taints and Tolerations, Pod Scheduling Specification"
    },
    {
      "id": "D2-Q04",
      "domain": "Domain 2",
      "domain_name": "워크로드 및 스케줄링 (Workloads & Scheduling)",
      "question_en": "Which NodeAffinity rule strictly mandates that a Pod must NEVER be scheduled on a node unless the node has the label `disktype=ssd`?",
      "question_kr": "노드에 `disktype=ssd` 라벨이 존재하지 않는 한, 파드가 절대로 해당 노드에 스케줄링되어서는 안 된다고 엄격하게 강제하는 NodeAffinity 규칙은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "preferredDuringSchedulingIgnoredDuringExecution",
          "text_kr": "preferredDuringSchedulingIgnoredDuringExecution"
        },
        {
          "key": "B",
          "text_en": "requiredDuringSchedulingIgnoredDuringExecution",
          "text_kr": "requiredDuringSchedulingIgnoredDuringExecution"
        },
        {
          "key": "C",
          "text_en": "requiredDuringSchedulingRequiredDuringExecution",
          "text_kr": "requiredDuringSchedulingRequiredDuringExecution"
        },
        {
          "key": "D",
          "text_en": "preferredDuringSchedulingRequiredDuringExecution",
          "text_kr": "preferredDuringSchedulingRequiredDuringExecution"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• `requiredDuringSchedulingIgnoredDuringExecution`은 '하드 룰(Hard Rule)'로, 스케줄링 시점에 조건이 만족되지 않으면 파드가 Pending 상태로 남고 절대 배치되지 않습니다.\n• `preferredDuring...`은 '소프트 룰'로, 조건을 만족하는 노드가 없더라도 다른 일반 노드에 스케줄링됩니다.",
      "key_concept": "NodeAffinity Hard Rule vs Soft Rule"
    },
    {
      "id": "D2-Q05",
      "domain": "Domain 2",
      "domain_name": "워크로드 및 스케줄링 (Workloads & Scheduling)",
      "question_en": "You want to run a monitoring agent pod on every single worker node in the cluster, automatically deploying to newly added nodes as well. Which Kubernetes workload resource is purpose-built for this requirement?",
      "question_kr": "클러스터의 모든 단일 워커 노드마다 모니터링 에이전트 파드를 정확히 하나씩 실행하고, 향후 노드가 추가되더라도 자동으로 배포되도록 구성하고자 합니다. 이 요구사항에 맞춤 설계된 쿠버네티스 워크로드 리소스는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "StatefulSet",
          "text_kr": "StatefulSet"
        },
        {
          "key": "B",
          "text_en": "DaemonSet",
          "text_kr": "DaemonSet"
        },
        {
          "key": "C",
          "text_en": "ReplicaSet with replicas: 0",
          "text_kr": "replicas: 0 으로 설정된 ReplicaSet"
        },
        {
          "key": "D",
          "text_en": "CronJob with schedule: '@reboot'",
          "text_kr": "schedule: '@reboot' 으로 설정된 CronJob"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• `DaemonSet`은 클러스터의 모든(또는 특정 조건을 만족하는) 노드에 파드의 복제본을 정확히 1개씩 실행하도록 보장하는 전용 컨트롤러입니다.\n• 모니터링 데몬(Prometheus Node Exporter)이나 로그 수집기(Fluentd, Logstash), 네트워크 CNI 에이전트에 주로 사용됩니다.",
      "key_concept": "DaemonSet, Node-level Agent Deployment"
    },
    {
      "id": "D2-Q06",
      "domain": "Domain 2",
      "domain_name": "워크로드 및 스케줄링 (Workloads & Scheduling)",
      "question_en": "How do Init Containers differ from regular application containers in a Pod?",
      "question_kr": "파드 내의 초기화 컨테이너(Init Containers)는 일반 애플리케이션 컨테이너와 어떻게 다르게 동작합니까?",
      "options": [
        {
          "key": "A",
          "text_en": "They run concurrently with the app containers and handle health checks.",
          "text_kr": "앱 컨테이너와 동시에 실행되어 헬스체크를 담당합니다."
        },
        {
          "key": "B",
          "text_en": "They always execute sequentially to completion before any app container is started.",
          "text_kr": "앱 컨테이너가 시작되기 전에 항상 순차적으로 실행되어 완전히 성공(0으로 종료)해야 합니다."
        },
        {
          "key": "C",
          "text_en": "They restart automatically whenever an app container crashes.",
          "text_kr": "앱 컨테이너가 비정상 종료될 때마다 자동으로 재시작됩니다."
        },
        {
          "key": "D",
          "text_en": "They do not support volume mounts.",
          "text_kr": "볼륨 마운트를 지원하지 않습니다."
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• `initContainers`는 일반 `containers`가 기동되기 전에 순서대로 실행됩니다.\n• 이전 초기화 컨테이너가 성공적으로 종료(exit code 0)되어야 다음 초기화 컨테이너 또는 앱 컨테이너가 시작되며, 실패할 경우 파드의 `restartPolicy`에 따라 재시도됩니다.",
      "key_concept": "Init Containers Lifecycle and Execution Order"
    },
    {
      "id": "D2-Q07",
      "domain": "Domain 2",
      "domain_name": "워크로드 및 스케줄링 (Workloads & Scheduling)",
      "question_en": "A CronJob is configured with `concurrencyPolicy: Forbid`. What occurs when the scheduled time arrives for a new Job execution, but the previous Job execution has not yet finished?",
      "question_kr": "CronJob이 `concurrencyPolicy: Forbid`로 설정되어 있습니다. 새로운 Job을 실행할 예정 시간이 되었으나 이전 주기의 Job 실행이 아직 완료되지 않았을 경우 어떤 동작이 발생합니까?",
      "options": [
        {
          "key": "A",
          "text_en": "The running Job is cancelled immediately and the new Job starts.",
          "text_kr": "실행 중인 기존 Job이 즉시 취소되고 새 Job이 시작됩니다."
        },
        {
          "key": "B",
          "text_en": "The CronJob controller skips the new Job run and lets the current Job continue.",
          "text_kr": "CronJob 컨트롤러가 새 Job의 실행을 건너뛰고(skip) 현재 Job을 계속 실행합니다."
        },
        {
          "key": "C",
          "text_en": "Both Jobs run simultaneously in parallel.",
          "text_kr": "두 Job이 동시에 병렬로 실행됩니다."
        },
        {
          "key": "D",
          "text_en": "The CronJob transitions into an Error state and stops future scheduling.",
          "text_kr": "CronJob이 Error 상태로 전환되어 향후 스케줄링이 중단됩니다."
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• `concurrencyPolicy: Forbid`는 동시 실행을 금지하므로, 이전 작업이 실행 중이면 새 작업의 실행을 건너뜁니다(Skip).\n• `Allow`(기본값): 동시 실행 허용.\n• `Replace`: 기존 실행 중인 작업을 취소하고 새 작업으로 대체.",
      "key_concept": "CronJob concurrencyPolicy (Allow, Forbid, Replace)"
    },
    {
      "id": "D2-Q08",
      "domain": "Domain 2",
      "domain_name": "워크로드 및 스케줄링 (Workloads & Scheduling)",
      "question_en": "Which command line creates a secret named 'db-secret' with a key 'password' and value 'secretpass' without creating a physical file?",
      "question_kr": "물리적 파일을 생성하지 않고 키는 'password', 값은 'secretpass'를 갖는 'db-secret' 시크릿을 명령형 커맨드로 즉시 생성하는 올바른 명령어는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "kubectl create secret generic db-secret --from-literal=password=secretpass",
          "text_kr": "kubectl create secret generic db-secret --from-literal=password=secretpass"
        },
        {
          "key": "B",
          "text_en": "kubectl make secret db-secret password=secretpass",
          "text_kr": "kubectl make secret db-secret password=secretpass"
        },
        {
          "key": "C",
          "text_en": "kubectl create secret password secretpass --name=db-secret",
          "text_kr": "kubectl create secret password secretpass --name=db-secret"
        },
        {
          "key": "D",
          "text_en": "kubectl secret put db-secret -k password -v secretpass",
          "text_kr": "kubectl secret put db-secret -k password -v secretpass"
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• `kubectl create secret generic <시크릿이름> --from-literal=<키>=<값>`을 사용하면 파일 생성 없이 CLI에서 base64로 자동 인코딩된 시크릿을 즉시 생성할 수 있습니다.",
      "key_concept": "kubectl create secret generic --from-literal"
    },
    {
      "id": "D2-Q09",
      "domain": "Domain 2",
      "domain_name": "워크로드 및 스케줄링 (Workloads & Scheduling)",
      "question_en": "A container in a pod has `resources.limits.memory` set to 256Mi. If the application process attempts to allocate 500Mi of memory during peak operation, what will happen to the container?",
      "question_kr": "파드 내의 컨테이너에 `resources.limits.memory`가 256Mi로 설정되어 있습니다. 피크 타임에 애플리케이션 프로세스가 500Mi의 메모리를 할당하려고 시도하면 해당 컨테이너에 어떤 일이 발생합니까?",
      "options": [
        {
          "key": "A",
          "text_en": "The container's CPU will be throttled automatically.",
          "text_kr": "컨테이너의 CPU가 자동으로 쓰로틀링(스로틀링)됩니다."
        },
        {
          "key": "B",
          "text_en": "The container will be killed by the Linux OOM (Out Of Memory) killer with exit code 137.",
          "text_kr": "컨테이너가 리눅스 OOM 킬러에 의해 종료 코드 137(OOMKilled)로 강제 종료됩니다."
        },
        {
          "key": "C",
          "text_en": "Kubernetes automatically scales up the memory limit dynamically.",
          "text_kr": "쿠버네티스가 메모리 제한을 동적으로 자동 상향합니다."
        },
        {
          "key": "D",
          "text_en": "The pod is migrated to another node without stopping.",
          "text_kr": "파드가 중단 없이 다른 노드로 즉시 이주됩니다."
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• CPU는 압축 가능한(compressible) 리소스이므로 한도를 넘기면 쓰로틀링(Throttling)되지만,\n• 메모리는 압축 불가능한(incompressible) 리소스이므로 한도(`limits.memory`)를 초과하면 커널 OOM 킬러에 의해 즉시 SIGKILL(Exit Code 137, OOMKilled) 처분됩니다.",
      "key_concept": "Resource Limits, OOMKilled (Exit Code 137), Memory vs CPU Limit"
    },
    {
      "id": "D2-Q10",
      "domain": "Domain 2",
      "domain_name": "워크로드 및 스케줄링 (Workloads & Scheduling)",
      "question_en": "How can you inject all key-value pairs from a ConfigMap named 'game-config' directly as environment variables into a container?",
      "question_kr": "'game-config'라는 ConfigMap에 들어있는 모든 키-값 쌍을 컨테이너 내부에 환경변수로 일괄 주입하려면 PodSpec에서 어떤 설정을 사용해야 합니까?",
      "options": [
        {
          "key": "A",
          "text_en": "spec.containers[].envFrom with configMapRef.name: game-config",
          "text_kr": "configMapRef.name: game-config 가 정의된 spec.containers[].envFrom 사용"
        },
        {
          "key": "B",
          "text_en": "spec.containers[].env with valueFrom.allKeys: game-config",
          "text_kr": "valueFrom.allKeys: game-config 가 정의된 spec.containers[].env 사용"
        },
        {
          "key": "C",
          "text_en": "spec.containers[].volumeMounts with type: EnvVars",
          "text_kr": "type: EnvVars 가 정의된 spec.containers[].volumeMounts 사용"
        },
        {
          "key": "D",
          "text_en": "spec.volumes[].configMap with injectAsEnv: true",
          "text_kr": "injectAsEnv: true 가 정의된 spec.volumes[].configMap 사용"
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• ConfigMap이나 Secret의 모든 키-값 항목을 한 번에 환경변수로 가져올 때는 `env` 대신 `envFrom` 블록의 `configMapRef` 또는 `secretRef`를 사용합니다.",
      "key_concept": "envFrom with configMapRef, Bulk Environment Variable Injection"
    }
  ],
  "domain3": [
    {
      "id": "D3-Q01",
      "domain": "Domain 3",
      "domain_name": "서비스 및 네트워킹 (Services & Networking)",
      "question_en": "In a Kubernetes Service definition of type NodePort, what does `targetPort` refer to?",
      "question_kr": "NodePort 타입의 쿠버네티스 서비스 정의에서 `targetPort`는 무엇을 의미합니까?",
      "options": [
        {
          "key": "A",
          "text_en": "The port on the worker node's external IP address.",
          "text_kr": "워커 노드의 외부 IP 주소에 열리는 포트."
        },
        {
          "key": "B",
          "text_en": "The port on which the Service itself serves traffic inside the cluster.",
          "text_kr": "클러스터 내부에서 서비스 가상 IP(VIP)가 트래픽을 수신하는 포트."
        },
        {
          "key": "C",
          "text_en": "The port on which the container inside the targeted Pod is listening.",
          "text_kr": "대상이 되는 파드 내부의 컨테이너가 실제로 수신 대기(리스닝)하고 있는 포트."
        },
        {
          "key": "D",
          "text_en": "The port used by the Ingress Controller to route traffic.",
          "text_kr": "인그레스 컨트롤러가 트래픽을 라우팅하기 위해 사용하는 포트."
        }
      ],
      "correct_answer": "C",
      "explanation_kr": "정답은 C입니다.\n\n• `port`: Service의 가상 IP가 클러스터 내부에서 노출하는 포트.\n• `targetPort`: 파드 내부의 컨테이너가 실제로 리스닝하고 있는 포트.\n• `nodePort`: 외부 클라이언트가 각 노드의 IP로 접근할 때 사용하는 포트 (30000~32767).",
      "key_concept": "Service Port vs TargetPort vs NodePort"
    },
    {
      "id": "D3-Q02",
      "domain": "Domain 3",
      "domain_name": "서비스 및 네트워킹 (Services & Networking)",
      "question_en": "What is the primary characteristic of a 'Headless Service' created with `spec.clusterIP: None`?",
      "question_kr": "`spec.clusterIP: None`으로 생성된 '헤드리스 서비스(Headless Service)'의 주요 특징은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "It does not allocate a cluster virtual IP and DNS queries return the individual IPs of the backend pods directly.",
          "text_kr": "단일 가상 IP(VIP)를 할당하지 않으며, DNS 질의 시 백엔드 개별 파드들의 IP 목록을 직접 반환합니다."
        },
        {
          "key": "B",
          "text_en": "It does not allow any network traffic to reach the pods.",
          "text_kr": "파드로의 모든 네트워크 트래픽 인입을 차단합니다."
        },
        {
          "key": "C",
          "text_en": "It can only be used with DaemonSets.",
          "text_kr": "오직 DaemonSet과만 함께 사용할 수 있습니다."
        },
        {
          "key": "D",
          "text_en": "It automatically assigns a public Load Balancer IP.",
          "text_kr": "퍼블릭 로드밸런서 IP를 자동으로 할당합니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• `clusterIP: None`으로 설정하면 kube-proxy가 프록시 작업을 수행하지 않고 VIP도 할당되지 않습니다.\n• 대신 CoreDNS에 질의했을 때 셀렉터와 일치하는 파드들의 실제 A 레코드(IP 목록)를 직접 반환하므로, StatefulSet 기반 데이터베이스 클러스터의 마스터-슬레이브 디스커버리에 주로 활용됩니다.",
      "key_concept": "Headless Service (clusterIP: None), StatefulSet DNS"
    },
    {
      "id": "D3-Q03",
      "domain": "Domain 3",
      "domain_name": "서비스 및 네트워킹 (Services & Networking)",
      "question_en": "A pod in the 'staging' namespace needs to send an HTTP request to a service named 'inventory-svc' located in the 'production' namespace on port 80. What is the Fully Qualified Domain Name (FQDN) to resolve this service?",
      "question_kr": "'staging' 네임스페이스의 파드가 'production' 네임스페이스에 있는 'inventory-svc' 서비스의 80번 포트로 HTTP 요청을 보내야 합니다. 이 서비스를 해석하기 위한 FQDN(전체 도메인 이름)은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "inventory-svc.staging.pod.cluster.local",
          "text_kr": "inventory-svc.staging.pod.cluster.local"
        },
        {
          "key": "B",
          "text_en": "inventory-svc.production.svc.cluster.local",
          "text_kr": "inventory-svc.production.svc.cluster.local"
        },
        {
          "key": "C",
          "text_en": "production.inventory-svc.k8s.local",
          "text_kr": "production.inventory-svc.k8s.local"
        },
        {
          "key": "D",
          "text_en": "http://inventory-svc:80/production",
          "text_kr": "http://inventory-svc:80/production"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• 쿠버네티스 CoreDNS 표준 FQDN 형식은 `<서비스명>.<네임스페이스>.svc.cluster.local`입니다.\n• 따라서 'production' 네임스페이스의 'inventory-svc'는 `inventory-svc.production.svc.cluster.local`로 해석됩니다.",
      "key_concept": "CoreDNS FQDN Resolution Pattern"
    },
    {
      "id": "D3-Q04",
      "domain": "Domain 3",
      "domain_name": "서비스 및 네트워킹 (Services & Networking)",
      "question_en": "You create an Ingress resource with path routing rules, but accessing the configured host returns a connection refused error or 404 from the node IP. What is the most likely cluster prerequisite missing?",
      "question_kr": "경로 기반 라우팅 규칙이 포함된 Ingress 리소스를 생성했으나, 노드 IP로 해당 호스트에 접속하면 연결 거부 또는 404 에러가 발생합니다. 클러스터에 누락되었을 가능성이 가장 높은 필수 전제 조건은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "The cluster lacks an active Ingress Controller (such as ingress-nginx) to implement the Ingress specification.",
          "text_kr": "Ingress 명세를 실제로 구현하고 트래픽을 처리할 활성화된 인그레스 컨트롤러(예: ingress-nginx)가 클러스터에 없습니다."
        },
        {
          "key": "B",
          "text_en": "NetworkPolicy does not permit ingress resources by default.",
          "text_kr": "NetworkPolicy가 기본적으로 ingress 리소스를 허용하지 않기 때문입니다."
        },
        {
          "key": "C",
          "text_en": "Ingress resources require a commercial SSL certificate before passing any traffic.",
          "text_kr": "Ingress 리소스는 트래픽을 전달하기 전에 상용 SSL 인증서가 반드시 필요합니다."
        },
        {
          "key": "D",
          "text_en": "CoreDNS must be reconfigured to register ingress paths.",
          "text_kr": "CoreDNS가 인그레스 경로를 등록하도록 재설정되어야 합니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• Ingress 리소스는 단순한 '라우팅 규칙 설정 데이터'에 불과합니다.\n• 이 규칙을 감시하여 실제 리버스 프록시(Nginx, HAProxy, Envoy 등)를 구동하고 트래픽을 분기해줄 **Ingress Controller**가 클러스터에 실행 중이지 않으면 아무런 동작도 일어나지 않습니다.",
      "key_concept": "Ingress Resource vs Ingress Controller"
    },
    {
      "id": "D3-Q05",
      "domain": "Domain 3",
      "domain_name": "서비스 및 네트워킹 (Services & Networking)",
      "question_en": "Which NetworkPolicy configuration successfully blocks all incoming ingress traffic to all pods in the 'secure-zone' namespace, effectively creating a default-deny policy?",
      "question_kr": "'secure-zone' 네임스페이스의 모든 파드로 들어오는 모든 인입(Ingress) 트래픽을 차단하여 완전한 기본 거부(default-deny) 상태를 만드는 올바른 NetworkPolicy 설정은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "spec.podSelector: {} with spec.policyTypes: ['Ingress'] and no ingress rules defined",
          "text_kr": "spec.podSelector: {} 와 spec.policyTypes: ['Ingress'] 를 지정하고 ingress 규칙 목록을 비워둠"
        },
        {
          "key": "B",
          "text_en": "spec.podSelector: '*' with spec.ingress: [{action: 'Deny'}]",
          "text_kr": "spec.podSelector: '*' 와 spec.ingress: [{action: 'Deny'}]"
        },
        {
          "key": "C",
          "text_en": "spec.ingress: [] with action: DropAll",
          "text_kr": "spec.ingress: [] 와 action: DropAll"
        },
        {
          "key": "D",
          "text_en": "spec.policyTypes: ['DenyAll']",
          "text_kr": "spec.policyTypes: ['DenyAll']"
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• `podSelector: {}`는 네임스페이스 내의 모든 파드를 대상으로 선택합니다.\n• `policyTypes: [Ingress]`를 선언하고 하위 `ingress:` 허용 목록을 전혀 제공하지 않으면, 모든 인입 트래픽이 거부(Default Deny)됩니다.",
      "key_concept": "NetworkPolicy Default Deny All Ingress"
    },
    {
      "id": "D3-Q06",
      "domain": "Domain 3",
      "domain_name": "서비스 및 네트워킹 (Services & Networking)",
      "question_en": "What is the default port range allocated for Kubernetes Services of type NodePort?",
      "question_kr": "NodePort 타입의 쿠버네티스 서비스에 기본적으로 할당되는 포트 범위는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "1024 - 5000",
          "text_kr": "1024 - 5000"
        },
        {
          "key": "B",
          "text_en": "30000 - 32767",
          "text_kr": "30000 - 32767"
        },
        {
          "key": "C",
          "text_en": "8000 - 9000",
          "text_kr": "8000 - 9000"
        },
        {
          "key": "D",
          "text_en": "49152 - 65535",
          "text_kr": "49152 - 65535"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• 쿠버네티스 NodePort의 기본 할당 범위는 `30000 ~ 32767`입니다.\n• 범위 변경이 필요한 경우 kube-apiserver의 `--service-node-port-range` 플래그로 수정할 수 있습니다.",
      "key_concept": "NodePort Port Allocation Range (30000-32767)"
    },
    {
      "id": "D3-Q07",
      "domain": "Domain 3",
      "domain_name": "서비스 및 네트워킹 (Services & Networking)",
      "question_en": "You need to allow pods with label `role: frontend` to connect to database pods with label `role: db` on TCP port 3306. In the NetworkPolicy applied to `role: db`, how should the `ingress.from` rule be written?",
      "question_kr": "`role: frontend` 라벨을 가진 파드들만 `role: db` 라벨을 가진 데이터베이스 파드의 TCP 3306 포트로 연결할 수 있도록 허용해야 합니다. `role: db`에 적용되는 NetworkPolicy의 `ingress.from` 규칙은 어떻게 작성해야 합니까?",
      "options": [
        {
          "key": "A",
          "text_en": "from: [ { podSelector: { matchLabels: { role: frontend } } } ] with ports: [ { protocol: TCP, port: 3306 } ]",
          "text_kr": "from: [ { podSelector: { matchLabels: { role: frontend } } } ] 및 ports: [ { protocol: TCP, port: 3306 } ]"
        },
        {
          "key": "B",
          "text_en": "from: [ { allowRole: frontend, targetPort: 3306 } ]",
          "text_kr": "from: [ { allowRole: frontend, targetPort: 3306 } ]"
        },
        {
          "key": "C",
          "text_en": "from: [ { serviceSelector: frontend-svc } ]",
          "text_kr": "from: [ { serviceSelector: frontend-svc } ]"
        },
        {
          "key": "D",
          "text_en": "from: [ { ipBlock: { cidr: 0.0.0.0/0 } } ]",
          "text_kr": "from: [ { ipBlock: { cidr: 0.0.0.0/0 } } ]"
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• NetworkPolicy의 `ingress.from` 하위에 `podSelector.matchLabels`를 지정하여 트래픽을 송신하는 소스 파드의 라벨을 명시하고,\n• `ports` 하위에 허용할 프로토콜(TCP)과 포트 번호(3306)를 지정합니다.",
      "key_concept": "NetworkPolicy PodSelector Ingress Rule"
    },
    {
      "id": "D3-Q08",
      "domain": "Domain 3",
      "domain_name": "서비스 및 네트워킹 (Services & Networking)",
      "question_en": "When a Kubernetes Service is created without a `spec.selector`, what must an administrator manually create to route traffic to external endpoints?",
      "question_kr": "쿠버네티스 서비스가 `spec.selector` 없이 생성되었을 때, 트래픽을 외부 IP/엔드포인트로 라우팅하기 위해 관리자가 수동으로 생성해야 하는 리소스는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "An Endpoints (or EndpointSlice) object with the exact same name as the Service.",
          "text_kr": "해당 서비스와 정확히 동일한 이름을 갖는 Endpoints (또는 EndpointSlice) 오브젝트."
        },
        {
          "key": "B",
          "text_en": "A secondary Ingress Controller.",
          "text_kr": "보조 인그레스 컨트롤러."
        },
        {
          "key": "C",
          "text_en": "A manual iptables rule on each worker node.",
          "text_kr": "각 워커 노드에 수동 iptables 규칙 생성."
        },
        {
          "key": "D",
          "text_en": "A ClusterIPBinding object.",
          "text_kr": "ClusterIPBinding 오브젝트."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• 서비스에 selector가 지정되어 있으면 쿠버네티스가 자동으로 파드 IP를 추적하여 Endpoints를 생성합니다.\n• 그러나 selector가 없는 서비스의 경우, 서비스 이름과 동일한 이름의 `Endpoints` 오브젝트를 수동으로 생성하여 외부 데이터베이스 IP 등을 등록할 수 있습니다.",
      "key_concept": "Services without Selectors, Manual Endpoints"
    },
    {
      "id": "D3-Q09",
      "domain": "Domain 3",
      "domain_name": "서비스 및 네트워킹 (Services & Networking)",
      "question_en": "Which command line quickly exposes a Deployment named 'web-server' on port 80 targeting container port 8080 as a ClusterIP service named 'web-service'?",
      "question_kr": "'web-server'라는 디플로이먼트를 서비스 포트 80, 컨테이너 타겟 포트 8080의 'web-service'라는 이름의 ClusterIP 서비스로 빠르게 노출하는 CLI 명령어는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "kubectl expose deployment web-server --name=web-service --port=80 --target-port=8080",
          "text_kr": "kubectl expose deployment web-server --name=web-service --port=80 --target-port=8080"
        },
        {
          "key": "B",
          "text_en": "kubectl create service clusterip web-service --expose=web-server:80:8080",
          "text_kr": "kubectl create service clusterip web-service --expose=web-server:80:8080"
        },
        {
          "key": "C",
          "text_en": "kubectl connect deployment web-server to port 80",
          "text_kr": "kubectl connect deployment web-server to port 80"
        },
        {
          "key": "D",
          "text_en": "kubectl route web-server --port=80:8080",
          "text_kr": "kubectl route web-server --port=80:8080"
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• `kubectl expose deployment <이름> --name=<서비스이름> --port=<서비스포트> --target-port=<파드포트>`를 사용하면 기본 ClusterIP 타입으로 즉시 매핑 서비스를 생성할 수 있습니다.",
      "key_concept": "kubectl expose deployment imperative command"
    },
    {
      "id": "D3-Q10",
      "domain": "Domain 3",
      "domain_name": "서비스 및 네트워킹 (Services & Networking)",
      "question_en": "A company wants to prevent pods in the 'finance' namespace from connecting to external public internet IP addresses, allowing only internal cluster communication. What type of NetworkPolicy rule must be defined?",
      "question_kr": "회사가 'finance' 네임스페이스의 파드들이 외부 퍼블릭 인터넷 IP로 연결되는 것을 차단하고 클러스터 내부 통신만 허용하고자 합니다. 어떤 유형의 NetworkPolicy 규칙을 정의해야 합니까?",
      "options": [
        {
          "key": "A",
          "text_en": "An Egress policy that restricts outgoing traffic to internal CIDR ranges or specific namespaces.",
          "text_kr": "외부 송출 트래픽을 내부 사설 CIDR 대역이나 특정 네임스페이스로 제한하는 Egress(송출) 정책."
        },
        {
          "key": "B",
          "text_en": "An Ingress policy with type: DropPublic.",
          "text_kr": "type: DropPublic 이 지정된 Ingress 정책."
        },
        {
          "key": "C",
          "text_en": "A PodSecurityStandard with isolateNetwork: true.",
          "text_kr": "isolateNetwork: true 가 지정된 PodSecurityStandard."
        },
        {
          "key": "D",
          "text_en": "A CoreDNS firewall filter.",
          "text_kr": "CoreDNS 방화벽 필터."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• 파드에서 외부로 나가는 트래픽을 제어하려면 `policyTypes: [Egress]` 정책을 작성하여 허용할 목적지(`to:`)를 내부 네임스페이스나 내부 IP 블록으로 한정해야 합니다.",
      "key_concept": "NetworkPolicy Egress Traffic Filtering"
    }
  ],
  "domain4": [
    {
      "id": "D4-Q01",
      "domain": "Domain 4",
      "domain_name": "스토리지 (Storage)",
      "question_en": "A PersistentVolume (PV) is created with a capacity of 10Gi, `accessModes: [ReadWriteOnce]`, and `storageClassName: manual`. A user creates a PersistentVolumeClaim (PVC) requesting 5Gi with `accessModes: [ReadWriteMany]` and `storageClassName: manual`. Why does the PVC remain in the 'Pending' status?",
      "question_kr": "용량 10Gi, `accessModes: [ReadWriteOnce]`, `storageClassName: manual`로 생성된 PersistentVolume(PV)이 있습니다. 사용자가 5Gi 용량, `accessModes: [ReadWriteMany]`, `storageClassName: manual`을 요청하는 PersistentVolumeClaim(PVC)을 생성했습니다. 이 PVC가 'Pending' 상태로 머무르는 이유는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "The requested storage capacity is smaller than the PV capacity.",
          "text_kr": "요청된 스토리지 용량이 PV 용량보다 작기 때문입니다."
        },
        {
          "key": "B",
          "text_en": "The accessModes between the PV (ReadWriteOnce) and the PVC (ReadWriteMany) do not match.",
          "text_kr": "PV의 접근 모드(ReadWriteOnce)와 PVC의 요청 접근 모드(ReadWriteMany)가 일치하지 않기 때문입니다."
        },
        {
          "key": "C",
          "text_en": "StorageClassName 'manual' is a reserved keyword in Kubernetes.",
          "text_kr": "StorageClassName 'manual'이 쿠버네티스 예약어이기 때문입니다."
        },
        {
          "key": "D",
          "text_en": "PVCs cannot bind to PVs without an active Pod attached.",
          "text_kr": "활성 파드가 연결되지 않으면 PVC가 PV에 바인딩될 수 없기 때문입니다."
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• PVC가 PV에 정상적으로 바인딩(Bound)되려면 **StorageClassName**, **AccessModes**, 그리고 **요청 용량(Capacity <= PV 용량)**이 모두 호환되어야 합니다.\n• PV는 단일 노드 전용(`ReadWriteOnce`)인 반면 PVC는 다중 노드 동시 쓰기(`ReadWriteMany`)를 요구하고 있으므로 바인딩되지 못하고 Pending 상태로 대기합니다.",
      "key_concept": "PV and PVC Binding Requirements, AccessModes Mismatch"
    },
    {
      "id": "D4-Q02",
      "domain": "Domain 4",
      "domain_name": "스토리지 (Storage)",
      "question_en": "Which PersistentVolumeReclaimPolicy preserves the underlying storage volume and its data when the bound PersistentVolumeClaim (PVC) is deleted, requiring an administrator to manually reclaim or clean up the resource?",
      "question_kr": "바인딩된 PersistentVolumeClaim(PVC)이 삭제되었을 때 기본 스토리지 볼륨과 데이터를 그대로 보존하여, 관리자가 수동으로 리소스를 회수하거나 정리하도록 요구하는 PersistentVolumeReclaimPolicy는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "Delete",
          "text_kr": "Delete"
        },
        {
          "key": "B",
          "text_en": "Retain",
          "text_kr": "Retain"
        },
        {
          "key": "C",
          "text_en": "Recycle",
          "text_kr": "Recycle"
        },
        {
          "key": "D",
          "text_en": "Archive",
          "text_kr": "Archive"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• `persistentVolumeReclaimPolicy: Retain`은 PVC가 삭제되어도 PV와 실제 백엔드 데이터를 삭제하지 않고 `Released` 상태로 유지하여 데이터 유실을 방지합니다.\n• `Delete`는 PVC 삭제 시 실제 스토리지 에셋까지 함께 자동 삭제합니다.",
      "key_concept": "Reclaim Policy: Retain vs Delete"
    },
    {
      "id": "D4-Q03",
      "domain": "Domain 4",
      "domain_name": "스토리지 (Storage)",
      "question_en": "What is the purpose of setting `volumeBindingMode: WaitForFirstConsumer` on a StorageClass?",
      "question_kr": "StorageClass에서 `volumeBindingMode: WaitForFirstConsumer`를 설정하는 주된 목적은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "It delays volume provisioning and binding until a Pod using the PVC is created and scheduled to a specific node.",
          "text_kr": "해당 PVC를 사용하는 파드가 실제로 생성되어 특정 노드에 스케줄링될 때까지 볼륨 프로비저닝과 바인딩을 지연시킵니다."
        },
        {
          "key": "B",
          "text_en": "It ensures only one container can consume the storage volume at any time.",
          "text_kr": "항상 단 하나의 컨테이너만 볼륨을 사용할 수 있도록 보장합니다."
        },
        {
          "key": "C",
          "text_en": "It compresses data before writing to disk.",
          "text_kr": "디스크에 쓰기 전에 데이터를 자동 압축합니다."
        },
        {
          "key": "D",
          "text_en": "It prevents the volume from being expanded in size.",
          "text_kr": "볼륨 크기가 확장되는 것을 방지합니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• 기본값인 `Immediate`는 PVC가 생성되는 즉시 볼륨을 프로비저닝하여, 특정 가용영역(AZ)이나 로컬 디스크에 종속된 볼륨의 경우 파드가 다른 노드에 배정되었을 때 볼륨을 마운트하지 못하는 문제가 발생할 수 있습니다.\n• `WaitForFirstConsumer`는 파드의 토폴로지 제약(NodeSelector, Affinity 등)을 먼저 평가하여 파드가 위치할 노드가 확정된 후에 볼륨을 프로비저닝하므로 이러한 문제를 방지합니다.",
      "key_concept": "StorageClass volumeBindingMode: WaitForFirstConsumer"
    },
    {
      "id": "D4-Q04",
      "domain": "Domain 4",
      "domain_name": "스토리지 (Storage)",
      "question_en": "Which AccessMode allows a volume to be mounted simultaneously as read-write by multiple pods running across multiple distinct worker nodes?",
      "question_kr": "서로 다른 여러 워커 노드에서 실행 중인 여러 파드가 동시에 읽기/쓰기(read-write)로 볼륨을 마운트할 수 있도록 허용하는 AccessMode는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "ReadWriteOnce (RWO)",
          "text_kr": "ReadWriteOnce (RWO)"
        },
        {
          "key": "B",
          "text_en": "ReadOnlyMany (ROX)",
          "text_kr": "ReadOnlyMany (ROX)"
        },
        {
          "key": "C",
          "text_en": "ReadWriteMany (RWX)",
          "text_kr": "ReadWriteMany (RWX)"
        },
        {
          "key": "D",
          "text_en": "ReadWriteOncePod (RWOP)",
          "text_kr": "ReadWriteOncePod (RWOP)"
        }
      ],
      "correct_answer": "C",
      "explanation_kr": "정답은 C입니다.\n\n• `ReadWriteMany (RWX)`는 여러 노드에서 동시에 읽기/쓰기가 가능한 모드로, NFS, AWS EFS, GlusterFS 등의 네트워크 파일시스템에서 지원됩니다.",
      "key_concept": "AccessModes: ReadWriteMany (RWX)"
    },
    {
      "id": "D4-Q05",
      "domain": "Domain 4",
      "domain_name": "스토리지 (Storage)",
      "question_en": "To enable dynamic expansion of PersistentVolumeClaim capacity in Kubernetes, what property must be explicitly set to `true` in the referenced StorageClass?",
      "question_kr": "쿠버네티스에서 PersistentVolumeClaim의 용량을 동적으로 확장(Resize)할 수 있도록 허용하려면 참조하는 StorageClass에서 어떤 속성을 명시적으로 `true`로 설정해야 합니까?",
      "options": [
        {
          "key": "A",
          "text_en": "allowVolumeExpansion",
          "text_kr": "allowVolumeExpansion"
        },
        {
          "key": "B",
          "text_en": "dynamicResizeEnabled",
          "text_kr": "dynamicResizeEnabled"
        },
        {
          "key": "C",
          "text_en": "autoScaleStorage",
          "text_kr": "autoScaleStorage"
        },
        {
          "key": "D",
          "text_en": "expandablePVC",
          "text_kr": "expandablePVC"
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• `StorageClass` 매니페스트에 `allowVolumeExpansion: true`가 설정되어 있어야 사용자가 기존 PVC의 `spec.resources.requests.storage` 값을 더 큰 값으로 편집하여 볼륨을 온라인으로 확장할 수 있습니다.",
      "key_concept": "StorageClass allowVolumeExpansion"
    },
    {
      "id": "D4-Q06",
      "domain": "Domain 4",
      "domain_name": "스토리지 (Storage)",
      "question_en": "Which configuration snippet in a Pod manifest correctly mounts an existing PersistentVolumeClaim named 'data-claim' to the container path `/var/www/html`?",
      "question_kr": "파드 매니페스트에서 'data-claim'이라는 기존 PersistentVolumeClaim을 컨테이너 내부 경로 `/var/www/html`에 올바르게 마운트하는 설정은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "spec.containers[].volumeMounts: [{name: web-data, mountPath: /var/www/html}] and spec.volumes: [{name: web-data, persistentVolumeClaim: {claimName: data-claim}}]",
          "text_kr": "spec.containers[].volumeMounts: [{name: web-data, mountPath: /var/www/html}] 및 spec.volumes: [{name: web-data, persistentVolumeClaim: {claimName: data-claim}}]"
        },
        {
          "key": "B",
          "text_en": "spec.containers[].pvcMount: {name: data-claim, path: /var/www/html}",
          "text_kr": "spec.containers[].pvcMount: {name: data-claim, path: /var/www/html}"
        },
        {
          "key": "C",
          "text_en": "spec.volumes: [{pvcName: data-claim, containerPath: /var/www/html}]",
          "text_kr": "spec.volumes: [{pvcName: data-claim, containerPath: /var/www/html}]"
        },
        {
          "key": "D",
          "text_en": "spec.mounts: [{claim: data-claim, target: /var/www/html}]",
          "text_kr": "spec.mounts: [{claim: data-claim, target: /var/www/html}]"
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• 파드 스펙의 `volumes` 블록에서 PVC 이름(`claimName`)과 볼륨 식별자(`name`)를 정의하고,\n• 컨테이너의 `volumeMounts` 블록에서 해당 볼륨 식별자(`name`)와 마운트할 디렉토리 경로(`mountPath`)를 연결합니다.",
      "key_concept": "Pod Volume Mount Syntax (volumes and volumeMounts)"
    },
    {
      "id": "D4-Q07",
      "domain": "Domain 4",
      "domain_name": "스토리지 (Storage)",
      "question_en": "What status does a PersistentVolume (PV) enter immediately after its bound PersistentVolumeClaim (PVC) is deleted, when the PV's reclaim policy is set to 'Retain'?",
      "question_kr": "PersistentVolume(PV)의 반환 정책(reclaim policy)이 'Retain'으로 설정되어 있을 때, 바인딩되어 있던 PVC가 삭제된 직후 PV는 어떤 상태(Status)로 전환됩니까?",
      "options": [
        {
          "key": "A",
          "text_en": "Available",
          "text_kr": "Available"
        },
        {
          "key": "B",
          "text_en": "Released",
          "text_kr": "Released"
        },
        {
          "key": "C",
          "text_en": "Pending",
          "text_kr": "Pending"
        },
        {
          "key": "D",
          "text_en": "Failed",
          "text_kr": "Failed"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• `Retain` 정책 하에서 PVC가 삭제되면 PV는 즉시 `Released` 상태가 됩니다.\n• 이 상태의 PV에는 이전 클레임의 데이터가 남아있으므로, 다른 신규 PVC가 자동으로 바인딩되지 못하며 관리자의 수동 조치(정제 후 claimRef 제거 등)가 필요합니다.",
      "key_concept": "PersistentVolume Lifecycle: Released Status"
    },
    {
      "id": "D4-Q08",
      "domain": "Domain 4",
      "domain_name": "스토리지 (Storage)",
      "question_en": "Why is the use of `hostPath` volumes generally discouraged for production applications running across multi-node clusters?",
      "question_kr": "다중 노드 클러스터에서 실행되는 프로덕션 애플리케이션에 `hostPath` 볼륨의 사용이 일반적으로 권장되지 않는 이유는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "Data is tied to a specific node's local filesystem; if the pod is rescheduled to another node, it cannot access the data.",
          "text_kr": "데이터가 특정 노드의 로컬 파일시스템에 종속되므로, 파드가 다른 노드로 재스케줄링되면 기존 데이터에 접근할 수 없습니다."
        },
        {
          "key": "B",
          "text_en": "hostPath volumes can only hold read-only data.",
          "text_kr": "hostPath 볼륨은 읽기 전용 데이터만 저장할 수 있기 때문입니다."
        },
        {
          "key": "C",
          "text_en": "Kubernetes automatically deletes hostPath directories on container restart.",
          "text_kr": "쿠버네티스가 컨테이너 재시작 시 hostPath 디렉토리를 자동으로 삭제하기 때문입니다."
        },
        {
          "key": "D",
          "text_en": "hostPath requires root access inside the pod.",
          "text_kr": "hostPath는 파드 내부의 루트 권한을 강제하기 때문입니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• `hostPath` 볼륨은 파드가 실행 중인 특정 노드의 로컬 디스크 파일/디렉토리를 마운트하므로 노드 장애 발생 시 데이터 격리 및 가용성을 보장할 수 없습니다.",
      "key_concept": "hostPath Limitations and Node Affinity"
    },
    {
      "id": "D4-Q09",
      "domain": "Domain 4",
      "domain_name": "스토리지 (Storage)",
      "question_en": "What is the Container Storage Interface (CSI) specification in Kubernetes designed to achieve?",
      "question_kr": "쿠버네티스의 컨테이너 스토리지 인터페이스(CSI) 사양은 무엇을 달성하기 위해 설계되었습니까?",
      "options": [
        {
          "key": "A",
          "text_en": "To enable third-party storage vendors to develop storage plugins out-of-tree without modifying core Kubernetes source code.",
          "text_kr": "서드파티 스토리지 벤더가 핵심 쿠버네티스 소스 코드를 수정하지 않고 외부(Out-of-tree) 플러그인 형태로 스토리지 드라이버를 개발할 수 있도록 하기 위함입니다."
        },
        {
          "key": "B",
          "text_en": "To replace Linux filesystem drivers with WebAssembly modules.",
          "text_kr": "리눅스 파일시스템 드라이버를 WebAssembly 모듈로 교체하기 위함입니다."
        },
        {
          "key": "C",
          "text_en": "To encrypt all persistent data automatically in memory.",
          "text_kr": "모든 영구 데이터를 메모리에서 자동으로 암호화하기 위함입니다."
        },
        {
          "key": "D",
          "text_en": "To eliminate the need for PVC objects.",
          "text_kr": "PVC 오브젝트의 필요성을 완전히 없애기 위함입니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• 과거의 In-tree 볼륨 플러그인 방식은 스토리지 코드 수정 시 쿠버네티스 자체를 재배포해야 했습니다.\n• CSI는 표준 인터페이스를 제공하여 벤더들이 독립적인 out-of-tree 컨트롤러/노드 플러그인으로 스토리지를 연동할 수 있도록 혁신했습니다.",
      "key_concept": "CSI (Container Storage Interface) Architecture"
    },
    {
      "id": "D4-Q10",
      "domain": "Domain 4",
      "domain_name": "스토리지 (Storage)",
      "question_en": "If a user attempts to delete a PersistentVolumeClaim (PVC) that is currently mounted and being actively used by a running Pod, what is the expected Kubernetes behavior?",
      "question_kr": "현재 실행 중인 파드에 의해 마운트되어 활발히 사용 중인 PersistentVolumeClaim(PVC)을 사용자가 삭제(`kubectl delete pvc`)하려고 시도할 때 쿠버네티스의 예상 동작은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "The PVC deletion is postponed (status shows Terminating) until the Pod using it is terminated (Storage Object in Use Protection).",
          "text_kr": "해당 볼륨을 사용 중인 파드가 종료될 때까지 PVC 삭제가 보류(Terminating 상태)됩니다 (Storage Object in Use Protection)."
        },
        {
          "key": "B",
          "text_en": "The Pod is killed immediately and the data is purged instantly.",
          "text_kr": "파드가 즉시 강제 종료되고 데이터가 즉시 영구 삭제됩니다."
        },
        {
          "key": "C",
          "text_en": "The delete command errors out immediately with exit code 1.",
          "text_kr": "삭제 명령이 종료 코드 1과 함께 즉시 거부 에러를 반환합니다."
        },
        {
          "key": "D",
          "text_en": "The volume unmounts while the container continues running without filesystem access.",
          "text_kr": "볼륨만 언마운트되고 컨테이너는 파일시스템 접근 없이 계속 실행됩니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• 쿠버네티스의 **Storage Object in Use Protection** 기능(Finalizer: `kubernetes.io/pvc-protection`)으로 인해, 실행 중인 파드가 마운트 중인 PVC는 즉시 삭제되지 않고 `Terminating` 상태로 머물며 안전하게 데이터와 파드를 보호합니다.",
      "key_concept": "Storage Object in Use Protection, Finalizers"
    }
  ],
  "domain5": [
    {
      "id": "D5-Q01",
      "domain": "Domain 5",
      "domain_name": "문제 해결 및 장애 진단 (Troubleshooting)",
      "question_en": "A worker node 'worker-1' shows a status of 'NotReady' in `kubectl get nodes`. You SSH into the node to investigate. Which Linux system commands are most effective to diagnose why the Kubernetes node agent is failing?",
      "question_kr": "`kubectl get nodes` 실행 시 워커 노드 'worker-1'이 'NotReady' 상태로 표시됩니다. 원인을 조사하기 위해 해당 노드에 SSH로 접속했습니다. 쿠버네티스 노드 에이전트의 실패 원인을 진단하는 데 가장 효과적인 리눅스 시스템 명령어 조합은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "systemctl status kubelet and journalctl -u kubelet -n 50 --no-pager",
          "text_kr": "systemctl status kubelet 및 journalctl -u kubelet -n 50 --no-pager"
        },
        {
          "key": "B",
          "text_en": "top and netstat -tuln",
          "text_kr": "top 및 netstat -tuln"
        },
        {
          "key": "C",
          "text_en": "cat /var/log/syslog | grep docker",
          "text_kr": "cat /var/log/syslog | grep docker"
        },
        {
          "key": "D",
          "text_en": "kubeadm reset --force",
          "text_kr": "kubeadm reset --force"
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• 워커 노드가 NotReady 상태일 때는 노드의 `kubelet` 서비스 상태를 확인하는 것이 1순위입니다.\n• `systemctl status kubelet`으로 실행 여부를 확인하고, 비정상 종료된 경우 `journalctl -u kubelet -n 50 --no-pager`를 통해 인증서 만료, 설정 파일 오탈자, 컨테이너 런타임 통신 장애 등의 구체적 에러 로그를 확인합니다.",
      "key_concept": "Node NotReady Diagnosis, kubelet troubleshooting with systemctl & journalctl"
    },
    {
      "id": "D5-Q02",
      "domain": "Domain 5",
      "domain_name": "문제 해결 및 장애 진단 (Troubleshooting)",
      "question_en": "A newly deployed Pod 'payment-app' immediately crashes and enters the `CrashLoopBackOff` state. How can you inspect the termination log of the container that just crashed prior to the restart?",
      "question_kr": "새로 배포된 'payment-app' 파드가 기동 직후 비정상 종료되며 `CrashLoopBackOff` 상태로 전환되었습니다. 컨테이너가 재시작되기 직전에 발생하여 비정상 종료를 유발한 이전 컨테이너의 로그를 확인하는 명령어는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "kubectl logs payment-app --previous",
          "text_kr": "kubectl logs payment-app --previous"
        },
        {
          "key": "B",
          "text_en": "kubectl get pod payment-app --watch-crashes",
          "text_kr": "kubectl get pod payment-app --watch-crashes"
        },
        {
          "key": "C",
          "text_en": "kubectl describe pod payment-app --history",
          "text_kr": "kubectl describe pod payment-app --history"
        },
        {
          "key": "D",
          "text_en": "cat /var/log/pods/payment-app/crash.log",
          "text_kr": "cat /var/log/pods/payment-app/crash.log"
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• 컨테이너가 크래시되어 계속 재시작되는 루프에 빠져 있을 때, `kubectl logs <pod-name> --previous` (또는 `-p`) 옵션을 주면 직전에 크래시된 컨테이너의 마지막 표준 출력/에러 로그를 즉시 열람할 수 있습니다.",
      "key_concept": "CrashLoopBackOff Debugging, kubectl logs --previous (-p)"
    },
    {
      "id": "D5-Q03",
      "domain": "Domain 5",
      "domain_name": "문제 해결 및 장애 진단 (Troubleshooting)",
      "question_en": "After editing `/etc/kubernetes/manifests/kube-apiserver.yaml` to add a new flag, the control plane stops responding completely and all `kubectl` commands fail with 'The connection to the server was refused'. How can you inspect the API server container errors on the master node?",
      "question_kr": "새로운 플래그를 추가하기 위해 `/etc/kubernetes/manifests/kube-apiserver.yaml`을 수정한 후, 컨트롤 플레인이 완전히 응답을 멈추고 모든 `kubectl` 명령어가 'The connection to the server was refused' 에러를 반환합니다. 마스터 노드에서 API 서버 컨테이너의 에러 로그를 확인하는 가장 적절한 방법은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "Use the container runtime CLI directly, e.g., `crictl ps -a` to find the stopped container ID, followed by `crictl logs <container-id>`.",
          "text_kr": "컨테이너 런타임 CLI를 직접 사용하여 `crictl ps -a`로 중지된 컨테이너 ID를 확인한 후 `crictl logs <container-id>`를 실행합니다."
        },
        {
          "key": "B",
          "text_en": "Run `kubectl logs kube-apiserver -n kube-system --force`.",
          "text_kr": "`kubectl logs kube-apiserver -n kube-system --force`를 실행합니다."
        },
        {
          "key": "C",
          "text_en": "Reboot the control plane node using `shutdown -r now`.",
          "text_kr": "`shutdown -r now`로 컨트롤 플레인 노드를 재부팅합니다."
        },
        {
          "key": "D",
          "text_en": "Re-run `kubeadm init` over the existing cluster.",
          "text_kr": "기존 클러스터 위에 `kubeadm init`을 다시 실행합니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• API 서버 자체가 다운되어 있을 때는 API 서버에 의존하는 `kubectl` 명령어가 전혀 동작하지 않습니다.\n• 따라서 노드 수준의 컨테이너 런타임 인터페이스인 `crictl` 명령(`crictl ps -a`, `crictl logs <ID>`)을 사용하여 API 서버 컨테이너가 어떤 플래그나 문법 오류로 인해 기동 실패했는지 직접 확인해야 합니다.",
      "key_concept": "API Server Down Diagnosis, Container Runtime crictl ps/logs"
    },
    {
      "id": "D5-Q04",
      "domain": "Domain 5",
      "domain_name": "문제 해결 및 장애 진단 (Troubleshooting)",
      "question_en": "You notice that a Service named 'auth-service' has an active ClusterIP, but any request directed to this service times out. Running `kubectl get endpoints auth-service` shows `<none>`. What is the most likely root cause?",
      "question_kr": "'auth-service'라는 서비스에 유효한 ClusterIP가 할당되어 있으나, 이 서비스로 보내는 모든 요청이 타임아웃됩니다. `kubectl get endpoints auth-service`를 실행해보니 `<none>`으로 표시됩니다. 가장 유력한 근본 원인은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "The Service's `spec.selector` labels do not match the labels defined in the target Pods' metadata.",
          "text_kr": "서비스의 `spec.selector` 라벨이 대상 파드의 메타데이터에 정의된 라벨과 일치하지 않습니다."
        },
        {
          "key": "B",
          "text_en": "The node running the pods has run out of disk space.",
          "text_kr": "파드를 실행 중인 노드의 디스크 공간이 부족합니다."
        },
        {
          "key": "C",
          "text_en": "CoreDNS is not running.",
          "text_kr": "CoreDNS가 실행 중이지 않습니다."
        },
        {
          "key": "D",
          "text_en": "ClusterIP services cannot have endpoints.",
          "text_kr": "ClusterIP 서비스는 엔드포인트를 가질 수 없습니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• 쿠버네티스 서비스는 `spec.selector`에 정의된 라벨과 일치하는 정상(Ready) 상태의 파드 IP들을 자동으로 수집하여 `Endpoints` 리소스를 구성합니다.\n• 엔드포인트가 `<none>`이라는 것은 서비스의 셀렉터와 파드의 라벨이 불일치(오탈자)하거나, 파드들의 준비성 프로브(Readiness Probe)가 실패하여 트래픽 대상에서 제외되었음을 의미합니다.",
      "key_concept": "Empty Endpoints (<none>), Service Selector Label Mismatch"
    },
    {
      "id": "D5-Q05",
      "domain": "Domain 5",
      "domain_name": "문제 해결 및 장애 진단 (Troubleshooting)",
      "question_en": "A Pod stays in the `ImagePullBackOff` state. In `kubectl describe pod`, the Events section indicates `Failed to pull image ... repository does not exist or may require 'docker login'`. What is required to resolve this issue if the image is stored in a private container registry?",
      "question_kr": "파드가 `ImagePullBackOff` 상태에 머물러 있습니다. `kubectl describe pod`의 Events 섹션에 `Failed to pull image ... repository does not exist or may require 'docker login'` 메시지가 나타납니다. 해당 이미지가 프라이빗 컨테이너 레지스트리에 저장되어 있는 경우 이 문제를 해결하기 위해 필요한 조치는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "Create a docker-registry Secret containing authentication credentials and reference it in the Pod's `spec.imagePullSecrets`.",
          "text_kr": "인증 자격 증명을 포함하는 docker-registry Secret을 생성하고 파드의 `spec.imagePullSecrets`에 참조합니다."
        },
        {
          "key": "B",
          "text_en": "Disable TLS verification in kubelet.",
          "text_kr": "kubelet의 TLS 검증을 비활성화합니다."
        },
        {
          "key": "C",
          "text_en": "Change the image pull policy to Always.",
          "text_kr": "이미지 풀 정책(imagePullPolicy)을 Always로 변경합니다."
        },
        {
          "key": "D",
          "text_en": "Grant cluster-admin permissions to the default ServiceAccount.",
          "text_kr": "default ServiceAccount에 cluster-admin 권한을 부여합니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• 프라이빗 레지스트리 이미지를 가져오려면 `kubectl create secret docker-registry <이름> --docker-server=... --docker-username=... --docker-password=...`로 시크릿을 생성한 후,\n• 파드 스펙의 `spec.imagePullSecrets: [{name: <시크릿이름>}]`에 등록해야 정상적으로 인증 후 이미지를 풀(Pull)할 수 있습니다.",
      "key_concept": "ImagePullBackOff, Private Registry Secret, imagePullSecrets"
    },
    {
      "id": "D5-Q06",
      "domain": "Domain 5",
      "domain_name": "문제 해결 및 장애 진단 (Troubleshooting)",
      "question_en": "Applications across the cluster are failing to resolve external domain names as well as internal service names. You inspect the `kube-system` namespace and see CoreDNS pods in `CrashLoopBackOff` state with logs showing `Loop (127.0.0.1:53 ... -> :53): loop detected`. What is the typical cause of this error?",
      "question_kr": "클러스터 전역의 애플리케이션들이 내부 서비스 이름 및 외부 도메인 이름을 해석하지 못하고 있습니다. `kube-system` 네임스페이스를 확인하니 CoreDNS 파드가 `CrashLoopBackOff` 상태이고 로그에 `Loop (127.0.0.1:53 ... -> :53): loop detected` 에러가 기록되어 있습니다. 이 에러의 전형적인 원인은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "Host node's /etc/resolv.conf points nameserver to a loopback address (127.0.0.53/127.0.0.1), creating a forwarding loop inside the CoreDNS forward plugin.",
          "text_kr": "호스트 노드의 /etc/resolv.conf 네임서버가 루프백 주소(127.0.0.53/127.0.0.1)를 가리키고 있어 CoreDNS 포워드 플러그인 내부에서 무한 순환 루프가 발생했기 때문입니다."
        },
        {
          "key": "B",
          "text_en": "The CoreDNS image is corrupt.",
          "text_kr": "CoreDNS 컨테이너 이미지가 손상되었기 때문입니다."
        },
        {
          "key": "C",
          "text_en": "Kubelet is blocking port 53 traffic.",
          "text_kr": "kubelet이 53번 포트 트래픽을 차단하고 있기 때문입니다."
        },
        {
          "key": "D",
          "text_en": "NetworkPolicy is missing a cluster-wide ingress allow.",
          "text_kr": "NetworkPolicy에 클러스터 전역 인그레스 허용 규칙이 누락되었기 때문입니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• CoreDNS는 업스트림 DNS 해석을 위해 기본적으로 호스트 노드의 `/etc/resolv.conf`를 참조합니다.\n• 호스트가 systemd-resolved(127.0.0.53)를 사용할 때 CoreDNS가 자기 자신에게 다시 DNS 질의를 포워딩하면서 루프(Loop)가 발생합니다.\n• kubelet의 `--resolv-conf` 경로를 실제 외부 DNS(8.8.8.8 등)가 정의된 파일로 지정하거나 CoreDNS Corefile의 loop 플러그인/포워딩 설정을 수정하여 해결합니다.",
      "key_concept": "CoreDNS Loop Detected Troubleshooting"
    },
    {
      "id": "D5-Q07",
      "domain": "Domain 5",
      "domain_name": "문제 해결 및 장애 진단 (Troubleshooting)",
      "question_en": "A Pod's status displays `Pending`. Running `kubectl describe pod` displays an Event: `0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 2 node(s) had insufficient cpu`. What action will allow this Pod to run?",
      "question_kr": "파드의 상태가 `Pending`으로 표시됩니다. `kubectl describe pod`를 실행하니 `0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 2 node(s) had insufficient cpu` 이벤트가 발생했습니다. 이 파드가 정상 실행되도록 조치할 수 있는 방법은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "Decrease the Pod's `resources.requests.cpu` or scale down/delete unnecessary workloads on worker nodes to free up CPU.",
          "text_kr": "해당 파드의 `resources.requests.cpu`를 낮추거나, 워커 노드의 불필요한 워크로드를 축소/삭제하여 가용 CPU를 확보합니다."
        },
        {
          "key": "B",
          "text_en": "Restart kube-scheduler.",
          "text_kr": "kube-scheduler를 재시작합니다."
        },
        {
          "key": "C",
          "text_en": "Remove the control-plane node from the cluster.",
          "text_kr": "클러스터에서 컨트롤 플레인 노드를 제거합니다."
        },
        {
          "key": "D",
          "text_en": "Add a toleration for memory pressure.",
          "text_kr": "메모리 압박에 대한 toleration을 추가합니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• 이벤트 로그 분석 결과: 1개 마스터 노드는 마스터 전용 테인트로 인해 거부되었고, 나머지 2개 워커 노드는 파드가 요구하는 CPU request를 충족시킬 여유 용량이 부족합니다.\n• 따라서 파드의 CPU request 요구량을 낮추거나 워커 노드의 여유 CPU를 확보해야 스케줄러가 노드를 배정할 수 있습니다.",
      "key_concept": "Pod Pending Diagnosis, Insufficient CPU / Resource Requests"
    },
    {
      "id": "D5-Q08",
      "domain": "Domain 5",
      "domain_name": "문제 해결 및 장애 진단 (Troubleshooting)",
      "question_en": "How can you quickly check the real-time resource utilization (CPU and Memory) of all worker nodes in the cluster?",
      "question_kr": "클러스터 내 모든 워커 노드의 실시간 리소스(CPU 및 메모리) 사용량을 신속하게 확인하는 명령어는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "kubectl top nodes",
          "text_kr": "kubectl top nodes"
        },
        {
          "key": "B",
          "text_en": "kubectl stats cluster",
          "text_kr": "kubectl stats cluster"
        },
        {
          "key": "C",
          "text_en": "kubectl get nodes --metrics",
          "text_kr": "kubectl get nodes --metrics"
        },
        {
          "key": "D",
          "text_en": "kubectl monitor nodes",
          "text_kr": "kubectl monitor nodes"
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• Metrics Server가 설치된 환경에서 `kubectl top nodes`와 `kubectl top pods` 명령을 사용하면 노드와 파드의 실시간 CPU(cores/m) 및 메모리(bytes/Mi) 사용량을 확인할 수 있습니다.",
      "key_concept": "kubectl top nodes/pods, Metrics Server"
    },
    {
      "id": "D5-Q09",
      "domain": "Domain 5",
      "domain_name": "문제 해결 및 장애 진단 (Troubleshooting)",
      "question_en": "A worker node suddenly transitions into 'NotReady' state with the condition `DiskPressure: True`. What behavior will the kubelet exhibit regarding workloads running on this node?",
      "question_kr": "워커 노드가 갑자기 `DiskPressure: True` 상태 조건과 함께 'NotReady' 또는 불안정한 상태로 전환되었습니다. kubelet은 이 노드에서 실행 중인 워크로드에 대해 어떤 조치를 취합니까?",
      "options": [
        {
          "key": "A",
          "text_en": "kubelet immediately starts reclaiming disk space by deleting unused container images and evicting pods according to their QoS class.",
          "text_kr": "kubelet이 미사용 컨테이너 이미지를 삭제하고 QoS 클래스 우선순위에 따라 파드들을 노드에서 퇴거(Eviction)시켜 디스크 공간 확보를 시도합니다."
        },
        {
          "key": "B",
          "text_en": "kubelet crashes and halts the server.",
          "text_kr": "kubelet이 비정상 종료되고 서버가 다운됩니다."
        },
        {
          "key": "C",
          "text_en": "All persistent volumes are unmounted immediately.",
          "text_kr": "모든 영구 볼륨이 즉시 강제 언마운트됩니다."
        },
        {
          "key": "D",
          "text_en": "The node automatically formats its root filesystem.",
          "text_kr": "노드가 루트 파일시스템을 자동으로 포맷합니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• `DiskPressure` 조건이 발동하면 노드 보호를 위해 kubelet이 데드 컨테이너와 캐시된 미사용 이미지를 가비지 컬렉션(GC)하고, 여전히 부족할 경우 BestEffort -> Burstable 우선순위로 파드를 Evict(축출)합니다.",
      "key_concept": "Node DiskPressure Condition and Pod Eviction"
    },
    {
      "id": "D5-Q10",
      "domain": "Domain 5",
      "domain_name": "문제 해결 및 장애 진단 (Troubleshooting)",
      "question_en": "You execute `kubectl get events -n prod --sort-by='.metadata.creationTimestamp'` and notice multiple warnings: `FailedScheduling: 0/4 nodes are available: 4 node(s) had taint {tier: backend}, that the pod didn't tolerate`. What is the fastest command to remove this taint from node 'node-1'?",
      "question_kr": "`kubectl get events -n prod --sort-by='.metadata.creationTimestamp'` 실행 결과 `FailedScheduling: 0/4 nodes are available: 4 node(s) had taint {tier: backend}, that the pod didn't tolerate` 경고가 다수 발생했습니다. 'node-1' 노드에서 이 테인트를 제거하는 가장 빠른 명령어는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "kubectl taint nodes node-1 tier:backend-",
          "text_kr": "kubectl taint nodes node-1 tier:backend-"
        },
        {
          "key": "B",
          "text_en": "kubectl taint nodes node-1 tier-",
          "text_kr": "kubectl taint nodes node-1 tier-"
        },
        {
          "key": "C",
          "text_en": "kubectl untaint node-1 tier=backend",
          "text_kr": "kubectl untaint node-1 tier=backend"
        },
        {
          "key": "D",
          "text_en": "kubectl delete taint tier from node-1",
          "text_kr": "kubectl delete taint tier from node-1"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• 쿠버네티스에서 Taint를 제거할 때는 `kubectl taint nodes <노드이름> <키>-` 또는 `kubectl taint nodes <노드이름> <키>=<값>:<이펙트>-`처럼 맨 뒤에 대시(`-`) 기호를 붙여 제거합니다.\n• `tier-` 또는 `tier=backend:NoSchedule-` 형식이 올바릅니다.",
      "key_concept": "Removing Taints with kubectl taint nodes <node> <key>-"
    }
  ],
  "mock1": [
    {
      "id": "D1-Q01",
      "domain": "Domain 1",
      "domain_name": "클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration)",
      "question_en": "You need to create a snapshot backup of an existing etcd instance running as a static pod. The etcd client certificates are located at /etc/kubernetes/pki/etcd/server.crt and /etc/kubernetes/pki/etcd/server.key, and the CA certificate is at /etc/kubernetes/pki/etcd/ca.crt. Which command correctly creates the snapshot at /var/lib/etcd-snapshot.db?",
      "question_kr": "스태틱 파드로 실행 중인 기존 etcd 인스턴스의 스냅샷 백업을 생성해야 합니다. etcd 클라이언트 인증서는 /etc/kubernetes/pki/etcd/server.crt 및 server.key에 위치하고, CA 인증서는 ca.crt에 위치합니다. /var/lib/etcd-snapshot.db 경로에 스냅샷을 올바르게 생성하는 명령어는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "etcdctl backup save --endpoints=https://127.0.0.1:2379 /var/lib/etcd-snapshot.db",
          "text_kr": "etcdctl backup save --endpoints=https://127.0.0.1:2379 /var/lib/etcd-snapshot.db"
        },
        {
          "key": "B",
          "text_en": "ETCDCTL_API=3 etcdctl snapshot save /var/lib/etcd-snapshot.db --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key",
          "text_kr": "ETCDCTL_API=3 etcdctl snapshot save /var/lib/etcd-snapshot.db --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key"
        },
        {
          "key": "C",
          "text_en": "kubectl snapshot etcd /var/lib/etcd-snapshot.db --all-certificates",
          "text_kr": "kubectl snapshot etcd /var/lib/etcd-snapshot.db --all-certificates"
        },
        {
          "key": "D",
          "text_en": "kubeadm backup etcd --output=/var/lib/etcd-snapshot.db",
          "text_kr": "kubeadm backup etcd --output=/var/lib/etcd-snapshot.db"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• etcd v3 API를 사용할 때는 환경변수 `ETCDCTL_API=3`을 지정해야 하며, `snapshot save <경로>` 명령어를 사용합니다.\n• 보안이 활성화된 etcd 클러스터 통신을 위해 `--cacert`, `--cert`, `--key` 옵션으로 유효한 인증서와 키를 반드시 함께 전달해야 합니다.\n• A는 인증서 플래그와 snapshot save 문법이 누락되었습니다.\n• C와 D는 존재하지 않는 명령어입니다.",
      "key_concept": "etcdctl snapshot save, TLS Authentication Flags (--cacert, --cert, --key)"
    },
    {
      "id": "D1-Q02",
      "domain": "Domain 1",
      "domain_name": "클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration)",
      "question_en": "You are tasked with upgrading the control plane node of a Kubernetes cluster using kubeadm from version 1.30.0 to 1.31.0. Before performing the package upgrade, what is the recommended procedure to ensure running workloads on the control plane node are safely evicted or ignored?",
      "question_kr": "kubeadm을 사용하여 쿠버네티스 컨트롤 플레인 노드를 버전 1.30.0에서 1.31.0으로 업그레이드해야 합니다. 패키지 업그레이드를 수행하기 전에 컨트롤 플레인 노드에서 실행 중인 워크로드를 안전하게 퇴거하거나 무시하도록 조치하는 권장 절차는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "kubectl delete node controlplane --force",
          "text_kr": "kubectl delete node controlplane --force"
        },
        {
          "key": "B",
          "text_en": "kubectl drain controlplane --ignore-daemonsets",
          "text_kr": "kubectl drain controlplane --ignore-daemonsets"
        },
        {
          "key": "C",
          "text_en": "kubectl cordon controlplane --delete-emptydir-data",
          "text_kr": "kubectl cordon controlplane --delete-emptydir-data"
        },
        {
          "key": "D",
          "text_en": "kubeadm upgrade prepare controlplane",
          "text_kr": "kubeadm upgrade prepare controlplane"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• 노드 유지보수 및 업그레이드 전에는 `kubectl drain <노드이름> --ignore-daemonsets`를 실행하여 노드를 스케줄링 불능(cordon) 상태로 만들고 기존 파드들을 안전하게 다른 노드로 축출(evict)해야 합니다.\n• DaemonSet 파드는 노드에서 배출될 수 없으므로 `--ignore-daemonsets` 플래그를 붙여야 drain 명령이 정상 완료됩니다.\n• 업그레이드가 완료된 후에는 `kubectl uncordon <노드이름>`으로 복구합니다.",
      "key_concept": "kubectl drain, Node Maintenance, Cluster Upgrade Procedure"
    },
    {
      "id": "D1-Q03",
      "domain": "Domain 1",
      "domain_name": "클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration)",
      "question_en": "A junior administrator needs read-only access to view and list Pods only within the 'development' namespace. Which set of RBAC resources must be created to achieve this without granting cluster-wide permissions?",
      "question_kr": "주니어 관리자가 'development' 네임스페이스 내에서만 파드를 조회(get)하고 목록화(list)할 수 있는 읽기 전용 권한이 필요합니다. 클러스터 전체 권한을 부여하지 않고 이를 달성하기 위해 생성해야 하는 RBAC 리소스 조합은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "A ClusterRole in the development namespace and a ClusterRoleBinding",
          "text_kr": "development 네임스페이스의 ClusterRole 및 ClusterRoleBinding"
        },
        {
          "key": "B",
          "text_en": "A Role defined in the development namespace and a RoleBinding in the development namespace",
          "text_kr": "development 네임스페이스에 정의된 Role과 development 네임스페이스의 RoleBinding"
        },
        {
          "key": "C",
          "text_en": "A ServiceAccount bound directly to the PodSpec without RBAC",
          "text_kr": "RBAC 없이 PodSpec에 직접 바인딩된 ServiceAccount"
        },
        {
          "key": "D",
          "text_en": "A ClusterRoleBinding scoped with a namespace filter flag",
          "text_kr": "네임스페이스 필터 플래그가 지정된 ClusterRoleBinding"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• 특정 네임스페이스로 범위를 제한할 때는 반드시 네임스페이스 리소스인 `Role`과 `RoleBinding`을 해당 네임스페이스(`development`) 내에 생성해야 합니다.\n• ClusterRole은 클러스터 전역 범위이며, ClusterRoleBinding을 사용하면 모든 네임스페이스에 권한이 전파되므로 최소 권한 원칙(Principle of Least Privilege)에 위배됩니다.",
      "key_concept": "RBAC Role vs ClusterRole, RoleBinding Scope"
    },
    {
      "id": "D1-Q04",
      "domain": "Domain 1",
      "domain_name": "클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration)",
      "question_en": "How does kubelet know to start and manage static pods such as kube-apiserver and kube-controller-manager on a control plane node?",
      "question_kr": "kubelet은 컨트롤 플레인 노드에서 kube-apiserver 및 kube-controller-manager와 같은 스태틱 파드(Static Pods)를 어떻게 인식하고 시작 및 관리합니까?",
      "options": [
        {
          "key": "A",
          "text_en": "The API server sends a webhook request to kubelet on boot.",
          "text_kr": "API 서버가 부팅 시 kubelet에 웹훅 요청을 보냅니다."
        },
        {
          "key": "B",
          "text_en": "kubelet watches the staticPodPath directory (default: /etc/kubernetes/manifests) defined in its configuration file.",
          "text_kr": "kubelet이 설정 파일에 정의된 staticPodPath 디렉토리(기본값: /etc/kubernetes/manifests)를 직접 감시합니다."
        },
        {
          "key": "C",
          "text_en": "systemd launches static pods using docker run commands directly.",
          "text_kr": "systemd가 docker run 명령어로 스태틱 파드를 직접 실행합니다."
        },
        {
          "key": "D",
          "text_en": "kube-scheduler assigns static pods to node-0 based on affinity.",
          "text_kr": "kube-scheduler가 어피니티에 따라 스태틱 파드를 node-0에 할당합니다."
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• 스태틱 파드는 API 서버의 개입 없이 노드의 `kubelet` 데몬이 특정 로컬 디렉토리(기본: `/etc/kubernetes/manifests`)에 위치한 YAML 매니페스트 파일을 주기적으로 스캔하여 직접 띄우고 라이프사이클을 관리합니다.\n• 컨트롤 플레인의 핵심 컴포넌트(apiserver, etcd, scheduler, controller-manager)는 모두 스태틱 파드로 구동됩니다.",
      "key_concept": "Static Pods, kubelet staticPodPath, Control Plane Bootstrap"
    },
    {
      "id": "D2-Q01",
      "domain": "Domain 2",
      "domain_name": "워크로드 및 스케줄링 (Workloads & Scheduling)",
      "question_en": "A deployment named 'frontend-deploy' was updated to an unstable image version, causing pods to crash. You need to immediately roll back this deployment to its immediately preceding revision. Which command should you run?",
      "question_kr": "'frontend-deploy'라는 이름의 디플로이먼트가 불안정한 이미지 버전으로 업데이트되어 파드들이 비정상 종료되고 있습니다. 이 디플로이먼트를 직전 리비전으로 즉시 롤백해야 합니다. 실행해야 하는 명령어는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "kubectl rollout undo deployment frontend-deploy",
          "text_kr": "kubectl rollout undo deployment frontend-deploy"
        },
        {
          "key": "B",
          "text_en": "kubectl revert deployment frontend-deploy --step=1",
          "text_kr": "kubectl revert deployment frontend-deploy --step=1"
        },
        {
          "key": "C",
          "text_en": "kubectl rollout restart deployment frontend-deploy",
          "text_kr": "kubectl rollout restart deployment frontend-deploy"
        },
        {
          "key": "D",
          "text_en": "kubectl set image deployment/frontend-deploy --previous",
          "text_kr": "kubectl set image deployment/frontend-deploy --previous"
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• `kubectl rollout undo deployment <이름>`은 추가 옵션이 없을 때 직전 리비전(Revision)으로 즉시 롤백합니다.\n• 특정 리비전으로 롤백하려면 `--to-revision=<번호>` 옵션을 지정할 수 있습니다.",
      "key_concept": "kubectl rollout undo, Deployment Rollback"
    },
    {
      "id": "D2-Q02",
      "domain": "Domain 2",
      "domain_name": "워크로드 및 스케줄링 (Workloads & Scheduling)",
      "question_en": "You are creating a multi-container Pod where a logging container needs to read log files generated by the primary application container. What type of volume should be defined in the Pod spec so that both containers can share this directory without persisting data to a remote storage system?",
      "question_kr": "로깅 컨테이너가 기본 애플리케이션 컨테이너에서 생성된 로그 파일을 읽어야 하는 멀티 컨테이너 파드를 생성하고 있습니다. 원격 스토리지 시스템에 데이터를 영구 저장하지 않고 두 컨테이너가 이 디렉토리를 공유할 수 있도록 Pod spec에 정의해야 하는 볼륨 유형은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "persistentVolumeClaim",
          "text_kr": "persistentVolumeClaim"
        },
        {
          "key": "B",
          "text_en": "emptyDir",
          "text_kr": "emptyDir"
        },
        {
          "key": "C",
          "text_en": "hostPath with type Socket",
          "text_kr": "hostPath with type Socket"
        },
        {
          "key": "D",
          "text_en": "configMap",
          "text_kr": "configMap"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• `emptyDir` 볼륨은 파드가 노드에 할당될 때 처음 생성되며, 해당 파드 내의 모든 컨테이너가 동일한 디렉토리를 읽고 쓸 수 있는 임시 공유 볼륨입니다.\n• 파드가 삭제되면 데이터도 함께 삭제되므로 사이드카 로깅 패턴이나 임시 작업 디렉토리에 가장 적합합니다.",
      "key_concept": "emptyDir Volume, Multi-container Shared Storage"
    },
    {
      "id": "D2-Q03",
      "domain": "Domain 2",
      "domain_name": "워크로드 및 스케줄링 (Workloads & Scheduling)",
      "question_en": "A node named 'node-dedicated' has been tainted with `dedicated=analytics:NoSchedule`. You need to ensure a new pod can be scheduled on this node while other pods avoid it. What must be included in the Pod's specification?",
      "question_kr": "'node-dedicated'라는 노드에 `dedicated=analytics:NoSchedule` 테인트가 적용되었습니다. 다른 일반 파드는 이 노드를 피하고, 특정 신규 파드만 이 노드에 스케줄링될 수 있도록 보장해야 합니다. 해당 파드의 Pod spec에 포함되어야 하는 설정은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "spec.nodeSelector with dedicated: analytics only",
          "text_kr": "dedicated: analytics 가 지정된 spec.nodeSelector 만 포함"
        },
        {
          "key": "B",
          "text_en": "spec.tolerations with key 'dedicated', operator 'Equal', value 'analytics', and effect 'NoSchedule'",
          "text_kr": "key 'dedicated', operator 'Equal', value 'analytics', effect 'NoSchedule' 이 정의된 spec.tolerations"
        },
        {
          "key": "C",
          "text_en": "spec.securityContext with privileged: true",
          "text_kr": "privileged: true 로 설정된 spec.securityContext"
        },
        {
          "key": "D",
          "text_en": "metadata.annotations with taint.ignore=true",
          "text_kr": "taint.ignore=true 가 정의된 metadata.annotations"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• 노드에 설정된 Taint(`NoSchedule`)는 기본적으로 파드가 스케줄링되는 것을 차단합니다.\n• 파드가 이 테인트를 무시하고 배정되려면 파드 스펙에 일치하는 `tolerations` 블록(key, value, effect)을 정의해야 합니다.",
      "key_concept": "Taints and Tolerations, Pod Scheduling Specification"
    },
    {
      "id": "D2-Q04",
      "domain": "Domain 2",
      "domain_name": "워크로드 및 스케줄링 (Workloads & Scheduling)",
      "question_en": "Which NodeAffinity rule strictly mandates that a Pod must NEVER be scheduled on a node unless the node has the label `disktype=ssd`?",
      "question_kr": "노드에 `disktype=ssd` 라벨이 존재하지 않는 한, 파드가 절대로 해당 노드에 스케줄링되어서는 안 된다고 엄격하게 강제하는 NodeAffinity 규칙은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "preferredDuringSchedulingIgnoredDuringExecution",
          "text_kr": "preferredDuringSchedulingIgnoredDuringExecution"
        },
        {
          "key": "B",
          "text_en": "requiredDuringSchedulingIgnoredDuringExecution",
          "text_kr": "requiredDuringSchedulingIgnoredDuringExecution"
        },
        {
          "key": "C",
          "text_en": "requiredDuringSchedulingRequiredDuringExecution",
          "text_kr": "requiredDuringSchedulingRequiredDuringExecution"
        },
        {
          "key": "D",
          "text_en": "preferredDuringSchedulingRequiredDuringExecution",
          "text_kr": "preferredDuringSchedulingRequiredDuringExecution"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• `requiredDuringSchedulingIgnoredDuringExecution`은 '하드 룰(Hard Rule)'로, 스케줄링 시점에 조건이 만족되지 않으면 파드가 Pending 상태로 남고 절대 배치되지 않습니다.\n• `preferredDuring...`은 '소프트 룰'로, 조건을 만족하는 노드가 없더라도 다른 일반 노드에 스케줄링됩니다.",
      "key_concept": "NodeAffinity Hard Rule vs Soft Rule"
    },
    {
      "id": "D3-Q01",
      "domain": "Domain 3",
      "domain_name": "서비스 및 네트워킹 (Services & Networking)",
      "question_en": "In a Kubernetes Service definition of type NodePort, what does `targetPort` refer to?",
      "question_kr": "NodePort 타입의 쿠버네티스 서비스 정의에서 `targetPort`는 무엇을 의미합니까?",
      "options": [
        {
          "key": "A",
          "text_en": "The port on the worker node's external IP address.",
          "text_kr": "워커 노드의 외부 IP 주소에 열리는 포트."
        },
        {
          "key": "B",
          "text_en": "The port on which the Service itself serves traffic inside the cluster.",
          "text_kr": "클러스터 내부에서 서비스 가상 IP(VIP)가 트래픽을 수신하는 포트."
        },
        {
          "key": "C",
          "text_en": "The port on which the container inside the targeted Pod is listening.",
          "text_kr": "대상이 되는 파드 내부의 컨테이너가 실제로 수신 대기(리스닝)하고 있는 포트."
        },
        {
          "key": "D",
          "text_en": "The port used by the Ingress Controller to route traffic.",
          "text_kr": "인그레스 컨트롤러가 트래픽을 라우팅하기 위해 사용하는 포트."
        }
      ],
      "correct_answer": "C",
      "explanation_kr": "정답은 C입니다.\n\n• `port`: Service의 가상 IP가 클러스터 내부에서 노출하는 포트.\n• `targetPort`: 파드 내부의 컨테이너가 실제로 리스닝하고 있는 포트.\n• `nodePort`: 외부 클라이언트가 각 노드의 IP로 접근할 때 사용하는 포트 (30000~32767).",
      "key_concept": "Service Port vs TargetPort vs NodePort"
    },
    {
      "id": "D3-Q02",
      "domain": "Domain 3",
      "domain_name": "서비스 및 네트워킹 (Services & Networking)",
      "question_en": "What is the primary characteristic of a 'Headless Service' created with `spec.clusterIP: None`?",
      "question_kr": "`spec.clusterIP: None`으로 생성된 '헤드리스 서비스(Headless Service)'의 주요 특징은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "It does not allocate a cluster virtual IP and DNS queries return the individual IPs of the backend pods directly.",
          "text_kr": "단일 가상 IP(VIP)를 할당하지 않으며, DNS 질의 시 백엔드 개별 파드들의 IP 목록을 직접 반환합니다."
        },
        {
          "key": "B",
          "text_en": "It does not allow any network traffic to reach the pods.",
          "text_kr": "파드로의 모든 네트워크 트래픽 인입을 차단합니다."
        },
        {
          "key": "C",
          "text_en": "It can only be used with DaemonSets.",
          "text_kr": "오직 DaemonSet과만 함께 사용할 수 있습니다."
        },
        {
          "key": "D",
          "text_en": "It automatically assigns a public Load Balancer IP.",
          "text_kr": "퍼블릭 로드밸런서 IP를 자동으로 할당합니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• `clusterIP: None`으로 설정하면 kube-proxy가 프록시 작업을 수행하지 않고 VIP도 할당되지 않습니다.\n• 대신 CoreDNS에 질의했을 때 셀렉터와 일치하는 파드들의 실제 A 레코드(IP 목록)를 직접 반환하므로, StatefulSet 기반 데이터베이스 클러스터의 마스터-슬레이브 디스커버리에 주로 활용됩니다.",
      "key_concept": "Headless Service (clusterIP: None), StatefulSet DNS"
    },
    {
      "id": "D3-Q03",
      "domain": "Domain 3",
      "domain_name": "서비스 및 네트워킹 (Services & Networking)",
      "question_en": "A pod in the 'staging' namespace needs to send an HTTP request to a service named 'inventory-svc' located in the 'production' namespace on port 80. What is the Fully Qualified Domain Name (FQDN) to resolve this service?",
      "question_kr": "'staging' 네임스페이스의 파드가 'production' 네임스페이스에 있는 'inventory-svc' 서비스의 80번 포트로 HTTP 요청을 보내야 합니다. 이 서비스를 해석하기 위한 FQDN(전체 도메인 이름)은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "inventory-svc.staging.pod.cluster.local",
          "text_kr": "inventory-svc.staging.pod.cluster.local"
        },
        {
          "key": "B",
          "text_en": "inventory-svc.production.svc.cluster.local",
          "text_kr": "inventory-svc.production.svc.cluster.local"
        },
        {
          "key": "C",
          "text_en": "production.inventory-svc.k8s.local",
          "text_kr": "production.inventory-svc.k8s.local"
        },
        {
          "key": "D",
          "text_en": "http://inventory-svc:80/production",
          "text_kr": "http://inventory-svc:80/production"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• 쿠버네티스 CoreDNS 표준 FQDN 형식은 `<서비스명>.<네임스페이스>.svc.cluster.local`입니다.\n• 따라서 'production' 네임스페이스의 'inventory-svc'는 `inventory-svc.production.svc.cluster.local`로 해석됩니다.",
      "key_concept": "CoreDNS FQDN Resolution Pattern"
    },
    {
      "id": "D3-Q04",
      "domain": "Domain 3",
      "domain_name": "서비스 및 네트워킹 (Services & Networking)",
      "question_en": "You create an Ingress resource with path routing rules, but accessing the configured host returns a connection refused error or 404 from the node IP. What is the most likely cluster prerequisite missing?",
      "question_kr": "경로 기반 라우팅 규칙이 포함된 Ingress 리소스를 생성했으나, 노드 IP로 해당 호스트에 접속하면 연결 거부 또는 404 에러가 발생합니다. 클러스터에 누락되었을 가능성이 가장 높은 필수 전제 조건은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "The cluster lacks an active Ingress Controller (such as ingress-nginx) to implement the Ingress specification.",
          "text_kr": "Ingress 명세를 실제로 구현하고 트래픽을 처리할 활성화된 인그레스 컨트롤러(예: ingress-nginx)가 클러스터에 없습니다."
        },
        {
          "key": "B",
          "text_en": "NetworkPolicy does not permit ingress resources by default.",
          "text_kr": "NetworkPolicy가 기본적으로 ingress 리소스를 허용하지 않기 때문입니다."
        },
        {
          "key": "C",
          "text_en": "Ingress resources require a commercial SSL certificate before passing any traffic.",
          "text_kr": "Ingress 리소스는 트래픽을 전달하기 전에 상용 SSL 인증서가 반드시 필요합니다."
        },
        {
          "key": "D",
          "text_en": "CoreDNS must be reconfigured to register ingress paths.",
          "text_kr": "CoreDNS가 인그레스 경로를 등록하도록 재설정되어야 합니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• Ingress 리소스는 단순한 '라우팅 규칙 설정 데이터'에 불과합니다.\n• 이 규칙을 감시하여 실제 리버스 프록시(Nginx, HAProxy, Envoy 등)를 구동하고 트래픽을 분기해줄 **Ingress Controller**가 클러스터에 실행 중이지 않으면 아무런 동작도 일어나지 않습니다.",
      "key_concept": "Ingress Resource vs Ingress Controller"
    },
    {
      "id": "D4-Q01",
      "domain": "Domain 4",
      "domain_name": "스토리지 (Storage)",
      "question_en": "A PersistentVolume (PV) is created with a capacity of 10Gi, `accessModes: [ReadWriteOnce]`, and `storageClassName: manual`. A user creates a PersistentVolumeClaim (PVC) requesting 5Gi with `accessModes: [ReadWriteMany]` and `storageClassName: manual`. Why does the PVC remain in the 'Pending' status?",
      "question_kr": "용량 10Gi, `accessModes: [ReadWriteOnce]`, `storageClassName: manual`로 생성된 PersistentVolume(PV)이 있습니다. 사용자가 5Gi 용량, `accessModes: [ReadWriteMany]`, `storageClassName: manual`을 요청하는 PersistentVolumeClaim(PVC)을 생성했습니다. 이 PVC가 'Pending' 상태로 머무르는 이유는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "The requested storage capacity is smaller than the PV capacity.",
          "text_kr": "요청된 스토리지 용량이 PV 용량보다 작기 때문입니다."
        },
        {
          "key": "B",
          "text_en": "The accessModes between the PV (ReadWriteOnce) and the PVC (ReadWriteMany) do not match.",
          "text_kr": "PV의 접근 모드(ReadWriteOnce)와 PVC의 요청 접근 모드(ReadWriteMany)가 일치하지 않기 때문입니다."
        },
        {
          "key": "C",
          "text_en": "StorageClassName 'manual' is a reserved keyword in Kubernetes.",
          "text_kr": "StorageClassName 'manual'이 쿠버네티스 예약어이기 때문입니다."
        },
        {
          "key": "D",
          "text_en": "PVCs cannot bind to PVs without an active Pod attached.",
          "text_kr": "활성 파드가 연결되지 않으면 PVC가 PV에 바인딩될 수 없기 때문입니다."
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• PVC가 PV에 정상적으로 바인딩(Bound)되려면 **StorageClassName**, **AccessModes**, 그리고 **요청 용량(Capacity <= PV 용량)**이 모두 호환되어야 합니다.\n• PV는 단일 노드 전용(`ReadWriteOnce`)인 반면 PVC는 다중 노드 동시 쓰기(`ReadWriteMany`)를 요구하고 있으므로 바인딩되지 못하고 Pending 상태로 대기합니다.",
      "key_concept": "PV and PVC Binding Requirements, AccessModes Mismatch"
    },
    {
      "id": "D4-Q02",
      "domain": "Domain 4",
      "domain_name": "스토리지 (Storage)",
      "question_en": "Which PersistentVolumeReclaimPolicy preserves the underlying storage volume and its data when the bound PersistentVolumeClaim (PVC) is deleted, requiring an administrator to manually reclaim or clean up the resource?",
      "question_kr": "바인딩된 PersistentVolumeClaim(PVC)이 삭제되었을 때 기본 스토리지 볼륨과 데이터를 그대로 보존하여, 관리자가 수동으로 리소스를 회수하거나 정리하도록 요구하는 PersistentVolumeReclaimPolicy는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "Delete",
          "text_kr": "Delete"
        },
        {
          "key": "B",
          "text_en": "Retain",
          "text_kr": "Retain"
        },
        {
          "key": "C",
          "text_en": "Recycle",
          "text_kr": "Recycle"
        },
        {
          "key": "D",
          "text_en": "Archive",
          "text_kr": "Archive"
        }
      ],
      "correct_answer": "B",
      "explanation_kr": "정답은 B입니다.\n\n• `persistentVolumeReclaimPolicy: Retain`은 PVC가 삭제되어도 PV와 실제 백엔드 데이터를 삭제하지 않고 `Released` 상태로 유지하여 데이터 유실을 방지합니다.\n• `Delete`는 PVC 삭제 시 실제 스토리지 에셋까지 함께 자동 삭제합니다.",
      "key_concept": "Reclaim Policy: Retain vs Delete"
    },
    {
      "id": "D4-Q03",
      "domain": "Domain 4",
      "domain_name": "스토리지 (Storage)",
      "question_en": "What is the purpose of setting `volumeBindingMode: WaitForFirstConsumer` on a StorageClass?",
      "question_kr": "StorageClass에서 `volumeBindingMode: WaitForFirstConsumer`를 설정하는 주된 목적은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "It delays volume provisioning and binding until a Pod using the PVC is created and scheduled to a specific node.",
          "text_kr": "해당 PVC를 사용하는 파드가 실제로 생성되어 특정 노드에 스케줄링될 때까지 볼륨 프로비저닝과 바인딩을 지연시킵니다."
        },
        {
          "key": "B",
          "text_en": "It ensures only one container can consume the storage volume at any time.",
          "text_kr": "항상 단 하나의 컨테이너만 볼륨을 사용할 수 있도록 보장합니다."
        },
        {
          "key": "C",
          "text_en": "It compresses data before writing to disk.",
          "text_kr": "디스크에 쓰기 전에 데이터를 자동 압축합니다."
        },
        {
          "key": "D",
          "text_en": "It prevents the volume from being expanded in size.",
          "text_kr": "볼륨 크기가 확장되는 것을 방지합니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• 기본값인 `Immediate`는 PVC가 생성되는 즉시 볼륨을 프로비저닝하여, 특정 가용영역(AZ)이나 로컬 디스크에 종속된 볼륨의 경우 파드가 다른 노드에 배정되었을 때 볼륨을 마운트하지 못하는 문제가 발생할 수 있습니다.\n• `WaitForFirstConsumer`는 파드의 토폴로지 제약(NodeSelector, Affinity 등)을 먼저 평가하여 파드가 위치할 노드가 확정된 후에 볼륨을 프로비저닝하므로 이러한 문제를 방지합니다.",
      "key_concept": "StorageClass volumeBindingMode: WaitForFirstConsumer"
    },
    {
      "id": "D4-Q04",
      "domain": "Domain 4",
      "domain_name": "스토리지 (Storage)",
      "question_en": "Which AccessMode allows a volume to be mounted simultaneously as read-write by multiple pods running across multiple distinct worker nodes?",
      "question_kr": "서로 다른 여러 워커 노드에서 실행 중인 여러 파드가 동시에 읽기/쓰기(read-write)로 볼륨을 마운트할 수 있도록 허용하는 AccessMode는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "ReadWriteOnce (RWO)",
          "text_kr": "ReadWriteOnce (RWO)"
        },
        {
          "key": "B",
          "text_en": "ReadOnlyMany (ROX)",
          "text_kr": "ReadOnlyMany (ROX)"
        },
        {
          "key": "C",
          "text_en": "ReadWriteMany (RWX)",
          "text_kr": "ReadWriteMany (RWX)"
        },
        {
          "key": "D",
          "text_en": "ReadWriteOncePod (RWOP)",
          "text_kr": "ReadWriteOncePod (RWOP)"
        }
      ],
      "correct_answer": "C",
      "explanation_kr": "정답은 C입니다.\n\n• `ReadWriteMany (RWX)`는 여러 노드에서 동시에 읽기/쓰기가 가능한 모드로, NFS, AWS EFS, GlusterFS 등의 네트워크 파일시스템에서 지원됩니다.",
      "key_concept": "AccessModes: ReadWriteMany (RWX)"
    },
    {
      "id": "D5-Q01",
      "domain": "Domain 5",
      "domain_name": "문제 해결 및 장애 진단 (Troubleshooting)",
      "question_en": "A worker node 'worker-1' shows a status of 'NotReady' in `kubectl get nodes`. You SSH into the node to investigate. Which Linux system commands are most effective to diagnose why the Kubernetes node agent is failing?",
      "question_kr": "`kubectl get nodes` 실행 시 워커 노드 'worker-1'이 'NotReady' 상태로 표시됩니다. 원인을 조사하기 위해 해당 노드에 SSH로 접속했습니다. 쿠버네티스 노드 에이전트의 실패 원인을 진단하는 데 가장 효과적인 리눅스 시스템 명령어 조합은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "systemctl status kubelet and journalctl -u kubelet -n 50 --no-pager",
          "text_kr": "systemctl status kubelet 및 journalctl -u kubelet -n 50 --no-pager"
        },
        {
          "key": "B",
          "text_en": "top and netstat -tuln",
          "text_kr": "top 및 netstat -tuln"
        },
        {
          "key": "C",
          "text_en": "cat /var/log/syslog | grep docker",
          "text_kr": "cat /var/log/syslog | grep docker"
        },
        {
          "key": "D",
          "text_en": "kubeadm reset --force",
          "text_kr": "kubeadm reset --force"
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• 워커 노드가 NotReady 상태일 때는 노드의 `kubelet` 서비스 상태를 확인하는 것이 1순위입니다.\n• `systemctl status kubelet`으로 실행 여부를 확인하고, 비정상 종료된 경우 `journalctl -u kubelet -n 50 --no-pager`를 통해 인증서 만료, 설정 파일 오탈자, 컨테이너 런타임 통신 장애 등의 구체적 에러 로그를 확인합니다.",
      "key_concept": "Node NotReady Diagnosis, kubelet troubleshooting with systemctl & journalctl"
    },
    {
      "id": "D5-Q02",
      "domain": "Domain 5",
      "domain_name": "문제 해결 및 장애 진단 (Troubleshooting)",
      "question_en": "A newly deployed Pod 'payment-app' immediately crashes and enters the `CrashLoopBackOff` state. How can you inspect the termination log of the container that just crashed prior to the restart?",
      "question_kr": "새로 배포된 'payment-app' 파드가 기동 직후 비정상 종료되며 `CrashLoopBackOff` 상태로 전환되었습니다. 컨테이너가 재시작되기 직전에 발생하여 비정상 종료를 유발한 이전 컨테이너의 로그를 확인하는 명령어는 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "kubectl logs payment-app --previous",
          "text_kr": "kubectl logs payment-app --previous"
        },
        {
          "key": "B",
          "text_en": "kubectl get pod payment-app --watch-crashes",
          "text_kr": "kubectl get pod payment-app --watch-crashes"
        },
        {
          "key": "C",
          "text_en": "kubectl describe pod payment-app --history",
          "text_kr": "kubectl describe pod payment-app --history"
        },
        {
          "key": "D",
          "text_en": "cat /var/log/pods/payment-app/crash.log",
          "text_kr": "cat /var/log/pods/payment-app/crash.log"
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• 컨테이너가 크래시되어 계속 재시작되는 루프에 빠져 있을 때, `kubectl logs <pod-name> --previous` (또는 `-p`) 옵션을 주면 직전에 크래시된 컨테이너의 마지막 표준 출력/에러 로그를 즉시 열람할 수 있습니다.",
      "key_concept": "CrashLoopBackOff Debugging, kubectl logs --previous (-p)"
    },
    {
      "id": "D5-Q03",
      "domain": "Domain 5",
      "domain_name": "문제 해결 및 장애 진단 (Troubleshooting)",
      "question_en": "After editing `/etc/kubernetes/manifests/kube-apiserver.yaml` to add a new flag, the control plane stops responding completely and all `kubectl` commands fail with 'The connection to the server was refused'. How can you inspect the API server container errors on the master node?",
      "question_kr": "새로운 플래그를 추가하기 위해 `/etc/kubernetes/manifests/kube-apiserver.yaml`을 수정한 후, 컨트롤 플레인이 완전히 응답을 멈추고 모든 `kubectl` 명령어가 'The connection to the server was refused' 에러를 반환합니다. 마스터 노드에서 API 서버 컨테이너의 에러 로그를 확인하는 가장 적절한 방법은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "Use the container runtime CLI directly, e.g., `crictl ps -a` to find the stopped container ID, followed by `crictl logs <container-id>`.",
          "text_kr": "컨테이너 런타임 CLI를 직접 사용하여 `crictl ps -a`로 중지된 컨테이너 ID를 확인한 후 `crictl logs <container-id>`를 실행합니다."
        },
        {
          "key": "B",
          "text_en": "Run `kubectl logs kube-apiserver -n kube-system --force`.",
          "text_kr": "`kubectl logs kube-apiserver -n kube-system --force`를 실행합니다."
        },
        {
          "key": "C",
          "text_en": "Reboot the control plane node using `shutdown -r now`.",
          "text_kr": "`shutdown -r now`로 컨트롤 플레인 노드를 재부팅합니다."
        },
        {
          "key": "D",
          "text_en": "Re-run `kubeadm init` over the existing cluster.",
          "text_kr": "기존 클러스터 위에 `kubeadm init`을 다시 실행합니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• API 서버 자체가 다운되어 있을 때는 API 서버에 의존하는 `kubectl` 명령어가 전혀 동작하지 않습니다.\n• 따라서 노드 수준의 컨테이너 런타임 인터페이스인 `crictl` 명령(`crictl ps -a`, `crictl logs <ID>`)을 사용하여 API 서버 컨테이너가 어떤 플래그나 문법 오류로 인해 기동 실패했는지 직접 확인해야 합니다.",
      "key_concept": "API Server Down Diagnosis, Container Runtime crictl ps/logs"
    },
    {
      "id": "D5-Q04",
      "domain": "Domain 5",
      "domain_name": "문제 해결 및 장애 진단 (Troubleshooting)",
      "question_en": "You notice that a Service named 'auth-service' has an active ClusterIP, but any request directed to this service times out. Running `kubectl get endpoints auth-service` shows `<none>`. What is the most likely root cause?",
      "question_kr": "'auth-service'라는 서비스에 유효한 ClusterIP가 할당되어 있으나, 이 서비스로 보내는 모든 요청이 타임아웃됩니다. `kubectl get endpoints auth-service`를 실행해보니 `<none>`으로 표시됩니다. 가장 유력한 근본 원인은 무엇입니까?",
      "options": [
        {
          "key": "A",
          "text_en": "The Service's `spec.selector` labels do not match the labels defined in the target Pods' metadata.",
          "text_kr": "서비스의 `spec.selector` 라벨이 대상 파드의 메타데이터에 정의된 라벨과 일치하지 않습니다."
        },
        {
          "key": "B",
          "text_en": "The node running the pods has run out of disk space.",
          "text_kr": "파드를 실행 중인 노드의 디스크 공간이 부족합니다."
        },
        {
          "key": "C",
          "text_en": "CoreDNS is not running.",
          "text_kr": "CoreDNS가 실행 중이지 않습니다."
        },
        {
          "key": "D",
          "text_en": "ClusterIP services cannot have endpoints.",
          "text_kr": "ClusterIP 서비스는 엔드포인트를 가질 수 없습니다."
        }
      ],
      "correct_answer": "A",
      "explanation_kr": "정답은 A입니다.\n\n• 쿠버네티스 서비스는 `spec.selector`에 정의된 라벨과 일치하는 정상(Ready) 상태의 파드 IP들을 자동으로 수집하여 `Endpoints` 리소스를 구성합니다.\n• 엔드포인트가 `<none>`이라는 것은 서비스의 셀렉터와 파드의 라벨이 불일치(오탈자)하거나, 파드들의 준비성 프로브(Readiness Probe)가 실패하여 트래픽 대상에서 제외되었음을 의미합니다.",
      "key_concept": "Empty Endpoints (<none>), Service Selector Label Mismatch"
    }
  ]
};

if (typeof window !== 'undefined') {
  window.EXAM_DATA = EXAM_DATA;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = EXAM_DATA;
}
