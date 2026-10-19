#!/usr/bin/env python3
"""
sync_docs_and_questions.py
학습 가이드 문서(docs/)와 문제 은행(questions/)의 설명 내용을 100% 일치시키고,
portal-docs-data.js 번들링을 갱신하는 통합 스크립트.
"""

import os
import json
import glob

DOCS_DIR = 'docs'

def append_section_if_not_present(filepath, section_title, content):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if section_title in text:
        # 기존 섹션 대체 또는 보강
        parts = text.split(section_title)
        text = parts[0]
    
    updated_text = text.rstrip() + "\n\n" + section_title + "\n\n" + content.strip() + "\n"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_text)
    print(f"Updated: {filepath}")

# 1. CKA 도메인 1 보강
d1_cbt_section = """
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
"""
append_section_if_not_present('docs/02_DOMAIN_1_CLUSTER_ARCHITECTURE.md', '## 1.6 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)', d1_cbt_section)

# 2. CKA 도메인 2 보강
d2_cbt_section = """
이 섹션은 CBT 문제 은행(**questions_domain2.json 250문항**)의 모든 핵심 개념(`key_concept`), 정답 해설 및 빈출 함정 키워드와 1:1로 일치하도록 정리된 요약본입니다.

| 출제 핵심 개념 (Key Concept) | 공식 출제 의도 및 필수 매니페스트 속성 | CBT 대표 오답 함정 & 판별 포인트 |
| :--- | :--- | :--- |
| **Deployment 롤링 업데이트** | • `strategy.rollingUpdate.maxSurge`: 동시 초과 허용 파드 수/비율<br>• `strategy.rollingUpdate.maxUnavailable`: 동시 불능 허용 파드 수/비율 | • 즉시 롤백: `kubectl rollout undo deployment/<name> --to-revision=1`<br>• 히스토리 기록 확인: `kubectl rollout history deployment/<name>` |
| **DaemonSet 스케줄링** | 클러스터 모든 노드에 파드 1개 보장, 마스터 노드 배포 시 Toleration 필수:<br>`key: node-role.kubernetes.io/control-plane, operator: Exists, effect: NoSchedule` | • `replicas` 필드가 없음 (DaemonSet에 replicas를 지정하면 YAML 에러 발생).<br>• 마스터 노드에 CNI나 모니터링 데몬 배포 시 toleration 누락 주의. |
| **StatefulSet & Headless Service** | • `serviceName: <headless-svc>` 명시<br>• `volumeClaimTemplates`로 파드마다 고유 PVC 자동 생성<br>• 파드명: `web-0`, `web-1` 고유 서수 인덱스 | • 일반 ClusterIP 서비스와 결합하면 안 되며 반드시 `spec.clusterIP: None`인 Headless Service와 결합해야 개별 파드 도메인 해석 가능. |
| **CronJob 동시성 제어** | `concurrencyPolicy`: `Allow`(기본), `Forbid`(이전 잡 미완료 시 새 잡 건너뜀), `Replace`(기존 잡 취소 후 새 잡 실행) | • `restartPolicy`는 Job/CronJob 파드에서 절대로 `Always`를 쓸 수 없음 (`OnFailure` 또는 `Never` 필수). |
| **멀티 컨테이너 & 사이드카** | 메인 컨테이너와 사이드카 컨테이너가 `emptyDir` 볼륨을 공유하여 로그 수집/프록시 수행 | • 컨테이너 간 통신은 `localhost`로 가능 (동일 네트워크 네임스페이스 및 IP 공유). |
| **Init Container 수명주기** | 메인 컨테이너 기동 전 1개씩 순차 완료되어야 함. 실패 시 메인 컨테이너는 절대 실행되지 않음 | • DB 준비 상태 대기: `until nc -z db 3306; do sleep 2; done`<br>• 리소스는 init 컨테이너 중 최댓값으로 평가됨. |
| **NodeAffinity Hard vs Soft** | • Hard: `requiredDuringSchedulingIgnoredDuringExecution`<br>• Soft: `preferredDuringSchedulingIgnoredDuringExecution` | • Hard 규칙 조건 미충족 시 파드는 `Pending` 상태로 머묾.<br>• Soft 규칙은 미충족 시에도 다른 노드에 스케줄링됨. |
| **Taints & Tolerations** | • 노드 테인트: `kubectl taint nodes node-1 env=prod:NoSchedule`<br>• 테인트 제거: `kubectl taint nodes node-1 env=prod:NoSchedule-` | • Toleration은 파드가 노드를 선택하는 것이 아니라, 노드의 Taint를 견디는(tolerate) 허가증임. |
| **securityContext 보안 제약** | `securityContext.runAsNonRoot: true`, `readOnlyRootFilesystem: true`, `capabilities.add: ["NET_ADMIN"]` | • root 사용자로 실행 시 파드가 즉시 에러로 중단됨.<br>• 파드 레벨 vs 컨테이너 레벨 설정 범위 구별. |
| **리소스 QoS 3대 등급** | • **Guaranteed**: CPU/Memory의 requests와 limits가 정확히 일치<br>• **Burstable**: requests < limits<br>• **BestEffort**: requests/limits 모두 미지정 | • 노드 메모리 고갈 시 OOM 킬러 퇴거 1순위는 `BestEffort`, 마지막 보호 대상은 `Guaranteed`. |
"""
append_section_if_not_present('docs/03_DOMAIN_2_WORKLOADS_SCHEDULING.md', '## 2.7 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)', d2_cbt_section)

# 3. CKA 도메인 3 보강
d3_cbt_section = """
이 섹션은 CBT 문제 은행(**questions_domain3.json 250문항**)의 모든 핵심 개념(`key_concept`), 정답 해설 및 빈출 함정 키워드와 1:1로 일치하도록 정리된 요약본입니다.

| 출제 핵심 개념 (Key Concept) | 공식 출제 의도 및 필수 매니페스트 속성 | CBT 대표 오답 함정 & 판별 포인트 |
| :--- | :--- | :--- |
| **3대 포트 체계 구분** | • `port`: Service 가상 IP(VIP)에서 수신하는 포트<br>• `targetPort`: 백엔드 Pod 컨테이너에서 실제 리스닝 중인 포트<br>• `nodePort`: 모든 워커 노드 물리 IP로 노출되는 외부 포트 (30000~32767) | • 클러스터 내부 파드가 서비스로 호출할 때는 `port`로 요청해야 하며, `targetPort`로 직접 쏘면 연결 실패. |
| **셀렉터 없는 Service & Endpoints** | 외부에 있는 레거시 DB나 서드파티 서비스를 내부 쿠버네티스 서비스 이름으로 참조할 때 수동 Endpoints 매핑 | • Service의 `spec.selector`를 비워두고, 동일한 `metadata.name`을 가진 `Endpoints` 리소스를 수동 생성해야 함. |
| **Headless Service DNS** | `spec.clusterIP: None` 설정 시 단일 가상 IP를 생성하지 않고, DNS 질의 시 백엔드 파드 IP 목록을 직접 반환 | • StatefulSet과 필수 결합하여 개별 파드 `<pod-name>.<svc>.<ns>.svc.cluster.local` A-레코드 해석 제공. |
| **Ingress pathType & Rewrite** | • `pathType: Prefix` (하위 경로 매칭) vs `Exact` (정확 매칭)<br>• Nginx rewrite: `nginx.ingress.kubernetes.io/rewrite-target: /$2` | • rewrite 어노테이션 누락 시 `/app` 경로 요청이 백엔드 컨테이너의 `/app`으로 그대로 전달되어 404 발생. |
| **Ingress TLS 인증서 바인딩** | `spec.tls[0].hosts` 목록 및 `spec.tls[0].secretName`에 `kubernetes.io/tls` 타입 Secret 매핑 | • Secret 내부 키 이름은 반드시 `tls.crt`와 `tls.key`여야 함. |
| **CoreDNS FQDN 표준** | 서비스: `<service-name>.<namespace>.svc.cluster.local`<br>파드: `<ip-하이픈-대체>.<namespace>.pod.cluster.local` | • 동일 네임스페이스 내에서는 `<service-name>` 단축어로 접근 가능.<br>• 타 네임스페이스 접근 시 `<svc>.<ns>` 필수. |
| **NetworkPolicy 트래픽 격리** | • CNI(Calico/Cilium) 지원 필수 (Flannel 단독 사용 시 동작 안 함)<br>• `policyTypes: ["Ingress", "Egress"]` 명시 | • `podSelector: {}`: 해당 네임스페이스의 모든 파드 대상.<br>• 규칙 미지정 시 기본 완전 차단(Default Deny). |
| **NetworkPolicy AND vs OR** | • **AND**: 동일 배열 요소 내에 `podSelector`와 `namespaceSelector`가 함께 있는 경우<br>• **OR**: `- namespaceSelector:` 와 `- podSelector:` 가 별도 대시(-)로 나뉜 경우 | • 특정 네임스페이스의 특정 파드만 허용하려면 반드시 단일 블록(AND)으로 작성해야 함. |
| **Egress CoreDNS 필수 허용** | 모든 Egress를 차단했을 때 DNS 질의가 막히므로, 포트 53(UDP/TCP) Egress 허용 규칙을 반드시 포함해야 함 | • `ports: [{protocol: UDP, port: 53}, {protocol: TCP, port: 53}]` 누락 시 서비스 이름 해석 불가. |
"""
append_section_if_not_present('docs/04_DOMAIN_3_SERVICES_NETWORKING.md', '## 3.5 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)', d3_cbt_section)

# 4. CKA 도메인 4 보강
d4_cbt_section = """
이 섹션은 CBT 문제 은행(**questions_domain4.json 250문항**)의 모든 핵심 개념(`key_concept`), 정답 해설 및 빈출 함정 키워드와 1:1로 일치하도록 정리된 요약본입니다.

| 출제 핵심 개념 (Key Concept) | 공식 출제 의도 및 필수 매니페스트 속성 | CBT 대표 오답 함정 & 판별 포인트 |
| :--- | :--- | :--- |
| **PV & PVC 바인딩 3대 조건** | 1. `storageClassName` 일치<br>2. `accessModes` 호환<br>3. PV 용량 $\\ge$ PVC 요청 용량 | • PVC 요청 용량이 PV보다 단 1바이트라도 크면 바인딩되지 않고 `Pending` 상태로 대기. |
| **AccessModes 4대 유형** | • `ReadWriteOnce` (RWO): 단일 노드에서 읽기/쓰기<br>• `ReadOnlyMany` (ROX): 여러 노드에서 읽기 전용<br>• `ReadWriteMany` (RWX): 여러 노드에서 읽기/쓰기 (NFS, EFS)<br>• `ReadWriteOncePod` (RWOP): 단일 파드 전용 | • AWS EBS 볼륨은 물리적으로 단일 노드에만 연결되므로 RWX를 지원하지 않음 (RWO만 지원). |
| **ReclaimPolicy 반환 정책** | • `Retain`: PVC 삭제 시 PV는 `Released` 상태가 되며 데이터 보존 (수동 정리 필요)<br>• `Delete`: PVC 삭제 시 PV 및 백엔드 물리 스토리지 자산까지 즉시 자동 삭제 | • `Released` 상태의 PV는 다른 PVC가 즉시 재바인딩할 수 없으며, `claimRef`를 수동 제거해야 `Available`로 복귀. |
| **WaitForFirstConsumer** | `StorageClass`의 `volumeBindingMode: WaitForFirstConsumer` | • PVC 생성 즉시 볼륨을 생성하지 않고, 파드가 어느 노드에 스케줄링될지 확정된 후 볼륨을 프로비저닝하여 토폴로지 불일치 스케줄링 실패 방지. |
| **온라인 볼륨 용량 확장** | `StorageClass`에 `allowVolumeExpansion: true` 설정 후, PVC의 `spec.resources.requests.storage`를 상향 편집 | • PVC 용량을 줄이는 축소(Shrink)는 쿠버네티스에서 절대 지원하지 않음 (오직 확장만 가능). |
| **subPath 마운트 기법** | `volumeMounts[0].subPath: my-config.json` | • 볼륨 전체를 `/etc/config`에 마운트하면 해당 디렉토리의 기존 파일들이 모두 가려지므로, 단일 파일만 덮어쓸 때는 `subPath` 필수. |
| **ConfigMap/Secret 권한 제어** | `volumes[0].configMap.defaultMode: 0400` (읽기 전용) | • 8진수 퍼미션 설정으로 컨테이너 내부 프로세스가 설정 파일을 위변조하지 못하도록 방어. |
| **PVC Protection Finalizer** | `kubernetes.io/pvc-protection` | • 파드가 사용 중인 PVC를 삭제 시도하면 즉시 삭제되지 않고 `Terminating` 상태로 보류됨. 파드가 종료되어야 비로소 삭제 완료. |
"""
append_section_if_not_present('docs/05_DOMAIN_4_STORAGE.md', '## 4.5 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)', d4_cbt_section)

# 5. CKA 도메인 5 보강
d5_cbt_section = """
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
"""
append_section_if_not_present('docs/06_DOMAIN_5_TROUBLESHOOTING.md', '## 5.5 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)', d5_cbt_section)

# 6. KCNA 영역 1~5 보강
kcna_d1_section = """
이 섹션은 CBT 문제 은행(**questions_kcna_domain1.json 50문항**)의 모든 핵심 개념(`key_concept`), 정답 해설 및 빈출 함정 키워드와 1:1로 일치하도록 정리된 요약본입니다.

| 출제 핵심 개념 (Key Concept) | 공식 출제 의도 및 CNCF 표준 정의 | CBT 대표 오답 함정 & 판별 포인트 |
| :--- | :--- | :--- |
| **CNCF 클라우드 네이티브 정의** | 회복성(Resilient), 관리 용이성(Manageable), 관측 가능성(Observable)을 갖춘 시스템 구축. 선언적 API(Declarative APIs)와 자동화된 변경 지원 | • "하드웨어 비용 절감"이나 "모놀리식 단일 배포"는 CNCF 클라우드 네이티브의 핵심 정의가 아님. |
| **12-Factor III: Config** | 환경마다 달라지는 설정(DB 주소, API 키 등)은 소스 코드와 엄격히 분리하여 실행 환경 변수로 주입 | • 설정을 코드에 하드코딩하거나 Git 저장소에 커밋하는 것은 12-Factor 위반. (Kubernetes에서는 ConfigMap/Secret 주입). |
| **12-Factor IX: Disposability** | 빠른 시작(Fast Startup)과 우아한 종료(Graceful Shutdown - SIGTERM 대응)로 견고성 극대화 | • 장시간 기동 대기나 비정상 강제 종료는 폐기 가능성 위반. |
| **불변 인프라 (Immutable Infra)** | 배포 후 서버를 직접 수정(패치, SSH 접속)하지 않고, 항상 새로운 이미지로 교체 배포 | • 운영 중인 컨테이너에 직접 들어가서 설정을 고치는 안티패턴 방지. |
| **서버리스 & Knative** | 이벤트 기반 실행, 자동 스케일링 (0으로 축소되는 Scale-to-Zero), 인프라 관리 추상화 | • Knative Serving(Scale-to-Zero)과 Knative Eventing(CloudEvents 기반 이벤트 라우팅)의 역할 분담. |
| **Envoy 프록시 & 서비스 메시** | 고성능 L7 프록시, 사이드카 배포를 통해 마이크로서비스 간 트래픽 제어, mTLS 상호 인증, 분산 관측성 제공 | • 애플리케이션 비즈니스 코드 수정 없이 인프라 계층에서 네트워크 기능 수행. |
"""
append_section_if_not_present('docs/kcna/01_CLOUD_NATIVE_ARCHITECTURE.md', '## 1.6 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)', kcna_d1_section)

kcna_d2_section = """
이 섹션은 CBT 문제 은행(**questions_kcna_domain2.json 100문항**)의 모든 핵심 개념(`key_concept`), 정답 해설 및 빈출 함정 키워드와 1:1로 일치하도록 정리된 요약본입니다.

| 출제 핵심 개념 (Key Concept) | 공식 출제 의도 및 쿠버네티스 원리 | CBT 대표 오답 함정 & 판별 포인트 |
| :--- | :--- | :--- |
| **Control Plane 컴포넌트 분담** | • **kube-apiserver**: 유일하게 etcd와 직접 통신하는 관문 REST API<br>• **etcd**: 분산 합의(Raft) 기반 고가용성 키-값 저장소<br>• **kube-scheduler**: 노드 리소스 평가 후 파드 배치 결정<br>• **kube-controller-manager**: Desired State 수렴 제어 루프 | • kube-scheduler는 파드를 직접 실행하는 프로세스가 아님 (실행은 워커 노드의 kubelet이 담당).<br>• etcd와 직접 통신할 수 있는 컴포넌트는 오직 apiserver뿐임. |
| **Worker Node 에이전트** | • **kubelet**: 노드 데몬, PodSpec 기반 컨테이너 구동/상태 보고<br>• **kube-proxy**: 서비스 가상 IP 포워딩 (iptables/IPVS)<br>• **CRI**: 컨테이너 런타임(containerd) | • kubelet은 쿠버네티스 파드로 뜨지 않고 노드 OS의 systemd 데몬으로 직접 실행됨. |
| **워크로드 컨트롤러 5종 비교** | • **Deployment**: 무상태 롤링 업데이트<br>• **DaemonSet**: 모든 노드 1개씩 실행 (로깅/모니터링)<br>• **StatefulSet**: 고유 식별자, 순차 배포, Headless 연계, DB<br>• **Job**: 1회성 완료 작업<br>• **CronJob**: 주기적 스케줄링 | • 모니터링 데몬 배포에 Deployment를 쓰면 특정 노드에 몰릴 수 있으므로 반드시 DaemonSet 사용. |
| **서비스 4대 타입** | `ClusterIP`(내부), `NodePort`(외부 30000~32767), `LoadBalancer`(클라우드 LB), `ExternalName`(CNAME) | • Headless 서비스는 `spec.clusterIP: None`으로 설정하여 DNS 직접 질의 지원. |
| **RBAC 인가 체계** | `Role` & `RoleBinding` (네임스페이스 단위) vs `ClusterRole` & `ClusterRoleBinding` (클러스터 전역) | • 노드(`nodes`)나 네임스페이스 자체는 비네임스페이스 리소스이므로 RoleBinding이 아닌 ClusterRoleBinding 필요. |
"""
append_section_if_not_present('docs/kcna/02_KUBERNETES_FUNDAMENTALS.md', '## 2.6 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)', kcna_d2_section)

kcna_d3_section = """
이 섹션은 CBT 문제 은행(**questions_kcna_domain3.json 50문항**)의 모든 핵심 개념(`key_concept`), 정답 해설 및 빈출 함정 키워드와 1:1로 일치하도록 정리된 요약본입니다.

| 출제 핵심 개념 (Key Concept) | 공식 출제 의도 및 표준 인터페이스 정의 | CBT 대표 오답 함정 & 판별 포인트 |
| :--- | :--- | :--- |
| **CRI (Container Runtime Interface)** | kubelet과 컨테이너 런타임(containerd, CRI-O) 간의 gRPC 통신 사양 | • 쿠버네티스 1.24에서 레거시 dockershim이 완전히 제거되어 containerd 직접 통신 표준화. |
| **OCI (Open Container Initiative)** | 컨테이너 런타임 표준(runtime-spec, runc) 및 이미지 포맷 표준(image-spec) | • 특정 벤더(Docker)에 종속되지 않고 어떤 OCI 호환 런타임에서도 동일하게 컨테이너 실행 보장. |
| **CNI (Container Network Interface)** | 파드에 IP 주소를 할당하고 파드 간 오버레이 네트워크 통신을 구성하는 플러그인 사양 (Calico, Flannel, Cilium) | • CNI 플러그인이 미설치되면 클러스터의 모든 워커 노드는 `NotReady` 상태로 유지됨. |
| **CSI (Container Storage Interface)** | 서드파티 스토리지 벤더가 쿠버네티스 코어 코드 수정 없이 플러그인 형태로 볼륨을 연동할 수 있게 해주는 외부(Out-of-tree) 사양 | • In-tree 스토리지 플러그인 방식의 유지보수 한계를 극복하기 위해 제정됨. |
| **Namespaces vs cgroups (Linux)** | • **Namespaces**: 프로세스 간 격리 (PID, Mount, Network, IPC, UTS, User)<br>• **cgroups**: CPU, Memory, I/O 등 시스템 자원 사용량 제한 및 계측 | • 격리(Isolation)는 Namespaces가 담당하고, 자원 제한(Resource Limits)은 cgroups가 담당함 (혼동 금지). |
| **3대 컨테이너 프로브** | • **StartupProbe**: 애플리케이션 초기 기동 완료 대기<br>• **LivenessProbe**: 컨테이너 멈춤(Hang) 감지 시 강제 재시작<br>• **ReadinessProbe**: 준비 미완료 시 서비스 엔드포인트에서 트래픽만 격리 | • Liveness 실패는 파드를 재시작시키지만, Readiness 실패는 파드를 죽이지 않고 트래픽 인입만 차단함. |
"""
append_section_if_not_present('docs/kcna/03_CONTAINER_ORCHESTRATION.md', '## 3.6 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)', kcna_d3_section)

kcna_d4_section = """
이 섹션은 CBT 문제 은행(**questions_kcna_domain4.json 30문항**)의 모든 핵심 개념(`key_concept`), 정답 해설 및 빈출 함정 키워드와 1:1로 일치하도록 정리된 요약본입니다.

| 출제 핵심 개념 (Key Concept) | 공식 출제 의도 및 모니터링 표준 | CBT 대표 오답 함정 & 판별 포인트 |
| :--- | :--- | :--- |
| **관측 가능성 3대 기둥** | • **Metrics**: 시계열 수치 데이터 (CPU, Memory, 요청 수)<br>• **Logs**: 타임스탬프가 찍힌 이벤트 텍스트 기록<br>• **Traces**: 분산 서비스 간 요청의 엔드투엔드 여정 추적 | • 메트릭만으로는 특정 에러의 근본 원인을 파악하기 어려우며, 3대 요소를 상호 연계해야 완전한 관측 가능성 달성. |
| **Prometheus 풀 모델** | 대상 엔드포인트(`/metrics`)를 일정한 주기(scrape_interval)로 직접 HTTP GET 요청하여 메트릭을 당겨오는(Pull) 아키텍처 | • 에이전트가 중앙 서버로 능동 전송하는 Push 방식이 아니라 서버가 대상을 Pull하는 방식임 (Pushgateway는 배치 작업 예외용). |
| **OpenTelemetry (OTel)** | 분산 시스템에서 메트릭, 로그, 트레이스를 생성, 수집, 내보내기 위한 벤더 중립적 오픈소스 표준 프레임워크 | • 특정 시각화 백엔드(Datadog, Jaeger 등)에 종속되지 않고 OTel Collector를 통해 다중 백엔드로 전송 가능. |
| **Jaeger 분산 추적** | 마이크로서비스 간의 트랜잭션 호출 흐름, 병목 지점 및 지연 시간(Latency)을 Span과 Trace 단위로 시각화 | • 단일 서버 로그만으로는 마이크로서비스 간 호출 지연 원인을 찾을 수 없으므로 Jaeger 분산 추적이 필수적임. |
"""
append_section_if_not_present('docs/kcna/04_OBSERVABILITY.md', '## 4.5 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)', kcna_d4_section)

kcna_d5_section = """
이 섹션은 CBT 문제 은행(**questions_kcna_domain5.json 30문항**)의 모든 핵심 개념(`key_concept`), 정답 해설 및 빈출 함정 키워드와 1:1로 일치하도록 정리된 요약본입니다.

| 출제 핵심 개념 (Key Concept) | 공식 출제 의도 및 GitOps/배포 표준 | CBT 대표 오답 함정 & 판별 포인트 |
| :--- | :--- | :--- |
| **GitOps 핵심 원칙** | • **단일 진실의 원천 (Single Source of Truth)**: Git 저장소가 전체 시스템의 원하는 상태(Desired State)를 보관<br>• 선언적 명세, 자동 동기화, 드리프트(Drift) 자동 감지 및 치유 | • 개발자가 클러스터 터미널에 직접 `kubectl apply`를 실행하는 것은 GitOps 원칙에 위배됨. 모든 변경은 Git PR을 통해 수행. |
| **GitOps 대표 도구** | • **Argo CD**: 쿠버네티스 전용 선언적 GitOps CD 도구 (웹 UI, Application CRD)<br>• **Flux**: 모듈식 GitOps 툴킷 | • Jenkins나 GitLab CI는 주로 CI(빌드/테스트) 단계에 사용되며, 클러스터 내부 동기화는 Argo CD/Flux가 담당. |
| **Helm 차트 표준 구조** | • `Chart.yaml`: 차트 메타데이터 (이름, 버전)<br>• `values.yaml`: 기본 설정 값 정의<br>• `templates/`: 매니페스트 템플릿 디렉토리 | • Helm은 쿠버네티스의 패키지 관리자로, 템플릿과 값을 결합하여 릴리스(Release)를 배포하고 손쉬운 롤백 지원. |
| **Harbor & Trivy 보안** | • **Harbor**: CNCF 졸업 오픈소스 프라이빗 컨테이너 레지스트리 (RBAC, 이미지 복제)<br>• **Trivy**: 취약점 스캐너 (CVE 취약점 및 설정 오류 사전 차단) | • 빌드된 컨테이너 이미지를 배포하기 전에 취약점 스캔을 통과해야 배포되도록 파이프라인 구성. |
"""
append_section_if_not_present('docs/kcna/05_APPLICATION_DELIVERY.md', '## 5.5 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)', kcna_d5_section)

# 7. portal-docs-data.js 자동 재생성
print("\\nRebuilding portal-docs-data.js from updated docs...")

doc_mapping = {
    'exam_guide': 'docs/00_CKA_EXAM_GUIDE.md',
    'glossary': 'docs/01_GLOSSARY_KR_EN.md',
    'domain1': 'docs/02_DOMAIN_1_CLUSTER_ARCHITECTURE.md',
    'domain2': 'docs/03_DOMAIN_2_WORKLOADS_SCHEDULING.md',
    'domain3': 'docs/04_DOMAIN_3_SERVICES_NETWORKING.md',
    'domain4': 'docs/05_DOMAIN_4_STORAGE.md',
    'domain5': 'docs/06_DOMAIN_5_TROUBLESHOOTING.md',
    'kubectl_cheat': 'docs/07_KUBECTL_CHEAT_SHEET.md',
    'kcna_guide': 'docs/kcna/00_KCNA_EXAM_GUIDE.md',
    'kcna_domain1': 'docs/kcna/01_CLOUD_NATIVE_ARCHITECTURE.md',
    'kcna_domain2': 'docs/kcna/02_KUBERNETES_FUNDAMENTALS.md',
    'kcna_domain3': 'docs/kcna/03_CONTAINER_ORCHESTRATION.md',
    'kcna_domain4': 'docs/kcna/04_OBSERVABILITY.md',
    'kcna_domain5': 'docs/kcna/05_APPLICATION_DELIVERY.md',
    'kcna_glossary': 'docs/kcna/06_KCNA_GLOSSARY.md'
}

docs_dict = {}
for key, filepath in doc_mapping.items():
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            docs_dict[key] = f.read()
    else:
        print(f"Warning: File not found: {filepath}")

with open('portal-docs-data.js', 'w', encoding='utf-8') as f:
    f.write('window.PORTAL_DOCS = ' + json.dumps(docs_dict, ensure_ascii=False) + ';\n')

print(f"portal-docs-data.js updated successfully! Size: {os.path.getsize('portal-docs-data.js')} bytes, {len(docs_dict)} documents.")
