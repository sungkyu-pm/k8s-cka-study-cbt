# 도메인 5: 문제 해결 및 장애 진단 (Troubleshooting)

> **출제 비중**: **30% (합격을 가르는 최대 비중 도메인)**  
> **핵심 키워드**: 노드 NotReady 진단, kubelet 데몬 복구(`journalctl`), 제어 평면 컴포넌트(Static Pod) 디버깅, 파드 장애(CrashLoopBackOff, Pending, ImagePullBackOff, OOMKilled), CoreDNS 진단

---

## 1. 4단계 체계적 트러블슈팅 워크플로우

장애가 발생했을 때 당황하지 않고 아래 4단계를 순서대로 진행합니다:

```
[1단계: 리소스 상태 확인]
  $ kubectl get nodes
  $ kubectl get pods -A -o wide

[2단계: 상세 이벤트 및 상태 확인]
  $ kubectl describe pod <pod-name> -n <ns>
  $ kubectl describe node <node-name>

[3단계: 애플리케이션 및 시스템 로그 확인]
  $ kubectl logs <pod-name> [-c <container-name>] [--previous]
  $ journalctl -u kubelet -n 100 --no-pager

[4단계: 컨테이너 런타임 직접 점검 (노드 내부)]
  $ crictl ps -a
  $ crictl logs <container-id>
```

---

## 2. 노드 장애 (Node NotReady) 진단 및 복구

### 2.1 원인 파악 및 kubelet 점검
워커 노드가 `NotReady` 상태인 주원인은 **kubelet 서비스 중단** 또는 **인증서/설정 오탈자**입니다.
```bash
# 1. 문제 노드로 SSH 접속
ssh node-1

# 2. kubelet 서비스 상태 확인
systemctl status kubelet

# 3. 실패 로그 확인 (원인 파악의 핵심)
journalctl -u kubelet -n 50 -e --no-pager

# 4. 서비스 활성화 및 재시작
systemctl daemon-reload
systemctl restart kubelet
systemctl enable kubelet
```

### 2.2 kubelet 설정 파일 오탈자 검사
`/var/lib/kubelet/config.yaml` 또는 `/etc/systemd/system/kubelet.service.d/10-kubeadm.conf` 파일 내의 경로 오탈자, 잘못된 클러스터 DNS IP(`clusterDNS`), 만료된 인증서 경로를 확인합니다.

---

## 3. 제어 평면 (Control Plane) 컴포넌트 디버깅

마스터 노드의 핵심 컴포넌트(API Server, Scheduler, Controller Manager, etcd)는 **Static Pod**로 실행됩니다.

* **매니페스트 디렉토리**: `/etc/kubernetes/manifests/`
* **주요 장애 유형**:
  * YAML 파일의 오탈자(typo)나 잘못된 플래그 옵션
  * 인증서 파일명이나 경로 오류
* **해결 팁**:
  * API 서버가 죽어 `kubectl` 명령 자체가 먹히지 않을 때는 **컨테이너 런타임 CLI(`crictl`)**를 사용합니다:
  ```bash
  # 실행 중이거나 종료된 컨테이너 조회
  crictl ps -a
  
  # API 서버 컨테이너 로그 직접 확인
  crictl logs <kube-apiserver-container-id>
  ```

---

## 4. 파드(Pod) 장애 유형별 원인 및 해결책

| 파드 상태 | 주 원인 | 확인 및 해결 방법 |
| :--- | :--- | :--- |
| **`Pending`** | • 노드 리소스(CPU/Memory) 부족<br>• Taint를 견디지 못함 (Toleration 누락)<br>• NodeSelector/Affinity 불일치 | `kubectl describe pod` 하단의 `Events:` 섹션 확인.<br>노드 용량 확보 또는 스케줄링 제약 수정. |
| **`ImagePullBackOff` / `ErrImagePull`** | • 이미지 이름/태그 오탈자<br>• 프라이빗 레지스트리 인증 시크릿(imagePullSecrets) 누락<br>• 네트워크 격리 | 이미지 이름 및 태그 확인.<br>`kubectl describe pod`에서 실패한 이미지 URL 점검. |
| **`CrashLoopBackOff`** | • 애플리케이션 시작 코드 오류(종료 코드 1 등)<br>• 필수 환경변수 또는 마운트 파일 누락<br>• 컨테이너의 포그라운드 프로세스 부재 | 이전 실행 로그 확인:<br>`kubectl logs <pod> --previous`<br>`kubectl describe pod`에서 Exit Code 확인. |
| **`OOMKilled`** (Exit Code 137) | • 컨테이너가 지정된 `resources.limits.memory` 초과 | `kubectl describe pod`에서 `Last State: Terminated, Reason: OOMKilled` 확인.<br>Memory Limit 상향 조정. |

---

## 5. 네트워크 및 DNS 트러블슈팅

클러스터 내부에서 도메인 이름 해석이 안 될 때:
```bash
# 1. CoreDNS 파드 상태 및 엔드포인트 확인
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl get ep -n kube-system kube-dns

# 2. 임시 디버깅 파드를 띄워 DNS 질의 테스트
kubectl run dns-test --image=busybox:1.28 --restart=Never --rm -it -- nslookup kubernetes.default

# 3. CoreDNS 로그 실시간 확인
kubectl logs -n kube-system -l k8s-app=kube-dns -f
```
