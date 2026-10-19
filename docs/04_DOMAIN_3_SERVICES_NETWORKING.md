# 도메인 3: 서비스 및 네트워킹 심층 가이드 (Services & Networking)

> **출제 비중**: **20%**  
> **핵심 세부 영역**: 4대 Service 타입 및 포트 매핑, Endpoints/EndpointSlice, Ingress(PathType, Rewrite, TLS), CoreDNS FQDN 해석, NetworkPolicy(AND/OR 조건, CIDR except)

---

## 3.1 서비스(Service) 4대 타입 및 포트 체계

쿠버네티스 파드는 언제든 생성·종료되면서 IP가 유동적으로 변합니다. 서비스는 이러한 파드들의 앞단에서 **고정 가상 IP(VIP)**를 제공하고 L4 로드밸런싱을 수행합니다.

### 1. 3가지 포트 개념 완벽 구별
```
[외부 클라이언트]
       │
       ▼ (NodePort: 30080)
 [워커 노드 물리 IP]
       │
       ▼ (port: 80)
 [쿠버네티스 Service VIP]
       │
       ▼ (targetPort: 8080)
 [파드 내부 컨테이너]
```
* **`port`**: 클러스터 내부의 다른 파드가 Service VIP로 요청할 때 사용하는 포트.
* **`targetPort`**: 백엔드 파드 내부 컨테이너에서 실제 리스닝 중인 포트.
* **`nodePort`**: 외부 사용자가 워커 노드 IP를 통해 직접 접근하는 포트 (범위: 30000~32767).

### 2. 4대 서비스 타입 비교
| 타입 | 용도 및 특징 | 실무 시나리오 |
| :--- | :--- | :--- |
| **ClusterIP** | 클러스터 내부 통신 전용 가상 IP 할당 (기본값) | 백엔드 API, 데이터베이스 등 내부 통신 |
| **NodePort** | 모든 노드의 특정 포트를 개방하여 외부 트래픽 수신 | 사설 온프레미스 노출, 개발/테스트 환경 |
| **LoadBalancer** | 클라우드 공급업체의 L4 외부 로드밸런서 자동 연동 | 퍼블릭 웹 서비스의 대외 프로덕션 노출 |
| **ExternalName** | 클러스터 내부 DNS에 외부 CNAME 레코드 매핑 | 외부 레거시 DB나 SaaS 도메인 연동 |

---

## 3.2 Endpoints 및 EndpointSlice 아키텍처

### 1. 셀렉터 없는 서비스와 수동 엔드포인트 연결
외부 데이터베이스를 쿠버네티스 내부 서비스로 래핑할 때 사용합니다:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  ports:
  - port: 3306
    targetPort: 3306
---
apiVersion: v1
kind: Endpoints
metadata:
  name: external-db   # 서비스 이름과 100% 동일해야 함!
subsets:
- addresses:
  - ip: 192.168.1.100 # 외부 물리 DB 서버 IP
  ports:
  - port: 3306
```

---

## 3.3 Ingress 및 Ingress Controller 심층 가이드

Ingress는 단일 외부 진입점(보통 80/443)을 통해 경로(Path)나 도메인(Host)에 따라 여러 내부 Service로 HTTP/HTTPS 트래픽을 분기하는 L7 규칙입니다.

### 1. 프로덕션 Ingress 매니페스트 (Rewrite 및 TLS 포함)
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: main-ingress
  namespace: prod
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2 # 하위 경로를 루트로 재작성
spec:
  ingressClassName: nginx                          # 인그레스 컨트롤러 지정
  tls:
  - hosts:
    - api.company.com
    secretName: company-tls-secret                 # TLS 인증서 시크릿
  rules:
  - host: api.company.com
    http:
      paths:
      - path: /order(/|$)(.*)
        pathType: ImplementationSpecific
        backend:
          service:
            name: order-service
            port:
              number: 8080
      - path: /user(/|$)(.*)
        pathType: ImplementationSpecific
        backend:
          service:
            name: user-service
            port:
              number: 8081
```

---

## 3.4 CoreDNS 서비스 디스커버리 및 FQDN 체계

쿠버네티스 내부 DNS는 클러스터 내 모든 서비스와 파드에 고유 FQDN을 부여합니다:

```
<서비스이름>.<네임스페이스>.svc.cluster.local
```
* **동일 네임스페이스 통신**: `http://order-service:8080`
* **타 네임스페이스 통신**: `http://order-service.prod:8080`
* **파드 직접 접근 FQDN**: `10-244-1-25.prod.pod.cluster.local`

---

## 3.5 NetworkPolicy 트래픽 방화벽 규칙 (심층 문법)

> **주의**: NetworkPolicy는 Calico, Cilium 등 정책 지원 CNI가 설치되어 있어야 효력이 발생합니다.

### 1. 기본 인입 완전 차단 (Default Deny All Ingress)
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: prod
spec:
  podSelector: {} # prod 네임스페이스 내 모든 파드 대상
  policyTypes:
  - Ingress
```

### 2. AND 조건 vs OR 조건 구별 (CKA 100% 빈출 함정)
* **논리적 AND (교집합)**: `namespaceSelector`와 `podSelector`가 **동일 중괄호 블록**에 위치
```yaml
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          env: prod
      podSelector:       # env=prod 네임스페이스 '안에 속하면서'
        matchLabels:
          app: frontend  # app=frontend 라벨을 가진 파드만 허용 (AND)
```
* **논리적 OR (합집합)**: 각각 **별도의 하이픈(-) 항목**으로 분리
```yaml
  ingress:
  - from:
    - namespaceSelector: # env=prod 네임스페이스의 '모든 파드' (OR)
        matchLabels:
          env: prod
    - podSelector:       # '어느 네임스페이스든' app=frontend 라벨을 가진 파드 (OR)
        matchLabels:
          app: frontend
```

### 3. IP 블록(CIDR) 및 예외(`except`) 허용 규칙
```yaml
  ingress:
  - from:
    - ipBlock:
        cidr: 192.168.0.0/16
        except:
        - 192.168.1.50/32 # 특정 단일 IP는 차단
    ports:
    - protocol: TCP
      port: 80
```

## 3.5 🎯 실전 CBT 문제 은행 핵심 출제 포인트 & 해설 매핑 (Questions & Key Concepts)

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
