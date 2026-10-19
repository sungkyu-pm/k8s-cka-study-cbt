# Certified Kubernetes Administrator (CKA) 학습 & CBT 플랫폼

> **한국어 사용자를 위한 CKA/CKAD 시험 대비 올인원(All-in-One) 학습 공간 및 실전 CBT 시뮬레이션 시스템**  
> Linux Foundation & CNCF 공식 커리큘럼 기준 5대 도메인 완벽 반영 | 한·영 듀얼 트랙 학습 | 실전 CBT 모의고사 & Kubectl 치트시트 지원

---

## 🔗 공식 시험 및 접수 링크 (Official Links)
* **Linux Foundation CKA 공식 포털**: [Linux Foundation Certified Kubernetes Administrator (CKA) ↗](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/)
* **CNCF 공식 자격증 안내**: [CNCF Certification Programs ↗](https://www.cncf.io/certification/cka/)
* **공식 쿠버네티스 문서 (시험 중 검색 및 열람 가능)**: [Kubernetes Documentation ↗](https://kubernetes.io/docs/)
* **CNCF CKA 커리큘럼 가이드**: [CNCF Curriculum Repository ↗](https://github.com/cncf/curriculum)
* **Linux Foundation 시험 예약 대시보드**: [My Portal (Pearson/PSI) ↗](https://trainingportal.linuxfoundation.org/)

---

## 🚀 빠른 시작 (Quick Start)

### 💻 방법 1: 로컬 서버 실행 (추천)
시험 응시 이력 저장, 실시간 채점, 오답 노트 누적 기록을 지원하는 전용 로컬 경량 백엔드 서버입니다 (추가 pip 라이브러리 설치 불필요).

터미널에서 아래 명령어를 실행하면 서버가 켜지며 브라우저가 자동으로 열립니다:
```bash
./run.sh
```
또는 직접 파이썬으로 실행:
```bash
python3 server.py
```
접속 주소: **`http://localhost:8080`**

---

### 📂 방법 2: 브라우저 직접 열기 (파일 모드)
서버 실행 없이 정적 파일 모드로 브라우저에서 바로 확인하고 싶다면:
* Finder에서 루트 폴더의 [`index.html`](file:///Users/sungkyu/Study/K8S/index.html)을 더블 클릭하여 크롬이나 사파리로 엽니다.

---

## 📂 프로젝트 구성 안내

```
K8S/
├── docs/                                      # 📚 체계적인 이론 및 실무 가이드 자료실
│   ├── 00_CKA_EXAM_GUIDE.md                  # 시험 개요, 5대 도메인 비중 및 3단계 합격 로드맵
│   ├── 01_GLOSSARY_KR_EN.md                  # [핵심] 쿠버네티스 필수 한·영 용어사전
│   ├── 02_DOMAIN_1_CLUSTER_ARCHITECTURE.md   # 도메인 1: 아키텍처, 설치 및 구성 (25%)
│   ├── 03_DOMAIN_2_WORKLOADS_SCHEDULING.md   # 도메인 2: 워크로드 및 스케줄링 (15%)
│   ├── 04_DOMAIN_3_SERVICES_NETWORKING.md    # 도메인 3: 서비스 및 네트워킹 (20%)
│   ├── 05_DOMAIN_4_STORAGE.md                # 도메인 4: 스토리지 (10%)
│   ├── 06_DOMAIN_5_TROUBLESHOOTING.md        # 도메인 5: 문제 해결 및 장애 진단 (30%)
│   └── 07_KUBECTL_CHEAT_SHEET.md             # 실전 합격 kubectl 명령형 커맨드 치트시트
│
├── questions/                                 # 📝 실전 수준 문제은행 (JSON 포맷)
│   ├── questions_domain1.json                # 도메인 1 전용 문제 & 상세 한국어 해설
│   ├── questions_domain2.json                # 도메인 2 전용 문제 & 상세 한국어 해설
│   ├── questions_domain3.json                # 도메인 3 전용 문제 & 상세 한국어 해설
│   ├── questions_domain4.json                # 도메인 4 전용 문제 & 상세 한국어 해설
│   ├── questions_domain5.json                # 도메인 5 전용 문제 & 상세 한국어 해설
│   └── mock_exam_1.json                      # 전 도메인 통합 실전 모의고사 세트 (20문항)
│
├── cbt-app/                                   # 💻 실전 CBT 가상 실습 웹 애플리케이션
│   ├── index.html                            # CBT 웹앱 메인 화면
│   ├── app.js                                # CBT 엔진 (타이머, 채점, 모드 전환, 오답노트)
│   ├── style.css                             # 쿠버네티스 공식 스타일 테마 & 반응형 UI
│   └── questions-data.js                     # 브라우저 즉시 구동용 문제 데이터 번들
│
├── data/                                      # 💾 시험 기록 및 통계 저장소
│   └── history.json                          # 모의고사 제출 결과 누적 JSON
│
├── index.html                                 # 🌐 메인 통합 학습 포털
├── portal.css                                 # 포털 테마 스타일시트
├── portal.js                                  # 포털 제어 로직 (탭 네비게이션, 검색, API 연동)
├── portal-docs-data.js                        # 오프라인/정적 서빙 대비 마크다운 번들
├── questions-data.js                          # 루트 레벨 문제 번들
├── server.py                                  # Python 3 내장 경량 HTTP 백엔드 (Port: 8080)
├── run.sh                                     # 원클릭 실행 쉘 스크립트
└── README.md                                  # 프로젝트 안내 문서
```

---

## 🎯 핵심 학습 전략 (한·영 듀얼 트랙 & 실전 팁)

실제 시험은 **100% 영문 환경**의 리눅스 터미널에서 진행되며, 복잡한 공식 매니페스트를 손으로 치다가는 시간이 절대적으로 부족합니다.

1. **이론 및 용어 정립**:
   * [`docs/01_GLOSSARY_KR_EN.md`](file:///Users/sungkyu/Study/K8S/docs/01_GLOSSARY_KR_EN.md)에서 영문 용어와 한국어 개념을 먼저 매핑합니다.
   * [`docs/02` ~ `06`](file:///Users/sungkyu/Study/K8S/docs/02_DOMAIN_1_CLUSTER_ARCHITECTURE.md) 도메인별 핵심 요약 노트에서 아키텍처 원리를 완벽히 이해합니다.
   * [`docs/07_KUBECTL_CHEAT_SHEET.md`](file:///Users/sungkyu/Study/K8S/docs/07_KUBECTL_CHEAT_SHEET.md)의 `$do` (`--dry-run=client -o yaml`) 명령을 손에 익힙니다.

2. **CBT 실습 시**:
   * **1단계 (학습 모드 - Study Mode)**:
     * 영문 지문을 먼저 읽어보고, 이해가 안 될 땐 **[🌐 한국어 번역 보기]** 버튼을 눌러 확인합니다.
     * 문제를 푼 직후 **[정답 확인]**을 눌러 왜 정답인지, 왜 오답인지 상세한 한국어 해설을 습득합니다.
   * **2단계 (실전 모드 - Exam Mode)**:
     * 실전 시험 환경과 동일하게 120분 타이머 카운트다운을 켜고, 영문 지문 위주로 신속하게 문제를 풉니다.
     * 아리송한 문제는 **[🚩 나중에 검토(Flag)]**로 표시해두고 마지막에 재검토합니다.
   * **3단계 (결과 분석 & 오답 노트)**:
     * 제출 후 **도메인별 성취도(%)**를 확인하여 취약한 도메인을 파악합니다 (합격 기준: 66% 이상).
     * **[틀린 문제만 오답노트 복습]** 버튼을 눌러 틀린 문제만 다시 풀며 완벽히 숙지합니다.
