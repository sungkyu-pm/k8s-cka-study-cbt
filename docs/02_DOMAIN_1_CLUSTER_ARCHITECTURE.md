# 도메인 1: 클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration)

> **출제 비중**: **25%**  
> **핵심 키워드**: RBAC(Role, ClusterRole, RoleBinding), kubeadm 클러스터 구축, etcd 백업 및 복구(`etcdctl snapshot`), 클러스터 버전 업그레이드, Static Pods, 高가용성(HA) 원칙

---

## 1. 역할 기반 접근 제어 (RBAC - Role-Based Access Control)

쿠버네티스 API 요청은 **인증(Authentication) ➔ 인가(Authorization / RBAC) ➔ 어드미션 제어(Admission Control)**의 3단계를 거칩니다.

### 1.1 Role vs ClusterRole
* **Role (네임스페이스 범위)**:
  * 특정 단일 네임스페이스(예: `development`) 안의 리소스에 대해서만 동작합니다.
  ```yaml
  apiVersion: rbac.authorization.k8s.io/v1
  kind: Role
  metadata:
    namespace: development
    name: pod-reader
  rules:
  - apiGroups: [""] # 코어 API 그룹
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "watch"]
  ```
* **ClusterRole (클러스터 전체 범위)**:
  * 네임스페이스에 속하지 않는 리소스(예: `nodes`, `persistentvolumes`, `namespaces`) 또는 모든 네임스페이스에 걸친 리소스에 적용됩니다.
  ```yaml
  apiVersion: rbac.authorization.k8s.io/v1
  kind: ClusterRole
  metadata:
    name: node-admin
  rules:
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["get", "list", "watch", "describe"]
  ```

### 1.2 RoleBinding vs ClusterRoleBinding
* **RoleBinding**: 특정 사용자/그룹/ServiceAccount에 Role 또는 ClusterRole을 **특정 네임스페이스 내에서만** 권한 부여.
* **ClusterRoleBinding**: 클러스터 전체 범위로 권한 부여.

### ⚡ 실전 핵심 CLI: `kubectl create role / rolebinding`
```bash
# 1. dev 네임스페이스에 pod 읽기 권한의 Role 생성
kubectl create role pod-reader --verb=get,list,watch --resource=pods -n dev

# 2. 사용자 john에게 해당 롤 바인딩
kubectl create rolebinding pod-reader-binding --role=pod-reader --user=john -n dev

# 3. 권한 검증 (테스트 필수!)
kubectl auth can-i create pods --as=john -n dev # no 출력
kubectl auth can-i get pods --as=john -n dev    # yes 출력
```

---

## 2. etcd 데이터베이스 백업 및 복원 (Backup & Restore)

> **CKA 시험 100% 빈출 문항**: etcd 스냅샷 저장 및 장애 시 복원 절차를 완벽히 외워야 합니다.

### 2.1 사전 정보 확인 (Static Pod 매니페스트 확인)
`/etc/kubernetes/manifests/etcd.yaml` 파일을 열어 etcd 인증서 경로 및 엔드포인트를 확인합니다:
* `--listen-client-urls`: 보통 `https://127.0.0.1:2379`
* `--cacert`: `/etc/kubernetes/pki/etcd/ca.crt`
* `--cert`: `/etc/kubernetes/pki/etcd/server.crt`
* `--key`: `/etc/kubernetes/pki/etcd/server.key`

### 2.2 etcd 백업 (Snapshot Save)
```bash
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /tmp/etcd-backup.db

# 백업 상태 확인
ETCDCTL_API=3 etcdctl --write-out=table snapshot status /tmp/etcd-backup.db
```

### 2.3 etcd 복원 (Snapshot Restore)
```bash
# 1. 새로운 데이터 디렉토리로 스냅샷 복원
ETCDCTL_API=3 etcdctl --data-dir=/var/lib/etcd-restored \
  snapshot restore /tmp/etcd-backup.db

# 2. etcd 매니페스트 수정 (/etc/kubernetes/manifests/etcd.yaml)
# hostPath volume의 path를 /var/lib/etcd에서 /var/lib/etcd-restored 로 변경!
# kubelet이 매니페스트 변경을 감지하고 etcd 파드를 자동 재시작함.
```

---

## 3. kubeadm 클러스터 버전 업그레이드 (Cluster Upgrade)

마스터(Control Plane) 노드 ➔ 워커(Worker) 노드 순서로 업그레이드를 수행합니다.

### 3.1 컨트롤 플레인 노드 업그레이드 (v1.30.0 ➔ v1.31.0 예시)
```bash
# 1. 노드 스케줄링 중단 및 기존 파드 퇴거
kubectl drain controlplane --ignore-daemonsets

# 2. kubeadm 패키지 업그레이드
apt-get update && apt-get install -y --allow-change-held-packages kubeadm=1.31.0-1.1

# 3. 업그레이드 계획 확인 및 적용
kubeadm upgrade plan
kubeadm upgrade apply v1.31.0 -y

# 4. kubelet 및 kubectl 업그레이드
apt-get update && apt-get install -y --allow-change-held-packages kubelet=1.31.0-1.1 kubectl=1.31.0-1.1
systemctl daemon-reload
systemctl restart kubelet

# 5. 노드 정상 스케줄링 복구
kubectl uncordon controlplane
```

### 3.2 워커 노드 업그레이드
```bash
# 마스터 노드에서 워커 노드 drain
kubectl drain node-1 --ignore-daemonsets

# 워커 노드 접속 후:
apt-get update && apt-get install -y --allow-change-held-packages kubeadm=1.31.0-1.1
kubeadm upgrade node # apply가 아니라 'node' 명령어 사용!
apt-get update && apt-get install -y --allow-change-held-packages kubelet=1.31.0-1.1 kubectl=1.31.0-1.1
systemctl daemon-reload
systemctl restart kubelet

# 마스터 노드로 돌아와 uncordon
kubectl uncordon node-1
```

---

## 4. 고가용성(HA) 아키텍처 및 etcd 쿼럼 원칙

* **etcd 쿼럼(Quorum)**: $Q = \lfloor N/2 \rfloor + 1$
  * 3개 노드: 과반수 2개 필요 (최대 1개 노드 장애 허용)
  * 5개 노드: 과반수 3개 필요 (최대 2개 노드 장애 허용)
  * 짝수 개의 etcd 노드는 홀수 개 대비 장애 허용 대수가 늘어나지 않으면서 분할 뇌(Split-brain) 위험만 증가시키므로 **반드시 홀수(3, 5개)로 구성**합니다.
