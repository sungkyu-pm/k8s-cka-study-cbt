# 도메인 2: 워크로드 및 스케줄링 (Workloads & Scheduling)

> **출제 비중**: **15%**  
> **핵심 키워드**: Deployment 롤아웃/롤백, ConfigMap & Secret 환경변수/볼륨 주입, Multi-container Pod, Taints & Tolerations, NodeAffinity, 리소스 제약(Requests/Limits)

---

## 1. 디플로이먼트 관리 및 롤아웃/롤백 (Deployment Rollout & Rollback)

### 1.1 빠른 생성 및 업데이트 (Imperative Commands)
```bash
# 1. Deployment 생성 (레플리카 3개, nginx 이미지)
kubectl create deployment my-deploy --image=nginx:1.20 --replicas=3

# 2. 이미지 롤링 업데이트 (1.20 -> 1.21)
kubectl set image deployment/my-deploy nginx=nginx:1.21

# 3. 롤아웃 진행 상태 모니터링
kubectl rollout status deployment/my-deploy

# 4. 배포 히스토리 확인 및 이전 버전으로 롤백
kubectl rollout history deployment/my-deploy
kubectl rollout undo deployment/my-deploy
kubectl rollout undo deployment/my-deploy --to-revision=1 # 특정 리비전 복원
```

---

## 2. ConfigMap & Secret 생성 및 주입 (Configuration)

### 2.1 CLI로 즉시 생성
```bash
# ConfigMap 생성
kubectl create configmap app-config --from-literal=APP_ENV=production --from-literal=DB_PORT=5432

# Secret 생성 (Generic)
kubectl create secret generic app-secret --from-literal=DB_PASSWORD=SuperSecret123!
```

### 2.2 파드 내 주입 2가지 방법 (환경변수 vs 볼륨 마운트)
* **환경변수로 일괄 주입 (`envFrom`)**:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: env-pod
spec:
  containers:
  - name: app
    image: busybox
    command: ['sh', '-c', 'env && sleep 3600']
    envFrom:
    - configMapRef:
        name: app-config
    - secretRef:
        name: app-secret
```
* **볼륨으로 마운트 (`volumes` & `volumeMounts`)**:
```yaml
spec:
  containers:
  - name: web
    image: nginx
    volumeMounts:
    - name: cfg-vol
      mountPath: /etc/config
      readOnly: true
  volumes:
  - name: cfg-vol
    configMap:
      name: app-config
```

---

## 3. 고급 스케줄링 제어 (Advanced Scheduling)

### 3.1 Taints & Tolerations (노드가 파드를 밀어냄)
* **노드에 Taint 부여**:
  ```bash
  # effect: NoSchedule, PreferNoSchedule, NoExecute
  kubectl taint nodes node-1 env=production:NoSchedule
  
  # Taint 제거 (맨 뒤에 '-' 추가)
  kubectl taint nodes node-1 env=production:NoSchedule-
  ```
* **파드에 Toleration 설정**:
  ```yaml
  spec:
    tolerations:
    - key: "env"
      operator: "Equal"
      value: "production"
      effect: "NoSchedule"
  ```

### 3.2 NodeAffinity (파드가 노드를 끌어당김)
* **Hard Rule (필수 조건)**: `requiredDuringSchedulingIgnoredDuringExecution` (조건 미일치 시 스케줄 불가)
* **Soft Rule (선호 조건)**: `preferredDuringSchedulingIgnoredDuringExecution` (우선 배정 시도)

```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: disktype
            operator: In
            values:
            - ssd
```

---

## 4. 멀티 컨테이너 파드 (Multi-container Pods)

하나의 파드 안에서 여러 컨테이너가 동일한 `localhost` 네트워크와 볼륨(`emptyDir`)을 공유합니다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
spec:
  containers:
  - name: app-producer
    image: busybox
    command: ["sh", "-c", "while true; do date >> /var/log/app.log; sleep 1; done"]
    volumeMounts:
    - name: shared-logs
      mountPath: /var/log
  - name: sidecar-consumer
    image: busybox
    command: ["sh", "-c", "tail -n+1 -F /var/log/app.log"]
    volumeMounts:
    - name: shared-logs
      mountPath: /var/log
  volumes:
  - name: shared-logs
    emptyDir: {}
```
