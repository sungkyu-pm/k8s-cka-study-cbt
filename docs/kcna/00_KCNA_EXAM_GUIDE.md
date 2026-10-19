# KCNA (Kubernetes and Cloud Native Associate) 공식 시험 안내 및 종합 전략 가이드

> **CNCF (Cloud Native Computing Foundation) & Linux Foundation 공인 인증**  
> 클라우드 네이티브 아키텍처, 쿠버네티스 핵심 원리, 컨테이너 오케스트레이션 및 GitOps/관측 가능성의 기초를 검증하는 글로벌 공인 자격증

---

## 1. KCNA vs CKA 핵심 비교 매트릭스

| 비교 항목 | KCNA (Associate) | CKA (Administrator) |
| :--- | :--- | :--- |
| **시험 성격** | **필기 객관식 (Multiple Choice, 4지선다)** | **100% 핸즈온 실기 (Live Cluster Terminal)** |
| **시험 시간** | **90분** | **120분** |
| **문항 수** | **60문항** | **15 ~ 20문항 (시나리오별 실습)** |
| **합격 기준** | **75% 이상 (45문항 이상 정답)** | **66% 이상** |
| **시험 범위** | 쿠버네티스 원리 + CNCF 에코시스템 전반 (12-Factor, OCI, CRI/CNI/CSI, Prometheus, GitOps) | 쿠버네티스 클러스터 구축, 운영, 트러블슈팅, 보안, 스토리지 실무 조작 |
| **응시 환경** | 온라인 감독관(PSI) 원격 모니터링 | 온라인 감독관(PSI) 원격 터미널 환경 |
| **유효 기간** | 3년 (재응시 또는 상위 자격 취득) | 3년 |
| **추천 대상** | 클라우드 엔지니어, DevOps 입문자, 솔루션 아키텍트, 백엔드 개발자 | K8s 클러스터 운영자, 인프라 엔지니어, 플랫폼 SRE |

---

## 2. 공식 시험 출제 영역 및 가중치 (Exam Curriculum)

```
┌────────────────────────────────────────────────────────────────────────┐
│                   KCNA Official Domain Breakdown                       │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Kubernetes Fundamentals (쿠버네티스 기본 원리)          : 46% (약 28문항) │
│ 2. Container Orchestration (컨테이너 오케스트레이션)       : 22% (약 13문항) │
│ 3. Cloud Native Architecture (클라우드 네이티브 아키텍처)   : 16% (약 10문항) │
│ 4. Cloud Native Observability (관측 가능성 및 모니터링)     :  8% (약  5문항) │
│ 5. Application Delivery & GitOps (애플리케이션 배포)        :  8% (약  5문항) │
└────────────────────────────────────────────────────────────────────────┘
```

### 세부 출제 체크리스트

#### 영역 1: 쿠버네티스 기본 원리 (Kubernetes Fundamentals - 46%)
- [ ] **Kubernetes 리소스 모델**: Pod, ReplicaSet, Deployment, StatefulSet, DaemonSet, Job, CronJob의 용도와 차이점.
- [ ] **쿠버네티스 아키텍처**:
  - Control Plane 구성요소: `kube-apiserver` (중앙 게이트웨이), `etcd` (분산 일관성 키-값 저장소), `kube-scheduler` (노드 배치), `kube-controller-manager` (루프 제어).
  - Worker Node 구성요소: `kubelet` (파드 생명주기 관리), `kube-proxy` (IP 테이블/IPVS 네트워크 룰 반영), `Container Runtime` (컨테이너 실행).
- [ ] **네트워킹 모델**: Pod-to-Pod 통신, Service 유형 (ClusterIP, NodePort, LoadBalancer, Headless), Ingress Controller, DNS 이름 규칙.
- [ ] **스토리지 추상화**: Volume, PersistentVolume (PV), PersistentVolumeClaim (PVC), StorageClass (동적 프로비저닝).
- [ ] **보안 및 접근 제어**: RBAC (Role, ClusterRole, RoleBinding, ClusterRoleBinding), ServiceAccount, SecurityContext (runAsUser, capabilities).

#### 영역 2: 컨테이너 오케스트레이션 (Container Orchestration - 22%)
- [ ] **오케스트레이션 개념**: 선언적 구성(Declarative) vs 명령형(Imperative), 자가 치유(Self-healing), 스케일링(HPA/VPA), 롤링 업데이트.
- [ ] **표준 인터페이스 규격**:
  - **CRI (Container Runtime Interface)**: containerd, CRI-O. (도커 쉼 폐지 및 OCI 표준).
  - **CNI (Container Network Interface)**: Flannel, Calico, Cilium.
  - **CSI (Container Storage Interface)**: 클라우드 블록/파일 스토리지 플러그인.
- [ ] **컨테이너 보안 격리**: Linux Namespaces (PID, Mount, Net, IPC, UTS), cgroups (CPU, Memory 리소스 제약), seccomp, AppArmor.

#### 영역 3: 클라우드 네이티브 아키텍처 (Cloud Native Architecture - 16%)
- [ ] **CNCF 정의**: 확장 가능(Scalable), 회복 탄력성(Resilient), 관리 가능(Manageable), 관찰 가능(Observable)한 시스템.
- [ ] **12-Factor App 방법론**: 설정 분리(Config), 무상태 프로세스(Stateless processes), 포트 바인딩(Port binding), 동시성(Concurrency), 폐기 가능성(Disposability).
- [ ] **마이크로서비스 vs 모놀리스**: 결합도, 장애 격리, 서비스 디스커버리, API 게이트웨이, 서킷 브레이커.
- [ ] **서버리스 & 이벤트 주도 아키텍처**: Knative, 이벤트 트리거, 콜드 스타트, FaaS(Function-as-a-Service).
- [ ] **CNCF Landscape 단계**: Sandbox -> Incubating -> Graduated (성숙도 모델 기준).

#### 영역 4: 관측 가능성 (Cloud Native Observability - 8%)
- [ ] **3대 기둥 (The Three Pillars)**: Metrics (측정치), Logs (이벤트 기록), Traces (분산 요청 흐름).
- [ ] **Prometheus 에코시스템**: 시계열 DB(TSDB), Pull 방식 수집, PromQL, Alertmanager, Exporter.
- [ ] **로깅 시스템**: Fluentd, Fluent Bit, Grafana Loki.
- [ ] **분산 추적(Distributed Tracing)**: Jaeger, OpenTelemetry (OTel), Span과 Trace ID 개념.
- [ ] **대시보드 시각화**: Grafana.

#### 영역 5: 애플리케이션 전달 & GitOps (Application Delivery - 8%)
- [ ] **CI/CD 파이프라인**: 지속적 통합과 지속적 배포의 개념 및 피드백 루프.
- [ ] **GitOps 원칙**:
  - Git을 단일 진실 공급원(Single Source of Truth)으로 사용.
  - 선언적 시스템 설명(Declarative description).
  - 자동화된 동기화(Pull-based Reconcile loop)와 드리프트 감지.
  - GitOps 대표 도구: Argo CD, Flux.
- [ ] **패키지 관리**: Helm (Chart.yaml, values.yaml, templates), Kustomize (오버레이 기반 무템플릿 관리).
- [ ] **컨테이너 레지스트리 및 공급망 보안**: Harbor, OCI Artifacts, 이미지 취약점 스캐닝 (Trivy), 이미지 서명 (Cosign).

---

## 3. 합격 실전 팁 (Exam Tips)

1. **시간 관리**:
   - 90분에 60문항이므로, 1문항당 평균 **1분 30초**가 주어집니다.
   - 객관식이므로 모르는 문제는 Flag 표시해두고 바로 다음 문제로 넘어가며, 1차 완주 후 남은 시간(약 20~25분)에 재검토합니다.
2. **CNCF Graduated 프로젝트 위주 암기**:
   - Kubernetes, Prometheus, Envoy, containerd, CoreDNS, Fluentd, Jaeger, Harbor, Helm, Argo CD, Open Policy Agent (OPA), TiKV, Vitess 등 Graduated 단계 프로젝트들의 역할과 성격을 명확히 구별해야 합니다.
3. **CRI / CNI / CSI 약어와 역할 구별**:
   - 런타임(CRI), 네트워크(CNI), 스토리지(CSI)의 추상화 계층 및 대표 구현체(Calico, containerd, Rook-Ceph)를 묻는 문제가 자주 출제됩니다.
4. **합격 기준**:
   - 60문제 중 45문제(75%) 이상을 득점해야 합격하므로, 배점이 46%로 가장 높은 `Kubernetes Fundamentals` 영역을 완벽히 마스터하는 것이 핵심입니다.
