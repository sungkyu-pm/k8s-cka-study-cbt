# 도메인 1: 클러스터 아키텍처, 설치 및 구성 심층 가이드 (Cluster Architecture, Installation & Configuration)

> **출제 비중**: **25%**  
> **핵심 세부 영역**: RBAC 권한 통제, kubeadm 부트스트랩, etcd 백업 및 복구, 버전 업그레이드, CSR 인증서 관리, Static Pods, Kubeconfig 컨텍스트

---

## 1.1 RBAC 심층 아키텍처 및 권한 부여 (Role-Based Access Control)

쿠버네티스 API 요청은 **인증(Authentication) ➔ 인가(Authorization / RBAC) ➔ 어드미션 제어(Admission Control)** 단계를 거쳐 처리됩니다.

```
[클라이언트 요청] 
      │
      ▼
[1. Authentication] ── 인증서/토큰 유효성 검증
      │
      ▼
[2. Authorization (RBAC)] ── Role/ClusterRole 권한 규칙 대조
      │
      ▼
[3. Admission Control] ── 리소스 유효성 검증 및 기본값 주입
      │
      ▼
[etcd 저장 및 반영]
```

### 1. Role vs ClusterRole 매트릭스
| 구분 | Role (역할) | ClusterRole (클러스터 역할) |
| :--- | :--- | :--- |
| **적용 범위** | 단일 특정 네임스페이스에 한정 | 클러스터 전체 범위 |
| **적용 대상 리소스** | 네임스페이스 리소스 (`pods`, `services`, `deployments`, `jobs`) | 비네임스페이스 리소스 (`nodes`, `persistentvolumes`, `namespaces`, `storageclasses`) 및 모든 네임스페이스의 리소스 |
| **바인딩 리소스** | `RoleBinding` | `ClusterRoleBinding` (또는 네임스페이스 한정 `RoleBinding`) |

### 2. Role 및 RoleBinding 실전 매니페스트
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: development
  name: developer-role
rules:
- apiGroups: ["", "apps"]
  resources: ["pods", "pods/log", "deployments"]
  verbs: ["get", "list", "watch", "create", "update"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: development
  name: developer-binding
subjects:
- kind: User
  name: developer-john
  apiGroup: rbac.authorization.k8s.io
- kind: ServiceAccount
  name: build-sa
  namespace: development
roleRef:
  kind: Role
  name: developer-role
  apiGroup: rbac.authorization.k8s.io
```

### ⚡ 실전 핵심 CLI (시험장 초고속 권한 부여 및 검증)
```bash
# 1. 특정 네임스페이스의 Role 생성
kubectl create role pod-manager --verb=get,list,create,delete --resource=pods -n dev

# 2. 특정 사용자에게 Role 바인딩
kubectl create rolebinding pod-manager-binding --role=pod-manager --user=alice -n dev

# 3. 클러스터 전체 노드 읽기 ClusterRole 및 바인딩
kubectl create clusterrole node-reader --verb=get,list --resource=nodes
kubectl create clusterrolebinding node-reader-binding --clusterrole=node-reader --serviceaccount=kube-system:monitor-sa

# 4. 권한 자가 검증 (Impersonation 테스트 필수!)
kubectl auth can-i create pods --as=alice -n dev          # 결과: yes
kubectl auth can-i delete deployments --as=alice -n dev   # 결과: no
```

---

## 1.2 kubeadm 클러스터 설치 및 노드 조인 (Cluster Bootstrap)

### 1. 마스터 노드 초기화 (`kubeadm init`)
```bash
# Calico CNI 권장 대역(192.168.0.0/16)으로 초기화
kubeadm init --pod-network-cidr=192.168.0.0/16 --apiserver-advertise-address=192.168.10.10

# 일반 사용자 환경설정 복사
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# CNI 플러그인(Calico) 설치
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/calico.yaml
```

### 2. 워커 노드 조인 커맨드 재생성
토큰 유효기간(기본 24시간)이 만료되었거나 조인 명령어를 분실했을 때:
```bash
# 신규 조인 토큰 생성 및 CA 해시가 포함된 전체 커맨드 출력
kubeadm token create --print-join-command

# 출력 예시:
# kubeadm join 192.168.10.10:6443 --token abcdef.0123456789abcdef \
#     --discovery-token-ca-cert-hash sha256:7f...
```

---

## 1.3 etcd 백업 및 복원 (Backup & Disaster Recovery)

> **CKA 시험 100% 빈출 문항**: etcd 스냅샷 저장 및 복원 절차

```
[백업 절차]
  1. /etc/kubernetes/manifests/etcd.yaml 에서 TLS 인증서 및 엔드포인트 확인
  2. ETCDCTL_API=3 etcdctl snapshot save 실행
  3. etcdctl snapshot status 로 무결성 검증

[복원 절차]
  1. ETCDCTL_API=3 etcdctl snapshot restore --data-dir=/var/lib/etcd-new
  2. /etc/kubernetes/manifests/etcd.yaml 의 hostPath 볼륨을 /var/lib/etcd-new 로 수정
  3. kubelet이 etcd 파드를 자동 재시작할 때까지 대기
```

### 1. etcd 스냅샷 생성
```bash
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /tmp/etcd-backup.db

# 스냅샷 상태 테이블 확인
ETCDCTL_API=3 etcdctl --write-out=table snapshot status /tmp/etcd-backup.db
```

### 2. etcd 스냅샷 복원
```bash
# 1. 새 디렉토리로 데이터베이스 복원
ETCDCTL_API=3 etcdctl --data-dir=/var/lib/etcd-restored \
  snapshot restore /tmp/etcd-backup.db

# 2. Static Pod 매니페스트 볼륨 수정
# 파일: /etc/kubernetes/manifests/etcd.yaml
# volumes:
# - name: etcd-data
#   hostPath:
#     path: /var/lib/etcd-restored   <-- 기존 /var/lib/etcd 에서 변경!
```

---

## 1.4 kubeadm 클러스터 버전 업그레이드 (Cluster Upgrade)

쿠버네티스 버전 업그레이드는 마이너 버전 1단계씩(`1.30.x` ➔ `1.31.x`) 순차적으로 진행해야 합니다.

### 1. 마스터(Control Plane) 노드 업그레이드
```bash
# 1. 노드 drain
kubectl drain controlplane --ignore-daemonsets

# 2. kubeadm 패키지 업그레이드
apt-get update && apt-get install -y --allow-change-held-packages kubeadm=1.31.0-1.1

# 3. 업그레이드 계획 검토 및 적용
kubeadm upgrade plan
kubeadm upgrade apply v1.31.0 -y

# 4. kubelet 및 kubectl 업그레이드
apt-get update && apt-get install -y --allow-change-held-packages kubelet=1.31.0-1.1 kubectl=1.31.0-1.1
systemctl daemon-reload
systemctl restart kubelet

# 5. 노드 uncordon
kubectl uncordon controlplane
```

### 2. 워커(Worker) 노드 업그레이드
```bash
# 마스터 노드에서 워커 노드 배출
kubectl drain worker-1 --ignore-daemonsets

# 워커 노드 접속 후:
apt-get update && apt-get install -y --allow-change-held-packages kubeadm=1.31.0-1.1
kubeadm upgrade node   # 주의: 워커에서는 'node' 명령어 사용!
apt-get update && apt-get install -y --allow-change-held-packages kubelet=1.31.0-1.1 kubectl=1.31.0-1.1
systemctl daemon-reload
systemctl restart kubelet

# 마스터 노드로 돌아와 복구
kubectl uncordon worker-1
```

---

## 1.5 인증서 수명주기 및 CSR 관리 (Certificates & CSR)

```bash
# 1. 클러스터 인증서 만료일 일괄 확인
kubeadm certs check-expiration

# 2. 모든 제어 평면 인증서 1년 연장 갱신
kubeadm certs renew all

# 3. 제출된 CSR 승인 및 거부
kubectl get csr
kubectl certificate approve <csr-name>
kubectl certificate deny <csr-name>
```

## 1.6 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)

이 섹션은 CBT 문제 은행(**questions_domain1.json 250문항**)의 모든 핵심 개념(`key_concept`), 정답 해설 및 빈출 함정 키워드와 1:1로 일치하도록 정리된 요약본입니다.

| 출제 핵심 개념 (Key Concept) | 공식 출제 의도 및 필수 명령어/파라미터 | CBT 대표 오답 함정 & 판별 포인트 |
| :--- | :--- | :--- |
| **etcdctl snapshot save** | TLS 3종 플래그 필수 (`--cacert`, `--cert`, `--key`) 및 `--endpoints=https://127.0.0.1:2379`, `ETCDCTL_API=3` | • `kubectl snapshot`이나 `kubeadm backup` 같은 가짜 명령어를 고르지 말 것.<br>• 인증서 플래그가 누락된 선택지는 오답. |
| **etcdctl snapshot restore** | `ETCDCTL_API=3 etcdctl snapshot restore <스냅샷> --data-dir=<새경로>` | • 복원 후 `/etc/kubernetes/manifests/etcd.yaml`의 `hostPath.path`를 반드시 새 경로로 수정해야 함.<br>• API 서버는 etcd 복원 완료 시까지 재시작하지 않음. |
| **Role vs ClusterRole** | • **Role**: 단일 네임스페이스 한정 (`pods`, `deployments`, `jobs`)<br>• **ClusterRole**: 클러스터 전체 리소스 (`nodes`, `persistentvolumes`, `namespaces`) | • `nodes` 리소스는 네임스페이스가 없으므로 `Role`로 권한을 부여할 수 없으며 반드시 `ClusterRole`과 `ClusterRoleBinding` 필요. |
| **kubectl auth can-i** | 권한 시뮬레이션: `kubectl auth can-i <verb> <resource> --as=<user> -n <ns>`<br>ServiceAccount: `--as=system:serviceaccount:<ns>:<sa-name>` | • SA 권한 확인 시 접두사 `system:serviceaccount:`가 생략되면 일반 유저로 취급되어 권한 불일치 발생. |
| **kubeadm init & join** | • 초기화: `kubeadm init --pod-network-cidr=192.168.0.0/16`<br>• 토큰 재발급: `kubeadm token create --print-join-command` | • CNI(Calico/Flannel) 배포 전까지 노드는 `NotReady` 상태로 유지됨.<br>• 토큰 만료(기본 24시간) 시 새 토큰을 발급해야 조인 가능. |
| **kubeadm 클러스터 업그레이드** | 1. 마스터: `drain` ➔ `kubeadm upgrade plan/apply` ➔ `kubelet/kubectl` 업그레이드 ➔ `restart kubelet` ➔ `uncordon`<br>2. 워커: `drain` ➔ `kubeadm upgrade node` ➔ `kubelet/kubectl` ➔ `uncordon` | • 워커 노드에서는 `kubeadm upgrade apply`가 아니라 반드시 `kubeadm upgrade node` 명령어를 사용해야 함.<br>• 마이너 버전 건너뛰기 불가 (`1.30 -> 1.32` 불가, `1.30 -> 1.31` 필수). |
| **Static Pod 디렉토리** | kubelet 데몬이 `/etc/kubernetes/manifests` 내의 YAML을 inotify로 실시간 감시 | • API 서버나 스케줄러가 다운되어 있어도 kubelet이 직접 실행·관리함.<br>• `kubectl create`로 제어 평면 파드를 직접 만드는 것이 아님. |
| **CSR 라이프사이클** | `kubectl get csr`, `kubectl certificate approve <name>`, `kubectl certificate deny <name>` | • 신규 유저/에이전트 인증서는 CSR 승인 후 `status.certificate`에서 base64 디코딩하여 추출. |
| **Kubeconfig Context** | `kubectl config get-contexts`, `kubectl config use-context <name>`, `kubectl config set-context --current --namespace=<ns>` | • `current-context` 필드가 현재 활성화된 클러스터-사용자-네임스페이스 튜플을 결정. |
