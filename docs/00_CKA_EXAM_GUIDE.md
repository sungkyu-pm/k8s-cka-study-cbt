# CKA (Certified Kubernetes Administrator) 시험 가이드 및 학습 로드맵

> **쿠버네티스 공인 관리자(CKA) 자격증 취득을 위한 완벽 안내서**  
> Linux Foundation & CNCF 공식 커리큘럼 기준 5대 도메인 완벽 반영 | 실기 & CBT 듀얼 대비 전략

---

## 🔗 공식 사이트 & 시험 접수 바로가기 (Official Links)

| 구분 | 주요 내용 및 공식 링크 |
| :--- | :--- |
| **🌐 Linux Foundation 공식 포털** | [Linux Foundation Training & Certification ↗](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/) |
| **📝 CNCF 공식 CKA 안내 페이지** | [CNCF Certified Kubernetes Administrator ↗](https://www.cncf.io/certification/cka/) |
| **📖 공식 쿠버네티스 문서 (시험 중 열람 가능)** | [Kubernetes Official Documentation ↗](https://kubernetes.io/docs/) |
| **📄 공식 CKA 커리큘럼 GitHub** | [CNCF Curriculum Repository ↗](https://github.com/cncf/curriculum) |
| **🖥️ PSI 시험 예약 및 대시보드** | [My Portal (Linux Foundation Candidate Portal) ↗](https://trainingportal.linuxfoundation.org/) |

---

## 1. 시험 개요 (Exam Overview)

* **시험 주관**: Linux Foundation & Cloud Native Computing Foundation (CNCF)
* **시험 방식**: 100% 실기(Performance-based / Hands-on) 원격 감독관 시험 (PSI Secure Browser 환경)
* **시험 시간**: 120분 (2시간)
* **문항 수**: 15 ~ 17문항 (실제 쿠버네티스 클러스터 터미널에서 작업 수행)
* **합격 기준**: **66% 이상** 득점 시 합격
* **재응시 기회 (Free Retake)**: 시험 1회 구매 시 **무료 재응시 기회 1회(Free Retake)** 기본 포함 (구매일로부터 12개월 이내)
* **인증 유효 기간**: 취득일로부터 **2년**
* **기반 쿠버네티스 버전**: 최신 안정화 버전 (보통 분기별 업데이트, 현재 v1.30 ~ v1.31 대응)

---

## 2. 도메인별 출제 비중 (Curriculum Weighting)

CKA 시험은 총 5개 도메인으로 구성되며, 특히 **문제 해결(Troubleshooting - 30%)**과 **클러스터 아키텍처(25%)**의 비중이 과반수(55%)를 차지합니다.

| 도메인 | 공식 도메인 명칭 | 출제 비중 | 핵심 평가 실무 역량 |
| :---: | :--- | :---: | :--- |
| **Domain 1** | **클러스터 아키텍처, 설치 및 구성**<br>*(Cluster Architecture, Installation & Configuration)* | **25%** | • kubeadm을 이용한 클러스터 설치 및 업그레이드<br>• etcd 데이터베이스 백업 및 복구(`etcdctl`)<br>• RBAC(Role, ClusterRole, RoleBinding) 권한 제어<br>• 고가용성(HA) 클러스터 아키텍처 이해 |
| **Domain 2** | **워크로드 및 스케줄링**<br>*(Workloads & Scheduling)* | **15%** | • Deployment 롤링 업데이트 및 롤백<br>• ConfigMap 및 Secret 생성 및 파드 주입<br>• DaemonSet, Job, CronJob 관리<br>• Taints & Tolerations, Node Affinity, 스케줄러 수동 제어 |
| **Domain 3** | **서비스 및 네트워킹**<br>*(Services & Networking)* | **20%** | • ClusterIP, NodePort, LoadBalancer 서비스 구성<br>• Ingress Controller 및 Ingress 라우팅 규칙<br>• CoreDNS 설정 및 파드 내부 도메인 질의<br>• NetworkPolicy를 활용한 인그레스/이그레스 트래픽 제어 |
| **Domain 4** | **스토리지**<br>*(Storage)* | **10%** | • PersistentVolume(PV) 및 PersistentVolumeClaim(PVC) 바인딩<br>• StorageClass와 동적 프로비저닝(Dynamic Provisioning)<br>• Pod 볼륨 마운트(VolumeMounts) 및 접근 모드(AccessModes)<br>• Reclaim Policy (Retain, Delete) 이해 |
| **Domain 5** | **문제 해결 (트러블슈팅)**<br>*(Troubleshooting)* | **30%** | • 클러스터 노드 장애 진단 및 복구(`systemctl`, `journalctl`)<br>• 핵심 컴포넌트(apiserver, scheduler, kubelet) 로그 분석<br>• 파드 비정상 상태(CrashLoopBackOff, ImagePullBackOff) 해결<br>• 네트워크 통신 실패 디버깅 |

---

## 3. 시험장 환경 및 필수 터미널 세팅 (Terminal Environment)

시험은 PSI 원격 데스크톱(XFCE GUI) 브라우저 내에서 진행됩니다. 터미널이 열리면 가장 먼저 아래 설정을 실행하여 시간을 대폭 단축해야 합니다.

### ⚡ 30초 시험장 초기 환경 설정
```bash
# 1. kubectl 단축어 설정
alias k=kubectl

# 2. yaml 생성용 dry-run 단축 환경변수 설정
export do="--dry-run=client -o yaml"
export now="--force --grace-period=0"

# 3. bash 자동완성 활성화
source <(kubectl completion bash)
complete -o default -F __start_kubectl k

# 4. vim 탭 간격(2칸) 및 들여쓰기 설정 (~/.vimrc)
cat <<EOF > ~/.vimrc
set tabstop=2
set shiftwidth=2
set expandtab
set number
EOF
```

### 💡 컨텍스트 전환(Context Switching) 주의사항
각 문제 상단에 지정된 **클러스터 컨텍스트 전환 명령어**가 주어집니다.
반드시 문제를 풀기 전 **지정된 컨텍스트로 전환 후 작업을 시작**해야 합니다:
```bash
# 예시:
kubectl config use-context k8s
```

---

## 4. CKA 합격을 위한 3단계 전략

```
[1단계: 핵심 아키텍처 & 용어 마스터]
  - docs/01_GLOSSARY_KR_EN.md: 영문/한글 핵심 쿠버네티스 개념 정리
  - docs/02 ~ 06: 도메인 1~5 핵심 이론 및 매니페스트 구조 파악
  - docs/07_KUBECTL_CHEAT_SHEET.md: Imperative 명령 숙달

[2단계: 명령형 커맨드(Imperative CLI) 중심 실습]
  - 매니페스트를 처음부터 작성하지 않고, 'k run', 'k create deployment'에 
    $do (--dry-run=client -o yaml)를 붙여 YAML 뼈대를 5초 만에 생성!
  - questions/ 폴더의 도메인별 실전 문제 및 개념 검증

[3단계: 실전 모의고사 반복 & 트러블슈팅 체화]
  - 본 포털의 [CBT 가상 실습] 탭 활용
  - 1회차: [학습 모드] 한/영 번역 토글과 상세 해설을 통해 개념 완벽 정리
  - 2회차: [실전 모드] 카운트다운 타이머와 함께 신속한 문제 풀이 훈련
  - 오답 분석표로 취약 도메인 집중 공략
```
