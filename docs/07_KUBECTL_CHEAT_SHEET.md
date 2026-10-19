# 실전 CKA 합격 치트시트 (Kubectl Imperative Commands Cheat Sheet)

> **시험 합격의 핵심**: CKA 시험은 시간이 생명입니다! 모든 YAML 매니페스트를 손으로 타이핑하지 말고, **명령형(Imperative) 커맨드 + `$do` (`--dry-run=client -o yaml`) 조합**으로 5초 만에 YAML 뼈대를 생성하여 풀이 시간을 절반으로 줄이세요.

---

## ⚡ 1. 필수 단축 환경변수 설정 (시험 시작 즉시 실행)
```bash
alias k=kubectl
export do="--dry-run=client -o yaml"
export now="--force --grace-period=0"
```

---

## 🚀 2. 초고속 리소스 생성 명령 (Imperative CLI)

### 2.1 Pod 생성
```bash
# 기본 Pod 생성
k run nginx-pod --image=nginx:alpine

# 라벨 지정 및 포트 지정
k run web-pod --image=nginx:alpine --port=80 --labels="tier=frontend,app=web"

# 환경변수 지정
k run db-pod --image=redis --env="DB_PORT=6379"

# YAML 파일로 추출 후 커스텀 수정 (매우 중요!)
k run custom-pod --image=nginx:alpine $do > pod.yaml
```

### 2.2 Deployment 생성 & 스케일링
```bash
# 디플로이먼트 생성 (레플리카 3개)
k create deployment my-dep --image=nginx:alpine --replicas=3

# YAML로 추출
k create deployment my-dep --image=nginx:alpine --replicas=3 $do > deploy.yaml

# 레플리카 즉시 스케일링
k scale deployment my-dep --replicas=5

# 이미지 업데이트 및 롤백
k set image deployment/my-dep nginx=nginx:1.21-alpine
k rollout undo deployment/my-dep
```

### 2.3 Service 생성 및 노출
```bash
# 1. 기존 디플로이먼트를 ClusterIP 서비스로 즉시 노출 (port 80 -> targetPort 80)
k expose deployment my-dep --port=80 --target-port=80 --name=my-svc

# 2. NodePort 서비스로 노출
k expose deployment my-dep --type=NodePort --port=80 --target-port=80 --name=my-node-svc

# 3. 직접 서비스 생성
k create service clusterip my-cs --tcp=80:80
k create service nodeport my-ns --tcp=80:80 --node-port=30080
```

### 2.4 ConfigMap & Secret 생성
```bash
# 리터럴 값으로 생성
k create configmap app-cfg --from-literal=COLOR=blue --from-literal=MAX_USERS=100
k create secret generic app-sec --from-literal=DB_PASS=MyPassword123!

# 파일로부터 생성
k create configmap app-cfg --from-file=config.properties
```

### 2.5 Job & CronJob 생성
```bash
# 1회성 Job 생성
k create job my-job --image=busybox -- echo "Job Completed!"

# CronJob 생성 (매 분마다 실행)
k create cronjob my-cron --image=busybox --schedule="* * * * *" -- echo "Hello Cron"
```

### 2.6 Ingress 생성 (K8s 1.19+ networking.k8s.io/v1)
```bash
k create ingress my-ing --rule="myapp.com/api*=api-svc:8080" $do > ingress.yaml
```

---

## 🔍 3. 리소스 조회, 필터링 및 JSONPath

### 3.1 라벨 셀렉터 검색 (`-l`)
```bash
# 특정 라벨을 가진 파드만 조회
k get pods -l env=prod
k get pods -l 'env in (prod, staging)'
k get pods -l env!=prod
```

### 3.2 빠른 JSONPath 정렬 및 특정 필드 추출
```bash
# 노드 이름과 내부 IP만 보기 좋게 출력
k get nodes -o custom-columns=NAME:.metadata.name,IP:.status.addresses[0].address

# 생성 시간 순으로 파드 정렬
k get pods -A --sort-by=.metadata.creationTimestamp

# 특정 파드의 컨테이너 이미지 이름만 추출
k get pod my-pod -o jsonpath='{.spec.containers[*].image}'

# 모든 노드의 OS 이미지 정보 추출
k get nodes -o jsonpath='{.items[*].status.nodeInfo.osImage}'
```

---

## 📑 4. 자주 쓰이는 리소스 단축어 (Shortnames)

| 단축어 | 풀네임 | 단축어 | 풀네임 |
| :---: | :--- | :---: | :--- |
| **po** | pods | **pv** | persistentvolumes |
| **deploy** | deployments | **pvc** | persistentvolumeclaims |
| **svc** | services | **sc** | storageclasses |
| **no** | nodes | **ing** | ingresses |
| **ns** | namespaces | **netpol** | networkpolicies |
| **cm** | configmaps | **sa** | serviceaccounts |
| **sec** | secrets | **cj** | cronjobs |
| **ds** | daemonsets | **sts** | statefulsets |

---

## ⌨️ 5. Vim 핵심 단축키 (시험장 편집 필수)

* **탭 간격 2칸 자동 세팅**: `set tabstop=2 shiftwidth=2 expandtab`
* **블록 들여쓰기**: `V`(비주얼 라인 모드)로 줄들을 선택한 뒤 `>` (오른쪽 들여쓰기) 또는 `<` (왼쪽)
* **여러 줄 주석 처리**: `Ctrl + v` ➔ 방향키로 맨 앞 열 선택 ➔ `Shift + i` ➔ `#` 입력 ➔ `Esc` 두 번
* **문자열 치환**: `:%s/찾을문자/바꿀문자/g`
