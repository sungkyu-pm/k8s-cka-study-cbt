# 도메인 4: 스토리지 (Storage)

> **출제 비중**: **10%**  
> **핵심 키워드**: PersistentVolume(PV), PersistentVolumeClaim(PVC), StorageClass(동적 프로비저닝), AccessModes, ReclaimPolicy, volumeMounts

---

## 1. PV 및 PVC 생명주기와 바인딩 원리

* **PV (PersistentVolume)**: 클러스터 관리자가 프로비저닝한 실제 스토리지 리소스 (네임스페이스 없음).
* **PVC (PersistentVolumeClaim)**: 사용자가 스토리지 용량과 접근 모드를 지정하여 요청하는 티켓 (특정 네임스페이스에 속함).
* **바인딩(Binding)**: PVC의 요구 조건(용량, AccessMode, StorageClassName)을 만족하는 적합한 PV가 있으면 1:1로 결합(Bound)됩니다.

### 1.1 AccessModes (접근 모드)
| 모드 (약어) | 풀네임 | 설명 |
| :--- | :--- | :--- |
| **RWO** | `ReadWriteOnce` | **단일 노드**에서만 읽기/쓰기 볼륨으로 마운트 가능 (EBS 등 블록 스토리지) |
| **ROX** | `ReadOnlyMany` | **여러 노드**에서 읽기 전용으로 동시 마운트 가능 |
| **RWX** | `ReadWriteMany` | **여러 노드**에서 읽기/쓰기로 동시 마운트 가능 (NFS, CephFS 등) |
| **RWOP** | `ReadWriteOncePod` | **단일 파드**에서만 읽기/쓰기 마운트 허용 (K8s 1.22+ 도입) |

---

## 2. 정적 프로비저닝 매니페스트 (Static Provisioning)

### 2.1 PersistentVolume 정의
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-log-data
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain # Retain, Delete, Recycle
  storageClassName: manual
  hostPath:
    path: /mnt/data
```

### 2.2 PersistentVolumeClaim 정의
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-log-data
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi # PV(5Gi)보다 작거나 같으면 바인딩 성공!
  storageClassName: manual
```

### 2.3 파드에 PVC 마운트
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: storage-pod
spec:
  containers:
  - name: web
    image: nginx
    volumeMounts:
    - name: storage-vol
      mountPath: /usr/share/nginx/html
  volumes:
  - name: storage-vol
    persistentVolumeClaim:
      claimName: pvc-log-data
```

---

## 3. StorageClass와 동적 프로비저닝 (Dynamic Provisioning)

사용자가 PVC를 생성하면 사전에 정의된 `StorageClass`의 프로비저너가 클라우드/스토리지 백엔드에 볼륨을 실시간으로 자동 생성합니다.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-storage
provisioner: kubernetes.io/no-provisioner # 또는 csi 드라이버
volumeBindingMode: WaitForFirstConsumer # 파드가 실제로 스케줄링될 때까지 볼륨 생성을 지연
reclaimPolicy: Delete
allowVolumeExpansion: true # 볼륨 용량 확장 허용 여부
```
* **`volumeBindingMode: WaitForFirstConsumer`**: 특히 로컬 볼륨이나 특정 가용 영역(AZ)에 묶여 있는 볼륨의 경우, 파드가 어느 노드에 배정될지 결정된 후 볼륨을 프로비저닝하므로 스케줄링 실패를 방지하는 매우 중요한 설정입니다.
