# 실전 CKA 합격 마스터 치트시트 (Kubectl Master Cheat Sheet)

> **CKA 시험 120분 타임어택 필살기**: 모든 YAML 매니페스트를 손으로 타이핑하지 마세요!  
> **명령형 커맨드(Imperative CLI) + `$do` (`--dry-run=client -o yaml`)** 조합으로 5초 만에 YAML 뼈대를 생성하여 풀이 시간을 절반 이하로 단축하세요.

---

## ⚡ 1. 30초 시험장 필수 초기 환경 설정 (Speed Boost)

시험 시작 후 터미널이 열리면 가장 먼저 실행합니다:

```bash
# 1. 단축 별칭 설정
alias k=kubectl

# 2. YAML 생성 및 강제 삭제 단축 환경변수 설정
export do="--dry-run=client -o yaml"
export now="--force --grace-period=0"

# 3. bash 자동완성 연동
source <(kubectl completion bash)
complete -o default -F __start_kubectl k

# 4. vim YAML 최적화 설정 (~/.vimrc)
cat <<EOF > ~/.vimrc
set tabstop=2
set shiftwidth=2
set expandtab
set number
set paste
EOF
```

---

## 🚀 2. 초고속 명령형(Imperative) 리소스 생성 모음

### 2.1 Pod 생성
```bash
# 기본 Pod 생성
k run nginx --image=nginx:alpine

# 라벨, 환경변수, 포트 지정
k run web --image=nginx:alpine --port=80 --labels="app=web,tier=front" --env="DB_PORT=3306"

# YAML 뼈대 즉시 추출 (수정용)
k run custom-pod --image=nginx:alpine $do > pod.yaml
```

### 2.2 Deployment 생성 및 조작
```bash
# 디플로이먼트 생성 (레플리카 3개)
k create deployment my-deploy --image=nginx:alpine --replicas=3

# YAML 추출
k create deployment my-deploy --image=nginx:alpine --replicas=3 $do > deploy.yaml

# 레플리카 즉시 스케일링
k scale deployment my-deploy --replicas=5

# 이미지 업데이트 및 롤백
k set image deployment/my-deploy nginx=nginx:1.21-alpine
k rollout undo deployment/my-deploy
k rollout undo deployment/my-deploy --to-revision=1
```

### 2.3 Service 노출 및 생성
```bash
# 기존 Deployment를 포트 80(컨테이너 8080)의 ClusterIP로 즉시 노출
k expose deployment my-deploy --port=80 --target-port=8080 --name=my-svc

# NodePort 타입으로 노출
k expose deployment my-deploy --type=NodePort --port=80 --target-port=8080 --name=my-node-svc

# 직접 서비스 생성
k create service clusterip my-svc --tcp=80:8080
k create service nodeport my-ns --tcp=80:8080 --node-port=30080
```

### 2.4 ConfigMap & Secret 생성
```bash
# 리터럴 값으로 생성
k create configmap app-cfg --from-literal=COLOR=blue --from-literal=MAX_USERS=100
k create secret generic app-sec --from-literal=DB_PASSWORD=SecurePass123!

# 프라이빗 컨테이너 레지스트리 인증 시크릿 생성
k create secret docker-registry reg-cred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=myuser \
  --docker-password=mypass \
  --docker-email=my@email.com
```

### 2.5 Job & CronJob 생성
```bash
# 1회성 Job 생성
k create job one-time-job --image=busybox -- sh -c "echo Job Completed"

# CronJob 생성 (매시 0분, 30분 실행)
k create cronjob half-hour --image=busybox --schedule="0,30 * * * *" -- echo "Half hour ping"
```

### 2.6 Ingress 생성 (networking.k8s.io/v1)
```bash
k create ingress my-ing --rule="myapp.com/api*=api-service:8080" $do > ingress.yaml
```

---

## 🔍 3. JSONPath 및 Custom-Columns 실전 10선

```bash
# 1. 노드 이름과 내부 IP만 표 형식으로 깔끔하게 출력
k get nodes -o custom-columns=NAME:.metadata.name,INTERNAL-IP:.status.addresses[0].address

# 2. 모든 네임스페이스 파드의 이름, 네임스페이스, 실행 노드 출력
k get pods -A -o custom-columns=NS:.metadata.namespace,POD:.metadata.name,NODE:.spec.nodeName

# 3. 특정 파드의 모든 컨테이너 이미지 목록만 추출
k get pod my-pod -o jsonpath='{.spec.containers[*].image}'

# 4. 모든 노드의 OS 이미지 버전 추출
k get nodes -o jsonpath='{.items[*].status.nodeInfo.osImage}'

# 5. 파드들을 생성 시간 순서로 정렬하여 조회
k get pods -A --sort-by=.metadata.creationTimestamp

# 6. 노드들을 CPU 할당량 순서로 정렬
k get nodes --sort-by=.status.capacity.cpu

# 7. PV들을 스토리지 용량 순서로 정렬
k get pv --sort-by=.spec.capacity.storage

# 8. 클러스터 내 모든 Service의 ClusterIP 추출
k get svc -A -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.clusterIP}{"\n"}{end}'

# 9. Ready 상태가 아닌 파드만 골라내기
k get pods -A --field-selector status.phase!=Running

# 10. Warning 타입의 클러스터 이벤트만 필터링
k get events -A --field-selector type=Warning
```

---

## 📑 4. 필수 단축어 (Shortnames) 레퍼런스

| 단축어 | 풀네임 | 단축어 | 풀네임 |
| :---: | :--- | :---: | :--- |
| **po** | pods | **pv** | persistentvolumes |
| **deploy** | deployments | **pvc** | persistentvolumeclaims |
| **svc** | services | **sc** | storageclasses |
| **no** | nodes | **ing** | ingresses |
| **ns** | namespaces | **netpol**| networkpolicies |
| **cm** | configmaps | **sa** | serviceaccounts |
| **sec** | secrets | **csr** | certificatesigningrequests |
| **ds** | daemonsets | **sts** | statefulsets |
| **cj** | cronjobs | **ep** | endpoints |

---

## ⌨️ 5. Vim 핵심 단축키 (YAML 초고속 편집)

* **들여쓰기 2칸 자동화**: `set tabstop=2 shiftwidth=2 expandtab`
* **블록 들여쓰기**: `V`(비주얼 라인 선택) ➔ `>`(오른쪽) 또는 `<`(왼쪽)
* **여러 줄 동시 주석 달기**:
  1. `Ctrl + v` (블록 비주얼 모드)
  2. 방향키 `j`로 주석 처리할 행들의 첫 열을 선택
  3. `Shift + i` (줄 맨 앞 대문자 I 삽입)
  4. `#` 입력
  5. `Esc` 두 번 누르면 선택한 모든 줄에 `#` 주석 적용!
* **문자열 일괄 치환**: `:%s/구문자/신문자/g`
* **현재 줄 복사 및 붙여넣기**: `yy` ➔ `p`
* **여러 줄 복사**: `5yy` (현재 줄 포함 5줄 복사) ➔ `p`
