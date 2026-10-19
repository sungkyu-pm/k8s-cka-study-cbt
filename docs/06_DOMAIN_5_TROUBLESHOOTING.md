# 도메인 5: 문제 해결 및 장애 진단 심층 가이드 (Troubleshooting)

> **출제 비중**: **30% (합격을 결정짓는 최상위 배점 도메인)**  
> **핵심 세부 영역**: 노드 NotReady 및 kubelet 데몬 복구, 제어 평면 Static Pods 장애 디버깅, Pod 4대 장애(CrashLoopBackOff, Pending, ImagePullBackOff, OOMKilled), CoreDNS 루프 진단, 네트워크 통신 복구

---

## 5.1 4단계 표준 트러블슈팅 워크플로우

시험장에서 장애 문제를 마주했을 때 당황하지 않고 체계적으로 진단하는 순서도입니다:

```
[1단계: 리소스 상태 및 광역 스캔]
  $ kubectl get nodes
  $ kubectl get pods -A -o wide

[2단계: 상세 이벤트 및 상태 플래그 확인]
  $ kubectl describe pod <pod-name> -n <ns>
  $ kubectl describe node <node-name>
  ──> 하단 Events 섹션에서 근본 원인 80% 식별!

[3단계: 애플리케이션 및 시스템 데몬 로그 분석]
  $ kubectl logs <pod-name> [-c <container>] [--previous]
  $ journalctl -u kubelet -n 100 --no-pager

[4단계: 저수준 컨테이너 런타임 직접 점검 (노드 내부)]
  $ ssh <node>
  $ crictl ps -a
  $ crictl logs <container-id>
```

---

## 5.2 노드 장애 (Node NotReady) 진단 및 복구 절차

### 1. `kubelet` 서비스 상태 확인 및 로그 추적
```bash
# 1. 문제 발생 워커 노드로 SSH 접속
ssh worker-1

# 2. 서비스 실행 상태 확인
systemctl status kubelet

# 3. 비정상 종료 시 에러 원인 추적
journalctl -u kubelet -n 100 -e --no-pager

# 4. 서비스 재시작
systemctl daemon-reload
systemctl restart kubelet
systemctl enable kubelet
```

### 2. 자주 발생하는 3대 kubelet 장애 원인 및 조치
1. **설정 파일 오탈자**:
   - `/var/lib/kubelet/config.yaml` 내부의 들여쓰기 오류, 잘못된 클러스터 DNS IP(`clusterDNS: [10.96.0.10]`)
2. **systemd 드롭인 인자 오류**:
   - `/etc/systemd/system/kubelet.service.d/10-kubeadm.conf` 파일 내 플래그 오탈자
3. **인증서 경로 또는 만료 오류**:
   - `/var/lib/kubelet/pki/kubelet-client-current.pem` 심볼릭 링크 손상

---

## 5.3 제어 평면(Control Plane) Static Pods 디버깅

마스터 노드의 핵심 컴포넌트(API Server, etcd, Scheduler, Controller-Manager)는 kubelet이 `/etc/kubernetes/manifests`를 감시하여 스태틱 파드로 구동합니다.

### ⚡ API 서버가 죽어 `kubectl` 명령이 전혀 먹히지 않을 때의 대처법
```bash
# 1. 컨테이너 런타임 CLI(crictl)를 직접 사용
crictl ps -a | grep kube-apiserver

# 2. 크래시된 컨테이너의 에러 로그 직접 열람
crictl logs <kube-apiserver-container-id>

# 3. 매니페스트 파일의 잘못된 플래그 또는 인증서 경로 수정
vi /etc/kubernetes/manifests/kube-apiserver.yaml
# 파일을 저장하면 kubelet이 파일 변경을 자동 감지(inotify)하여 수초 내 재기동함!
```

---

## 5.4 파드(Pod) 장애 유형별 원인 및 해결 매트릭스

| 장애 상태 | 주 원인 (Root Cause) | 해결 방법 (Remedy) |
| :--- | :--- | :--- |
| **`CrashLoopBackOff`** | • 컨테이너 내부 애플리케이션 시작 오류 (Exit Code 1)<br>• 필수 환경변수 또는 설정 파일 부재<br>• 포그라운드 프로세스 부재로 즉시 종료 | `kubectl logs <pod> --previous` 로 직전 에러 로그 확인.<br>`kubectl describe pod`에서 `Last State: Terminated, Exit Code` 분석 후 매니페스트 수정. |
| **`ImagePullBackOff`** / `ErrImagePull` | • 이미지 이름 또는 태그 오탈자 (예: `ngnix:latest`)<br>• 프라이빗 레지스트리 인증 시크릿 누락<br>• 노드 외부 인터넷 네트워크 단절 | `kubectl describe pod`의 Events에서 이미지 URL 확인.<br>`kubectl create secret docker-registry` 후 `spec.imagePullSecrets`에 등록. |
| **`Pending`** | • 노드 CPU/메모리 부족 (`Insufficient cpu/memory`)<br>• Taint를 견디지 못함 (`untolerated taint`)<br>• NodeSelector/Affinity 불일치 | 파드의 `requests`를 낮추거나 불필요한 파드 정리.<br>파드 스펙에 일치하는 `tolerations` 또는 `nodeSelector` 추가. |
| **`OOMKilled`** (Exit Code 137) | • 컨테이너가 `limits.memory` 한도 초과 | `kubectl describe pod`에서 `Reason: OOMKilled` 확인.<br>파드의 `resources.limits.memory` 값을 상향 조정. |
| **`ContainerCreating`** (장기 지연) | • 참조하는 Secret 또는 ConfigMap이 존재하지 않음<br>• PVC 볼륨 마운트 지연 또는 네트워크 스토리지 연결 실패 | `kubectl describe pod` Events에서 `MountVolume.SetUp failed` 확인.<br>누락된 Secret/ConfigMap 생성 또는 PVC 상태 점검. |

---

## 5.5 서비스 및 네트워크 통신 장애 디버깅

### 1. 서비스 VIP로 요청 시 타임아웃 ➔ 엔드포인트 누락 확인
```bash
# 1. 서비스 엔드포인트 목록 조회
kubectl get endpoints <service-name>

# 만약 <none>으로 나온다면?
# ➔ 원인 1: Service의 spec.selector 라벨과 Pod의 metadata.labels 불일치 (오탈자 확인)
# ➔ 원인 2: 백엔드 파드의 readinessProbe가 실패하여 엔드포인트에서 제외됨
```

### 2. CoreDNS 순환 루프 에러 (`Loop detected`) 복구
* **증상**: 클러스터 내부의 모든 도메인 해석 불가, CoreDNS 파드가 `CrashLoopBackOff` 상태.
* **원인**: 호스트 노드의 `/etc/resolv.conf` 네임서버가 `127.0.0.53` 또는 `127.0.0.1`로 설정되어 CoreDNS가 자기 자신에게 재귀 포워딩 루프 발생.
* **해결**: CoreDNS ConfigMap(`kubectl edit cm coredns -n kube-system`)에서 `loop` 플러그인을 주석 처리하거나, kubelet 설정의 `resolvConf` 경로를 실제 외부 DNS(8.8.8.8 등)가 정의된 파일로 변경.

---

## 5.6 실전 긴급 복구 명령어

```bash
# 1. 멈춘 파드 유예 시간 없이 즉시 강제 삭제
kubectl delete pod <pod-name> --force --grace-period=0

# 2. 임시 대화형 네트워크 테스트 파드 구동
kubectl run net-debug --image=busybox:1.28 --rm -it --restart=Never -- nslookup kubernetes.default
kubectl run net-debug --image=curlimages/curl --rm -it --restart=Never -- curl -v http://order-service:8080

# 3. 전체 네임스페이스의 경고(Warning) 이벤트 실시간 감시
kubectl get events -A --field-selector type=Warning --sort-by='.metadata.creationTimestamp'
```

## 5.5 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)

이 섹션은 CBT 문제 은행(**questions_domain5.json 250문항**)의 모든 핵심 개념(`key_concept`), 정답 해설 및 빈출 함정 키워드와 1:1로 일치하도록 정리된 요약본입니다.

| 출제 핵심 개념 (Key Concept) | 공식 출제 의도 및 필수 트러블슈팅 절차 | CBT 대표 오답 함정 & 판별 포인트 |
| :--- | :--- | :--- |
| **CrashLoopBackOff 분석** | • 컨테이너 프로세스가 기동 후 비정상 종료(Exit Code 1, 2 등) 반복<br>• 직전 컨테이너 종료 로그: `kubectl logs <pod> -c <container> -p` | • 실행 중인 파드 로그(`kubectl logs`)에는 에러가 없고 재시작만 반복될 수 있으므로 반드시 `-p`(--previous) 플래그로 직전 크래시 원인 확인. |
| **OOMKilled (Exit Code 137)** | 컨테이너 메모리 사용량이 `resources.limits.memory` 한도를 초과하여 리눅스 커널 OOM Killer에 의해 SIGKILL(9 + 128 = 137)됨 | • CPU 초과는 프로세스를 강제 종료하지 않고 Throttling(지연)을 발생시키지만, 메모리 초과는 즉시 OOMKilled 강제 종료됨. 해결책: limit 상향. |
| **ImagePullBackOff / ErrImagePull** | 1. 이미지 이름 또는 태그 오탈자<br>2. 프라이빗 레지스트리 인증 시크릿(`imagePullSecrets`) 누락<br>3. 네트워크 DNS 차단 | • `kubectl describe pod`의 맨 아래 Events 섹션에서 정확한 에러 메시지(401 Unauthorized vs 404 Not Found) 확인. |
| **Pod Pending 상태 해결** | 1. 노드 CPU/메모리 자원 부족<br>2. 노드의 Taint를 파드가 견디지 못함 (Toleration 누락)<br>3. `nodeSelector` 라벨과 일치하는 노드가 없음 | • 스케줄러 다운 시에도 모든 신규 파드가 Pending 상태가 됨 (`kubectl get pods -n kube-system` 확인). |
| **Node NotReady 긴급 복구** | 1. 워커 노드 SSH 접속<br>2. `systemctl status kubelet`, `journalctl -u kubelet -n 100 --no-pager`<br>3. CNI 플러그인 인터페이스 및 설정 확인 | • `/var/lib/kubelet/config.yaml`의 문법 오탈자나 인증서 만료 확인.<br>• kubelet 데몬이 꺼져 있으면 컨테이너 런타임이 살아 있어도 노드는 NotReady. |
| **제어 평면 다운 디버깅** | API 서버가 다운되면 `kubectl` 명령어 자체가 작동하지 않음! | • 노드 로컬에서 컨테이너 런타임 CLI 사용: `crictl ps -a`, `crictl logs <id>`<br>• `/etc/kubernetes/manifests` 내의 Static Pod YAML 오탈자 복구. |
| **서비스 통신 타임아웃** | 서비스 VIP로는 핑이 가지 않으며 정상 동작함. 통신 실패 시 `kubectl get ep <svc>`로 백엔드 파드 IP 바인딩 확인 | • 라벨 셀렉터 불일치 또는 파드의 `readinessProbe` 실패로 인해 파드가 서비스 엔드포인트에서 제외된 것이 주원인. |
| **파드 강제 삭제** | 노드 다운 등으로 파드가 `Terminating` 상태에서 멈춘 경우:<br>`kubectl delete pod <name> --force --grace-period=0` | • 정상 상태에서는 `--grace-period=0`을 남용하지 말고 정상 종료를 대기해야 함. |
