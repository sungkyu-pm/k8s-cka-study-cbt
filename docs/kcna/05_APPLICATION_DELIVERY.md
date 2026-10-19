# 영역 5: 애플리케이션 전달 & GitOps (Application Delivery - 8%)

> 클라우드 네이티브 환경에서 애플리케이션을 안전하고 신속하게 배포하기 위한 CI/CD 현대화 원칙, GitOps 아키텍처(Argo CD / Flux), 헬름(Helm) 패키징 및 공급망 보안

---

## 1. CI/CD 파이프라인 현대화

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MODERN CLOUD NATIVE CI/CD                       │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Continuous Integration (CI) : 코드 커밋 -> 테스트 -> OCI 이미지 빌드 │
│ 2. Security Scanning          : Trivy 취약점 점검 -> Cosign 서명       │
│ 3. Artifact Registry           : OCI Artifacts / Helm 차트 레지스트리 보관 │
│ 4. Continuous Delivery (CD)   : GitOps Controller에 의한 클러스터 동기화│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. GitOps 원칙 및 아키텍처

GitOps는 **Git 저장소를 전체 시스템의 "단일 진실 공급원(Single Source of Truth)"**으로 삼아 인프라와 애플리케이션 배포를 선언적으로 관리하는 운영 모델입니다:

```
[ Developer ] ──(git push)──► [ Git Repository ] ◄──(Pull & Reconcile)── [ GitOps Operator ]
                                (Manifests/Helm)                         (Argo CD / Flux)
                                                                                │
                                                                         (동기화 / Diff 반영)
                                                                                ▼
                                                                        [ K8s Cluster ]
```

### GitOps의 4대 핵심 원칙 (OpenGitOps 표준)
1. **선언적(Declarative)**: 시스템의 원하는 상태는 선언적 방식으로 표현되어야 함.
2. **버전 관리 및 불변(Versioned and Immutable)**: 원하는 상태는 Git에 저장되며 모든 변경 이력이 영구 보존됨.
3. **자동화된 풀링(Pulled Automatically)**: 클러스터 내부의 소프트웨어 에이전트가 Git의 선언된 상태를 자동으로 풀링(Pull).
4. **지속적 조정(Continuously Reconciled)**: 실제 클러스터 상태와 Git 상태 사이의 드리프트(Drift)를 실시간 감지하여 자동 일치시킴.

### 대표 GitOps 도구
- **Argo CD** (CNCF Graduated):
  - 시각적 웹 UI와 풍부한 권한 관리를 제공하는 선언적 쿠버네티스 GitOps 도구.
- **Flux** (CNCF Graduated):
  - 경량화된 여러 독립 컨트롤러(Source, Kustomize, Helm, Notification)로 구성된 유연한 GitOps 툴킷.

---

## 3. 쿠버네티스 패키지 관리: 헬름 (Helm)

**Helm**은 쿠버네티스의 "apt" 또는 "yum"과 같은 패키지 매니저로, 복잡한 쿠버네티스 매니페스트들을 단일 단위(차트, Chart)로 패키징하고 배포 및 롤백할 수 있게 지원합니다.

### 차트(Chart) 디렉토리 핵심 구조
```
my-chart/
├── Chart.yaml       # 차트 메타데이터 (이름, 버전, 설명, 의존성)
├── values.yaml      # 템플릿에 주입할 기본 설정값 (사용자가 오버라이드 가능)
├── templates/       # Go 템플릿 문법으로 작성된 K8s YAML 파일들
│   ├── deployment.yaml
│   ├── service.yaml
│   └── _helpers.tpl
└── charts/          # 하위 종속 차트들
```

- **Release (릴리즈)**: Helm 차트가 특정 클러스터에 배포되어 실행 중인 인스턴스.
- **Rollback (롤백)**: 문제 발생 시 `helm rollback <release> <revision>` 명령어로 즉각 이전 상태로 복구.

---

## 4. 컨테이너 공급망 보안 (Supply Chain Security)

1. **Harbor** (CNCF Graduated):
   - 기업용 오픈소스 신뢰할 수 있는 클라우드 네이티브 레지스트리.
   - 역할 기반 접근 제어(RBAC), 이미지 복제, 취약점 스캐닝 내장.
2. **취약점 스캐너 (Vulnerability Scanning)**:
   - **Trivy**: 컨테이너 OS 패키지 및 애플리케이션 종속성(CVE)의 보안 결함을 탐지.
3. **디지털 서명 및 검증 (Image Signing)**:
   - **Cosign (Sigstore)** / **Notary**: 배포 전 이미지가 변조되지 않았음을 암호화 서명으로 증명하고 Admission Controller(Kyverno, OPA Gatekeeper)에서 검증.

## 5.5 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)

이 섹션은 CBT 문제 은행(**questions_kcna_domain5.json 30문항**)의 모든 핵심 개념(`key_concept`), 정답 해설 및 빈출 함정 키워드와 1:1로 일치하도록 정리된 요약본입니다.

| 출제 핵심 개념 (Key Concept) | 공식 출제 의도 및 GitOps/배포 표준 | CBT 대표 오답 함정 & 판별 포인트 |
| :--- | :--- | :--- |
| **GitOps 핵심 원칙** | • **단일 진실의 원천 (Single Source of Truth)**: Git 저장소가 전체 시스템의 원하는 상태(Desired State)를 보관<br>• 선언적 명세, 자동 동기화, 드리프트(Drift) 자동 감지 및 치유 | • 개발자가 클러스터 터미널에 직접 `kubectl apply`를 실행하는 것은 GitOps 원칙에 위배됨. 모든 변경은 Git PR을 통해 수행. |
| **GitOps 대표 도구** | • **Argo CD**: 쿠버네티스 전용 선언적 GitOps CD 도구 (웹 UI, Application CRD)<br>• **Flux**: 모듈식 GitOps 툴킷 | • Jenkins나 GitLab CI는 주로 CI(빌드/테스트) 단계에 사용되며, 클러스터 내부 동기화는 Argo CD/Flux가 담당. |
| **Helm 차트 표준 구조** | • `Chart.yaml`: 차트 메타데이터 (이름, 버전)<br>• `values.yaml`: 기본 설정 값 정의<br>• `templates/`: 매니페스트 템플릿 디렉토리 | • Helm은 쿠버네티스의 패키지 관리자로, 템플릿과 값을 결합하여 릴리스(Release)를 배포하고 손쉬운 롤백 지원. |
| **Harbor & Trivy 보안** | • **Harbor**: CNCF 졸업 오픈소스 프라이빗 컨테이너 레지스트리 (RBAC, 이미지 복제)<br>• **Trivy**: 취약점 스캐너 (CVE 취약점 및 설정 오류 사전 차단) | • 빌드된 컨테이너 이미지를 배포하기 전에 취약점 스캔을 통과해야 배포되도록 파이프라인 구성. |
