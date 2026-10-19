# 도메인 4: 스토리지 심층 가이드 (Storage)

> **출제 비중**: **10%**  
> **핵심 세부 영역**: PV/PVC 바인딩 메커니즘, 4대 AccessModes, ReclaimPolicy, StorageClass 동적 프로비저닝, WaitForFirstConsumer, 온라인 볼륨 확장, subPath 및 CSI 아키텍처

---

## 4.1 PV & PVC 생명주기 및 바인딩 3대 원칙

```
[관리자 프로비저닝] ── PV (Available)
                          │
       [1:1 매칭 바인딩]   ▼
[사용자 요청서]    ── PVC (Bound) ◀── 파드에 볼륨으로 마운트
                          │
        [PVC 삭제 시]     ▼
                   PV (Released) ── ReclaimPolicy (Retain / Delete)
```

### 1. PVC ➔ PV 바인딩을 위한 3대 일치 조건
1. **스토리지 용량**: PV의 용량 $\ge$ PVC의 요청 용량이어야 합니다.
2. **AccessModes**: PV의 지원 모드와 PVC의 요청 모드가 호환되어야 합니다.
3. **StorageClass**: 이름이 정확히 일치해야 합니다. (수동 바인딩 시 `storageClassName: ""` 명시)

---

## 4.2 4대 AccessModes (접근 모드) 완벽 비교

| 모드 (약어) | 풀네임 | 허용 노드 수 | 지원 스토리지 유형 |
| :--- | :--- | :--- | :--- |
| **RWO** | `ReadWriteOnce` | **단일 노드**에서만 R/W 가능 | AWS EBS, GCE PD, Azure Disk 등 일반 블록 스토리지 |
| **ROX** | `ReadOnlyMany` | **여러 노드**에서 Read-Only 가능 | 배포 이미지 캐시, 읽기 전용 문서 저장소 |
| **RWX** | `ReadWriteMany` | **여러 노드**에서 R/W 동시 가능 | NFS, AWS EFS, CephFS, GlusterFS 등 네트워크 파일시스템 |
| **RWOP** | `ReadWriteOncePod` | **단일 파드**에서만 R/W 가능 (K8s 1.22+) | 단일 파드 전용 엄격한 스토리지 잠금 필요 시 |

---

## 4.3 ReclaimPolicy (반환 정책) 동작 원리

* **`Retain`**:
  - PVC가 삭제되어도 PV와 실제 디스크 데이터는 절대 삭제되지 않고 **`Released`** 상태로 보존됩니다.
  - 새 PVC가 즉시 바인딩되지 않으므로, 관리자가 데이터를 백업/정리한 후 PV 매니페스트의 `spec.claimRef` 항목을 제거해야 `Available` 상태로 복귀합니다.
* **`Delete`**:
  - PVC 삭제 시 연관된 클라우드 스토리지 에셋(AWS EBS 디스크 등)이 즉시 자동 영구 삭제됩니다. (동적 프로비저닝 기본값)

---

## 4.4 StorageClass & 동적 프로비저닝 (Dynamic Provisioning)

### 1. `volumeBindingMode: WaitForFirstConsumer`의 필수성
기본값인 `Immediate`는 PVC 생성 즉시 볼륨을 프로비저닝하여, 특정 가용영역(AZ-a)에 묶인 디스크가 생성되었는데 파드가 다른 노드(AZ-b)에 배정되어 볼륨을 마운트하지 못하는 스케줄링 실패(`VolumeZoneAffinity`)가 발생합니다.

`WaitForFirstConsumer`는 **파드가 실제로 어느 노드에 스케줄링될지 결정된 후 볼륨을 생성**하므로 토폴로지 불일치를 완벽히 방지합니다.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-storage
provisioner: ebs.csi.aws.com
volumeBindingMode: WaitForFirstConsumer # 지연 바인딩 필수
reclaimPolicy: Delete
allowVolumeExpansion: true             # 온라인 용량 확장 허용
parameters:
  type: gp3
```

---

## 4.5 볼륨 온라인 동적 확장 및 제약 사항

* **확장 절차**:
  1. StorageClass에 `allowVolumeExpansion: true`가 설정되어 있는지 확인.
  2. 기존 PVC를 `kubectl edit pvc <name>`으로 열고 `spec.resources.requests.storage`를 상향 조정 (예: `5Gi` ➔ `10Gi`).
  3. CSI 드라이버가 파일시스템을 온라인으로 자동 확장.
* **중요 제약**:
  - 쿠버네티스는 **볼륨 용량 축소(Shrink)를 절대 지원하지 않습니다.** (데이터 손상 방지 목적)

---

## 4.6 파드 볼륨 마운트 실전 기법

### 1. `subPath`를 활용한 단일 파일 마운트
디렉토리의 다른 기존 파일들을 덮어쓰지 않고 특정 설정 파일만 주입:
```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: conf-volume
      mountPath: /etc/nginx/conf.d/default.conf # 디렉토리가 아닌 단일 파일 위치
      subPath: default.conf                    # ConfigMap 내의 키 이름
  volumes:
  - name: conf-volume
    configMap:
      name: nginx-custom-conf
```

### 2. Storage Object in Use Protection (Finalizer)
파드가 사용 중인 PVC를 실수로 삭제(`kubectl delete pvc`)하더라도, `kubernetes.io/pvc-protection` Finalizer가 등록되어 있어 파드가 종료될 때까지 실제 삭제가 보류되고 `Terminating` 상태로 안전하게 대기합니다.
