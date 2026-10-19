# 도메인 3: 서비스 및 네트워킹 (Services & Networking)

> **출제 비중**: **20%**  
> **핵심 키워드**: ClusterIP, NodePort, Ingress 라우팅 규칙, CoreDNS 서비스 디스커버리, NetworkPolicy 격리 및 트래픽 제어

---

## 1. 쿠버네티스 서비스 (Services) 핵심 포트 체계

서비스는 동적으로 생성/소멸하는 파드들의 가변적인 IP를 추상화하여 고정 가상 IP(VIP)를 제공합니다.

### 1.1 세 가지 포트 개념 완벽 구별
* **`port`**: 클러스터 내부의 다른 파드가 **Service IP로 접근할 때 사용하는 포트**.
* **`targetPort`**: 실제 백엔드 **파드(컨테이너) 내부에서 리스닝하고 있는 포트**.
* **`nodePort`**: NodePort 서비스 사용 시 외부 클라이언트가 **각 워커 노드의 실제 IP로 접근할 포트** (범위: 30000~32767).

### ⚡ 실전 명령어 (CLI 빠른 생성)
```bash
# 디플로이먼트를 포트 80(타겟 80)으로 클러스터 내부 노출 (ClusterIP)
kubectl expose deployment my-deploy --port=80 --target-port=80 --name=my-svc

# NodePort 타입으로 노출
kubectl expose deployment my-deploy --type=NodePort --port=80 --target-port=80 --name=my-nodeport-svc
```

---

## 2. 인그레스 (Ingress) 라우팅 규칙

Ingress는 클러스터 외부의 HTTP/HTTPS 트래픽을 내부 서비스로 라우팅하는 L7 규칙입니다.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

---

## 3. CoreDNS 및 서비스 디스커버리 (DNS Resolution)

쿠버네티스 내부 DNS는 다음 정규 FQDN(Fully Qualified Domain Name)을 생성합니다:
```
<service-name>.<namespace>.svc.cluster.local
```
* **동일 네임스페이스 내 통신**: 서비스 이름(`http://web-service`)만으로 즉시 해석 가능.
* **다른 네임스페이스 통신**: `<service-name>.<namespace>` (예: `http://api-service.backend`)로 접근.

---

## 4. 네트워크 정책 (NetworkPolicy) 트래픽 통제

> **주의**: NetworkPolicy는 클러스터에 Calico, Cilium, WeaveNet 등 네트워크 정책을 지원하는 **CNI 플러그인이 설치되어 있어야 실제로 적용**됩니다.

### 4.1 기본 완전 차단 정책 (Default Deny All Ingress)
특정 네임스페이스 내의 모든 인입 트래픽을 차단하여 화이트리스트 방식으로 운영하고자 할 때:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: prod
spec:
  podSelector: {} # 네임스페이스 내 모든 파드 대상
  policyTypes:
  - Ingress
```

### 4.2 특정 라벨을 가진 파드에서만 인입 허용
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-db
  namespace: prod
spec:
  podSelector:
    matchLabels:
      app: database # 정책 적용 대상 (DB 파드)
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend # frontend 파드만 접근 허용
    ports:
    - protocol: TCP
      port: 5432
```
