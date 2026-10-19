# 도메인 2: 워크로드 및 스케줄링 심층 가이드 (Workloads & Scheduling)

> **출제 비중**: **15%**  
> **핵심 세부 영역**: Deployment 롤아웃/롤백, DaemonSet/StatefulSet, Job/CronJob, 멀티컨테이너/Init컨테이너, Taints & Tolerations, NodeAffinity, ConfigMap/Secret 주입, 리소스 QoS

---

## 2.1 Deployment 수명주기 및 롤링 업데이트 (Rollout & Rollback)

### 1. 무중단 배포 전략 파라미터 (`maxSurge` & `maxUnavailable`)
```yaml
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%        # 롤아웃 중 최대 허용 파드 초과 생성 수 (4 * 25% = 1개, 최대 5개)
      maxUnavailable: 25%  # 롤아웃 중 일시 사용 불가 허용 수 (4 * 25% = 1개, 최소 3개 가용)
```

### ⚡ 실전 핵심 CLI
```bash
# 1. Deployment 생성 및 즉시 이미지 변경
kubectl create deployment web-app --image=nginx:1.20 --replicas=3
kubectl set image deployment/web-app nginx=nginx:1.21-alpine

# 2. 롤아웃 일시 중지 (여러 설정 한 번에 변경 시)
kubectl rollout pause deployment/web-app
kubectl set resources deployment/web-app -c=nginx --limits=cpu=200m,memory=256Mi
kubectl rollout resume deployment/web-app

# 3. 배포 이력 조회 및 특정 리비전 롤백
kubectl rollout history deployment/web-app
kubectl rollout undo deployment/web-app --to-revision=1
```

---

## 2.2 DaemonSet & StatefulSet 심층 아키텍처

### 1. DaemonSet 마스터 노드 허용 매니페스트
컨트롤 플레인 노드(`node-role.kubernetes.io/control-plane`)의 테인트를 견디도록 파드 템플릿에 Toleration을 명시합니다:
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: node-exporter
  template:
    metadata:
      labels:
        app: node-exporter
    spec:
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        operator: Exists
        effect: NoSchedule
      containers:
      - name: exporter
        image: prom/node-exporter:v1.5.0
```

### 2. StatefulSet & Headless Service 연동
```yaml
apiVersion: v1
kind: Service
metadata:
  name: db-headless
spec:
  clusterIP: None       # Headless 서비스 지정 필수
  selector:
    app: db
  ports:
  - port: 3306
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db
spec:
  serviceName: "db-headless"
  replicas: 3
  selector:
    matchLabels:
      app: db
  template:
    metadata:
      labels:
        app: db
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        volumeMounts:
        - name: data
          mountPath: /var/lib/mysql
  volumeClaimTemplates:  # 각 파드(db-0, db-1, db-2)마다 고유한 PVC 자동 생성
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
```

---

## 2.3 Job & CronJob 배치 워크로드

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: nightly-backup
spec:
  schedule: "0 2 * * *"               # 매일 새벽 2시 실행
  concurrencyPolicy: Forbid           # 이전 작업 미완료 시 새 작업 건너뜀 (Allow, Forbid, Replace)
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      backoffLimit: 4                 # 최대 재시도 실패 횟수
      template:
        spec:
          restartPolicy: OnFailure    # Job은 Always 불가! (OnFailure 또는 Never)
          containers:
          - name: backup
            image: busybox
            command: ["sh", "-c", "echo 'Backup completed'"]
```

---

## 2.4 멀티 컨테이너 & Init 컨테이너 패턴

### 1. 사이드카 로깅 패턴 (`emptyDir` 공유)
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-with-sidecar
spec:
  containers:
  - name: app
    image: busybox
    command: ["sh", "-c", "while true; do date >> /var/log/app.log; sleep 2; done"]
    volumeMounts:
    - name: shared-log
      mountPath: /var/log
  - name: log-sidecar
    image: busybox
    command: ["sh", "-c", "tail -n+1 -F /var/log/app.log"]
    volumeMounts:
    - name: shared-log
      mountPath: /var/log
  volumes:
  - name: shared-log
    emptyDir: {}
```

### 2. Init 컨테이너 사전 점검
```yaml
spec:
  initContainers:
  - name: wait-for-db
    image: busybox:1.28
    command: ['sh', '-c', 'until nc -z -w 2 db-service 3306; do echo waiting for db; sleep 2; done']
  containers:
  - name: web
    image: nginx
```

---

## 2.5 고급 스케줄링 (Taints, Tolerations & Affinity)

### 1. Taints & Tolerations (노드가 파드를 밀어냄)
```bash
# 노드에 Taint 적용
kubectl taint nodes node-1 env=prod:NoSchedule

# 노드 Taint 제거 (맨 끝에 - 추가)
kubectl taint nodes node-1 env=prod:NoSchedule-
```
```yaml
spec:
  tolerations:
  - key: "env"
    operator: "Equal"
    value: "prod"
    effect: "NoSchedule"
```

### 2. NodeAffinity (파드가 노드를 끌어당김)
* **Hard Rule**: `requiredDuringSchedulingIgnoredDuringExecution` (조건 미일치 시 절대 배정 불가)
* **Soft Rule**: `preferredDuringSchedulingIgnoredDuringExecution` (우선 배정 시도)

```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: disktype
            operator: In
            values: ["ssd", "nvme"]
```

### 3. PodAntiAffinity (고가용성 분산 배치)
동일 서비스 파드가 같은 노드에 중복 배치되지 않도록 격리:
```yaml
spec:
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values: ["web-frontend"]
        topologyKey: "kubernetes.io/hostname"
```

---

## 2.6 ConfigMap / Secret 주입 및 리소스 제약 (QoS)

```yaml
spec:
  containers:
  - name: backend
    image: my-app:v1
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m"
      limits:
        memory: "512Mi"    # 초과 시 OOMKilled (Exit Code 137)
        cpu: "500m"        # 초과 시 CPU Throttling
    envFrom:               # ConfigMap/Secret 키-값 일괄 주입
    - configMapRef:
        name: app-config
    volumeMounts:
    - name: conf-vol
      mountPath: /etc/app/config.json
      subPath: config.json # 기존 디렉토리를 덮어쓰지 않고 단일 파일만 마운트
  volumes:
  - name: conf-vol
    configMap:
      name: app-config
      defaultMode: 0400    # 읽기 전용 권한 설정
```
