# 영역 4: 관측 가능성 및 모니터링 (Cloud Native Observability - 8%)

> 분산 클라우드 네이티브 환경에서 시스템 내부 상태를 파악하기 위한 관측 가능성의 3대 기둥(Metrics, Logs, Traces)과 CNCF 오픈소스 모니터링 생태계

---

## 1. 관측 가능성의 3대 기둥 (The Three Pillars of Observability)

```
                       ┌─────────────────────────────────────────┐
                       │          OBSERVABILITY PILLARS          │
                       └────────────────────┬────────────────────┘
                                            │
         ┌──────────────────────────────────┼──────────────────────────────────┐
         ▼                                  ▼                                  ▼
┌──────────────────┐               ┌──────────────────┐               ┌──────────────────┐
│  Metrics (메트릭) │               │   Logs (로그)    │               │  Traces (추적)   │
├──────────────────┤               ├──────────────────┤               ├──────────────────┤
│ 수치형 시계열 집계  │               │ 타임스탬프 이벤트  │               │ 분산 요청의 전 구간│
│ CPU/메모리, RPS, │               │ 상세 컨텍스트 기록 │               │ 지연 시간 및 호출선│
│ Prometheus, PromQL│               │ Fluentd, Loki    │               │ Jaeger, OTel     │
└──────────────────┘               └──────────────────┘               └──────────────────┘
```

| 기둥 | 성격 | 주요 용도 | 대표 오픈소스 도구 |
| :--- | :--- | :--- | :--- |
| **Metrics (메트릭)** | 시간의 흐름에 따른 수치 데이터(측정값)의 집계 | 실시간 모니터링, 알림(Alerting), 트렌드 분석, 자동 확장(HPA) | **Prometheus**, Thanos, Cortex, VictoriaMetrics |
| **Logs (로그)** | 특정 시점에 발생한 이벤트에 대한 텍스트/JSON 기록 | 장애 발생 시 근본 원인(Root Cause) 상세 디버깅 및 감사(Audit) | **Fluentd**, Fluent Bit, Grafana Loki |
| **Traces (분산 추적)** | 마이크로서비스 간에 전파되는 단일 사용자 요청의 흐름 추적 | 분산 시스템 병목 구간 식별 및 엔드투엔드(End-to-End) 지연 분석 | **Jaeger**, Zipkin, **OpenTelemetry** |

---

## 2. 프로메테우스 (Prometheus) 아키텍처 및 핵심 원리

Prometheus는 CNCF의 2번째 정식 졸업(Graduated) 프로젝트로, 사실상의 클라우드 네이티브 메트릭 표준입니다:

```
[ Application / Pods ] ──(HTTP GET /metrics)──► [ Prometheus Server ] ──► [ Alertmanager ] ──► Slack/Email
                                                       │
                                                (PromQL 쿼리)
                                                       │
                                                       ▼
                                                [ Grafana Dashboard ]
```

### 핵심 특징
1. **Pull 기반 수집 모델**:
   - 프로메테우스 서버가 주기적(`scrape_interval: 15s`)으로 대상 엔드포인트(`http://target:9090/metrics`)에 HTTP GET 요청을 보내 메트릭을 수집(Scrape).
   - *Push가 필요한 배치 작업*을 위해 보조적으로 **Pushgateway**를 지원.
2. **다차원 데이터 모델**:
   - `metric_name{label1="value1", label2="value2"} value [timestamp]`
   - 레이블(Labels)을 통한 정밀한 필터링 및 집계 지원.
3. **PromQL (Prometheus Query Language)**:
   - 시계열 데이터를 실시간으로 조회하고 계산하기 위한 강력한 쿼리 언어 (예: `rate(http_requests_total[5m])`).
4. **Alertmanager**:
   - PromQL 룰에 따라 발생한 경고(Alert)를 수신하여 중복 제거, 그룹화, 라우팅(슬랙, 페이저듀티, 이메일) 처리.

---

## 3. 분산 추적 (Distributed Tracing) & OpenTelemetry (OTel)

### 1) 분산 추적의 핵심 개념
- **Trace**: 하나의 외부 요청이 시작되어 완료될 때까지 여러 마이크로서비스를 거쳐 처리되는 전체 트랜잭션의 DAG(방향성 비순환 그래프).
- **Span**: 단일 서비스나 컴포넌트 내에서 수행된 작업 단위.
  - 고유한 `Span ID`, 시작/종료 시간, 부모 Span ID(`Parent Span ID`), 태그/이벤트 포함.
- **Trace Context**: 서비스 간 HTTP 헤더(예: `traceparent`)를 통해 Trace ID를 전파하여 분산된 스팬들을 하나로 연결.

### 2) CNCF OpenTelemetry (OTel)
- 분산 추적 표준(OpenTracing)과 메트릭 수집 표준(OpenMetrics/OpenCensus)을 하나로 통합한 CNCF의 차세대 핵심 프로젝트.
- **언어 독립적인 API, SDK, 툴링**을 제공하며, 수집된 데이터를 OTLP(OpenTelemetry Protocol) 프로토콜로 백엔드(Jaeger, Prometheus, Datadog 등)에 전송.

---

## 4. 로깅 생태계 (Fluentd vs Fluent Bit vs Loki)

- **Fluentd** (CNCF Graduated):
  - 루비와 C로 작성된 풍부한 플러그인 생태계를 갖춘 로그 수집기 및 변환기.
- **Fluent Bit** (CNCF Graduated):
  - C언어로 작성된 초경량(수 MB 메모리 점유) 고성능 로그 포워더. 쿠버네티스 노드의 DaemonSet으로 널리 배포됨.
- **Grafana Loki**:
  - 로그 본문을 전체 인덱싱하지 않고, 레이블(Labels) 메타데이터만 인덱싱하여 스토리지 비용과 메모리를 극적으로 절감하는 클라우드 네이티브 로깅 솔루션.

## 4.5 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)

이 섹션은 CBT 문제 은행(**questions_kcna_domain4.json 30문항**)의 모든 핵심 개념(`key_concept`), 정답 해설 및 빈출 함정 키워드와 1:1로 일치하도록 정리된 요약본입니다.

| 출제 핵심 개념 (Key Concept) | 공식 출제 의도 및 모니터링 표준 | CBT 대표 오답 함정 & 판별 포인트 |
| :--- | :--- | :--- |
| **관측 가능성 3대 기둥** | • **Metrics**: 시계열 수치 데이터 (CPU, Memory, 요청 수)<br>• **Logs**: 타임스탬프가 찍힌 이벤트 텍스트 기록<br>• **Traces**: 분산 서비스 간 요청의 엔드투엔드 여정 추적 | • 메트릭만으로는 특정 에러의 근본 원인을 파악하기 어려우며, 3대 요소를 상호 연계해야 완전한 관측 가능성 달성. |
| **Prometheus 풀 모델** | 대상 엔드포인트(`/metrics`)를 일정한 주기(scrape_interval)로 직접 HTTP GET 요청하여 메트릭을 당겨오는(Pull) 아키텍처 | • 에이전트가 중앙 서버로 능동 전송하는 Push 방식이 아니라 서버가 대상을 Pull하는 방식임 (Pushgateway는 배치 작업 예외용). |
| **OpenTelemetry (OTel)** | 분산 시스템에서 메트릭, 로그, 트레이스를 생성, 수집, 내보내기 위한 벤더 중립적 오픈소스 표준 프레임워크 | • 특정 시각화 백엔드(Datadog, Jaeger 등)에 종속되지 않고 OTel Collector를 통해 다중 백엔드로 전송 가능. |
| **Jaeger 분산 추적** | 마이크로서비스 간의 트랜잭션 호출 흐름, 병목 지점 및 지연 시간(Latency)을 Span과 Trace 단위로 시각화 | • 단일 서버 로그만으로는 마이크로서비스 간 호출 지연 원인을 찾을 수 없으므로 Jaeger 분산 추적이 필수적임. |
