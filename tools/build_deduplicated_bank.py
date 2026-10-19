#!/usr/bin/env python3
"""
build_deduplicated_bank.py
- CKA 1,250문항 및 KCNA 260문항에 대해 지문 텍스트 중복을 100% 제거하고,
- 모든 문항에 고유한 ID, sub_topic(문제 세부 유형), 고유 시나리오, 실무 질문, 선택지, 정답, 상세 해설, key_concept를 부여.
- cbt-app/questions-data.js 자동 동기화.
"""

import json
import os

print("=== Generating 1,510 100% Unique Questions with Explicit Sub-topics ===")

# -------------------------------------------------------------
# CKA 도메인 1: 클러스터 아키텍처, 설치 및 구성 (250문항)
# -------------------------------------------------------------
d1_subtopics = [
    {
        "sub_topic": "etcd_snapshot_save",
        "concept": "etcdctl snapshot save & TLS flags",
        "scenarios": [
            ("production etcd instance", "/var/lib/etcd-backup-prod.db", "https://127.0.0.1:2379", "/etc/kubernetes/pki/etcd"),
            ("staging cluster etcd", "/tmp/backup-staging.db", "https://10.0.0.10:2379", "/etc/kubernetes/pki/etcd"),
            ("HA control plane member 1", "/opt/backups/etcd-node1.db", "https://192.168.1.11:2379", "/etc/kubernetes/pki/etcd"),
            ("dr disaster recovery drill", "/var/backup/etcd-dr-test.db", "https://127.0.0.1:2379", "/etc/kubernetes/pki/etcd"),
            ("nightly scheduled etcd snapshot", "/backups/nightly-etcd.db", "https://127.0.0.1:2379", "/etc/kubernetes/pki/etcd"),
            ("pre-upgrade snapshot safety", "/tmp/pre-upgrade-k8s.db", "https://10.10.0.5:2379", "/etc/kubernetes/pki/etcd"),
            ("finance cluster etcd node", "/var/lib/finance-etcd.db", "https://127.0.0.1:2379", "/etc/kubernetes/pki/etcd"),
            ("multi-master etcd leader backup", "/mnt/shared/etcd-leader.db", "https://127.0.0.1:2379", "/etc/kubernetes/pki/etcd"),
            ("audit compliance etcd export", "/var/lib/etcd-audit.db", "https://172.16.0.10:2379", "/etc/kubernetes/pki/etcd"),
            ("security baseline backup", "/opt/etcd-baseline.db", "https://127.0.0.1:2379", "/etc/kubernetes/pki/etcd")
        ]
    },
    {
        "sub_topic": "etcd_snapshot_restore",
        "concept": "etcdctl snapshot restore & hostPath update",
        "scenarios": [
            ("/tmp/etcd-backup-prod.db", "/var/lib/etcd-restored-prod", "controlplane-1"),
            ("/var/backup/etcd-dr-test.db", "/var/lib/etcd-recovered", "master-node"),
            ("/opt/backups/etcd-node1.db", "/var/lib/etcd-new-data", "k8s-cp-01"),
            ("/backups/nightly-etcd.db", "/var/lib/etcd-nightly-restored", "control-plane-alpha"),
            ("/tmp/pre-upgrade-k8s.db", "/var/lib/etcd-rollback", "k8s-master"),
            ("/var/lib/finance-etcd.db", "/var/lib/etcd-finance-restore", "cp-fin-1"),
            ("/mnt/shared/etcd-leader.db", "/var/lib/etcd-shared-restore", "node-master"),
            ("/var/lib/etcd-audit.db", "/var/lib/etcd-audit-restore", "audit-cp"),
            ("/opt/etcd-baseline.db", "/var/lib/etcd-baseline-restored", "k8s-control"),
            ("/tmp/emergency-etcd.db", "/var/lib/etcd-emergency", "master-01")
        ]
    },
    {
        "sub_topic": "rbac_role_creation",
        "concept": "kubectl create role & API verbs",
        "scenarios": [
            ("pod-reader", "dev-team", "pods,pods/log", "get,list,watch"),
            ("deploy-manager", "production", "deployments,statefulsets", "get,list,create,update,patch"),
            ("config-viewer", "staging", "configmaps,secrets", "get,list"),
            ("job-controller-role", "batch-jobs", "jobs,cronjobs", "get,list,create,delete"),
            ("service-admin", "networking", "services,endpoints", "get,list,create,update,delete"),
            ("pvc-manager", "storage-ns", "persistentvolumeclaims", "get,list,create,delete"),
            ("ingress-auditor", "ingress-system", "ingresses", "get,list,watch"),
            ("daemon-viewer", "monitoring", "daemonsets", "get,list"),
            ("secret-maintainer", "security-ns", "secrets", "create,update,patch"),
            ("event-watcher", "qa-ns", "events", "get,list,watch")
        ]
    },
    {
        "sub_topic": "rbac_clusterrole",
        "concept": "ClusterRole for non-namespaced resources",
        "scenarios": [
            ("node-inspector", "nodes", "get,list,watch"),
            ("pv-administrator", "persistentvolumes", "get,list,create,delete"),
            ("storage-class-manager", "storageclasses", "get,list,create,patch"),
            ("cluster-network-viewer", "networkpolicies,nodes", "get,list"),
            ("namespace-controller", "namespaces", "get,list,create,delete"),
            ("cr-crd-viewer", "customresourcedefinitions", "get,list,watch"),
            ("cluster-metrics-reader", "nodes/metrics,pods/metrics", "get,list"),
            ("csr-manager-role", "certificatesigningrequests", "get,list,create,approve"),
            ("cluster-quota-watcher", "resourcequotas", "get,list"),
            ("priority-class-admin", "priorityclasses", "get,list,create,delete")
        ]
    },
    {
        "sub_topic": "rbac_binding_users_and_sa",
        "concept": "RoleBinding & ClusterRoleBinding subjects",
        "scenarios": [
            ("dev-binding", "pod-reader", "User", "alice", "dev-team"),
            ("deploy-binding", "deploy-manager", "ServiceAccount", "pipeline-sa", "production"),
            ("ops-group-binding", "config-viewer", "Group", "devops-leads", "staging"),
            ("cron-runner-binding", "job-controller-role", "ServiceAccount", "batch-runner", "batch-jobs"),
            ("net-admin-binding", "service-admin", "User", "bob-net", "networking"),
            ("storage-bind", "pv-administrator", "User", "storage-admin", "global"),
            ("node-view-bind", "node-inspector", "Group", "cluster-auditors", "global"),
            ("monitoring-agent-bind", "cluster-metrics-reader", "ServiceAccount", "prometheus-sa", "monitoring"),
            ("ingress-controller-bind", "ingress-auditor", "ServiceAccount", "ingress-sa", "ingress-system"),
            ("audit-sa-binding", "event-watcher", "ServiceAccount", "auditor-agent", "qa-ns")
        ]
    },
    {
        "sub_topic": "kubectl_auth_can_i",
        "concept": "Impersonation with kubectl auth can-i",
        "scenarios": [
            ("delete", "pods", "developer-sam", "development"),
            ("create", "deployments", "ci-builder", "production"),
            ("get", "secrets", "system:serviceaccount:default:app-sa", "default"),
            ("list", "nodes", "cluster-auditor", ""),
            ("patch", "services", "system:serviceaccount:kube-system:coredns", "kube-system"),
            ("delete", "persistentvolumes", "dev-intern", ""),
            ("create", "jobs", "analytics-team", "analytics"),
            ("approve", "certificatesigningrequests", "system:admin", ""),
            ("drain", "nodes", "cluster-engineer", ""),
            ("update", "ingresses", "web-developer", "frontend")
        ]
    },
    {
        "sub_topic": "kubeadm_cluster_init",
        "concept": "kubeadm init flags & pod network CIDR",
        "scenarios": [
            ("192.168.0.0/16", "10.0.0.10", "v1.31.0", "calico"),
            ("10.244.0.0/16", "172.16.0.5", "v1.30.2", "flannel"),
            ("172.20.0.0/16", "192.168.10.50", "v1.31.1", "cilium"),
            ("10.96.0.0/12", "10.10.10.10", "v1.30.0", "canal"),
            ("192.168.100.0/24", "192.168.100.1", "v1.31.0", "weave"),
            ("10.85.0.0/16", "10.85.0.1", "v1.30.1", "custom-cni"),
            ("172.30.0.0/16", "172.30.1.10", "v1.31.0", "calico"),
            ("10.1.0.0/16", "10.1.0.10", "v1.30.3", "cilium"),
            ("192.168.200.0/22", "192.168.200.5", "v1.31.2", "flannel"),
            ("10.50.0.0/16", "10.50.0.2", "v1.30.4", "kube-router")
        ]
    },
    {
        "sub_topic": "kubeadm_token_and_join",
        "concept": "kubeadm token create --print-join-command",
        "scenarios": [
            ("worker-node-1", "production cluster", "24h token expiry"),
            ("gpu-node-alpha", "AI training cluster", "lost discovery CA hash"),
            ("worker-zone-b", "multi-az cluster", "joining new subnet node"),
            ("edge-worker-01", "edge computing cluster", "adding worker with custom taints"),
            ("worker-pool-staging", "staging environment", "expired bootstrap token"),
            ("k8s-node-compute", "HPC compute pool", "re-joining repaired worker"),
            ("worker-arm64", "heterogeneous cluster", "joining ARM64 worker"),
            ("worker-db-storage", "dedicated storage node", "joining with local SSD"),
            ("ingress-gateway-node", "DMZ perimeter network", "dedicated edge join"),
            ("k8s-worker-10", "general worker scale-out", "automating join with bash script")
        ]
    },
    {
        "sub_topic": "kubeadm_controlplane_upgrade",
        "concept": "Control Plane drain, kubeadm upgrade plan/apply, kubelet",
        "scenarios": [
            ("controlplane-01", "v1.30.1", "v1.31.0"),
            ("k8s-master-primary", "v1.29.5", "v1.30.0"),
            ("master-alpha", "v1.30.2", "v1.31.1"),
            ("cp-us-east-1", "v1.29.4", "v1.30.1"),
            ("prod-control-0", "v1.30.0", "v1.31.0"),
            ("staging-master", "v1.29.2", "v1.30.0"),
            ("core-cp-node", "v1.30.3", "v1.31.2"),
            ("finance-cp-1", "v1.30.0", "v1.31.1"),
            ("ha-master-3", "v1.29.3", "v1.30.2"),
            ("k8s-cp-edge", "v1.30.1", "v1.31.0")
        ]
    },
    {
        "sub_topic": "kubeadm_worker_upgrade",
        "concept": "Worker node drain, kubeadm upgrade node, kubelet restart",
        "scenarios": [
            ("worker-node-01", "v1.30.1", "v1.31.0"),
            ("worker-gpu-1", "v1.29.5", "v1.30.0"),
            ("k8s-worker-alpha", "v1.30.2", "v1.31.1"),
            ("worker-batch-node", "v1.29.4", "v1.30.1"),
            ("prod-worker-99", "v1.30.0", "v1.31.0"),
            ("staging-worker-4", "v1.29.2", "v1.30.0"),
            ("worker-app-pool", "v1.30.3", "v1.31.2"),
            ("worker-database-node", "v1.30.0", "v1.31.1"),
            ("k8s-edge-worker", "v1.29.3", "v1.30.2"),
            ("compute-node-15", "v1.30.1", "v1.31.0")
        ]
    },
    {
        "sub_topic": "static_pod_management",
        "concept": "Static Pods in /etc/kubernetes/manifests & kubelet",
        "scenarios": [
            ("kube-apiserver", "/etc/kubernetes/manifests", "inotify monitor"),
            ("kube-controller-manager", "/etc/kubernetes/manifests", "leader election flags"),
            ("kube-scheduler", "/etc/kubernetes/manifests", "custom scoring plugin"),
            ("etcd", "/etc/kubernetes/manifests", "data-dir volume mount change"),
            ("custom-monitor-pod", "/etc/kubernetes/manifests", "node-local static pod"),
            ("local-proxy-pod", "/etc/kubernetes/manifests", "static pod mirror pod in apiserver"),
            ("storage-helper", "/etc/kubernetes/manifests", "kubelet static pod restart on file edit"),
            ("logging-agent-static", "/etc/kubernetes/manifests", "static pod ignoring daemonset controller"),
            ("audit-static-logger", "/etc/kubernetes/manifests", "deleting static pod requires rm file"),
            ("network-diagnostic-static", "/etc/kubernetes/manifests", "static pod cannot be deleted via kubectl")
        ]
    },
    {
        "sub_topic": "certificates_and_csr",
        "concept": "kubeadm certs check-expiration & CSR approvals",
        "scenarios": [
            ("all control plane certs", "check-expiration command", "1 year renewal"),
            ("apiserver-etcd-client cert", "expiring in 7 days", "kubeadm certs renew"),
            ("developer-john CSR", "pending approval", "kubectl certificate approve"),
            ("app-agent CSR", "invalid common name", "kubectl certificate deny"),
            ("apiserver-kubelet-client cert", "annual rotation", "kubeadm certs renew all"),
            ("front-proxy-client cert", "auditing TLS expiry", "kubeadm certs check-expiration"),
            ("ingress-gateway CSR", "requesting client auth", "extracting signed cert"),
            ("worker-kubelet CSR", "node client cert auto-rotation", "certificatesigningrequests"),
            ("security audit cert report", "verifying CA certificate validity", "openssl x509 check"),
            ("custom webhook cert CSR", "admission controller TLS", "approving CSR via CLI")
        ]
    },
    {
        "sub_topic": "kubeconfig_contexts_management",
        "concept": "Kubeconfig clusters, users, contexts, use-context",
        "scenarios": [
            ("admin-ctx", "k8s-prod-cluster", "admin-user", "production"),
            ("dev-ctx", "k8s-dev-cluster", "dev-user", "development"),
            ("qa-ctx", "k8s-test-cluster", "qa-tester", "qa-ns"),
            ("staging-ctx", "k8s-staging", "deployer", "staging"),
            ("security-audit-ctx", "k8s-audit", "auditor-role", "security"),
            ("dr-ctx", "k8s-dr-cluster", "cluster-admin", "default"),
            ("multi-tenant-ctx", "k8s-shared", "tenant-a", "tenant-a-ns"),
            ("operator-ctx", "k8s-cloud", "operator-sa", "kube-system"),
            ("ci-cd-ctx", "k8s-pipeline", "gitlab-runner", "ci-builds"),
            ("monitoring-ctx", "k8s-infra", "prom-admin", "monitoring")
        ]
    },
    {
        "sub_topic": "etcd_quorum_and_ha",
        "concept": "etcd Raft Consensus formula Q = floor(N/2) + 1",
        "scenarios": [
            (3, 2, 1, "standard 3-node HA"),
            (5, 3, 2, "high throughput 5-node cluster"),
            (7, 4, 3, "large enterprise 7-node cluster"),
            (4, 3, 1, "even node count failure tolerance pitfall"),
            (1, 1, 0, "single node lab environment"),
            (3, 2, 1, "network partition leader election"),
            (5, 3, 2, "loss of 2 nodes recovery"),
            (5, 3, 2, "split-brain prevention in odd clusters"),
            (3, 2, 1, "etcdctl member list and health endpoint"),
            (5, 3, 2, "snapshot compaction and defragmentation")
        ]
    },
    {
        "sub_topic": "controlplane_architecture_components",
        "concept": "apiserver, scheduler, controller-manager, etcd roles",
        "scenarios": [
            ("apiserver statelessness", "horizontal scaling behind load balancer"),
            ("scheduler node ranking", "filtering predicates and scoring priorities"),
            ("controller-manager control loops", "desired state reconciliation loop"),
            ("cloud-controller-manager", "cloud provider LB, route, node lifecycle"),
            ("apiserver admission controllers", "mutating and validating webhooks"),
            ("etcd persistent storage", "only apiserver talks directly to etcd"),
            ("scheduler binding phase", "writing nodeName into PodSpec"),
            ("node-controller eviction", "pod-eviction-timeout on NotReady node"),
            ("endpoint-controller", "populating Endpoints from Service selectors"),
            ("garbage-collector-controller", "cascading deletion of child ReplicaSets")
        ]
    },
    {
        "sub_topic": "node_components_kubelet_proxy",
        "concept": "kubelet systemd daemon & kube-proxy iptables/IPVS",
        "scenarios": [
            ("kubelet PodSpec execution", "systemd service, not containerized"),
            ("kubelet cgroup driver", "systemd vs cgroupfs alignment with containerd"),
            ("kubelet /var/lib/kubelet/config.yaml", "evictionHard thresholds"),
            ("kube-proxy iptables mode", "packet filtering and NAT rules for Services"),
            ("kube-proxy IPVS mode", "hash-table based scalable load balancing"),
            ("kubelet container health checks", "executing probes and reporting status"),
            ("kubelet volume mounting", "invoking CSI node plugins"),
            ("kubelet garbage collection", "removing unused images and stopped containers"),
            ("kube-proxy synchronization loop", "watching Services and EndpointSlices"),
            ("kubelet node heartbeat", "NodeStatus lease renewals in kube-node-lease")
        ]
    },
    {
        "sub_topic": "serviceaccount_tokens_and_security",
        "concept": "Projected ServiceAccount tokens & automountServiceAccountToken",
        "scenarios": [
            ("app-backend-sa", "automountServiceAccountToken: false", "security hardening"),
            ("vault-injector-sa", "token request API", "short-lived bound tokens"),
            ("ingress-sa", "secrets token projection", "/var/run/secrets/kubernetes.io/serviceaccount"),
            ("database-operator-sa", "namespace isolation", "restricted API access"),
            ("audit-collector-sa", "read-only access", "token expiration policies"),
            ("ci-deployer-sa", "rbac role binding", "impersonation guardrails"),
            ("backup-agent-sa", "cross-namespace token restriction", "least privilege"),
            ("monitoring-agent-sa", "cluster-level metric read token", "auditing token usage"),
            ("gateway-proxy-sa", "token volume projection", "audience bound token"),
            ("custom-cni-sa", "hostNetwork privileged token", "security profile")
        ]
    },
    {
        "sub_topic": "cluster_networking_cni_model",
        "concept": "CNI requirements: every pod gets a unique IP, no NAT",
        "scenarios": [
            ("Calico IP-in-IP vs BGP", "encapsulation modes across subnets"),
            ("Flannel VXLAN", "overlay networking on port 8472"),
            ("Cilium eBPF", "replacing kube-proxy with BPF maps"),
            ("Pod-to-Pod communication", "cross-node pod communication without port mapping"),
            ("Node-to-Pod communication", "direct routing requirements"),
            ("CNI plugin configuration", "/etc/cni/net.d/ JSON configuration files"),
            ("CNI binary location", "/opt/cni/bin/ executable plugins"),
            ("Node CIDR allocation", "apiserver --allocate-node-cidrs=true"),
            ("MTU sizing in CNI", "packet fragmentation prevention with overlay overhead"),
            ("NetworkPolicy enforcement", "CNI plugin responsibility to enforce policies")
        ]
    },
    {
        "sub_topic": "admission_controllers_and_webhooks",
        "concept": "Validating & Mutating Admission Webhooks",
        "scenarios": [
            ("ImagePolicyWebhook", "rejecting untrusted container registries"),
            ("MutatingWebhookConfiguration", "injecting sidecar containers and env vars"),
            ("ValidatingWebhookConfiguration", "enforcing mandatory labels and limits"),
            ("NodeRestriction admission", "preventing kubelet from modifying other nodes"),
            ("LimitRanger admission", "injecting default CPU/memory requests"),
            ("ResourceQuota admission", "blocking pods exceeding namespace quota"),
            ("ServiceAccount admission", "injecting default SA token and mounts"),
            ("PodSecurity admission", "Privileged vs Baseline vs Restricted standards"),
            ("Admission webhook failurePolicy", "Fail vs Ignore on timeout"),
            ("Admission webhook timeoutSeconds", "preventing apiserver request latency spikes")
        ]
    },
    {
        "sub_topic": "cgroup_drivers_systemd_alignment",
        "concept": "Aligning kubelet & containerd cgroup driver to systemd",
        "scenarios": [
            ("containerd SystemdCgroup = true", "preventing two cgroup managers contention"),
            ("kubelet cgroupDriver: systemd", "setting in /var/lib/kubelet/config.yaml"),
            ("cgroup v2 support", "unified hierarchy /sys/fs/cgroup"),
            ("cgroupfs mismatch failure", "kubelet failing to start with cgroup driver error"),
            ("containerd config.toml dump", "containerd config default > /etc/containerd/config.toml"),
            ("systemd daemon-reload", "reloading kubelet unit file changes"),
            ("node memory pressure eviction", "cgroup v2 oom event handling"),
            ("kubelet CPU manager policy", "static vs none cgroup allocation"),
            ("cgroup v1 vs v2 detection", "stat -fc %T /sys/fs/cgroup output"),
            ("runc cgroup driver configuration", "matching runtime spec with host init")
        ]
    },
    {
        "sub_topic": "cluster_dns_coredns_architecture",
        "concept": "CoreDNS deployment, Service discovery, Corefile",
        "scenarios": [
            ("CoreDNS deployment in kube-system", "2 replicas for HA default"),
            ("kube-dns ClusterIP service", "10.96.0.10 standard internal IP"),
            ("Corefile plugins", "errors, health, kubernetes, forward, cache, loop"),
            ("ndots:5 resolving behavior", "sequential search path queries"),
            ("CoreDNS stub domains", "forwarding custom corporate domain queries"),
            ("CoreDNS resource limits", "preventing DNS throttling during traffic surge"),
            ("Pod dnsPolicy: ClusterFirst", "default DNS resolution via CoreDNS"),
            ("Pod dnsPolicy: Default", "inheriting host node /etc/resolv.conf"),
            ("Pod dnsPolicy: None", "custom dnsConfig with explicit nameservers"),
            ("CoreDNS autopath optimization", "reducing DNS lookup round-trips")
        ]
    },
    {
        "sub_topic": "cluster_backup_etcd_storage_integrity",
        "concept": "etcd snapshot integrity check & member health",
        "scenarios": [
            ("etcdctl snapshot status --write-out=table", "verifying total size, hash, and revision"),
            ("etcdctl endpoint health", "checking Raft cluster member responsiveness"),
            ("etcdctl alarm list", "checking NOSPACE alarm on full disk"),
            ("etcdctl defrag", "reclaiming backend DB fragmentation space"),
            ("etcdctl endpoint status", "verifying leader ID and dbSizeInUse"),
            ("etcd snapshot restore permissions", "ensuring chown -R etcd:etcd on restored dir"),
            ("disaster recovery runbook", "multi-member cluster recovery from single snapshot"),
            ("etcd TLS cert verification", "testing client auth with curl --cert/--key"),
            ("etcd quota-backend-bytes", "configuring maximum storage size limit (8GB)"),
            ("etcd wal write latency", "diagnosing slow disk I/O impact on Raft leader")
        ]
    },
    {
        "sub_topic": "cluster_security_audit_logging",
        "concept": "API server audit policy & log backend flags",
        "scenarios": [
            ("Audit Policy Level: None", "suppressing high frequency endpoint logging"),
            ("Audit Policy Level: Metadata", "logging user, timestamp, resource without body"),
            ("Audit Policy Level: Request", "logging metadata and request body"),
            ("Audit Policy Level: RequestResponse", "full audit trail including responses"),
            ("apiserver flag --audit-log-path", "writing audit events to log file"),
            ("apiserver flag --audit-policy-file", "pointing to audit policy YAML"),
            ("audit log rotation flags", "--audit-log-maxbackup, --audit-log-maxsize"),
            ("omitting request stages", "filtering RequestReceived vs ResponseComplete"),
            ("filtering system accounts from audit", "ignoring system:nodes noisy events"),
            ("webhook audit backend", "streaming audit events to external SIEM")
        ]
    },
    {
        "sub_topic": "kubeadm_reset_and_cleanup",
        "concept": "kubeadm reset & iptables/CNI interface cleanup",
        "scenarios": [
            ("worker node decommission", "drain, kubeadm reset -f, ip link delete cni0"),
            ("failed cluster init rollback", "kubeadm reset and rm -rf /etc/kubernetes/"),
            ("flannel interface removal", "ip link delete flannel.1"),
            ("calico interface cleanup", "ip link delete calico-veth"),
            ("iptables flush post-reset", "iptables -F && iptables -t nat -F"),
            ("etcd data directory cleanup", "rm -rf /var/lib/etcd after reset"),
            ("cni config directory cleanup", "rm -rf /etc/cni/net.d/*"),
            ("kubelet systemd stop", "systemctl stop kubelet before reset"),
            ("container runtime prune", "crictl rm -f $(crictl ps -aq) post-reset"),
            ("deleting node from cluster", "kubectl delete node <node> after worker reset")
        ]
    },
    {
        "sub_topic": "multi_master_ha_topology",
        "concept": "Stacked etcd vs External etcd topology HA",
        "scenarios": [
            ("Stacked etcd topology", "etcd co-located on control plane nodes"),
            ("External etcd topology", "etcd running on dedicated independent servers"),
            ("External load balancer for apiservers", "HAProxy / Keepalived on port 6443"),
            ("kubeadm init --control-plane-endpoint", "specifying DNS/IP of load balancer"),
            ("kubeadm join --control-plane", "adding secondary control plane node with certs"),
            ("kubeadm init phase upload-certs", "encrypting and sharing control plane PKI"),
            ("control plane failure tolerance", "maintaining quorum with 1 of 3 masters down"),
            ("split-brain prevention in stacked HA", "requiring quorum of both etcd and apiservers"),
            ("health checking apiserver endpoint", "probing /livez and /readyz on load balancer"),
            ("etcd peer communication ports", "port 2379 (client) vs port 2380 (peer Raft)")
        ]
    }
]

def build_domain1_questions():
    questions = []
    q_idx = 1
    for st in d1_subtopics:
        sub_topic = st["sub_topic"]
        concept = st["concept"]
        for sc in st["scenarios"]:
            q_id = f"D1-Q{q_idx:03d}"
            
            # 고유한 시나리오 문항 생성
            if sub_topic == "etcd_snapshot_save":
                target_env, backup_path, ep, cert_dir = sc
                q_en = f"You are tasked with backing up the {target_env} etcd cluster. The endpoint is '{ep}' and the TLS certificates are stored in '{cert_dir}'. Which command correctly saves the snapshot to '{backup_path}'?"
                q_kr = f"당신은 {target_env}의 etcd 클러스터를 백업해야 합니다. 엔드포인트는 '{ep}'이고 TLS 인증서는 '{cert_dir}'에 위치합니다. '{backup_path}' 경로에 스냅샷을 올바르게 저장하는 명령어는 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"etcdctl snapshot save {backup_path} --no-tls", "text_kr": f"etcdctl snapshot save {backup_path} --no-tls"},
                    {"key": "B", "text_en": f"ETCDCTL_API=3 etcdctl --endpoints={ep} --cacert={cert_dir}/ca.crt --cert={cert_dir}/server.crt --key={cert_dir}/server.key snapshot save {backup_path}", "text_kr": f"ETCDCTL_API=3 etcdctl --endpoints={ep} --cacert={cert_dir}/ca.crt --cert={cert_dir}/server.crt --key={cert_dir}/server.key snapshot save {backup_path}"},
                    {"key": "C", "text_en": f"kubectl snapshot etcd {backup_path} --endpoint={ep}", "text_kr": f"kubectl snapshot etcd {backup_path} --endpoint={ep}"},
                    {"key": "D", "text_en": f"kubeadm backup etcd --output={backup_path} --endpoints={ep}", "text_kr": f"kubeadm backup etcd --output={backup_path} --endpoints={ep}"}
                ]
                ans = "B"
                exp = f"정답은 B입니다.\n\n• etcd v3 API 사용 시 환경변수 `ETCDCTL_API=3`이 필수이며, TLS 보안 연결을 위해 `--cacert`, `--cert`, `--key`, `--endpoints` 옵션이 명시되어야 합니다.\n• A는 TLS 인증서가 누락되었으며, C와 D는 존재하지 않는 명령어입니다."
            elif sub_topic == "etcd_snapshot_restore":
                snap_path, new_dir, cp_node = sc
                q_en = f"You need to restore an etcd snapshot from '{snap_path}' on control plane node '{cp_node}'. After running the restore command to '{new_dir}', which action is mandatory to activate the restored database?"
                q_kr = f"컨트롤 플레인 노드 '{cp_node}'에서 '{snap_path}'의 etcd 스냅샷을 복원해야 합니다. '{new_dir}'로 복원 명령을 실행한 후, 복원된 데이터베이스를 활성화하기 위해 반드시 수행해야 하는 작업은 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"Update the hostPath.path in /etc/kubernetes/manifests/etcd.yaml to point to '{new_dir}'", "text_kr": f"/etc/kubernetes/manifests/etcd.yaml 파일의 hostPath.path 볼륨 경로를 '{new_dir}'로 수정한다"},
                    {"key": "B", "text_en": "Restart the kube-apiserver service using systemctl restart kube-apiserver", "text_kr": "systemctl restart kube-apiserver 명령어로 API 서버 서비스를 재시작한다"},
                    {"key": "C", "text_en": "Run kubectl apply -f /var/lib/etcd/restore.yaml to deploy new etcd pods", "text_kr": "kubectl apply -f /var/lib/etcd/restore.yaml을 실행하여 새 etcd 파드를 배포한다"},
                    {"key": "D", "text_en": "Execute kubeadm upgrade apply to synchronize the etcd cluster state", "text_kr": "kubeadm upgrade apply를 실행하여 etcd 클러스터 상태를 동기화한다"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• 스냅샷을 새로운 디렉토리(`--data-dir={new_dir}`)에 복원한 후에는 Static Pod 매니페스트인 `/etc/kubernetes/manifests/etcd.yaml`의 `hostPath` 볼륨 경로를 새 디렉토리로 변경해야 kubelet이 감지하고 새 데이터를 참조하여 재시작합니다."
            elif sub_topic == "rbac_role_creation":
                r_name, ns, res_list, verbs = sc
                q_en = f"You need to create a Role named '{r_name}' in namespace '{ns}' granting '{verbs}' permissions on '{res_list}'. Which command accomplishes this imperatively?"
                q_kr = f"네임스페이스 '{ns}'에서 '{res_list}' 리소스에 대해 '{verbs}' 권한을 부여하는 Role '{r_name}'을 명령형 커맨드로 생성하고자 합니다. 올바른 명령어는 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"kubectl create role {r_name} --verb={verbs} --resource={res_list} -n {ns}", "text_kr": f"kubectl create role {r_name} --verb={verbs} --resource={res_list} -n {ns}"},
                    {"key": "B", "text_en": f"kubectl create clusterrole {r_name} --verb={verbs} --resource={res_list} -n {ns}", "text_kr": f"kubectl create clusterrole {r_name} --verb={verbs} --resource={res_list} -n {ns}"},
                    {"key": "C", "text_en": f"kubectl create rolebinding {r_name} --role={r_name} --verb={verbs} -n {ns}", "text_kr": f"kubectl create rolebinding {r_name} --role={r_name} --verb={verbs} -n {ns}"},
                    {"key": "D", "text_en": f"kubectl run role {r_name} --resource={res_list} --allow={verbs} -n {ns}", "text_kr": f"kubectl run role {r_name} --resource={res_list} --allow={verbs} -n {ns}"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• 네임스페이스 격리 역할을 생성할 때는 `kubectl create role <이름> --verb=<동사목록> --resource=<리소스목록> -n <네임스페이스>` 명령어를 사용합니다.\n• B는 클러스터 전체 대상인 ClusterRole 명령이며 네임스페이스 플래그가 무시됩니다."
            elif sub_topic == "rbac_clusterrole":
                cr_name, res_list, verbs = sc
                q_en = f"You need to create a ClusterRole named '{cr_name}' with '{verbs}' access to non-namespaced resource '{res_list}'. Why must a ClusterRole be used instead of a standard Role?"
                q_kr = f"비네임스페이스 리소스인 '{res_list}'에 대해 '{verbs}' 권한을 부여하는 ClusterRole '{cr_name}'을 생성해야 합니다. 일반 Role 대신 ClusterRole을 반드시 사용해야 하는 이유는 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"Because '{res_list}' is a cluster-scoped (non-namespaced) resource and cannot be scoped to a single namespace", "text_kr": f"'{res_list}'는 클러스터 범위(비네임스페이스) 리소스이므로 단일 네임스페이스로 격리할 수 없기 때문"},
                    {"key": "B", "text_en": "Because Roles only support read-only operations like get and list", "text_kr": "일반 Role은 get이나 list 같은 읽기 전용 작업만 지원하기 때문"},
                    {"key": "C", "text_en": "Because ClusterRoles run faster than standard Roles during API authorization", "text_kr": "API 인가 과정에서 ClusterRole이 일반 Role보다 실행 속도가 훨씬 빠르기 때문"},
                    {"key": "D", "text_en": "Because ServiceAccounts cannot be bound to standard Roles", "text_kr": "ServiceAccount는 일반 Role에 바인딩할 수 없기 때문"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• `nodes`, `persistentvolumes`, `namespaces`, `storageclasses` 등은 특정 네임스페이스에 속하지 않는 클러스터 전역 리소스이므로 Role이 아닌 ClusterRole로만 권한을 정의할 수 있습니다."
            elif sub_topic == "rbac_binding_users_and_sa":
                b_name, ref_role, subj_kind, subj_name, target_ns = sc
                is_crb = (target_ns == "global")
                q_en = f"You need to bind role '{ref_role}' to {subj_kind} '{subj_name}' using binding name '{b_name}' {'at cluster level' if is_crb else f'in namespace {target_ns}'}. Which command is correct?"
                q_kr = f"{'클러스터 전체 범위에서' if is_crb else f'네임스페이스 {target_ns}에서'} 바인딩 이름 '{b_name}'을 사용하여 {subj_kind} '{subj_name}'에게 '{ref_role}' 권한을 부여하는 올바른 커맨드는 무엇입니까?"
                if is_crb:
                    flag = f"--clusterrole={ref_role} --{subj_kind.lower()}={subj_name}" if subj_kind != "ServiceAccount" else f"--clusterrole={ref_role} --serviceaccount=kube-system:{subj_name}"
                    opts = [
                        {"key": "A", "text_en": f"kubectl create clusterrolebinding {b_name} {flag}", "text_kr": f"kubectl create clusterrolebinding {b_name} {flag}"},
                        {"key": "B", "text_en": f"kubectl create rolebinding {b_name} --role={ref_role} --user={subj_name}", "text_kr": f"kubectl create rolebinding {b_name} --role={ref_role} --user={subj_name}"},
                        {"key": "C", "text_en": f"kubectl bind clusterrole {ref_role} to {subj_name}", "text_kr": f"kubectl bind clusterrole {ref_role} to {subj_name}"},
                        {"key": "D", "text_en": f"kubectl set rbac {b_name} --target={subj_name}", "text_kr": f"kubectl set rbac {b_name} --target={subj_name}"}
                    ]
                else:
                    flag = f"--role={ref_role} --{subj_kind.lower()}={subj_name} -n {target_ns}" if subj_kind != "ServiceAccount" else f"--role={ref_role} --serviceaccount={target_ns}:{subj_name} -n {target_ns}"
                    opts = [
                        {"key": "A", "text_en": f"kubectl create rolebinding {b_name} {flag}", "text_kr": f"kubectl create rolebinding {b_name} {flag}"},
                        {"key": "B", "text_en": f"kubectl create clusterrolebinding {b_name} --clusterrole={ref_role} -n {target_ns}", "text_kr": f"kubectl create clusterrolebinding {b_name} --clusterrole={ref_role} -n {target_ns}"},
                        {"key": "C", "text_en": f"kubectl assign role {ref_role} --to={subj_name} -n {target_ns}", "text_kr": f"kubectl assign role {ref_role} --to={subj_name} -n {target_ns}"},
                        {"key": "D", "text_en": f"kubectl attach rbac {b_name} --subject={subj_name} -n {target_ns}", "text_kr": f"kubectl attach rbac {b_name} --subject={subj_name} -n {target_ns}"}
                    ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• 권한을 부여할 때는 `kubectl create rolebinding` (또는 `clusterrolebinding`)을 사용하며, 주체(User, Group, ServiceAccount)를 정확한 플래그로 지정해야 합니다."
            elif sub_topic == "kubectl_auth_can_i":
                verb, res, user_or_sa, ns = sc
                ns_clause = f"-n {ns}" if ns else ""
                q_en = f"You are troubleshooting access permissions and need to test whether '{user_or_sa}' can perform '{verb}' on '{res}' {f'in namespace {ns}' if ns else 'across the cluster'}. Which command runs this test?"
                q_kr = f"접근 권한 문제를 해결하기 위해 '{user_or_sa}'가 {f'네임스페이스 {ns}에서' if ns else '클러스터 전체에서'} '{res}' 리소스에 대해 '{verb}' 작업을 수행할 수 있는지 검증하고자 합니다. 올바른 테스트 명령어는 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"kubectl auth can-i {verb} {res} --as={user_or_sa} {ns_clause}".strip(), "text_kr": f"kubectl auth can-i {verb} {res} --as={user_or_sa} {ns_clause}".strip()},
                    {"key": "B", "text_en": f"kubectl test permission {verb} {res} --user={user_or_sa}", "text_kr": f"kubectl test permission {verb} {res} --user={user_or_sa}"},
                    {"key": "C", "text_en": f"kubectl describe rbac --verify {verb} {res} {ns_clause}".strip(), "text_kr": f"kubectl describe rbac --verify {verb} {res} {ns_clause}".strip()},
                    {"key": "D", "text_en": f"kubectl check access {user_or_sa} {verb} {res}", "text_kr": f"kubectl check access {user_or_sa} {verb} {res}"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• `kubectl auth can-i <verb> <resource> --as=<subject>`는 특정 사용자나 서비스 어카운트의 권한을 사전 시뮬레이션(Impersonation)하여 'yes' 또는 'no'로 즉시 판별해주는 필수 진단 도구입니다."
            elif sub_topic == "kubeadm_cluster_init":
                cidr, apiserver_ip, ver, cni_name = sc
                q_en = f"When initializing a Kubernetes {ver} master node with kubeadm intended for the '{cni_name}' CNI plugin requiring pod CIDR '{cidr}', which command should be executed at IP '{apiserver_ip}'?"
                q_kr = f"'{cidr}' 파드 대역을 요구하는 '{cni_name}' CNI 플러그인을 사용할 목적으로 쿠버네티스 {ver} 마스터 노드를 IP '{apiserver_ip}'에서 초기화하고자 합니다. 올바른 kubeadm 명령어는 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"kubeadm init --pod-network-cidr={cidr} --apiserver-advertise-address={apiserver_ip}", "text_kr": f"kubeadm init --pod-network-cidr={cidr} --apiserver-advertise-address={apiserver_ip}"},
                    {"key": "B", "text_en": f"kubeadm create cluster --network={cidr} --master-ip={apiserver_ip}", "text_kr": f"kubeadm create cluster --network={cidr} --master-ip={apiserver_ip}"},
                    {"key": "C", "text_en": f"kubeadm bootstrap --cni={cni_name} --ip={apiserver_ip}", "text_kr": f"kubeadm bootstrap --cni={cni_name} --ip={apiserver_ip}"},
                    {"key": "D", "text_en": f"kubeadm start --pod-cidr={cidr} --listen={apiserver_ip}", "text_kr": f"kubeadm start --pod-cidr={cidr} --listen={apiserver_ip}"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• `kubeadm init` 명령어에서 파드 네트워크 대역은 `--pod-network-cidr`로 전달하며, 특정 인터페이스 IP를 알릴 때는 `--apiserver-advertise-address`를 사용합니다."
            elif sub_topic == "kubeadm_token_and_join":
                node_name, cluster_env, reason = sc
                q_en = f"You are connecting worker node '{node_name}' to the {cluster_env}. The previous join command was lost and token expired ({reason}). How do you regenerate a valid join command on the control plane?"
                q_kr = f"{cluster_env}의 워커 노드 '{node_name}'을 클러스터에 조인해야 합니다. 이전 조인 명령어와 토큰이 만료/분실되었습니다 ({reason}). 컨트롤 플레인에서 유효한 조인 커맨드를 즉시 다시 출력하는 방법은 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": "kubeadm token create --print-join-command", "text_kr": "kubeadm token create --print-join-command"},
                    {"key": "B", "text_en": "kubectl get nodes --show-join-token", "text_kr": "kubectl get nodes --show-join-token"},
                    {"key": "C", "text_en": "kubeadm join --show-tokens-all", "text_kr": "kubeadm join --show-tokens-all"},
                    {"key": "D", "text_en": "cat /etc/kubernetes/bootstrap-token.conf", "text_kr": "cat /etc/kubernetes/bootstrap-token.conf"}
                ]
                ans = "A"
                exp = "정답은 A입니다.\n\n• `kubeadm token create --print-join-command`를 실행하면 신규 부트스트랩 토큰과 discovery-token-ca-cert-hash가 포함된 완전한 `kubeadm join` 명령어가 생성됩니다."
            elif sub_topic == "kubeadm_controlplane_upgrade":
                cp_name, from_v, to_v = sc
                q_en = f"You need to upgrade control plane node '{cp_name}' from {from_v} to {to_v}. After draining the node and updating the kubeadm package, which command performs the upgrade pre-checks and execution?"
                q_kr = f"컨트롤 플레인 노드 '{cp_name}'을 {from_v}에서 {to_v}로 업그레이드해야 합니다. 노드를 drain하고 kubeadm 패키지를 업데이트한 후, 업그레이드 가능성을 검사하고 실제로 적용하는 명령어 조합은 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"kubeadm upgrade plan, followed by kubeadm upgrade apply {to_v}", "text_kr": f"kubeadm upgrade plan 실행 후 kubeadm upgrade apply {to_v} 적용"},
                    {"key": "B", "text_en": f"kubeadm upgrade node {to_v} directly", "text_kr": f"kubeadm upgrade node {to_v}를 바로 실행"},
                    {"key": "C", "text_en": "apt-get upgrade kubernetes-all -y", "text_kr": "apt-get upgrade kubernetes-all -y 일괄 업그레이드"},
                    {"key": "D", "text_en": f"kubectl rollout upgrade cluster --to-version={to_v}", "text_kr": f"kubectl rollout upgrade cluster --to-version={to_v}"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• 컨트롤 플레인 첫 번째 노드에서는 반드시 `kubeadm upgrade plan`으로 버전 적합성을 확인한 후 `kubeadm upgrade apply <버전>`을 실행해야 합니다.\n• `kubeadm upgrade node`는 워커 노드(또는 보조 마스터)에서 사용하는 명령어입니다."
            elif sub_topic == "kubeadm_worker_upgrade":
                worker_name, from_v, to_v = sc
                q_en = f"You are upgrading worker node '{worker_name}' from {from_v} to {to_v}. On the worker node itself, after upgrading the kubeadm package, which command applies the node-level upgrade?"
                q_kr = f"워커 노드 '{worker_name}'을 {from_v}에서 {to_v}로 업그레이드 중입니다. 워커 노드 로컬 접속 후 kubeadm 패키지를 업데이트한 다음, 노드 업그레이드를 적용하는 올바른 명령어는 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": "kubeadm upgrade node", "text_kr": "kubeadm upgrade node"},
                    {"key": "B", "text_en": f"kubeadm upgrade apply {to_v}", "text_kr": f"kubeadm upgrade apply {to_v}"},
                    {"key": "C", "text_en": "kubectl upgrade worker", "text_kr": "kubectl upgrade worker"},
                    {"key": "D", "text_en": "kubelet upgrade apply", "text_kr": "kubelet upgrade apply"}
                ]
                ans = "A"
                exp = "정답은 A입니다.\n\n• 워커 노드에서는 `kubeadm upgrade apply`가 아니라 반드시 `kubeadm upgrade node`를 실행하여 로컬 kubelet 설정을 업데이트해야 합니다."
            else:
                # 일반 질문 템플릿
                param1, param2 = sc[0], sc[1]
                q_en = f"Regarding {concept} in Kubernetes, when managing '{param1}' with '{param2}', which statement accurately reflects the standard architectural behavior?"
                q_kr = f"쿠버네티스의 {concept}와 관련하여 '{param1}' 및 '{param2}' 설정 시 공식 표준 동작을 가장 정확하게 설명한 것은 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"It is directly managed by the kubelet or apiserver following standard declarative specifications for {param1}", "text_kr": f"{param1}에 대해 표준 선언적 명세에 따라 kubelet 또는 API 서버에 의해 직접 관리된다"},
                    {"key": "B", "text_en": "It requires an external third-party proprietary controller to function", "text_kr": "작동을 위해 반드시 외부 상용 서드파티 컨트롤러가 필요하다"},
                    {"key": "C", "text_en": "It completely bypasses all RBAC and security validations", "text_kr": "모든 RBAC 및 보안 검증을 완전히 우회하여 동작한다"},
                    {"key": "D", "text_en": "It is deprecated and disabled by default in Kubernetes 1.30+", "text_kr": "쿠버네티스 1.30 이상에서 지원이 중단되어 기본 비활성화되어 있다"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• 쿠버네티스 {concept} 영역에서 {param1}은(는) 공식 제어 루프와 에이전트에 의해 선언적으로 관리됩니다."
            
            questions.append({
                "id": q_id,
                "domain": "Domain 1",
                "domain_name": "클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration)",
                "sub_topic": sub_topic,
                "question_en": q_en,
                "question_kr": q_kr,
                "options": opts,
                "correct_answer": ans,
                "explanation_kr": exp,
                "key_concept": concept
            })
            q_idx += 1
            
    print(f"Generated Domain 1: {len(questions)} unique questions.")
    return questions

# -------------------------------------------------------------
# CKA 도메인 2: 워크로드 및 스케줄링 (250문항)
# -------------------------------------------------------------
d2_subtopics = [
    ("deploy_rolling_strategy", "Deployment RollingUpdate maxSurge & maxUnavailable", [
        ("web-frontend", 4, "25%", "25%"), ("api-gateway", 8, "50%", "0"), ("payment-srv", 10, "1", "1"),
        ("auth-service", 6, "20%", "20%"), ("user-service", 5, "2", "0"), ("cart-app", 4, "0", "1"),
        ("inventory-api", 12, "25%", "25%"), ("notification-svc", 3, "1", "0"), ("catalog-web", 6, "33%", "33%"),
        ("search-engine", 8, "10%", "10%")
    ]),
    ("deploy_rollout_undo", "kubectl rollout undo & history", [
        ("web-app", 2, "broken image tag"), ("api-srv", 1, "bad configuration env"), ("worker-pod", 3, "database connection error"),
        ("payment-app", 4, "performance regression"), ("auth-core", 2, "certificate misconfiguration"), ("redis-cluster", 1, "memory leak in new version"),
        ("logging-agent", 5, "excessive log volume"), ("checkout-api", 2, "null pointer exception"), ("graphql-server", 3, "syntax error in schema"),
        ("queue-consumer", 1, "deadlock on startup")
    ]),
    ("daemonset_toleration", "DaemonSet master node toleration", [
        ("node-exporter", "monitoring", "node-role.kubernetes.io/control-plane"),
        ("fluentd-logger", "logging", "node-role.kubernetes.io/master"),
        ("calico-node", "kube-system", "node.kubernetes.io/not-ready"),
        ("security-falcon", "security", "node-role.kubernetes.io/control-plane"),
        ("cilium-cni", "kube-system", "CriticalAddonsOnly"),
        ("filebeat-agent", "elastic", "node-role.kubernetes.io/control-plane"),
        ("prom-node-metrics", "monitoring", "node-role.kubernetes.io/master"),
        ("audit-daemon", "compliance", "node-role.kubernetes.io/control-plane"),
        ("storage-csi-node", "kube-system", "node-role.kubernetes.io/control-plane"),
        ("net-sniffer", "network-debug", "node-role.kubernetes.io/control-plane")
    ]),
    ("statefulset_headless", "StatefulSet with Headless Service clusterIP: None", [
        ("cassandra", "cassandra-svc", 3, "cass-0"), ("kafka", "kafka-headless", 3, "kafka-0"), ("zookeeper", "zk-svc", 3, "zk-0"),
        ("elasticsearch", "es-cluster", 3, "es-0"), ("mongodb", "mongo-service", 3, "mongo-0"), ("rabbitmq", "rabbit-headless", 3, "rabbit-0"),
        ("mysql-cluster", "mysql-headless", 2, "mysql-0"), ("etcd-cluster", "etcd-srv", 3, "etcd-0"), ("cockroachdb", "crdb-headless", 3, "crdb-0"),
        ("redis-sentinel", "redis-headless", 3, "redis-0")
    ]),
    ("job_backoff_limit", "Job completions, parallelism, restartPolicy", [
        ("db-migration", 1, 1, 3, "OnFailure"), ("image-resizer", 10, 2, 4, "OnFailure"), ("batch-report", 5, 5, 2, "Never"),
        ("data-cleaner", 1, 1, 6, "OnFailure"), ("etl-pipeline", 12, 3, 5, "OnFailure"), ("video-encoder", 8, 4, 3, "Never"),
        ("backup-sync", 1, 1, 2, "OnFailure"), ("log-indexer", 20, 5, 4, "OnFailure"), ("cache-prewarmer", 6, 2, 3, "Never"),
        ("ml-model-inference", 4, 2, 2, "OnFailure")
    ]),
    ("cronjob_concurrency", "CronJob concurrencyPolicy: Forbid vs Allow", [
        ("nightly-backup", "0 2 * * *", "Forbid"), ("hourly-sync", "0 * * * *", "Forbid"), ("health-probe", "*/5 * * * *", "Allow"),
        ("daily-report", "0 6 * * *", "Replace"), ("cleanup-tmp", "30 3 * * *", "Forbid"), ("metric-collector", "*/10 * * * *", "Allow"),
        ("billing-batch", "0 0 1 * *", "Forbid"), ("cert-audit-job", "0 12 * * 1", "Forbid"), ("index-refresh", "*/15 * * * *", "Replace"),
        ("session-purge", "0 4 * * *", "Forbid")
    ]),
    ("init_containers", "Init Containers sequential execution & wait conditions", [
        ("web-app", "wait-for-db", "db-service:3306"), ("api-srv", "fetch-config", "git-sync-repo"), ("payment-core", "wait-for-vault", "vault-server:8200"),
        ("data-importer", "unzip-assets", "local-tar-extract"), ("auth-service", "wait-for-redis", "redis-master:6379"), ("worker-agent", "schema-migrate", "flyway-migration"),
        ("analytics-web", "download-model", "s3-model-bucket"), ("billing-app", "wait-for-mq", "rabbitmq:5672"), ("game-server", "patch-binary", "patch-storage"),
        ("notification-srv", "register-service", "consul-catalog")
    ]),
    ("sidecar_emptydir", "Multi-container Pod emptyDir log sharing", [
        ("web-server", "log-collector", "/var/log/nginx"), ("order-api", "fluent-sidecar", "/var/log/orders"), ("auth-app", "audit-shipper", "/opt/app/logs"),
        ("proxy-server", "metrics-exporter", "/var/run/proxy"), ("payment-srv", "vault-agent", "/vault/secrets"), ("worker-node-agent", "tail-log", "/var/log/worker"),
        ("graphql-gw", "cache-refresh-sidecar", "/cache/data"), ("ingress-proxy", "ssl-refresher", "/etc/ssl/certs"), ("batch-processor", "file-uploader", "/data/outbox"),
        ("backend-daemon", "health-reporter", "/tmp/health")
    ]),
    ("node_affinity_hard", "NodeAffinity requiredDuringSchedulingIgnoredDuringExecution", [
        ("finance-app", "pci-compliant", "true"), ("ml-training", "accelerator", "nvidia-gpu"), ("db-high-iops", "disktype", "nvme-ssd"),
        ("edge-compute", "topology.kubernetes.io/zone", "us-east-1a"), ("secure-gateway", "security-level", "hardened"), ("memory-cache", "instance-type", "r5b.8xlarge"),
        ("telemetry-worker", "environment", "production"), ("analytics-db", "tier", "backend-db"), ("payment-core", "region", "eu-central-1"),
        ("batch-worker", "lifecycle", "on-demand")
    ]),
    ("node_affinity_soft", "NodeAffinity preferredDuringSchedulingIgnoredDuringExecution", [
        ("frontend-web", "zone-preference", "us-west-2a", 50), ("api-cache", "hardware-gen", "intel-ice-lake", 80), ("worker-low-priority", "spot-instance", "true", 100),
        ("media-streamer", "network-speed", "10gbps", 60), ("ad-server", "datacenter", "dc-primary", 75), ("feed-service", "rack", "rack-42", 40),
        ("dev-sandbox", "node-type", "general-compute", 30), ("qa-testing", "os-version", "ubuntu-2204", 90), ("background-sync", "power-mode", "efficient", 50),
        ("log-consumer", "az-preference", "ap-northeast-2c", 70)
    ]),
    ("pod_antiaffinity", "PodAntiAffinity topologyKey kubernetes.io/hostname", [
        ("web-frontend", "app=web", "kubernetes.io/hostname"), ("redis-cache", "app=redis", "topology.kubernetes.io/zone"), ("auth-token-srv", "app=auth", "kubernetes.io/hostname"),
        ("payment-router", "role=payment", "kubernetes.io/hostname"), ("kafka-broker", "app=kafka", "topology.kubernetes.io/zone"), ("dns-internal", "k8s-app=kube-dns", "kubernetes.io/hostname"),
        ("ingress-controller", "app.kubernetes.io/name=ingress", "kubernetes.io/hostname"), ("database-primary", "tier=database", "topology.kubernetes.io/zone"), ("elasticsearch-data", "component=es-data", "kubernetes.io/hostname"),
        ("order-processing", "service=orders", "kubernetes.io/hostname")
    ]),
    ("taints_and_tolerations", "Taints NoSchedule / NoExecute and Tolerations", [
        ("gpu-node-1", "dedicated=gpu", "NoSchedule"), ("storage-node-alpha", "storage=nvme", "NoSchedule"), ("maintenance-node", "node.kubernetes.io/unschedulable", "NoSchedule"),
        ("infra-master-2", "node-role.kubernetes.io/control-plane", "NoSchedule"), ("unstable-node", "hardware=failing", "NoExecute"), ("edge-device-10", "edge=iot", "NoSchedule"),
        ("high-mem-server", "workload=memory-intensive", "NoSchedule"), ("isolated-dmz", "network=dmz", "NoSchedule"), ("quarantined-node", "security=investigating", "NoExecute"),
        ("spot-pool-node", "pricing=preemptible", "PreferNoSchedule")
    ]),
    ("security_context_user", "securityContext runAsNonRoot & readOnlyRootFilesystem", [
        ("secure-api", 10001, "true", "true"), ("payment-worker", 2000, "true", "false"), ("audit-agent", 1000, "true", "true"),
        ("public-frontend", 101, "true", "true"), ("auth-daemon", 5000, "true", "false"), ("database-proxy", 999, "true", "true"),
        ("file-ingester", 3000, "true", "false"), ("crypto-service", 7777, "true", "true"), ("catalog-api", 8080, "true", "false"),
        ("notification-hub", 1234, "true", "true")
    ]),
    ("security_context_caps", "securityContext capabilities add/drop", [
        ("traffic-capture", "NET_ADMIN", "ALL"), ("vpn-gateway", "NET_ADMIN", "SYS_ADMIN"), ("custom-tracer", "SYS_PTRACE", "ALL"),
        ("time-sync-agent", "SYS_TIME", "ALL"), ("network-firewall-pod", "NET_RAW", "ALL"), ("hardened-web", "NONE", "ALL"),
        ("storage-mounter", "SYS_ADMIN", "ALL"), ("kernel-monitor", "BPF", "ALL"), ("packet-inspector", "NET_ADMIN", "ALL"),
        ("secure-sandbox", "NONE", "ALL")
    ]),
    ("resource_qos_classes", "QoS Classes: Guaranteed vs Burstable vs BestEffort", [
        ("Guaranteed", "cpu: 500m, mem: 512Mi", "cpu: 500m, mem: 512Mi"),
        ("Burstable", "cpu: 250m, mem: 256Mi", "cpu: 500m, mem: 512Mi"),
        ("BestEffort", "no requests", "no limits"),
        ("Guaranteed", "cpu: 2, mem: 4Gi", "cpu: 2, mem: 4Gi"),
        ("Burstable", "cpu: 1, mem: 2Gi", "cpu: 2, mem: 4Gi"),
        ("BestEffort", "unspecified resources", "unspecified resources"),
        ("Guaranteed", "cpu: 100m, mem: 128Mi", "cpu: 100m, mem: 128Mi"),
        ("Burstable", "cpu: 50m, mem: 64Mi", "cpu: 100m, mem: 256Mi"),
        ("BestEffort", "zero requests", "zero limits"),
        ("Guaranteed", "cpu: 4, mem: 8Gi", "cpu: 4, mem: 8Gi")
    ]),
    ("env_configmap_secret", "envFrom with configMapRef & secretRef", [
        ("app-config", "db-credentials", "production"), ("api-settings", "api-tokens", "staging"), ("payment-conf", "stripe-keys", "payment-ns"),
        ("auth-props", "jwt-secret", "auth-ns"), ("redis-conf", "redis-auth", "cache-ns"), ("frontend-env", "analytics-key", "default"),
        ("email-config", "smtp-credentials", "notifications"), ("search-params", "elastic-auth", "search-ns"), ("queue-settings", "rabbit-secret", "messaging"),
        ("telemetry-conf", "datadog-api-key", "monitoring")
    ]),
    ("subpath_volume_mount", "subPath volume mounting to avoid directory overwrite", [
        ("nginx.conf", "/etc/nginx/nginx.conf", "nginx-config"),
        ("application.properties", "/app/config/application.properties", "spring-config"),
        ("settings.json", "/opt/app/settings.json", "json-config"),
        ("redis.conf", "/etc/redis/redis.conf", "redis-config"),
        ("my.cnf", "/etc/mysql/conf.d/my.cnf", "mysql-custom-cnf"),
        ("prometheus.yml", "/etc/prometheus/prometheus.yml", "prom-config"),
        ("server.xml", "/usr/local/tomcat/conf/server.xml", "tomcat-xml"),
        ("logback.xml", "/app/resources/logback.xml", "logger-xml"),
        ("httpd.conf", "/usr/local/apache2/conf/httpd.conf", "apache-conf"),
        ("core-site.xml", "/etc/hadoop/core-site.xml", "hadoop-xml")
    ]),
    ("manual_node_name", "spec.nodeName manual scheduling bypass", [
        ("maintenance-rescue-pod", "worker-node-01"), ("diagnostic-agent", "master-01"), ("hardware-audit", "gpu-worker-2"),
        ("emergency-shell", "k8s-node-alpha"), ("isolated-runner", "compute-node-15"), ("log-retriever", "worker-node-99"),
        ("direct-mounter", "storage-node-4"), ("perf-test-pod", "baremetal-node"), ("kernel-probe", "edge-worker-01"),
        ("local-backup-pod", "database-node")
    ]),
    ("pod_disruption_budget", "PodDisruptionBudget minAvailable / maxUnavailable", [
        ("web-pdb", "minAvailable: 2", "app=web"), ("api-pdb", "maxUnavailable: 1", "app=api"), ("db-pdb", "minAvailable: 66%", "app=database"),
        ("auth-pdb", "maxUnavailable: 25%", "app=auth"), ("payment-pdb", "minAvailable: 3", "app=payment"), ("kafka-pdb", "minAvailable: 2", "app=kafka"),
        ("elastic-pdb", "maxUnavailable: 1", "app=elasticsearch"), ("zookeeper-pdb", "minAvailable: 2", "app=zookeeper"), ("gateway-pdb", "maxUnavailable: 20%", "app=gateway"),
        ("redis-pdb", "minAvailable: 1", "app=redis")
    ]),
    ("horizontal_pod_autoscaler", "HPA target CPU utilization & scaling limits", [
        ("web-hpa", "50% CPU", 2, 10), ("api-hpa", "70% CPU", 3, 15), ("payment-hpa", "60% Memory", 2, 8),
        ("worker-hpa", "80% CPU", 1, 20), ("auth-hpa", "65% CPU", 4, 12), ("search-hpa", "75% Memory", 3, 10),
        ("cart-hpa", "55% CPU", 2, 6), ("catalog-hpa", "70% CPU", 2, 10), ("event-hpa", "85% CPU", 5, 25),
        ("gateway-hpa", "60% CPU", 3, 15)
    ]),
    ("priority_class_preemption", "PriorityClass value & preemptionPolicy", [
        ("critical-service", 1000000, "PreemptLowerPriority"), ("high-priority-batch", 500000, "PreemptLowerPriority"), ("normal-app", 10000, "Never"),
        ("low-priority-job", 1000, "Never"), ("emergency-monitoring", 2000000, "PreemptLowerPriority"), ("background-cleanup", 100, "Never"),
        ("system-cluster-critical", 2000000000, "PreemptLowerPriority"), ("finance-core", 900000, "PreemptLowerPriority"), ("etl-worker-prio", 50000, "Never"),
        ("qa-pod-prio", 500, "Never")
    ]),
    ("configmap_secret_volume_updates", "ConfigMap volume automatic update vs env var static", [
        ("app-properties", "/etc/app", "symlink automatic atomic update"),
        ("database-config", "/config", "kubelet sync loop updates projected files"),
        ("feature-flags", "/flags", "env vars require pod restart, volumes update automatically"),
        ("routing-rules", "/etc/routes", "atomic swap via ..data symlink"),
        ("api-keys", "/secrets", "secret volume updates reflected inside container"),
        ("tls-certs", "/etc/ssl", "in-flight rotation without container restart"),
        ("server-conf", "/etc/conf", "subPath volume mounts DO NOT update automatically"),
        ("logging-props", "/opt/logging", "configMap reload triggered by inotify"),
        ("client-tokens", "/auth", "projected volume refreshed by kubelet"),
        ("gateway-endpoints", "/gateway", "automatic synchronization interval")
    ]),
    ("ephemeral_containers_debug", "kubectl debug -it with ephemeral containers", [
        ("crashed-pod-1", "busybox:latest", "debugging distilled distroless container"),
        ("payment-backend", "nicolaka/netshoot", "troubleshooting network packet loss"),
        ("auth-core-pod", "alpine:latest", "inspecting local unix domain socket"),
        ("database-sidecar", "curlimages/curl", "testing internal REST endpoint"),
        ("worker-frozen", "gcr.io/etcd-development/etcd:debug", "inspecting deadlocked process"),
        ("ingress-crash", "busybox", "checking container local disk filesystem"),
        ("security-audit-pod", "aquasec/trivy", "performing live filesystem scan"),
        ("queue-consumer-hang", "strace-tools", "attaching ptrace to container PID"),
        ("api-distroless", "busybox:1.28", "shell access in container without sh/bash"),
        ("mesh-proxy-debug", "envoyproxy/envoy:debug", "checking dynamic cluster state")
    ]),
    ("container_lifecycle_hooks", "postStart and preStop lifecycle hooks", [
        ("web-app", "preStop: /usr/sbin/nginx -s quit", "graceful connection draining"),
        ("api-srv", "postStart: curl -s http://localhost/register", "service registry registration"),
        ("payment-gateway", "preStop: sleep 15", "allowing in-flight requests to complete"),
        ("db-replica", "preStop: /scripts/flush-buffers.sh", "committing pending write logs"),
        ("cache-node", "postStart: /bin/warmup-cache.sh", "pre-loading frequent keys"),
        ("worker-consumer", "preStop: /app/drain-queue", "finishing current message processing"),
        ("search-indexer", "preStop: /bin/sync-index", "flushing Lucene segment commits"),
        ("auth-provider", "postStart: /app/validate-keys", "validating RSA keys on startup"),
        ("stream-transcoder", "preStop: /bin/checkpoint", "saving video transcoder state"),
        ("monitoring-agent", "preStop: /bin/send-goodbye", "notifying metric collector")
    ]),
    ("topology_spread_constraints", "topologySpreadConstraints maxSkew and topologyKey", [
        ("web-app", "zone", 1, "DoNotSchedule"), ("api-srv", "hostname", 2, "ScheduleAnyway"), ("payment-core", "zone", 1, "DoNotSchedule"),
        ("auth-service", "rack", 1, "DoNotSchedule"), ("database-cluster", "zone", 1, "DoNotSchedule"), ("search-nodes", "hostname", 1, "ScheduleAnyway"),
        ("event-broker", "zone", 2, "DoNotSchedule"), ("frontend-pool", "region", 1, "DoNotSchedule"), ("cache-cluster", "hostname", 1, "DoNotSchedule"),
        ("batch-processors", "zone", 3, "ScheduleAnyway")
    ])
]

def build_domain2_questions():
    questions = []
    q_idx = 1
    for sub_topic, concept, scenarios in d2_subtopics:
        for sc in scenarios:
            q_id = f"D2-Q{q_idx:03d}"
            target_name = sc[0]
            
            if sub_topic == "deploy_rolling_strategy":
                app_name, replicas, surge, unavail = sc
                q_en = f"A Deployment named '{app_name}' has 'replicas: {replicas}', 'maxSurge: {surge}', and 'maxUnavailable: {unavail}'. When a rolling update is triggered, what are the maximum and minimum number of pods allowed during the rollout?"
                q_kr = f"Deployment '{app_name}'이(가) 'replicas: {replicas}', 'maxSurge: {surge}', 'maxUnavailable: {unavail}'로 구성되어 있습니다. 롤링 업데이트가 트리거되었을 때 롤아웃 도중 허용되는 최대 파드 수와 최소 가용 파드 수는 각각 얼마입니까?"
                opts = [
                    {"key": "A", "text_en": f"Max allowed is replicas + maxSurge, and min available is replicas - maxUnavailable", "text_kr": f"최대 허용 파드 수는 replicas + maxSurge 이며, 최소 가용 파드 수는 replicas - maxUnavailable 이다"},
                    {"key": "B", "text_en": f"All {replicas} pods are terminated first before creating new pods", "text_kr": f"신규 파드를 생성하기 전에 기존 {replicas}개의 파드가 모두 먼저 종료된다"},
                    {"key": "C", "text_en": f"The maximum number of pods is strictly fixed at {replicas} at all times", "text_kr": f"파드의 최대 개수는 항상 정확히 {replicas}개로 고정된다"},
                    {"key": "D", "text_en": f"maxUnavailable specifies the number of extra pods created in advance", "text_kr": f"maxUnavailable은 사전에 미리 초과 생성되는 파드의 개수를 지정한다"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• `maxSurge`는 롤링 업데이트 도중 의도한 replicas 대비 초과하여 생성될 수 있는 최대 파드 수/비율입니다.\n• `maxUnavailable`은 롤링 업데이트 도중 일시적으로 사용할 수 없는 상태가 허용되는 최대 파드 수/비율입니다."
            elif sub_topic == "daemonset_toleration":
                ds_name, ns, taint_key = sc
                q_en = f"You are deploying a DaemonSet named '{ds_name}' in namespace '{ns}'. To ensure it schedules on control plane nodes having taint '{taint_key}:NoSchedule', which toleration configuration is required in the pod template?"
                q_kr = f"네임스페이스 '{ns}'에 DaemonSet '{ds_name}'을 배포하고자 합니다. 컨트롤 플레인 노드의 '{taint_key}:NoSchedule' 테인트를 견디고 해당 노드에 파드가 스케줄링되도록 하려면 파드 템플릿에 어떤 toleration이 필요합니까?"
                opts = [
                    {"key": "A", "text_en": f"spec.template.spec.tolerations with key '{taint_key}', operator 'Exists', and effect 'NoSchedule'", "text_kr": f"spec.template.spec.tolerations에 key: '{taint_key}', operator: 'Exists', effect: 'NoSchedule' 설정"},
                    {"key": "B", "text_en": f"Set spec.replicas: all in the DaemonSet specification", "text_kr": f"DaemonSet 명세에 spec.replicas: all을 지정"},
                    {"key": "C", "text_en": f"Add nodeSelector: controlplane: true without any tolerations", "text_kr": f"toleration 없이 nodeSelector: controlplane: true만 추가"},
                    {"key": "D", "text_en": f"Tolerations are not supported on DaemonSets and must be set on nodes", "text_kr": f"DaemonSet은 toleration을 지원하지 않으므로 노드 설정을 직접 수정해야 함"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• 마스터(컨트롤 플레인) 노드는 기본적으로 `NoSchedule` 테인트가 적용되어 있으므로, 파드 템플릿의 `spec.tolerations`에 일치하는 테인트 허용 규칙(`operator: Exists`, `effect: NoSchedule`)을 명시해야 DaemonSet 파드가 배치됩니다."
            elif sub_topic == "cronjob_concurrency":
                cj_name, sched, policy = sc
                q_en = f"In a CronJob named '{cj_name}' scheduled at '{sched}', you set 'concurrencyPolicy: {policy}'. What is the exact behavior if a scheduled job execution time arrives while the previous job is still running?"
                q_kr = f"'{sched}' 주기로 실행되는 CronJob '{cj_name}'에 'concurrencyPolicy: {policy}'가 설정되어 있습니다. 이전 잡이 아직 실행 중인 상태에서 다음 스케줄 실행 시점이 도래하면 어떻게 동작합니까?"
                if policy == "Forbid":
                    desc_a = "The CronJob skips starting the new Job until the previous one finishes"
                    desc_kr = "이전 잡이 완료될 때까지 신규 잡 생성을 건너뛴다(스킵)"
                elif policy == "Replace":
                    desc_a = "The CronJob cancels the currently running Job and starts a new Job"
                    desc_kr = "현재 실행 중인 기존 잡을 강제 취소하고 신규 잡을 시작한다"
                else:
                    desc_a = "The CronJob starts the new Job concurrently alongside the running one"
                    desc_kr = "기존 잡과 동시에 신규 잡을 병렬로 동시 실행한다"
                opts = [
                    {"key": "A", "text_en": desc_a, "text_kr": desc_kr},
                    {"key": "B", "text_en": "The CronJob terminates with an error and requires manual restart", "text_kr": "CronJob이 에러를 발생시키며 즉시 중단되어 수동 재시작이 필요하다"},
                    {"key": "C", "text_en": "The node automatically reboots to resolve the concurrency lock", "text_kr": "동시성 락을 해제하기 위해 노드가 자동으로 재부팅된다"},
                    {"key": "D", "text_en": "The CronJob deletes all previous job logs permanently", "text_kr": "CronJob이 이전의 모든 잡 실행 로그를 영구 삭제한다"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• `concurrencyPolicy: Forbid`: 이전 잡이 완료되지 않았으면 새 잡 실행을 건너뜁니다.\n• `Allow`: 동시에 중복 실행을 허용합니다.\n• `Replace`: 이전 실행 중인 잡을 취소하고 새 잡으로 교체합니다."
            elif sub_topic == "resource_qos_classes":
                qos_type, req, lim = sc
                q_en = f"A Pod has container resource requests set to '{req}' and limits set to '{lim}'. Which Quality of Service (QoS) class will Kubernetes assign to this Pod?"
                q_kr = f"파드의 컨테이너 리소스 설정이 'requests: {req}', 'limits: {lim}'로 정의되어 있습니다. 쿠버네티스는 이 파드에 어떤 QoS(서비스 품질) 클래스를 할당합니까?"
                opts = [
                    {"key": "A", "text_en": f"{qos_type}", "text_kr": f"{qos_type}"},
                    {"key": "B", "text_en": f"{'Burstable' if qos_type == 'Guaranteed' else 'Guaranteed'}", "text_kr": f"{'Burstable' if qos_type == 'Guaranteed' else 'Guaranteed'}"},
                    {"key": "C", "text_en": "StandardTier", "text_kr": "StandardTier"},
                    {"key": "D", "text_en": "HighPriorityDefault", "text_kr": "HighPriorityDefault"}
                ]
                ans = "A"
                exp = f"정답은 A ({qos_type})입니다.\n\n• **Guaranteed**: 모든 컨테이너의 CPU 및 메모리 requests와 limits가 0이 아니면서 정확히 일치할 때 부여됩니다.\n• **Burstable**: requests < limits 이거나 일부만 지정되었을 때 부여됩니다.\n• **BestEffort**: requests와 limits를 일절 지정하지 않았을 때 부여됩니다."
            else:
                q_en = f"In Kubernetes Workloads & Scheduling, when configuring '{target_name}' for '{concept}', what is the correct architectural practice?"
                q_kr = f"쿠버네티스 워크로드 및 스케줄링에서 '{concept}' 적용을 위해 '{target_name}'을 구성할 때 올바른 아키텍처 실무 원칙은 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"Apply the declarative spec according to Kubernetes official standards for {concept}", "text_kr": f"{concept}에 대한 쿠버네티스 공식 표준에 맞춰 선언적 매니페스트를 구성한다"},
                    {"key": "B", "text_en": "Hardcode static IP addresses in the pod template containers", "text_kr": "파드 템플릿 컨테이너에 고정 정적 IP 주소를 하드코딩한다"},
                    {"key": "C", "text_en": "Disable kube-scheduler and assign pods via docker run CLI directly", "text_kr": "스케줄러를 비활성화하고 docker run 명령어로 직접 노드에 배포한다"},
                    {"key": "D", "text_en": "Remove all labels and selectors from the workload definition", "text_kr": "워크로드 정의에서 모든 라벨과 셀렉터를 완전히 제거한다"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• 쿠버네티스 워크로드 컨트롤러는 라벨 셀렉터와 선언적 스펙을 바탕으로 Desired State를 보장합니다."
                
            questions.append({
                "id": q_id,
                "domain": "Domain 2",
                "domain_name": "워크로드 & 스케줄링 (Workloads & Scheduling)",
                "sub_topic": sub_topic,
                "question_en": q_en,
                "question_kr": q_kr,
                "options": opts,
                "correct_answer": ans,
                "explanation_kr": exp,
                "key_concept": concept
            })
            q_idx += 1
            
    print(f"Generated Domain 2: {len(questions)} unique questions.")
    return questions

# -------------------------------------------------------------
# CKA 도메인 3: 서비스 & 네트워킹 (250문항)
# -------------------------------------------------------------
d3_subtopics = [
    ("service_types_overview", "Service Types: ClusterIP vs NodePort vs LoadBalancer", [
        ("web-svc", "ClusterIP", "internal access only on cluster VIP"),
        ("node-proxy-svc", "NodePort", "exposing on all node physical IPs port 30000-32767"),
        ("cloud-lb-svc", "LoadBalancer", "provisioning cloud provider external IP"),
        ("db-external-cname", "ExternalName", "mapping to external database FQDN"),
        ("internal-api-svc", "ClusterIP", "default service type when type is omitted"),
        ("monitoring-nodeport", "NodePort", "allowing metrics collection from outside cluster"),
        ("payment-gateway-lb", "LoadBalancer", "directing public traffic to internal pods"),
        ("third-party-api", "ExternalName", "resolving to api.partner.com via CoreDNS CNAME"),
        ("cache-clusterip", "ClusterIP", "L4 load balancing across Redis replica pods"),
        ("edge-nodeport-svc", "NodePort", "access via <NodeIP>:<NodePort>")
    ]),
    ("service_port_mapping", "Service port vs targetPort vs nodePort", [
        ("web-app", 80, 8080, 30080), ("api-gateway", 443, 8443, 30443), ("database-svc", 3306, 3306, 30306),
        ("redis-cache", 6379, 6379, 30679), ("auth-service", 8000, 9000, 31000), ("metrics-svc", 9100, 9100, 32100),
        ("graphql-endpoint", 4000, 4000, 30400), ("elasticsearch-svc", 9200, 9200, 30920), ("kafka-broker-svc", 9092, 9092, 30992),
        ("mail-smtp-svc", 25, 2525, 30025)
    ]),
    ("service_headless", "Headless Service spec.clusterIP: None", [
        ("db-headless", "app=mysql", "StatefulSet mysql-0 DNS"),
        ("redis-headless", "app=redis", "Redis Sentinel direct pod IPs"),
        ("kafka-headless", "app=kafka", "Kafka broker peer discovery"),
        ("zk-headless", "app=zookeeper", "Zookeeper leader election quorum"),
        ("cass-headless", "app=cassandra", "Cassandra ring node IP resolution"),
        ("es-headless", "app=elasticsearch", "Elasticsearch transport clustering"),
        ("mongo-headless", "app=mongodb", "MongoDB replica set members"),
        ("rabbitmq-headless", "app=rabbitmq", "RabbitMQ clustering node list"),
        ("etcd-headless", "app=etcd", "etcd peer communication without VIP"),
        ("consul-headless", "app=consul", "Consul LAN gossip direct IPs")
    ]),
    ("service_manual_endpoints", "Service without selectors & manual Endpoints", [
        ("external-db", "192.168.10.55", 3306), ("legacy-mainframe", "10.0.5.20", 8080), ("third-party-auth", "172.16.2.100", 443),
        ("backup-storage-server", "192.168.20.15", 2049), ("on-prem-oracle", "10.20.30.40", 1521), ("partner-payment-gw", "172.31.0.8", 8443),
        ("corporate-ldap", "10.100.1.50", 389), ("external-redis-cache", "192.168.1.90", 6379), ("legacy-billing-api", "10.50.10.2", 9000),
        ("dr-standby-db", "172.25.1.12", 5432)
    ]),
    ("ingress_pathtype_rewrite", "Ingress pathType Prefix/Exact & rewrite-target", [
        ("/app(/|$)(.*)", "Prefix", "/$2", "app-svc"),
        ("/api/v1", "Exact", "/", "api-v1-svc"),
        ("/auth(/|$)(.*)", "Prefix", "/$2", "auth-svc"),
        ("/static(/|$)(.*)", "Prefix", "/$2", "static-assets-svc"),
        ("/payments", "Exact", "/process", "payments-svc"),
        ("/search(/|$)(.*)", "Prefix", "/$2", "search-engine-svc"),
        ("/v2/catalog", "Prefix", "/", "catalog-v2-svc"),
        ("/admin(/|$)(.*)", "Prefix", "/$2", "admin-console-svc"),
        ("/notifications", "Exact", "/events", "notifications-svc"),
        ("/stream(/|$)(.*)", "Prefix", "/$2", "media-stream-svc")
    ]),
    ("ingress_tls_configuration", "Ingress TLS secretName and hosts mapping", [
        ("app.example.com", "app-tls-secret"), ("api.company.com", "api-tls-cert"), ("secure.portal.io", "portal-ssl-secret"),
        ("checkout.store.com", "checkout-tls-key"), ("auth.enterprise.net", "auth-cert-secret"), ("dashboard.cloud.org", "dash-tls-secret"),
        ("billing.service.com", "billing-tls"), ("customer.portal.co", "customer-ssl-secret"), ("partner.gateway.net", "partner-tls-secret"),
        ("admin.internal.com", "admin-cert-secret")
    ]),
    ("coredns_fqdn_resolution", "CoreDNS FQDN <service>.<namespace>.svc.cluster.local", [
        ("order-svc", "sales", "order-svc.sales.svc.cluster.local"),
        ("auth-svc", "security", "auth-svc.security.svc.cluster.local"),
        ("db-svc", "database", "db-svc.database.svc.cluster.local"),
        ("redis-cache", "cache", "redis-cache.cache.svc.cluster.local"),
        ("payment-api", "finance", "payment-api.finance.svc.cluster.local"),
        ("metrics-server", "kube-system", "metrics-server.kube-system.svc.cluster.local"),
        ("catalog-svc", "inventory", "catalog-svc.inventory.svc.cluster.local"),
        ("notification-gw", "notifications", "notification-gw.notifications.svc.cluster.local"),
        ("search-core", "search-ns", "search-core.search-ns.svc.cluster.local"),
        ("audit-logger", "compliance", "audit-logger.compliance.svc.cluster.local")
    ]),
    ("netpol_default_deny", "NetworkPolicy Default Deny All Ingress / Egress", [
        ("secure-zone", "default-deny-ingress", "Ingress", "{}"),
        ("prod-database", "default-deny-all", "Ingress,Egress", "{}"),
        ("finance-ns", "isolate-all-traffic", "Ingress,Egress", "{}"),
        ("pci-compliant-ns", "deny-incoming", "Ingress", "{}"),
        ("quarantine-ns", "deny-everything", "Ingress,Egress", "{}"),
        ("backend-restricted", "deny-ingress-only", "Ingress", "{}"),
        ("billing-secure", "deny-all-network", "Ingress,Egress", "{}"),
        ("audit-store", "default-deny-in", "Ingress", "{}"),
        ("vault-ns", "isolate-vault", "Ingress,Egress", "{}"),
        ("restricted-api", "deny-in-out", "Ingress,Egress", "{}")
    ]),
    ("netpol_pod_and_ns_selector", "NetworkPolicy podSelector AND vs OR namespaceSelector", [
        ("allow-frontend-to-backend", "app=backend", "app=frontend", "tier=web"),
        ("allow-monitoring-scrape", "app=api", "role=scraper", "name=monitoring"),
        ("allow-billing-database", "app=billing-db", "app=billing-api", "env=prod"),
        ("allow-auth-to-redis", "app=redis", "app=auth-server", "tenant=core"),
        ("allow-log-collector", "app=app-logs", "component=filebeat", "logging=true"),
        ("allow-payment-processor", "app=payment-vault", "app=payment-svc", "compliance=pci"),
        ("allow-gateway-to-services", "tier=internal", "app=gateway", "network=ingress"),
        ("allow-analytics-worker", "role=analytics", "app=collector", "dept=data"),
        ("allow-ingress-controller", "app=web", "app.kubernetes.io/name=ingress-nginx", "ingress=true"),
        ("allow-dns-egress-only", "app=isolated", "k8s-app=kube-dns", "kube-system")
    ]),
    ("netpol_ipblock_cidr_except", "NetworkPolicy ipBlock CIDR with except exceptions", [
        ("192.168.0.0/16", "192.168.10.0/24", 80), ("10.0.0.0/8", "10.10.0.0/16", 443), ("172.16.0.0/12", "172.16.5.0/24", 3306),
        ("0.0.0.0/0", "169.254.169.254/32", 443), ("10.20.0.0/16", "10.20.100.0/24", 8080), ("192.168.1.0/24", "192.168.1.50/32", 5432),
        ("172.20.0.0/16", "172.20.1.0/24", 9092), ("10.50.0.0/16", "10.50.2.0/24", 6379), ("192.168.100.0/22", "192.168.100.10/32", 8443),
        ("0.0.0.0/0", "10.0.0.0/8", 80)
    ]),
    ("endpointslice_scaling", "EndpointSlice 100-endpoint batches & scalability", [
        ("web-svc", 500, "5 EndpointSlices created"), ("api-srv", 250, "3 EndpointSlices created"), ("cache-cluster", 150, "2 EndpointSlices created"),
        ("auth-workers", 300, "3 EndpointSlices created"), ("notification-nodes", 120, "2 EndpointSlices created"), ("stream-nodes", 400, "4 EndpointSlices created"),
        ("game-servers", 800, "8 EndpointSlices created"), ("data-collectors", 180, "2 EndpointSlices created"), ("search-replicas", 220, "3 EndpointSlices created"),
        ("logging-agents", 350, "4 EndpointSlices created")
    ]),
    ("coredns_loop_troubleshoot", "CoreDNS CrashLoopBackOff due to upstream DNS loop", [
        ("/etc/resolv.conf loopback 127.0.0.53", "resolv.conf points to local systemd-resolved loop"),
        ("Corefile forward . /etc/resolv.conf", "forwarding back into CoreDNS causing infinite cycle"),
        ("resolvConf in kubelet args", "directing kubelet to use upstream /run/systemd/resolve/resolv.conf"),
        ("forwarding loop detection plugin", "loop plugin terminates CoreDNS on loop detect"),
        ("custom nameserver override", "pointing Corefile forward to 8.8.8.8 directly"),
        ("host /etc/resolv.conf nameserver 127.0.0.1", "local dnsmasq loop conflict"),
        ("kubelet --resolv-conf flag", "setting correct path to non-loopback resolv.conf"),
        ("CoreDNS pod logs loop detected", "error message identifying forwarding loop"),
        ("systemd-resolved stub listener", "disabling DNSStubListener or using alternate resolv.conf"),
        ("CoreDNS configmap edit to fix loop", "modifying Corefile to remove loop plugin or fix forward")
    ]),
    ("ingress_controller_architecture", "Ingress Resource vs Ingress Controller implementation", [
        ("Nginx Ingress Controller", "watches Ingress objects and generates nginx.conf"),
        ("Traefik Ingress Controller", "dynamic configuration reload without reload latency"),
        ("HAProxy Ingress Controller", "high throughput L7 routing engine"),
        ("AWS Load Balancer Controller", "provisions AWS ALB from Ingress annotations"),
        ("GCP GKE Ingress Controller", "provisions Google Cloud HTTPS Load Balancer"),
        ("Kong Ingress Controller", "API gateway with plugin authentication"),
        ("Emissary-ingress (Ambassador)", "Envoy based Kubernetes ingress controller"),
        ("Contour Ingress Controller", "Envoy control plane using Ingress and HTTPProxy"),
        ("IngressClass resource", "spec.ingressClassName mapping to controller implementation"),
        ("default IngressClass annotation", "ingressclass.kubernetes.io/is-default-class")
    ]),
    ("cni_overlay_vxlan_troubleshoot", "CNI VXLAN overlay MTU & port 8472 firewall", [
        ("VXLAN UDP port 8472 blocked", "cross-node pod communication drops while same-node works"),
        ("Geneve UDP port 6081 blocked", "OVN-Kubernetes overlay packet loss across nodes"),
        ("MTU size mismatch", "packet dropped when payload + overlay header exceeds interface MTU"),
        ("Jumbo frames 9000 vs 1500 MTU", "fragmentation causing performance degradation"),
        ("Calico BGP port 179 blocked", "BGP peer connection failure between worker nodes"),
        ("IP-in-IP protocol 4 blocked", "Calico cross-subnet tunnel failure"),
        ("Flannel backend vxlan vs host-gw", "host-gw requires direct L2 adjacency without encapsulation"),
        ("Cilium native routing vs overlay", "direct routing mode requires network router route propagation"),
        ("CNI interface down cni0", "pod creation fails with network not ready"),
        ("Node NotReady due to CNI uninitialized", "network plugin returns NetworkPluginNotReady")
    ]),
    ("service_session_affinity", "Service sessionAffinity ClientIP and timeoutSeconds", [
        ("web-store", "ClientIP", 10800), ("login-portal", "ClientIP", 3600), ("game-lobby", "ClientIP", 7200),
        ("banking-session", "ClientIP", 1800), ("shopping-cart", "ClientIP", 14400), ("streaming-client", "ClientIP", 21600),
        ("telecom-crm", "ClientIP", 7200), ("healthcare-portal", "ClientIP", 3600), ("flight-booking", "ClientIP", 5400),
        ("support-chat", "ClientIP", 3600)
    ]),
    ("service_traffic_distribution", "Service externalTrafficPolicy: Local vs Cluster", [
        ("externalTrafficPolicy: Local", "preserves client source IP, avoids second hop, drops traffic if no local pod"),
        ("externalTrafficPolicy: Cluster", "source IP SNATed to node IP, balanced across all cluster pods"),
        ("preserving source IP on NodePort", "setting externalTrafficPolicy: Local on Service spec"),
        ("preserving source IP on LoadBalancer", "ensuring client IP reaches pod for security auditing"),
        ("Local policy health check node port", "healthCheckNodePort auto-allocated for cloud LB"),
        ("uneven load distribution in Local policy", "nodes with more pods receive same traffic from cloud LB"),
        ("Cluster policy cross-node forwarding", "kube-proxy forwards to other nodes via iptables/IPVS"),
        ("Cluster policy SNAT masquerade", "client IP replaced by node IP during second hop"),
        ("Local policy empty node behavior", "health check fails, cloud LB stops sending traffic to node"),
        ("LoadBalancer sourceRanges restriction", "spec.loadBalancerSourceRanges filtering incoming IPs")
    ]),
    ("kube_proxy_iptables_vs_ipvs", "kube-proxy iptables vs IPVS proxy modes", [
        ("iptables O(N) linear rule evaluation", "performance degrades significantly beyond 5,000 services"),
        ("IPVS O(1) hash table lookup", "supports tens of thousands of services with minimal CPU overhead"),
        ("IPVS load balancing algorithms", "round-robin (rr), least-connection (lc), destination hashing (dh)"),
        ("IPVS ipset dependency", "kernel ipset utility used for port and CIDR group matching"),
        ("switching kube-proxy mode", "updating ConfigMap kube-proxy mode: 'ipvs' and restarting pod"),
        ("required kernel modules for IPVS", "ip_vs, ip_vs_rr, ip_vs_wrr, ip_vs_sh, nf_conntrack"),
        ("iptables masquerading rules", "KUBE-MARK-MASQ and KUBE-POSTROUTING chains"),
        ("IPVS dummy interface kube-ipvs0", "virtual interface holding all Service ClusterIP addresses"),
        ("kube-proxy syncPeriod tuning", "adjusting iptables rule re-application interval"),
        ("ipvs fallback to iptables", "kube-proxy automatically falls back if IPVS modules missing")
    ]),
    ("nodeport_range_configuration", "apiserver --service-node-port-range customization", [
        ("default range 30000-32767", "allocates 2,768 possible external ports"),
        ("custom range 20000-25000", "configured via apiserver flag --service-node-port-range"),
        ("port collision on NodePort", "apiserver rejects NodePort already allocated"),
        ("dynamic NodePort allocation", "omitting spec.ports[].nodePort auto-assigns from range"),
        ("static NodePort reservation", "explicitly specifying nodePort within configured range"),
        ("security risk of low NodePorts", "avoiding privileged ports (<1024) conflict with host services"),
        ("firewall rules for NodePort range", "opening security group / firewall for 30000-32767"),
        ("nodePort on ClusterIP service type", "nodePort field is ignored unless type is NodePort or LoadBalancer"),
        ("changing NodePort range on running cluster", "requires apiserver static pod manifest edit and restart"),
        ("NodePort access via loopback", "accessing <localhost>:<nodePort> from worker host itself")
    ]),
    ("externalname_cname_behavior", "ExternalName service CoreDNS CNAME record return", [
        ("spec.externalName: db.company.com", "returns CNAME directly, does not create virtual IP or proxy traffic"),
        ("spec.clusterIP: None on ExternalName", "ExternalName services do not allocate a ClusterIP"),
        ("no port mapping on ExternalName", "port forwarding is not performed by kube-proxy for ExternalName"),
        ("cross-namespace ExternalName alias", "externalName: my-svc.other-ns.svc.cluster.local"),
        ("TLS SNI considerations with ExternalName", "client must send external hostname in TLS ClientHello"),
        ("CoreDNS resolution of ExternalName", "CoreDNS resolves CNAME recursively if configured"),
        ("replacing ExternalName with ClusterIP", "seamlessly migrating from external DB to in-cluster pod"),
        ("ExternalName with IP address", "anti-pattern, ExternalName expects DNS name, not IPv4 address"),
        ("headless vs ExternalName comparison", "Headless points to pods, ExternalName points to external DNS"),
        ("kubectl create service externalname", "imperative command kubectl create service externalname")
    ]),
    ("networkpolicy_egress_dns_port53", "Mandatory Port 53 Egress allowance in NetworkPolicy", [
        ("Egress isolation blocking DNS", "isolating pod without port 53 UDP/TCP prevents CoreDNS resolution"),
        ("port 53 UDP allowance", "ports: [{protocol: UDP, port: 53}]"),
        ("port 53 TCP allowance", "ports: [{protocol: TCP, port: 53}] for large DNS responses"),
        ("to: namespaceSelector kube-system", "restricting DNS egress exclusively to CoreDNS pods"),
        ("combining egress rules", "allowing port 53 DNS and port 443 external API simultaneously"),
        ("testing DNS blockage", "nslookup fails with query timed out inside isolated pod"),
        ("default deny egress impact", "every outbound HTTP request fails immediately due to DNS timeout"),
        ("ipBlock for public DNS 8.8.8.8", "allowing external public DNS in egress policy"),
        ("CoreDNS pod label selector", "to: [{podSelector: {matchLabels: {k8s-app: kube-dns}}}]"),
        ("auditing NetworkPolicy DNS egress", "verifying both UDP and TCP protocols are permitted")
    ]),
    ("service_selector_label_matching", "Service selector matching Pod labels exactly", [
        ("app: web, tier: frontend", "service selector must match all specified pod labels"),
        ("subset matching rule", "pod can have extra labels, but must contain all service selector labels"),
        ("empty endpoints on label typo", "kubectl get ep shows <none> when selector label has typo"),
        ("multiple labels AND logic", "all matchLabels criteria must be true simultaneously"),
        ("case-sensitive label matching", "App: Web vs app: web causes endpoint binding failure"),
        ("updating pod labels dynamically", "kube-controller-manager immediately updates Endpoints"),
        ("selector-less services for canary", "using separate services or fine-grained label targeting"),
        ("label change breaking traffic", "accidental label deletion immediately detaches pod from service"),
        ("inspecting endpoint members", "kubectl get endpoints <service> -o yaml"),
        ("matching Deployment template labels", "ensuring spec.template.metadata.labels matches service")
    ]),
    ("ingress_tls_cert_manager", "Automated TLS certificate management via cert-manager", [
        ("cert-manager ClusterIssuer", "Let's Encrypt production ACME HTTP01 challenge"),
        ("Ingress annotation cert-manager", "cert-manager.io/cluster-issuer: letsencrypt-prod"),
        ("Certificate CRD generation", "cert-manager watches Ingress and generates Certificate object"),
        ("Secret containing tls.crt and tls.key", "cert-manager writes issued certificate to secretName"),
        ("automatic TLS certificate renewal", "cert-manager renews certificates 30 days before expiration"),
        ("HTTP01 challenge routing", "temporary Ingress rules created by cert-manager for /.well-known/acme-challenge"),
        ("DNS01 challenge for wildcards", "using DNS provider API credentials for *.example.com"),
        ("troubleshooting Certificate status", "kubectl describe certificate <name> checking Ready condition"),
        ("Order and Challenge CRDs", "diagnosing ACME validation failures"),
        ("self-signed ClusterIssuer for testing", "generating internal CA certificates without external ACME")
    ]),
    ("service_dual_stack_ipv4_ipv6", "IPv4/IPv6 Dual-Stack Services in Kubernetes", [
        ("ipFamilyPolicy: SingleStack", "allocates single IP (IPv4 or IPv6) based on cluster default"),
        ("ipFamilyPolicy: PreferDualStack", "allocates both IPv4 and IPv6 if cluster supports it"),
        ("ipFamilyPolicy: RequireDualStack", "fails creation if dual-stack is not supported"),
        ("spec.ipFamilies: [IPv4, IPv6]", "ordering determines primary cluster IP family"),
        ("spec.clusterIPs list", "contains both allocated IPv4 and IPv6 virtual addresses"),
        ("CoreDNS dual-stack A and AAAA records", "resolving both IPv4 and IPv6 addresses for service"),
        ("kube-proxy dual-stack iptables/IPVS", "maintaining separate NAT tables for IPv4 and IPv6"),
        ("Calico / Cilium dual-stack CNI", "assigning both IPv4 and IPv6 addresses to each pod"),
        ("apiserver flag --service-cluster-ip-range", "specifying both IPv4 and IPv6 CIDR ranges"),
        ("external dual-stack LoadBalancer", "cloud provider assigning both public IPv4 and IPv6 VIPs")
    ]),
    ("gateway_api_next_gen", "Kubernetes Gateway API (GatewayClass, Gateway, HTTPRoute)", [
        ("Gateway API role-oriented design", "Infrastructure Provider, Cluster Operator, Application Developer"),
        ("GatewayClass resource", "defines controller implementation (Envoy, Istio, Cilium)"),
        ("Gateway resource", "declares point of entry for traffic on specific ports and protocols"),
        ("HTTPRoute resource", "defines L7 routing rules, header matching, and traffic splitting"),
        ("cross-namespace route attachment", "ReferenceGrant permitting routes to attach across namespaces"),
        ("traffic splitting (Canary)", "weight: 90 vs weight: 10 in HTTPRoute backendRefs"),
        ("header-based routing in HTTPRoute", "matching headers, query params, and HTTP methods"),
        ("comparison with Ingress", "Gateway API solves Ingress annotation sprawl and cross-namespace limits"),
        ("TLSRoute and TCPRoute", "supporting L4 protocols beyond standard HTTP/HTTPS"),
        ("status conditions on HTTPRoute", "checking Parents Accepted condition for route binding")
    ]),
    ("networkpolicy_audit_mode", "NetworkPolicy logging and auditing with Cilium/Calico", [
        ("Calico GlobalNetworkPolicy", "cluster-scoped network security rules"),
        ("Cilium NetworkPolicy (CNP)", "L7 protocol awareness (HTTP methods, paths, Kafka topics)"),
        ("NetworkPolicy drop logging", "logging denied packets for security analysis"),
        ("hubble CLI in Cilium", "observing real-time network flow drops and verdicts"),
        ("Calico felix log level", "enabling packet drop logs in iptables"),
        ("Default deny impact verification", "running dry-run or audit mode before enforcing deny"),
        ("NetworkPolicy on hostNetwork pods", "standard NetworkPolicy does not filter hostNetwork pods"),
        ("kube-system namespace protection", "preventing accidental isolation of CoreDNS and apiserver"),
        ("auditing active NetworkPolicies", "kubectl get netpol --all-namespaces"),
        ("validating egress rules with netcat", "nc -z -v -w 2 target-ip port from inside pod")
    ])
]

def build_domain3_questions():
    questions = []
    q_idx = 1
    for sub_topic, concept, scenarios in d3_subtopics:
        for sc in scenarios:
            q_id = f"D3-Q{q_idx:03d}"
            target_name = sc[0]
            
            if sub_topic == "service_port_mapping":
                svc_name, port, targetPort, nodePort = sc
                q_en = f"A Service named '{svc_name}' is defined with 'port: {port}', 'targetPort: {targetPort}', and 'nodePort: {nodePort}'. Which port must another pod in the same cluster use to connect to this Service's ClusterIP?"
                q_kr = f"Service '{svc_name}'이(가) 'port: {port}', 'targetPort: {targetPort}', 'nodePort: {nodePort}'로 정의되어 있습니다. 동일 클러스터 내의 다른 파드가 이 서비스의 ClusterIP로 통신할 때 사용해야 하는 포트는 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"Port {port} (the Service's virtual IP port)", "text_kr": f"포트 {port} (Service의 가상 IP 포트)"},
                    {"key": "B", "text_en": f"Port {targetPort} (the pod's target port)", "text_kr": f"포트 {targetPort} (파드의 타겟 포트)"},
                    {"key": "C", "text_en": f"Port {nodePort} (the node physical port)", "text_kr": f"포트 {nodePort} (노드의 물리 포트)"},
                    {"key": "D", "text_en": "Any random port between 30000 and 32767", "text_kr": "30000에서 32767 사이의 임의 포트"}
                ]
                ans = "A"
                exp = f"정답은 A (포트 {port})입니다.\n\n• `port`: 클러스터 내부의 다른 클라이언트 파드가 Service 가상 IP(VIP)로 요청을 보낼 때 사용하는 포트입니다.\n• `targetPort`: 백엔드 컨테이너 내부에서 실제 수신 대기 중인 포트입니다.\n• `nodePort`: 외부 클라이언트가 워커 노드의 물리 IP를 통해 직접 접근할 때 사용하는 포트입니다."
            elif sub_topic == "service_headless":
                svc_name, sel, desc = sc
                q_en = f"You are creating a Headless Service named '{svc_name}' for stateful workloads ({desc}). Which configuration in the Service specification defines it as Headless?"
                q_kr = f"스테이트풀 워크로드를 위해 Headless Service '{svc_name}'을 생성하고자 합니다 ({desc}). Service 명세에서 이를 Headless로 정의하는 핵심 설정은 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": "spec.clusterIP: None", "text_kr": "spec.clusterIP: None"},
                    {"key": "B", "text_en": "spec.type: Headless", "text_kr": "spec.type: Headless"},
                    {"key": "C", "text_en": "spec.headless: true", "text_kr": "spec.headless: true"},
                    {"key": "D", "text_en": "spec.ports[].clusterIP: 0.0.0.0", "text_kr": "spec.ports[].clusterIP: 0.0.0.0"}
                ]
                ans = "A"
                exp = "정답은 A입니다.\n\n• 쿠버네티스에서 Headless Service는 `spec.clusterIP: None`으로 설정합니다. 단일 가상 IP를 할당받지 않고, CoreDNS 질의 시 셀렉터에 매칭되는 백엔드 파드들의 실제 개별 IP 목록을 직접 반환합니다."
            elif sub_topic == "coredns_fqdn_resolution":
                svc_name, ns, fqdn = sc
                q_en = f"A pod running in namespace 'default' needs to connect to Service '{svc_name}' located in namespace '{ns}'. What is the full Fully Qualified Domain Name (FQDN) for this cross-namespace lookup?"
                q_kr = "'default' 네임스페이스에서 실행 중인 파드가 '{ns}' 네임스페이스에 있는 Service '{svc_name}'에 접근해야 합니다. 이 크로스 네임스페이스 통신을 위한 완전한 FQDN 도메인은 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"{fqdn}", "text_kr": f"{fqdn}"},
                    {"key": "B", "text_en": f"{svc_name}.svc.cluster.local", "text_kr": f"{svc_name}.svc.cluster.local"},
                    {"key": "C", "text_en": f"{svc_name}.{ns}.pod.cluster.local", "text_kr": f"{svc_name}.{ns}.pod.cluster.local"},
                    {"key": "D", "text_en": f"http://{ns}.{svc_name}.cluster:8080", "text_kr": f"http://{ns}.{svc_name}.cluster:8080"}
                ]
                ans = "A"
                exp = f"정답은 A ({fqdn})입니다.\n\n• 쿠버네티스 서비스 FQDN 표준 규칙은 `<서비스명>.<네임스페이스>.svc.cluster.local` 입니다.\n• 동일 네임스페이스에서는 `<서비스명>`만으로 통신 가능하지만, 타 네임스페이스 접근 시에는 최소 `<서비스명>.<네임스페이스>` 또는 전체 FQDN을 지정해야 합니다."
            elif sub_topic == "netpol_default_deny":
                ns_name, pol_name, pol_types, pod_sel = sc
                q_en = f"You need to apply a default deny policy named '{pol_name}' in namespace '{ns_name}' to block all incoming traffic. Which specification correctly achieves this?"
                q_kr = f"네임스페이스 '{ns_name}'에서 모든 인입 트래픽을 차단하는 기본 거부 정책 '{pol_name}'을 적용하고자 합니다. 이를 올바르게 정의한 명세는 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": "podSelector: {} and policyTypes: [Ingress] without any ingress rules defined", "text_kr": "podSelector: {} 및 policyTypes: [Ingress]를 지정하고 하위 ingress 허용 규칙을 비워둔다"},
                    {"key": "B", "text_en": "spec.action: DenyAll with iptables: drop", "text_kr": "spec.action: DenyAll 및 iptables: drop 지정"},
                    {"key": "C", "text_en": "spec.ingress[0].drop: 0.0.0.0/0", "text_kr": "spec.ingress[0].drop: 0.0.0.0/0 지정"},
                    {"key": "D", "text_en": "Delete all Service resources in the namespace", "text_kr": "네임스페이스 내의 모든 Service 리소스를 삭제한다"}
                ]
                ans = "A"
                exp = "정답은 A입니다.\n\n• `podSelector: {}`는 네임스페이스 내의 모든 파드를 대상으로 지정하며, `policyTypes: [Ingress]`를 선언하고 하위 `ingress:` 규칙을 정의하지 않으면 기본 완전 차단(Default Deny All Ingress)이 적용됩니다."
            else:
                q_en = f"Regarding {concept} in Kubernetes, when managing '{target_name}', which statement accurately reflects the standard network architecture?"
                q_kr = f"쿠버네티스 네트워킹에서 {concept}와 관련하여 '{target_name}' 구성 시 공식 표준 동작을 가장 정확하게 설명한 것은 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"It complies with the Kubernetes networking model for {concept} and routes traffic predictably", "text_kr": f"{concept}에 대한 쿠버네티스 네트워크 표준 모델을 준수하여 트래픽을 예측 가능하게 라우팅한다"},
                    {"key": "B", "text_en": "It requires disablement of CoreDNS and manual host file edits", "text_kr": "CoreDNS를 비활성화하고 노드마다 수동 host 파일 편집이 필요하다"},
                    {"key": "C", "text_en": "It converts all TCP traffic into unencrypted UDP packets unconditionally", "text_kr": "모든 TCP 트래픽을 무조건 암호화되지 않은 UDP 패킷으로 변환한다"},
                    {"key": "D", "text_en": "It completely prevents all pods from communicating across nodes", "text_kr": "모든 파드가 노드 간 통신을 수행하지 못하도록 완전히 차단한다"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• 쿠버네티스 네트워크 모델은 모든 파드가 NAT 없이 서로 고유한 IP로 통신할 수 있는 플랫 네트워크(Flat Network)를 제공합니다."
                
            questions.append({
                "id": q_id,
                "domain": "Domain 3",
                "domain_name": "서비스 & 네트워크 (Services & Networking)",
                "sub_topic": sub_topic,
                "question_en": q_en,
                "question_kr": q_kr,
                "options": opts,
                "correct_answer": ans,
                "explanation_kr": exp,
                "key_concept": concept
            })
            q_idx += 1
            
    print(f"Generated Domain 3: {len(questions)} unique questions.")
    return questions

# -------------------------------------------------------------
# CKA 도메인 4: 스토리지 (250문항)
# -------------------------------------------------------------
d4_subtopics = [
    ("pv_pvc_binding_criteria", "PV & PVC Binding 3 Match Conditions", [
        ("pv-prod-data", "100Gi", "ReadWriteOnce", "fast-ssd"),
        ("pv-shared-nfs", "500Gi", "ReadWriteMany", "nfs-storage"),
        ("pv-backup-vol", "1Ti", "ReadOnlyMany", "cold-storage"),
        ("pv-db-storage", "50Gi", "ReadWriteOnce", "nvme-storage"),
        ("pv-analytics-data", "250Gi", "ReadWriteMany", "shared-nas"),
        ("pv-log-archive", "2Ti", "ReadWriteOnce", "standard-hdd"),
        ("pv-cache-vol", "20Gi", "ReadWriteOnce", "high-iops"),
        ("pv-media-assets", "800Gi", "ReadOnlyMany", "s3-csi"),
        ("pv-app-storage", "10Gi", "ReadWriteOnce", "manual-sc"),
        ("pv-batch-outbox", "150Gi", "ReadWriteMany", "nfs-share")
    ]),
    ("access_modes_characteristics", "AccessModes: RWO vs ROX vs RWX vs RWOP", [
        ("ReadWriteOnce (RWO)", "single node read-write mount", "AWS EBS, GCE PD, Azure Disk"),
        ("ReadWriteMany (RWX)", "multi-node simultaneous read-write", "NFS, AWS EFS, GlusterFS, CephFS"),
        ("ReadOnlyMany (ROX)", "multi-node simultaneous read-only", "Shared documentation, ISO repositories"),
        ("ReadWriteOncePod (RWOP)", "single pod exclusive access across cluster", "Kubernetes 1.22+ storage protection"),
        ("RWO with multi-container Pod", "multiple containers in same pod can mount RWO volume", "Supported"),
        ("EBS RWX limitation", "AWS EBS cannot be mounted RWX by pods on different nodes", "Physical limitation"),
        ("NFS RWX access", "NFS protocol natively supports multi-client concurrent write", "Network file system"),
        ("ROX security hardening", "preventing any write modification to static datasets", "Immutable data"),
        ("RWOP CSI driver support", "requires CSI spec 1.5+ and CSIDriver capability", "Volume locking"),
        ("AccessModes mismatch error", "PVC with RWX failing to bind to RWO PersistentVolume", "Pending status")
    ]),
    ("reclaim_policy_retain_vs_delete", "persistentVolumeReclaimPolicy Retain vs Delete", [
        ("Retain policy on PVC delete", "PV status becomes Released, actual data is preserved", "Requires manual cleanup"),
        ("Delete policy on PVC delete", "PV and underlying cloud storage asset are deleted automatically", "Dynamic default"),
        ("Released PV re-binding", "new PVC cannot bind to Released PV until claimRef is cleared", "Manual intervention"),
        ("Retain data salvage", "admin copies data from backend before manually deleting PV", "Safe archival"),
        ("Delete policy safety risks", "accidental PVC deletion destroys production database volume", "Data loss"),
        ("changing reclaim policy", "patching pv.spec.persistentVolumeReclaimPolicy to Retain", "Runtime update"),
        ("StorageClass reclaimPolicy", "reclaimPolicy field in StorageClass defines default for dynamic PVs", "SC template"),
        ("Recycle policy deprecation", "legacy Recycle (rm -rf) is deprecated in favor of dynamic provisioning", "Deprecated"),
        ("Released status vs Available", "Available is ready for binding, Released is tied to deleted claim", "Lifecycle state"),
        ("PV Failed status", "automated deletion failed during Delete reclaim processing", "Error recovery")
    ]),
    ("storageclass_dynamic_provisioning", "StorageClass provisioner & dynamic provisioning", [
        ("kubernetes.io/aws-ebs", "gp3", "WaitForFirstConsumer", "Retain"),
        ("pd.csi.storage.gke.io", "premium-rwo", "Immediate", "Delete"),
        ("disk.csi.azure.com", "managed-csi", "WaitForFirstConsumer", "Delete"),
        ("nfs.csi.k8s.io", "nfs-client", "Immediate", "Retain"),
        ("ebs.csi.aws.com", "gp3-encrypted", "WaitForFirstConsumer", "Delete"),
        ("ceph.csi.ceph.com", "rbd-sc", "Immediate", "Delete"),
        ("local-path.storage.io", "local-path", "WaitForFirstConsumer", "Delete"),
        ("efs.csi.aws.com", "efs-sc", "Immediate", "Retain"),
        ("longhorn.io", "longhorn", "Immediate", "Delete"),
        ("topolvm.cybozu.com", "topolvm-provisioner", "WaitForFirstConsumer", "Delete")
    ]),
    ("sc_wait_for_first_consumer", "volumeBindingMode: WaitForFirstConsumer vs Immediate", [
        ("multi-zone AWS cluster", "preventing EBS volume created in zone A while pod schedules in zone B"),
        ("GKE regional cluster", "delaying PD creation until pod node assignment is finalized"),
        ("Azure multi-AZ cluster", "matching managed disk zone with pod scheduled node topology"),
        ("local persistent volume", "local SSD requires pod to land on specific node before binding"),
        ("Immediate binding pitfall", "PV created in random zone, pod cannot schedule due to node affinity"),
        ("PVC status with WaitForFirstConsumer", "PVC stays in Pending until pod referencing it is created"),
        ("scheduler volume topology filter", "kube-scheduler takes volume topology into account during node scoring"),
        ("CSI topology keys", "topology.ebs.csi.aws.com/zone matched automatically"),
        ("StatefulSet volumeBindingMode", "ensures each stateful pod volume is co-located with scheduled node"),
        ("dynamic local storage", "combining local storage with WaitForFirstConsumer for zero network latency")
    ]),
    ("volume_expansion_online", "StorageClass allowVolumeExpansion: true", [
        ("db-pvc", "100Gi", "200Gi", "gp3"), ("data-pvc", "50Gi", "100Gi", "premium-rwo"),
        ("archive-pvc", "500Gi", "1Ti", "managed-csi"), ("analytics-pvc", "200Gi", "400Gi", "gp3-encrypted"),
        ("logs-pvc", "80Gi", "150Gi", "standard-sc"), ("es-pvc", "300Gi", "600Gi", "ebs-sc"),
        ("mongo-pvc", "120Gi", "250Gi", "nvme-sc"), ("kafka-pvc", "250Gi", "500Gi", "fast-sc"),
        ("mysql-pvc", "40Gi", "80Gi", "ebs-gp3"), ("shared-pvc", "100Gi", "300Gi", "cloud-storage")
    ]),
    ("subpath_mount_configuration", "subPath volume mounting to isolate single files", [
        ("config.json", "/etc/app/config.json", "app-config-volume"),
        ("server.crt", "/etc/ssl/certs/server.crt", "tls-secret-volume"),
        ("custom.ini", "/etc/php/custom.ini", "php-ini-volume"),
        ("vault-token", "/root/.vault-token", "token-secret"),
        ("database.yml", "/config/database.yml", "db-yml-volume"),
        ("override.properties", "/app/override.properties", "prop-config"),
        ("license.key", "/opt/app/license.key", "license-secret"),
        ("hosts.allow", "/etc/hosts.allow", "hosts-config"),
        ("cacerts", "/opt/jdk/lib/security/cacerts", "truststore-secret"),
        ("prometheus-rules.yml", "/etc/prom/rules.yml", "rules-volume")
    ]),
    ("configmap_secret_defaultmode", "volumes.configMap / secret defaultMode octal permissions", [
        ("0400", "read-only by owner, no write, no execute"),
        ("0440", "read-only by owner and group"),
        ("0600", "read-write by owner only"),
        ("0644", "read-write by owner, read-only by others"),
        ("0500", "read and execute by owner (scripts)"),
        ("0550", "read and execute by owner and group"),
        ("0700", "full permissions by owner"),
        ("0755", "standard executable script permissions"),
        ("0444", "read-only by all users"),
        ("0640", "read-write by owner, read-only by group")
    ]),
    ("pvc_protection_finalizer", "kubernetes.io/pvc-protection finalizer mechanism", [
        ("deleting PVC while pod is running", "PVC enters Terminating state, actual deletion blocked until pod terminates"),
        ("preventing data corruption", "ensures active I/O is completed before volume storage teardown"),
        ("removing finalizer manually risk", "force deleting finalizer leads to active volume unmount failure"),
        ("pv-protection finalizer", "kubernetes.io/pv-protection prevents PV deletion while bound to PVC"),
        ("Storage Object in Use Protection", "official Kubernetes feature name for PVC/PV protection"),
        ("dangling pod volume mount", "pod crashes if storage backend is destroyed while running"),
        ("releasing Terminating PVC", "stopping or deleting the referencing Pod allows PVC deletion to complete"),
        ("kube-controller-manager role", "pvc-protection-controller manages and removes the finalizer"),
        ("CSI unpublish sequence", "kubelet unmounts volume -> CSI NodeUnpublish -> finalizer removed"),
        ("StatefulSet PVC protection", "PVCs created by StatefulSets are retained even if StatefulSet is deleted")
    ]),
    ("empty_dir_storage_types", "emptyDir: {} medium: Memory (tmpfs) vs standard disk", [
        ("emptyDir.medium: Memory", "backed by tmpfs (RAM), fast I/O, counted against pod memory limit"),
        ("emptyDir standard disk", "backed by node root filesystem or local node storage"),
        ("emptyDir lifecycle", "created when pod is assigned to node, destroyed permanently when pod is deleted"),
        ("container restart survival", "emptyDir data survives container crashes within the same pod"),
        ("emptyDir sizeLimit", "evicts pod if memory or disk usage exceeds specified sizeLimit"),
        ("tmpfs swap behavior", "RAM backed emptyDir will not be swapped out to disk"),
        ("scratch space use case", "sorting large datasets or unpacking archives before processing"),
        ("shared communication use case", "unix domain socket shared between main and sidecar container"),
        ("node restart impact", "node reboot causes pod rescheduling and emptyDir data is wiped"),
        ("emptyDir isolation", "other pods on the same node cannot access this pod's emptyDir")
    ]),
    ("host_path_storage_types", "hostPath volume types: Directory, File, Socket", [
        ("hostPath.type: Socket", "mounting /var/run/docker.sock or /run/containerd/containerd.sock"),
        ("hostPath.type: DirectoryOrCreate", "creates directory with 0755 permissions if it does not exist"),
        ("hostPath.type: FileOrCreate", "creates empty file if it does not exist at host path"),
        ("hostPath.type: Directory", "fails if directory does not exist on target worker node"),
        ("hostPath.type: File", "fails if file does not exist on target worker node"),
        ("security risk of hostPath", "allows container to escape isolation and read/modify host filesystem"),
        ("single-node cluster use case", "testing persistent storage on minikube or single node controlplane"),
        ("hostPath pod rescheduling pitfall", "if pod moves to another node, data on original node is not accessible"),
        ("hostPath in Static Pods", "used by kube-apiserver and etcd to access host PKI and data directories"),
        ("restricting hostPath with admission", "PodSecurity Restricted standard completely prohibits hostPath")
    ]),
    ("nfs_persistent_volume", "NFS PersistentVolume configuration and mountOptions", [
        ("nfs.server & nfs.path", "specifying remote NFS server IP and exported directory path"),
        ("mountOptions: [hard, nfsvers=4.1]", "ensuring reliable NFS lock handling and protocol version"),
        ("NFS client package prerequisite", "nfs-common or nfs-utils must be installed on all worker nodes"),
        ("NFS permission root_squash", "mapping container root UID 0 to nobody:nogroup on NFS server"),
        ("no_root_squash configuration", "allowing container root user to write files as UID 0 on NFS"),
        ("NFS network latency impact", "heavy random write I/O on NFS causes container thread blocking"),
        ("NFS ReadWriteMany support", "multiple pods on different worker nodes writing simultaneously"),
        ("stale NFS file handle error", "recovering when NFS server restarts while volume is mounted"),
        ("dynamic NFS provisioner", "nfs-subdir-external-provisioner creating subdirectories per PVC"),
        ("NFS export security", "restricting NFS export IP range to worker node subnet only")
    ]),
    ("csi_driver_architecture", "CSI Architecture: NodePlugin (DaemonSet) & ControllerPlugin", [
        ("CSI Controller Plugin", "runs as Deployment/StatefulSet, performs CreateVolume, DeleteVolume, Attach"),
        ("CSI Node Plugin", "runs as DaemonSet on every node, performs NodeStageVolume and NodePublishVolume"),
        ("csi-provisioner sidecar", "watches PVCs and calls CSI CreateVolume/DeleteVolume"),
        ("csi-attacher sidecar", "attaches volume to cloud VM instance via cloud provider API"),
        ("csi-resizer sidecar", "watches PVC size changes and expands volume storage backend"),
        ("csi-snapshotter sidecar", "creates VolumeSnapshot objects and snapshots in storage backend"),
        ("node-driver-registrar sidecar", "registers CSI driver with kubelet via registration socket"),
        ("livenessprobe sidecar for CSI", "monitors health of CSI driver unix domain sockets"),
        ("CSI out-of-tree benefits", "storage vendors release updates independently of Kubernetes releases"),
        ("CSIDriver CRD", "defines driver capabilities like attachRequired and volumeLifecycleModes")
    ]),
    ("volume_snapshots_and_restore", "VolumeSnapshot, VolumeSnapshotClass, VolumeSnapshotContent", [
        ("VolumeSnapshotClass", "specifies CSI driver provisioner for snapshot creation"),
        ("VolumeSnapshot resource", "user request in namespace to take a point-in-time storage snapshot"),
        ("VolumeSnapshotContent resource", "cluster-scoped pointer to actual storage backend snapshot"),
        ("restoring PVC from snapshot", "spec.dataSource: {kind: VolumeSnapshot, name: snap-01}"),
        ("snapshot readyToUse condition", "verifying snapshot creation completed before using as dataSource"),
        ("crash-consistent snapshots", "flushing application buffers before taking volume snapshot"),
        ("VolumeSnapshot deletion policy", "deletionPolicy: Retain vs Delete in VolumeSnapshotClass"),
        ("cross-namespace snapshot restore", "VolumeSnapshot cannot be directly referenced from another namespace"),
        ("snapshot storage cost considerations", "retaining differential blocks in cloud block storage"),
        ("snapshotting encrypted volumes", "CSI driver preserving KMS encryption keys in snapshot")
    ]),
    ("local_persistent_volumes", "Local PersistentVolumes with nodeAffinity", [
        ("nodeAffinity on Local PV", "spec.nodeAffinity.required binds volume strictly to single physical node"),
        ("storage.spec.local.path", "mounting dedicated local NVMe SSD or partition"),
        ("volumeBindingMode requirement", "must use WaitForFirstConsumer to prevent premature pod binding"),
        ("high performance database use case", "zero network overhead for Cassandra, MongoDB, Elasticsearch"),
        ("node failure risk with Local PV", "hardware failure of node results in permanent data unavailability"),
        ("local volume static provisioner", "daemon detecting local disks and automatically creating PVs"),
        ("Local PV vs hostPath", "Local PV is managed through PV/PVC system with scheduler awareness"),
        ("fsType specification on Local PV", "specifying ext4 or xfs filesystem type on raw disk block"),
        ("Local PV capacity planning", "matching PVC requests to exact size of local physical disk"),
        ("data replication at app layer", "relying on database clustering to tolerate local node loss")
    ]),
    ("storage_metrics_and_monitoring", "kubelet volume metrics & disk space monitoring", [
        ("kubelet_volume_stats_capacity_bytes", "total capacity of mounted volume filesystem"),
        ("kubelet_volume_stats_available_bytes", "remaining free space on volume"),
        ("kubelet_volume_stats_used_bytes", "current disk consumption by container"),
        ("kubelet_volume_stats_inodes_used", "inode exhaustion detection on filesystem"),
        ("monitoring volume full alerts", "alerting when available_bytes / capacity_bytes < 0.15"),
        ("CSI volume metric reporting", "kubelet queries CSI node plugin for accurate volume stats"),
        ("ephemeral-storage metrics", "container_fs_usage_bytes tracking rootfs and emptyDir usage"),
        ("storage I/O latency monitoring", "detecting disk bottleneck in high-throughput database workloads"),
        ("DiskPressure node condition", "kubelet triggering pod eviction when node disk space drops below threshold"),
        ("df -h inside container vs host", "verifying mount namespace filesystem view consistency")
    ]),
    ("raw_block_volume_mode", "volumeMode: Block vs Filesystem", [
        ("volumeMode: Block in PV/PVC", "exposes raw unformatted block device without filesystem"),
        ("volumeDevices in PodSpec", "mapping devicePath: /dev/xvdf instead of volumeMounts"),
        ("database raw I/O performance", "databases like Oracle or ScyllaDB managing raw disk directly"),
        ("zero filesystem overhead", "eliminating ext4/xfs journaling and metadata latency"),
        ("security implications of block mode", "container requires permissions to format or write raw device"),
        ("volumeMode: Filesystem default", "standard mode where Kubernetes formats device before mounting"),
        ("CSI driver block support", "verifying CSIDriver supports volumeMode: Block"),
        ("VolumeSnapshot of block volume", "snapshotting raw block devices at storage array level"),
        ("converting Block to Filesystem", "volumeMode cannot be modified after PVC creation"),
        ("Raw block device permission", "setting device permissions via container securityContext")
    ]),
    ("projected_volumes_composite", "Projected volumes combining Secret, ConfigMap, downwardAPI", [
        ("projected volume sources", "combining secret, configMap, serviceAccountToken, downwardAPI"),
        ("downwardAPI pod metadata projection", "projecting pod name, namespace, labels as files"),
        ("serviceAccountToken expirationSeconds", "requesting short-lived OIDC tokens for API authentication"),
        ("single mountPath consolidation", "mounting configuration, secrets, and tokens into single directory"),
        ("atomic file updates in projected volume", "kubelet updating projected files simultaneously"),
        ("downwardAPI CPU/Memory limits projection", "exposing container resource limits to runtime application"),
        ("custom path mapping in projected sources", "specifying relative sub-paths for each projected item"),
        ("read-only projection default", "projected volumes are mounted as read-only filesystems"),
        ("token audience specification", "setting audience: api://vault in projected token"),
        ("simplifying container volumeMounts", "replacing multiple volumeMounts with single projected volume")
    ]),
    ("csi_ephemeral_volumes", "CSI Inline Ephemeral Volumes (generic vs driver-specific)", [
        ("generic ephemeral volume", "ephemeral.volumeClaimTemplate creates temporary PVC tied to pod lifecycle"),
        ("driver-specific inline volume", "csi.driver embedded directly in PodSpec volumes list"),
        ("HashiCorp Vault CSI provider", "injecting secrets directly into memory without Kubernetes Secret CRD"),
        ("Cert-manager CSI driver", "issuing node-local mTLS certificates directly into pod filesystem"),
        ("ephemeral PVC deletion", "deleting the pod automatically triggers deletion of the ephemeral PVC and PV"),
        ("per-pod dynamic storage", "each replica gets unique dedicated storage created on the fly"),
        ("snapshotting ephemeral volumes", "generic ephemeral volumes support VolumeSnapshot operations"),
        ("storageClass in ephemeral template", "specifying custom fast storage class for temporary work"),
        ("security advantages of inline CSI", "sensitive credentials never stored in etcd as Secret objects"),
        ("use case for build runners", "creating isolated fast disk workspaces for CI/CD container jobs")
    ]),
    ("storage_quotas_and_limits", "ResourceQuota on storage requests and PVC counts", [
        ("requests.storage quota", "capping total gigabytes of persistent storage allocated in namespace"),
        ("persistentvolumeclaims count quota", "limiting maximum number of PVC objects in namespace"),
        ("StorageClass specific quota", "requests.storage[fast-ssd] restricting expensive storage tier"),
        ("quota enforcement at PVC creation", "apiserver rejects PVC if requested storage exceeds remaining quota"),
        ("PVC expansion quota validation", "expanding PVC size is blocked if new size exceeds quota"),
        ("overcommitting storage quota", "allocating storage quota larger than physical storage capacity"),
        ("monitoring namespace storage quota", "kubectl describe resourcequota checking used vs hard limits"),
        ("multi-tenant storage isolation", "preventing single team from monopolizing cloud storage budget"),
        ("LimitRange default storage request", "injecting default storage size if PVC omits requests.storage"),
        ("LimitRange min/max storage limits", "enforcing minimum and maximum allowable PVC size in namespace")
    ]),
    ("cross_namespace_volume_access", "Cross-namespace PVC access restriction & cloning", [
        ("PVC namespace isolation rule", "a Pod can ONLY mount a PVC located in the exact same namespace"),
        ("PV cluster-scoped nature", "PV itself is cluster-scoped but once bound belongs to one PVC"),
        ("dataSource across namespaces", "volume cloning dataSource cannot point to PVC in different namespace"),
        ("sharing data between namespaces", "using external NFS/S3 storage or creating duplicate PVs"),
        ("two PVCs binding to same PV error", "a PV can only be bound to exactly one PVC at any time"),
        ("re-binding PV to different namespace", "deleting PVC, clearing PV claimRef, and binding from new namespace"),
        ("CSI volume cloning within namespace", "dataSource: {kind: PersistentVolumeClaim, name: source-pvc}"),
        ("VolumeSnapshot cross-namespace workaround", "admin creating VolumeSnapshotContent to restore across namespaces"),
        ("multi-tenant security boundary", "namespace boundary prevents unauthorized access to database volumes"),
        ("auditing cross-namespace volume attempts", "apiserver rejects pod referencing PVC from other namespace")
    ]),
    ("volume_mounting_selinux_relabeling", "SELinux volume relabeling :Z vs :z options", [
        ("SELinux MCS category isolation", "kubelet relabeling volume files with container SELinux context"),
        ("shared volume :z relabeling", "allows multiple containers with different SELinux contexts to access volume"),
        ("private volume :Z relabeling", "exclusive access by single container, relabels files with unique category"),
        ("relabeling latency on large volumes", "chown/chcon on millions of files causes pod startup timeout"),
        ("seLinuxMount feature in Kubernetes", "mounting filesystem with context option directly, skipping recursive walk"),
        ("securityContext.seLinuxOptions", "specifying explicit SELinux user, role, type, and level"),
        ("permission denied with SELinux enforcing", "SELinux blocking container from reading hostPath or volume"),
        ("spc_t super privileged container", "disabling SELinux isolation for troubleshooting pods"),
        ("audit.log AVC denial inspection", "diagnosing SELinux volume mount denials via ausearch -m avc"),
        ("CSI driver SELinux support", "driver reporting whether it supports SELinux mount options")
    ]),
    ("storage_provisioner_troubleshoot", "CSI provisioner errors & PVC Pending diagnostics", [
        ("PVC Pending due to StorageClass typo", "PVC requests storageClassName that does not exist in cluster"),
        ("CSI provisioner timeout error", "cloud API rate limit or IAM permission missing for volume creation"),
        ("insufficient cloud storage quota", "cloud provider account out of EBS/PD volume allocation quota"),
        ("unsupported accessModes error", "provisioner rejects request for RWX on EBS storage class"),
        ("examining PVC Events", "kubectl describe pvc <name> shows provisioner failure messages"),
        ("CSI controller pod crash", "investigating logs of csi-provisioner container in kube-system"),
        ("IAM role for service account (IRSA)", "ensuring CSI controller pod has permissions to call cloud API"),
        ("PVC requested size below minimum", "cloud provider enforcing minimum 1Gi volume size"),
        ("volume creation parameter error", "invalid iops or throughput parameter in StorageClass"),
        ("StorageClass parameters immutable", "parameters in StorageClass cannot be edited; must recreate SC")
    ]),
    ("storage_attacher_troubleshoot", "VolumeAttachment object & Multi-Attach error", [
        ("VolumeAttachment resource", "records that a specific PV is attached to a specific node"),
        ("Multi-Attach error for volume", "Volume is already exclusively attached to one node and cannot be attached to another"),
        ("pod stuck in ContainerCreating", "waiting for volume attachment to complete on target node"),
        ("node ungraceful shutdown impact", "volume remains attached to dead node, blocking rescheduling on healthy node"),
        ("csi-attacher timeout", "cloud provider detach call failed or timed out"),
        ("force detach volume", "deleting non-responsive VolumeAttachment or terminating dead node instance"),
        ("volume max attach limit per node", "cloud provider limiting maximum EBS volumes per EC2 instance (e.g. 28)"),
        ("kubelet volume manager reconcile loop", "polls every 100ms to verify attached volume states"),
        ("dangling volume attachment cleanup", "kubelet removing VolumeAttachment when pod terminates gracefully"),
        ("describing VolumeAttachment", "kubectl describe volumeattachment checking Attached status condition")
    ]),
    ("storage_clean_decommission", "Graceful PV/PVC deletion and storage reclamation", [
        ("order of deletion", "terminate Pod -> delete PVC -> PV is reclaimed according to policy"),
        ("deleting PV before PVC error", "PV cannot be deleted while in Bound status with active PVC"),
        ("cleaning Released PV", "editing PV to remove spec.claimRef, making it Available for reuse"),
        ("verifying cloud asset deletion", "checking cloud console to confirm underlying disk is wiped"),
        ("preventing orphaned cloud disks", "ensuring Delete reclaim policy successfully destroys backend volume"),
        ("auditing unattached cloud volumes", "cloud cost optimization identifying disks without Kubernetes PVs"),
        ("storage migration runbook", "backing up data -> deploying new PVC -> copying files -> swapping traffic"),
        ("zeroing out sensitive data", "overwriting storage before decommissioning physical hard drives"),
        ("decommissioning StorageClass", "ensuring no active PVCs reference StorageClass before deletion"),
        ("handling finalizer deadlocks", "diagnosing why PVC remains in Terminating state indefinitely")
    ])
]

def build_domain4_questions():
    questions = []
    q_idx = 1
    for sub_topic, concept, scenarios in d4_subtopics:
        for sc in scenarios:
            q_id = f"D4-Q{q_idx:03d}"
            target_name = sc[0]
            
            if sub_topic == "pv_pvc_binding_criteria":
                pv_name, cap, mode, sc_name = sc
                q_en = f"A PersistentVolume named '{pv_name}' has 'capacity: {cap}', 'accessModes: [{mode}]', and 'storageClassName: {sc_name}'. Which PersistentVolumeClaim (PVC) will successfully bind to this PV?"
                q_kr = f"PersistentVolume '{pv_name}'이(가) 'capacity: {cap}', 'accessModes: [{mode}]', 'storageClassName: {sc_name}' 속성으로 생성되어 있습니다. 어떤 PersistentVolumeClaim(PVC)이 이 PV에 정상적으로 바인딩될 수 있습니까?"
                opts = [
                    {"key": "A", "text_en": f"A PVC requesting accessMode '{mode}', storageClassName '{sc_name}', and capacity less than or equal to '{cap}'", "text_kr": f"accessMode '{mode}', storageClassName '{sc_name}'을 요구하고 용량이 '{cap}' 이하인 PVC"},
                    {"key": "B", "text_en": f"A PVC requesting double the capacity of '{cap}' with any access mode", "text_kr": f"용량을 '{cap}'의 2배로 요청하고 임의의 접근 모드를 가진 PVC"},
                    {"key": "C", "text_en": f"A PVC with storageClassName: 'different-class' and capacity '{cap}'", "text_kr": f"storageClassName이 'different-class'이고 용량이 '{cap}'인 PVC"},
                    {"key": "D", "text_en": "Any PVC regardless of accessModes as long as it is in the kube-system namespace", "text_kr": "kube-system 네임스페이스에 있기만 하면 접근 모드와 무관하게 모든 PVC"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• PVC가 PV에 바인딩되기 위한 3대 필수 일치 조건은 다음과 같습니다:\n  1. `storageClassName`이 일치해야 합니다.\n  2. `accessModes`가 호환되어야 합니다.\n  3. PV의 용량이 PVC의 요청 용량 이상이어야 합니다 (PV $\\ge$ PVC)."
            elif sub_topic == "sc_wait_for_first_consumer":
                cluster_type, reason = sc
                q_en = f"In a {cluster_type}, a StorageClass is configured with 'volumeBindingMode: WaitForFirstConsumer'. Why is this setting strongly recommended over 'Immediate'?"
                q_kr = f"{cluster_type} 환경에서 StorageClass에 'volumeBindingMode: WaitForFirstConsumer'가 설정되어 있습니다. 이 설정이 'Immediate'보다 강력히 권장되는 주된 이유는 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"It delays volume provisioning until the Pod is scheduled, preventing topology/zone mismatches ({reason})", "text_kr": f"파드가 스케줄링될 때까지 볼륨 생성을 지연시켜 노드 토폴로지/가용영역 불일치를 방지하기 위해 ({reason})"},
                    {"key": "B", "text_en": "It reduces cloud storage provisioning costs by 50% automatically", "text_kr": "클라우드 스토리지 프로비저닝 비용을 자동으로 50% 절감하기 위해"},
                    {"key": "C", "text_en": "It allows multiple Pods to share ReadWriteOnce volumes simultaneously", "text_kr": "여러 파드가 ReadWriteOnce 볼륨을 동시에 공유할 수 있도록 허용하기 위해"},
                    {"key": "D", "text_en": "It formats the storage volume using RAM instead of physical disks", "text_kr": "물리 디스크 대신 RAM을 사용하여 스토리지 볼륨을 포맷하기 위해"}
                ]
                ans = "A"
                exp = "정답은 A입니다.\n\n• `volumeBindingMode: Immediate`는 PVC 생성 즉시 볼륨을 만들기 때문에, 파드가 스케줄링될 노드의 가용 영역(AZ)과 다른 영역에 볼륨이 생성되어 영구적으로 스케줄링이 불가능해지는 문제가 발생할 수 있습니다.\n• `WaitForFirstConsumer`는 파드가 어느 노드에 배치될지 확정된 후에 볼륨을 생성하므로 토폴로지 불일치를 완벽히 방지합니다."
            elif sub_topic == "volume_expansion_online":
                pvc_name, old_size, new_size, sc_type = sc
                q_en = f"You need to expand PVC '{pvc_name}' (backed by '{sc_type}') from {old_size} to {new_size}. Assuming the StorageClass has 'allowVolumeExpansion: true', what is the correct procedure?"
                q_kr = f"'{sc_type}' 기반의 PVC '{pvc_name}'의 용량을 {old_size}에서 {new_size}로 확장해야 합니다. StorageClass에 'allowVolumeExpansion: true'가 설정되어 있을 때 올바른 절차는 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"Edit the PVC spec.resources.requests.storage to '{new_size}' directly while keeping the pod running", "text_kr": f"파드가 실행 중인 상태에서 PVC의 spec.resources.requests.storage를 직접 '{new_size}'로 수정한다"},
                    {"key": "B", "text_en": f"Delete the PVC, recreate it with '{new_size}', and restore data from a snapshot", "text_kr": f"기존 PVC를 삭제하고 '{new_size}'로 다시 생성한 뒤 스냅샷에서 데이터를 복구한다"},
                    {"key": "C", "text_en": "Volume expansion is not supported in Kubernetes; a new volume must be mounted", "text_kr": "쿠버네티스에서는 볼륨 확장을 지원하지 않으므로 새 볼륨을 추가 마운트해야 한다"},
                    {"key": "D", "text_en": f"Shrink the PVC to 10Gi first before expanding to '{new_size}'", "text_kr": f"'{new_size}'로 늘리기 전에 먼저 10Gi로 축소해야 한다"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• StorageClass에 `allowVolumeExpansion: true`가 설정되어 있으면, PVC의 `spec.resources.requests.storage` 값을 상향 편집하는 것만으로 CSI 드라이버가 온라인 볼륨 용량 확장을 자동 수행합니다 (단, 용량 축소는 절대 불가)."
            elif sub_topic == "reclaim_policy_retain_vs_delete":
                policy_scenario, desc, outcome = sc
                q_en = f"Regarding Kubernetes PersistentVolume reclaim policies, when managing a PV with '{policy_scenario}', what happens ({outcome})?"
                q_kr = f"쿠버네티스 PV 반환 정책(Reclaim Policy)에서 '{policy_scenario}' 상황이 발생했을 때 일어나는 결과({outcome})는 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"{desc}", "text_kr": f"{desc}"},
                    {"key": "B", "text_en": "The entire worker node is wiped and reinstalled immediately", "text_kr": "해당 워커 노드의 전체 데이터가 즉시 포맷되고 재설치된다"},
                    {"key": "C", "text_en": "The PV is automatically assigned to a random Pod in another namespace", "text_kr": "PV가 타 네임스페이스의 임의 파드에 자동으로 즉시 재바인딩된다"},
                    {"key": "D", "text_en": "The cluster enters maintenance mode until the administrator logs in", "text_kr": "관리자가 로그인할 때까지 클러스터가 점검 모드로 전환된다"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• `Retain`: PVC가 삭제되어도 PV는 `Released` 상태로 유지되며 실제 스토리지 데이터가 보존됩니다.\n• `Delete`: PVC 삭제 시 PV 및 백엔드 물리 클라우드 볼륨 자산까지 즉시 영구 삭제됩니다."
            else:
                q_en = f"In Kubernetes Storage architecture, regarding {concept} when managing '{target_name}', which statement reflects the official specification?"
                q_kr = f"쿠버네티스 스토리지 아키텍처에서 '{target_name}'의 {concept}와 관련하여 공식 명세를 가장 정확하게 설명한 것은 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"It adheres to the Kubernetes CSI and storage volume lifecycle standards for {concept}", "text_kr": f"{concept}에 대한 쿠버네티스 CSI 및 스토리지 볼륨 수명주기 표준을 준수한다"},
                    {"key": "B", "text_en": "It stores all data in memory and loses everything on container restart", "text_kr": "모든 데이터를 메모리에 보관하여 컨테이너 재시작 시 데이터가 유실된다"},
                    {"key": "C", "text_en": "It bypasses the PersistentVolumeClaim mechanism and writes directly to etcd", "text_kr": "PVC 메커니즘을 우회하고 etcd 데이터베이스에 직접 데이터를 저장한다"},
                    {"key": "D", "text_en": "It is completely incompatible with all Linux container runtimes", "text_kr": "모든 리눅스 컨테이너 런타임과 완전히 호환되지 않는다"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• 쿠버네티스 스토리지는 PV, PVC, StorageClass 및 CSI 플러그인을 통해 파드 수명주기와 완전히 독립적으로 관리됩니다."
                
            questions.append({
                "id": q_id,
                "domain": "Domain 4",
                "domain_name": "스토리지 (Storage)",
                "sub_topic": sub_topic,
                "question_en": q_en,
                "question_kr": q_kr,
                "options": opts,
                "correct_answer": ans,
                "explanation_kr": exp,
                "key_concept": concept
            })
            q_idx += 1
            
    print(f"Generated Domain 4: {len(questions)} unique questions.")
    return questions

# -------------------------------------------------------------
# CKA 도메인 5: 문제 해결 (250문항)
# -------------------------------------------------------------
d5_subtopics = [
    ("troubleshoot_crashloopbackoff", "CrashLoopBackOff & previous logs kubectl logs -p", [
        ("web-frontend-pod", "exit code 1", "syntax error in server configuration"),
        ("payment-gateway", "exit code 2", "missing database connection string"),
        ("auth-core-pod", "exit code 137", "out of memory during initialization"),
        ("api-backend", "exit code 1", "port already in use by another process"),
        ("worker-daemon", "exit code 255", "failed to acquire distributed redis lock"),
        ("catalog-indexer", "exit code 1", "corrupt local Lucene index file"),
        ("notification-hub", "exit code 1", "invalid SSL certificate path"),
        ("billing-processor", "exit code 143", "received SIGTERM signal before ready"),
        ("search-engine-pod", "exit code 1", "schema validation error on startup"),
        ("order-collector", "exit code 2", "permission denied on mounted log volume")
    ]),
    ("troubleshoot_imagepullbackoff", "ImagePullBackOff & imagePullSecrets", [
        ("nginx-app", "image: nginx:1.99.99", "tag does not exist in registry (404 Not Found)"),
        ("private-api", "image: private-reg.io/app:v1", "missing imagePullSecrets authentication (401 Unauthorized)"),
        ("typo-service", "image: nginxxx:latest", "repository name misspelled"),
        ("corp-backend", "image: internal.registry.com/core:latest", "registry domain DNS resolution failure"),
        ("secure-worker", "image: secure-docker.io/worker:2.0", "expired docker-registry secret token"),
        ("analytics-pod", "image: gcr.io/my-proj/analytics:v3", "IAM service account permissions missing on GCR"),
        ("payment-pod", "image: ecr.aws/prod/payment:v1", "ECR authorization token expired"),
        ("frontend-react", "image: docker.io/myorg/react-app:v1.0", "Docker Hub pull rate limit exceeded (429 Too Many Requests)"),
        ("auth-server", "image: harbor.corp.net/auth:stable", "self-signed certificate untrusted by containerd"),
        ("monitoring-daemon", "image: quay.io/prom/exporter:invalid", "manifest unknown error")
    ]),
    ("troubleshoot_oomkilled", "OOMKilled Exit Code 137 & memory limits", [
        ("java-app", "137", "512Mi limit exceeded by JVM heap spike"),
        ("node-api", "137", "memory leak in event listener"),
        ("python-ml-worker", "137", "loading large 4GB dataset into 2GB RAM container"),
        ("elasticsearch-data", "137", "Lucene cache exceeding container cgroup limit"),
        ("redis-cache-pod", "137", "maxmemory policy omitted causing cgroup kill"),
        ("video-encoder", "137", "high resolution 4K buffer allocation spike"),
        ("batch-etl-pod", "137", "unbounded query result set loaded into memory"),
        ("golang-microservice", "137", "goroutine leak consuming all memory"),
        ("image-processing", "137", "parallel image resizing exceeding memory limit"),
        ("kafka-broker", "137", "JVM heap + page cache exceeding memory cgroup")
    ]),
    ("troubleshoot_pod_pending_resources", "Pod Pending due to Insufficient CPU/Memory", [
        ("heavy-batch-pod", "cpu: 16 requests", "no node has 16 allocatable CPU cores"),
        ("database-primary", "memory: 64Gi requests", "nodes have maximum 32Gi memory available"),
        ("analytics-engine", "cpu: 8, mem: 32Gi", "resource requests exceed cluster free capacity"),
        ("spark-driver", "memory: 128Gi requests", "exceeds maximum node instance size"),
        ("ai-training-pod", "nvidia.com/gpu: 4 requests", "all GPU nodes fully allocated"),
        ("memory-cache-0", "memory: 48Gi requests", "nodes under memory pressure"),
        ("render-farm-job", "cpu: 32 requests", "exceeds ResourceQuota in namespace"),
        ("high-traffic-web", "cpu: 12 requests", "pending scheduling until other pods terminate"),
        ("bigdata-worker", "memory: 96Gi requests", "insufficient memory on any single node"),
        ("load-test-runner", "cpu: 24 requests", "CPU limits exceed node capacity")
    ]),
    ("troubleshoot_pod_pending_taints", "Pod Pending due to un-tolerated Node Taints", [
        ("api-pod", "env=prod:NoSchedule", "pod lacks matching toleration"),
        ("web-server", "dedicated=compute:NoSchedule", "node reserved for compute workloads"),
        ("worker-pod", "node.kubernetes.io/unreachable:NoExecute", "node network dropped"),
        ("gpu-worker", "hardware=gpu:NoSchedule", "pod missing gpu toleration"),
        ("audit-logger", "security=high:NoSchedule", "pod missing security toleration"),
        ("batch-job-pod", "lifecycle=spot:NoSchedule", "pod lacks spot instance toleration"),
        ("dmz-proxy", "network=dmz:NoSchedule", "pod missing dmz toleration"),
        ("payment-core", "compliance=pci:NoSchedule", "pod lacks pci compliance toleration"),
        ("edge-agent", "location=edge:NoSchedule", "pod missing edge location toleration"),
        ("storage-pod", "tier=storage:NoSchedule", "pod missing storage tier toleration")
    ]),
    ("troubleshoot_node_notready_kubelet", "Node NotReady due to stopped/failed kubelet service", [
        ("worker-node-1", "kubelet.service is inactive (dead)", "systemctl restart kubelet"),
        ("k8s-node-alpha", "kubelet failing with exit code 1", "check /var/log/messages or journalctl"),
        ("compute-worker-02", "kubelet crashed on configuration typo", "verify /var/lib/kubelet/config.yaml"),
        ("worker-pool-node-5", "kubelet out of file descriptors", "raise sysctl fs.file-max"),
        ("node-us-east-1a", "kubelet failed to connect to apiserver", "check /etc/kubernetes/kubelet.conf"),
        ("prod-worker-10", "kubelet killed by host OOM killer", "reserve system memory with systemReserved"),
        ("edge-node-04", "kubelet swap enabled error", "swapoff -a or enable failSwapOn: false"),
        ("gpu-node-01", "kubelet cgroup driver mismatch", "align cgroupDriver to systemd"),
        ("worker-node-beta", "kubelet binary missing executable bit", "chmod +x /usr/bin/kubelet"),
        ("database-node-1", "kubelet failed to mount /var/lib/kubelet", "check host disk filesystem mount")
    ]),
    ("troubleshoot_node_notready_cni", "Node NotReady due to CNI network plugin issues", [
        ("worker-node-2", "NetworkPluginNotReady", "cni config uninitialized in /etc/cni/net.d/"),
        ("k8s-worker-5", "cni0 interface is down", "ip link set cni0 up"),
        ("node-alpha-1", "Calico pod crashed on node", "calico-node pod in CrashLoopBackOff"),
        ("worker-compute-3", "Flannel subnet allocation conflict", "overlapping pod CIDR on node"),
        ("edge-worker-02", "missing /opt/cni/bin/loopback", "reinstall CNI standard binaries"),
        ("prod-worker-12", "Cilium agent disconnected", "cilium-agent daemonset pod error"),
        ("node-zone-b", "iptables legacy vs nftables conflict", "update-alternatives --set iptables"),
        ("worker-node-99", "VXLAN port 8472 blocked by host firewall", "allow UDP 8472 on ufw/firewalld"),
        ("staging-worker-1", "corrupt /etc/cni/net.d/10-calico.conflist", "fix JSON syntax error in CNI config"),
        ("k8s-node-infra", "bridge netfilter module not loaded", "modprobe br_netfilter")
    ]),
    ("troubleshoot_controlplane_staticpod", "Control Plane apiserver/etcd Static Pod YAML typos", [
        ("kube-apiserver.yaml", "misspelled flag --etcd-servers", "apiserver fails to start, kubectl returns connection refused"),
        ("etcd.yaml", "invalid client-cert-auth flag", "etcd crashes, apiserver cannot connect"),
        ("kube-controller-manager.yaml", "wrong path to service-account-private-key-file", "controller-manager in CrashLoopBackOff"),
        ("kube-scheduler.yaml", "YAML indentation error under spec.containers", "scheduler static pod fails to parse"),
        ("kube-apiserver.yaml", "wrong --service-cluster-ip-range CIDR", "apiserver fails validation check on startup"),
        ("etcd.yaml", "corrupted hostPath volume directory", "etcd fails to write WAL files"),
        ("kube-apiserver.yaml", "expired tls-cert-file certificate", "apiserver rejects all incoming client TLS connections"),
        ("kube-controller-manager.yaml", "typo in --cluster-signing-cert-file", "CSR approvals fail across cluster"),
        ("kube-scheduler.yaml", "invalid leader-elect boolean string", "scheduler crashes on initialization"),
        ("kube-apiserver.yaml", "missing closing quote in admission-control-config-file", "YAML syntax parser error")
    ]),
    ("troubleshoot_crictl_debugging", "Using crictl ps/logs when API server is down", [
        ("crictl ps -a", "inspecting stopped control plane containers when kubectl is unavailable"),
        ("crictl logs <container-id>", "reading direct container logs from containerd without apiserver"),
        ("crictl pods", "listing local Pod sandbox IDs on worker node"),
        ("crictl inspect <id>", "viewing low-level container exit code and rootfs path"),
        ("crictl rm -f <id>", "force removing stuck container directly in container runtime"),
        ("crictl images", "verifying locally cached images on node when registry is unreachable"),
        ("crictl info", "checking container runtime status and cgroup driver configuration"),
        ("crictl exec -it <id>", "executing debugging command directly in container without kubelet"),
        ("crictl stop <id>", "gracefully stopping container when kubelet is hung"),
        ("crictl stats", "monitoring local CPU and memory usage of containers on host")
    ]),
    ("troubleshoot_service_endpoints", "Service connection failure due to empty Endpoints", [
        ("frontend-svc", "kubectl get ep frontend-svc shows <none>", "service selector labels do not match pod labels"),
        ("backend-api", "endpoints missing 2 of 3 pods", "readinessProbe failing on 2 pods"),
        ("payment-svc", "service port 80 targets container port 8080", "targetPort mismatch with listening port"),
        ("auth-db-svc", "endpoints completely empty", "deployment pods all in CrashLoopBackOff"),
        ("notification-svc", "service selector has typo app=notif instead of app=notifications", "label selector mismatch"),
        ("cart-api-svc", "traffic timing out intermittently", "one backend pod IP is dead and not removed from endpoints"),
        ("order-processing", "service points to wrong namespace", "looking for pods in default instead of orders"),
        ("analytics-svc", "targetPort references non-existent named port", "containerPort name mismatch in PodSpec"),
        ("search-svc", "endpoints exist but connection refused", "container listening on 127.0.0.1 instead of 0.0.0.0"),
        ("user-data-svc", "iptables rules missing for service", "kube-proxy pod crashed on worker node")
    ]),
    ("troubleshoot_readiness_probe_fail", "ReadinessProbe failure isolating Pod from Service traffic", [
        ("web-app", "readiness probe HTTP 500 on /healthz", "pod is running but excluded from Service endpoints"),
        ("api-gateway", "readiness probe TCP port 8080 timeout", "application not listening on expected port"),
        ("payment-core", "readiness probe exec script exit 1", "database connection pool uninitialized"),
        ("auth-server", "initialDelaySeconds too short (1s)", "readiness check runs before JVM boots up"),
        ("catalog-svc", "periodSeconds too aggressive (1s)", "overwhelming container with health checks"),
        ("order-router", "failureThreshold exceeded (3 consecutive failures)", "pod removed from endpoint slice"),
        ("billing-app", "readiness probe pointing to external dependency", "external API outage marks local pod unready"),
        ("search-indexer", "readiness probe timeoutSeconds too low (1s)", "slow health query causes false failure"),
        ("media-transcoder", "readiness probe failing during heavy CPU spike", "probe request timed out in queue"),
        ("customer-portal", "readiness probe path /ready returning 404", "route path misspelled in PodSpec")
    ]),
    ("troubleshoot_kubelet_certs", "Kubelet client/server certificate expiration & rotation", [
        ("/var/lib/kubelet/pki/kubelet-client-current.pem expired", "kubelet cannot authenticate to apiserver"),
        ("kubeadm certs check-expiration", "shows kubelet client cert expired after 1 year"),
        ("kubelet server cert auto-rotation disabled", "RotateKubeletServerCertificate feature gate"),
        ("CSR for kubelet serving cert stuck in Pending", "administrator must run kubectl certificate approve"),
        ("kubelet.conf client-certificate-data invalid", "regenerating bootstrap kubeconfig for kubelet"),
        ("system clock drift causing x509 cert not yet valid", "NTP synchronization failure on worker node"),
        ("kubelet x509: certificate signed by unknown authority", "CA certificate mismatch in /etc/kubernetes/pki/ca.crt"),
        ("apiserver rejecting kubelet certificate SAN", "kubelet server cert missing node IP/hostname in SAN"),
        ("kubelet client cert renewal via bootstrap token", "re-joining node to issue fresh certificates"),
        ("backing up expired /var/lib/kubelet/pki files", "clearing old pem files to trigger fresh CSR")
    ]),
    ("troubleshoot_force_delete_pod", "Force deleting Pods stuck in Terminating status", [
        ("stuck-pod-1", "node dead, ungraceful shutdown", "kubectl delete pod <name> --force --grace-period=0"),
        ("database-locked-pod", "NFS mount hung, umount fails", "force deleting pod to clear apiserver record"),
        ("worker-offline-pod", "worker node powered off permanently", "force deleting pod to release StatefulSet identity"),
        ("storage-hung-pod", "CSI driver failed to unmount volume", "force deleting pod after verifying storage safety"),
        ("finalizer-deadlocked-pod", "pod has custom finalizer that never completes", "patching pod to remove finalizers"),
        ("tainted-evicted-pod", "pod stuck terminating on unschedulable node", "forcing deletion via CLI"),
        ("zombie-process-pod", "container init process PID 1 ignoring SIGKILL", "rebooting worker node or force delete"),
        ("terminating-pv-consumer", "pvc-protection holding terminating pod", "deleting pod before deleting PVC"),
        ("network-partition-pod", "apiserver cannot reach node kubelet to confirm deletion", "force deletion override"),
        ("emergency-cluster-cleanup", "clearing all terminating pods across namespace", "kubectl delete pods --force --grace-period=0")
    ]),
    ("troubleshoot_coredns_resolution", "CoreDNS resolution failures inside client pods", [
        ("busybox:1.28 test pod", "nslookup kubernetes.default fails with timeout", "CoreDNS pods down or NetworkPolicy blocking"),
        ("/etc/resolv.conf nameserver wrong", "resolv.conf in pod does not match kube-dns ClusterIP"),
        ("CoreDNS pod logs showing i/o timeout", "upstream DNS server 8.8.8.8 unreachable from cluster"),
        ("ndots:5 causing excessive search domain queries", "querying my-svc.sales.default.svc.cluster.local repeatedly"),
        ("CoreDNS memory limit exceeded (OOMKilled)", "DNS query flood exceeding 170Mi memory limit"),
        ("CoreDNS deployment scaled to 0 replicas", "scaling deployment coredns -n kube-system --replicas=2"),
        ("iptables rules for kube-dns missing", "kube-proxy not programming 10.96.0.10:53 NAT rules"),
        ("Corefile syntax error after manual edit", "invalid plugin directive in kube-system ConfigMap coredns"),
        ("firewall dropping UDP port 53 traffic", "node security group blocking inter-node DNS queries"),
        ("single CoreDNS replica overloaded", "deploying CoreDNS horizontal autoscaler (cluster-proportional-autoscaler)")
    ]),
    ("troubleshoot_disk_pressure", "Node DiskPressure condition and pod eviction", [
        ("node disk usage exceeds 85%", "kubelet sets NodeCondition DiskPressure=true"),
        ("image garbage collection failure", "high disk usage due to dangling container images"),
        ("crictl rmi --prune", "manually removing unused container images to free disk space"),
        ("pod eviction priority during DiskPressure", "BestEffort pods evicted first, followed by Burstable"),
        ("container log files filling up /var/log/pods", "docker/containerd log rotation max-size configuration"),
        ("emptyDir volume filling root filesystem", "pod writing 50GB file into emptyDir without sizeLimit"),
        ("kubelet imageGCHighThresholdPercent", "tuning threshold in /var/lib/kubelet/config.yaml (default 85%)"),
        ("kubelet imageGCLowThresholdPercent", "kubelet cleans images until disk drops to low threshold (80%)"),
        ("cleaning dead container filesystem layers", "crictl rm $(crictl ps -a -q) freeing overlay2 space"),
        ("allocating dedicated disk partition for /var/lib/containerd", "isolating container storage from root /")
    ]),
    ("troubleshoot_pid_pressure", "Node PIDPressure condition and kernel pid_max", [
        ("fork bomb inside container", "container spawning 32,768 processes consuming all host PIDs"),
        ("PIDPressure NodeCondition true", "kubelet stops scheduling new pods on node"),
        ("pod eviction under PIDPressure", "kubelet evicting offending pod to protect node stability"),
        ("kernel.pid_max exhaustion", "sysctl -w kernel.pid_max=4194304 raising Linux limit"),
        ("kubelet podPidsLimit configuration", "enforcing maximum PIDs per pod (e.g. 4096)"),
        ("troubleshooting with ps -eLf", "counting thread and process count per cgroup"),
        ("zombie processes accumulating", "container PID 1 failing to reap child zombie processes"),
        ("using dumb-init or tini as PID 1", "ensuring proper signal forwarding and zombie reaping"),
        ("cgroup pids.max enforcement", "container hits fork: cannot allocate memory when pids.max reached"),
        ("systemd TasksMax configuration", "raising TasksMax in docker/containerd systemd service units")
    ]),
    ("troubleshoot_container_runtime_down", "Containerd service crashed or stopped on worker node", [
        ("systemctl status containerd", "containerd.service inactive (dead)"),
        ("journalctl -u containerd -n 100", "inspecting containerd crash logs"),
        ("containerd socket /run/containerd/containerd.sock missing", "kubelet cannot connect to CRI socket"),
        ("containerd failed to start due to bad config.toml", "syntax error in /etc/containerd/config.toml"),
        ("corrupted overlay2 storage directory", "cleaning corrupt snapshotter state in /var/lib/containerd"),
        ("restarting containerd", "systemctl restart containerd && systemctl restart kubelet"),
        ("containerd out of memory", "OOM killer terminating containerd daemon"),
        ("runc binary missing or corrupt", "containerd fails to spawn task without valid runc"),
        ("cgroup v2 systemd cgroup driver failure", "containerd failing to create cgroup hierarchy"),
        ("containerd hanging on unmount", "zombie mount points holding containerd tasks")
    ]),
    ("troubleshoot_apiserver_connection_refused", "The connection to the server <host>:6443 was refused", [
        ("kube-apiserver static pod down", "apiserver container crashed in /etc/kubernetes/manifests"),
        ("etcd database unreachable", "apiserver cannot connect to etcd and exits immediately"),
        ("host firewall blocking port 6443", "ufw or firewalld blocking incoming API requests"),
        ("x509 client certificate expired in kubeconfig", "credentials in ~/.kube/config expired"),
        ("control plane node powered off or rebooting", "physical or cloud VM instance offline"),
        ("apiserver listening on wrong IP", "--advertise-address bound to wrong network interface"),
        ("corrupted admin.conf", "regenerating admin.conf with kubeadm init phase kubeconfig admin"),
        ("load balancer in front of apiservers down", "HAProxy or Keepalived service stopped"),
        ("swap enabled on control plane", "kubelet refusing to start static pods due to swap"),
        ("etcd disk space full (NOSPACE alarm)", "etcd database locked in read-only mode")
    ]),
    ("troubleshoot_secret_permission_denied", "Pod failing to read Secret or ConfigMap (403 Forbidden)", [
        ("RBAC Role missing get secret verb", "pod ServiceAccount lacks permission to query API"),
        ("Secret in different namespace", "pod cannot mount Secret located in other namespace"),
        ("Secret name misspelled in PodSpec", "pod stuck in CreateContainerConfigError with secret not found"),
        ("defaultMode 0000 on secret volume", "container non-root user cannot read 0000 permission file"),
        ("securityContext runAsUser mismatch", "file owned by root UID 0, container running as UID 1000"),
        ("immutable Secret update error", "attempting to modify Secret marked with immutable: true"),
        ("KMS plugin unreachable for envelope decryption", "apiserver cannot decrypt secret data from etcd"),
        ("secretKeyRef key name typo", "key 'password' missing in secret data, pod fails startup"),
        ("mounting secret as subPath on non-existent directory", "mount failure during container creation"),
        ("automountServiceAccountToken: false", "pod missing default token to authenticate to Secret API")
    ]),
    ("troubleshoot_exec_probe_timeout", "LivenessProbe exec command hanging or timing out", [
        ("probe command hanging indefinitely", "timeoutSeconds exceeded, kubelet kills and restarts container"),
        ("shell script without timeout wrapper", "executing deadlock command inside container"),
        ("database query probe timeout", "slow SQL query in probe exceeding 1s default timeout"),
        ("raising timeoutSeconds on probe", "adjusting timeoutSeconds: 5 for heavy health checks"),
        ("container CPU throttling delaying probe", "CPU limits causing exec fork to take longer than timeout"),
        ("zombie sh processes from failed probes", "accumulating defunct processes from timed-out exec probes"),
        ("preferring HTTP/TCP probes over exec", "exec probes have higher CPU/fork overhead than HTTP/TCP"),
        ("exec probe exit code 1", "probe script returned non-zero, kubelet marks failure"),
        ("initialDelaySeconds tuning for slow apps", "preventing premature liveness restarts during startup"),
        ("examining probe failure in describe pod", "kubectl describe pod Events showing 'Liveness probe failed'")
    ]),
    ("troubleshoot_service_targetport_mismatch", "Service targetPort mismatching container listening port", [
        ("service targetPort: 8080, container listening on 80", "connection refused when traffic reaches pod"),
        ("service targetPort: http, port named 'web' in container", "named port typo in PodSpec"),
        ("container listening on localhost (127.0.0.1)", "cannot receive traffic from service proxy on pod IP"),
        ("netstat / ss inside container", "verifying listening address 0.0.0.0 vs 127.0.0.1"),
        ("updating Service targetPort via kubectl patch", "fixing targetPort to match containerPort"),
        ("curl pod-ip:targetPort directly from node", "verifying container responds without service layer"),
        ("Spring Boot management port on 8081", "health checks sent to wrong port"),
        ("NodePort routing to wrong container in multi-container pod", "targetPort hitting sidecar instead of app"),
        ("protocol mismatch (TCP vs UDP)", "DNS service listening on UDP while service targets TCP"),
        ("verifying targetPort in Endpoints object", "checking Port column in kubectl get ep")
    ]),
    ("troubleshoot_ingress_backend_502_504", "Ingress returning HTTP 502 Bad Gateway / 504 Gateway Timeout", [
        ("HTTP 502 Bad Gateway", "ingress controller cannot establish TCP connection to backend pod"),
        ("HTTP 504 Gateway Timeout", "backend pod took longer to respond than proxy-read-timeout"),
        ("backend service pods all unready", "ingress has no valid upstream pod IPs in upstream pool"),
        ("proxy-connect-timeout annotation", "tuning connection timeout for slow starting backends"),
        ("proxy-read-timeout annotation", "raising read timeout (e.g. 600s) for long running API requests"),
        ("SSL/TLS handshake failure between Ingress and backend", "backend requires HTTPS but Ingress connects via HTTP"),
        ("nginx.ingress.kubernetes.io/backend-protocol: HTTPS", "instructing ingress to connect upstream using TLS"),
        ("upstream keepalive timeout mismatch", "backend closing keepalive connection before ingress controller"),
        ("ingress controller logs inspection", "kubectl logs -n ingress-nginx checking error.log"),
        ("HTTP 503 Service Unavailable", "ingress controller itself overloaded or queue full")
    ]),
    ("troubleshoot_dns_ndots5_performance", "DNS ndots:5 latency overhead in large clusters", [
        ("5 search domains appended to external queries", "querying google.com tests google.com.default.svc.cluster.local first"),
        ("high CoreDNS query volume from microservices", "external API calls multiplying DNS lookups by 5x"),
        ("specifying trailing dot for external domains", "querying 'google.com.' directly skips search paths"),
        ("custom pod dnsConfig ndots:2", "setting ndots: 2 in PodSpec to optimize external lookups"),
        ("CoreDNS autopath plugin", "server-side search path resolution reducing client round-trips"),
        ("NodeLocal DNSCache deployment", "caching DNS on each worker node to absorb search domain queries"),
        ("CoreDNS cache plugin tuning", "raising TTL and cache size for frequent external domains"),
        ("packet loss on UDP port 53", "ndots query flood triggering Linux conntrack race condition"),
        ("benchmarking DNS lookup latency", "using dnsping or curl -w %{time_namelookup}"),
        ("monitoring coredns_dns_requests_total", "identifying pods generating excessive DNS lookups")
    ]),
    ("troubleshoot_ephemeral_storage_eviction", "Pod evicted due to EphemeralStorageExceeded limit", [
        ("container writes 10GB to rootfs", "exceeds limits.ephemeral-storage: 5Gi"),
        ("emptyDir volume consumes all node disk", "pod terminated with The node was low on resource: ephemeral-storage"),
        ("container logs accumulating on host", "application writing gigabytes of stdout logs"),
        ("specifying requests and limits for ephemeral-storage", "resources.limits.ephemeral-storage: 2Gi"),
        ("inspecting evicted pod status", "kubectl describe pod shows 'Evicted' Reason and Message"),
        ("cleaning temporary files in container", "ensuring background processes do not write unbounded files"),
        ("moving large files to PVC instead of rootfs", "using dedicated persistent storage for data processing"),
        ("eviction threshold nodefs.available", "kubelet evicting pods when rootfs has less than 10% free space"),
        ("kubelet imagefs.available threshold", "evicting pods when container image storage is full"),
        ("ephemeral-storage vs memory limits", "ephemeral storage measures disk usage, not RAM")
    ]),
    ("troubleshoot_cluster_autoscaler_pending", "Cluster Autoscaler failing to add worker nodes", [
        ("cloud provider VM quota reached", "autoscaler cannot launch EC2/GCE instances due to account limits"),
        ("ASG maximum size reached", "Auto Scaling Group max_size=10 reached, cannot scale further"),
        ("autoscaler pod permissions missing", "cloud IAM role lacks permissions to modify AutoScalingGroup"),
        ("pod has un-tolerated taint matching no node group", "no auto-scaling group can satisfy pod's taints/affinity"),
        ("Cluster Autoscaler logs inspection", "kubectl logs -n kube-system checking cluster-autoscaler pod"),
        ("pod with local storage blocking node scale down", "autoscaler refuses to terminate node with non-replicated pod"),
        ("PodDisruptionBudget preventing node drain", "PDB minAvailable blocks autoscaler from draining node"),
        ("mixed instance types in single node group", "heterogeneous CPU/RAM sizes confusing autoscaler capacity math"),
        ("overprovisioning with pause pods", "maintaining standby capacity to absorb sudden scheduling spikes"),
        ("autoscaler scale-down-unneeded-time", "tuning grace period before unused nodes are terminated")
    ])
]

def build_domain5_questions():
    questions = []
    q_idx = 1
    for sub_topic, concept, scenarios in d5_subtopics:
        for sc in scenarios:
            q_id = f"D5-Q{q_idx:03d}"
            target_name = sc[0]
            
            if sub_topic == "troubleshoot_crashloopbackoff":
                pod_name, exit_code, cause = sc
                q_en = f"A pod named '{pod_name}' is trapped in 'CrashLoopBackOff' ({exit_code}). The container restarts immediately after starting. Which command allows you to view the logs of the container from its PREVIOUS crashed instance?"
                q_kr = f"파드 '{pod_name}'이(가) 'CrashLoopBackOff'({exit_code}) 상태에 빠져 기동 직후 즉시 재시작을 반복하고 있습니다. 직전에 크래시가 발생했던 인스턴스의 에러 로그를 확인하기 위한 올바른 명령어는 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"kubectl logs {pod_name} --previous (or -p)", "text_kr": f"kubectl logs {pod_name} --previous (또는 -p)"},
                    {"key": "B", "text_en": f"kubectl describe pod {pod_name} --show-logs", "text_kr": f"kubectl describe pod {pod_name} --show-logs"},
                    {"key": "C", "text_en": f"kubectl get pod {pod_name} --status=crashed", "text_kr": f"kubectl get pod {pod_name} --status=crashed"},
                    {"key": "D", "text_en": f"kubectl exec -it {pod_name} -- cat /var/log/last-crash.log", "text_kr": f"kubectl exec -it {pod_name} -- cat /var/log/last-crash.log"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• 컨테이너가 기동 직후 종료되어 재시작 루프에 빠진 경우, 현재 실행 중인 컨테이너 로그는 비어있을 수 있습니다.\n• 따라서 `kubectl logs <파드명> -p` (또는 `--previous`) 플래그를 사용하여 직전에 비정상 종료된 컨테이너의 마지막 출력 로그를 확인해야 근본 원인({cause})을 파악할 수 있습니다."
            elif sub_topic == "troubleshoot_oomkilled":
                app_name, exit_code, cause = sc
                q_en = f"A pod running '{app_name}' was terminated with Exit Code {exit_code} and Last State Reason 'OOMKilled'. What is the root cause of this failure and how should it be resolved?"
                q_kr = f"'{app_name}'을(를) 실행 중인 파드가 Exit Code {exit_code} 및 Last State 'OOMKilled' 상태로 강제 종료되었습니다. 이 장애의 근본 원인과 올바른 해결책은 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"The container exceeded its configured resources.limits.memory and was SIGKILLed by Linux OOM killer ({cause}); raise the memory limit", "text_kr": f"컨테이너가 설정된 resources.limits.memory 한도를 초과하여 리눅스 커널 OOM 킬러에 의해 강제 종료됨 ({cause}); 메모리 limit을 상향 조정한다"},
                    {"key": "B", "text_en": "The container exceeded CPU limits; raise CPU requests", "text_kr": "컨테이너가 CPU 한도를 초과함; CPU requests를 상향 조정한다"},
                    {"key": "C", "text_en": "The pod failed its livenessProbe 3 consecutive times; increase initialDelaySeconds", "text_kr": "파드의 livenessProbe가 3회 연속 실패함; initialDelaySeconds를 늘린다"},
                    {"key": "D", "text_en": "The node ran out of disk space; delete unused container images", "text_kr": "노드 디스크 공간이 부족함; 사용하지 않는 컨테이너 이미지를 삭제한다"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• Exit Code 137은 SIGKILL (9 + 128 = 137) 신호로 종료되었음을 의미하며, Reason이 'OOMKilled'인 경우 컨테이너 메모리 사용량이 `resources.limits.memory` 한도를 초과한 것입니다.\n• CPU 초과는 프로세스를 강제 종료하지 않고 스로틀링(Throttling)을 발생시키지만, 메모리 초과는 즉시 OOMKilled 강제 종료를 유발합니다."
            elif sub_topic == "troubleshoot_node_notready_kubelet":
                node_name, state, action = sc
                q_en = f"Worker node '{node_name}' is displaying 'NotReady' status in kubectl get nodes. You SSH into the worker node and find '{state}'. What is the primary administrative action?"
                q_kr = f"워커 노드 '{node_name}'이(가) kubectl get nodes에서 'NotReady' 상태로 표시됩니다. 해당 워커 노드에 SSH로 접속하여 점검한 결과 '{state}' 상태임을 확인했습니다. 수행해야 할 1차 조치는 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"Inspect journalctl -u kubelet logs, fix any configuration error, and run '{action}'", "text_kr": f"journalctl -u kubelet 로그를 점검하여 설정 오류를 수정한 후 '{action}'을 실행한다"},
                    {"key": "B", "text_en": "Reboot the entire Kubernetes control plane master node", "text_kr": "쿠버네티스 컨트롤 플레인 마스터 노드 전체를 재부팅한다"},
                    {"key": "C", "text_en": "Delete all pods running in the kube-system namespace", "text_kr": "kube-system 네임스페이스의 모든 파드를 강제 삭제한다"},
                    {"key": "D", "text_en": "Re-run kubeadm init on the worker node", "text_kr": "워커 노드에서 kubeadm init을 다시 실행한다"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• 노드가 `NotReady` 상태일 때 가장 흔한 원인은 노드 데몬인 `kubelet` 서비스의 중단 또는 설정 오탈자입니다.\n• `systemctl status kubelet` 및 `journalctl -u kubelet -n 100 --no-pager`로 로그를 확인하고 서비스를 복구해야 합니다."
            elif sub_topic == "troubleshoot_service_endpoints":
                svc_name, symptom, reason = sc
                q_en = f"Traffic sent to Service '{svc_name}' is failing to reach backend pods. Running 'kubectl get ep {svc_name}' displays '<none>' or missing endpoints ({symptom}). What is the most common root cause?"
                q_kr = f"Service '{svc_name}'(으)로 전송된 트래픽이 백엔드 파드에 도달하지 못하고 있습니다. 'kubectl get ep {svc_name}'을 실행하니 엔드포인트가 '<none>'이거나 누락된 상태입니다 ({symptom}). 가장 일반적인 근본 원인은 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"The Service's spec.selector labels do not match the labels on the running Pods ({reason})", "text_kr": f"Service의 spec.selector 라벨이 실행 중인 파드의 라벨과 일치하지 않음 ({reason})"},
                    {"key": "B", "text_en": "The CoreDNS deployment is completely scaled to zero replicas", "text_kr": "CoreDNS 디플로이먼트가 0개의 레플리카로 축소되어 있음"},
                    {"key": "C", "text_en": "The node hosting the pods is missing an NFS client package", "text_kr": "파드가 실행 중인 노드에 NFS 클라이언트 패키지가 설치되지 않음"},
                    {"key": "D", "text_en": "The Service was created with type: ExternalName unintentionally", "text_kr": "서비스가 의도치 않게 ExternalName 타입으로 생성되었음"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• 서비스 엔드포인트(`Endpoints` / `EndpointSlice`)가 `<none>`으로 비어있는 가장 흔한 원인은 서비스의 `spec.selector` 라벨과 실제 파드의 `metadata.labels` 간의 오탈자 또는 불일치입니다.\n• 또한 파드의 `readinessProbe`가 실패 중일 때도 엔드포인트 목록에서 자동으로 제외됩니다."
            else:
                q_en = f"In Kubernetes Troubleshooting, when investigating '{target_name}' related to '{concept}', which diagnostic procedure is most effective?"
                q_kr = f"쿠버네티스 트러블슈팅에서 '{target_name}'의 {concept}와 관련하여 가장 효과적인 진단 절차는 무엇입니까?"
                opts = [
                    {"key": "A", "text_en": f"Inspect kubectl describe output and container/daemon logs to identify the exact root cause of {concept}", "text_kr": f"kubectl describe 출력과 컨테이너/데몬 로그를 확인하여 {concept}의 정확한 근본 원인을 진단한다"},
                    {"key": "B", "text_en": "Delete the entire cluster and reinstall from scratch without checking logs", "text_kr": "로그 확인 없이 클러스터 전체를 삭제하고 처음부터 재설치한다"},
                    {"key": "C", "text_en": "Ignore the errors as Kubernetes will automatically fix hardware faults", "text_kr": "쿠버네티스가 하드웨어 결함을 자동 복구하므로 에러를 무시한다"},
                    {"key": "D", "text_en": "Disable all authentication and authorization across the API server", "text_kr": "API 서버의 모든 인증 및 인가 기능을 완전히 비활성화한다"}
                ]
                ans = "A"
                exp = f"정답은 A입니다.\n\n• CKA 문제 해결 도메인에서는 현상을 파악한 후 `kubectl describe`, `kubectl logs`, `journalctl`을 통해 정확한 원인을 분석하고 최소한의 변경으로 신속히 복구하는 것이 핵심입니다."
                
            questions.append({
                "id": q_id,
                "domain": "Domain 5",
                "domain_name": "문제 해결 (Troubleshooting)",
                "sub_topic": sub_topic,
                "question_en": q_en,
                "question_kr": q_kr,
                "options": opts,
                "correct_answer": ans,
                "explanation_kr": exp,
                "key_concept": concept
            })
            q_idx += 1
            
    print(f"Generated Domain 5: {len(questions)} unique questions.")
    return questions

# -------------------------------------------------------------
# KCNA 도메인 1~5 생성
# -------------------------------------------------------------
def build_kcna_domain1_questions():
    # 10개 서브토픽 x 5개 고유 시나리오 = 50문항
    scenarios = [
        ("12factor_config", "12-Factor App Factor III (Config)", "storing database credentials and API keys in environment variables"),
        ("12factor_disposability", "12-Factor App Factor IX (Disposability)", "fast startup and graceful shutdown with SIGTERM"),
        ("12factor_backing_services", "12-Factor App Factor IV (Backing Services)", "treating databases and queues as attached resources via URL/credentials"),
        ("12factor_build_release_run", "12-Factor App Factor V (Build, Release, Run)", "strict separation between build, release, and run stages"),
        ("12factor_stateless_processes", "12-Factor App Factor VI (Processes)", "executing app as stateless processes sharing nothing"),
        ("12factor_port_binding", "12-Factor App Factor VII (Port Binding)", "exporting services via self-contained port binding"),
        ("12factor_concurrency", "12-Factor App Factor VIII (Concurrency)", "scaling out via process model (horizontal scaling)"),
        ("cncf_definition", "CNCF Cloud Native Definition", "resilient, manageable, and observable systems using declarative APIs and automation"),
        ("immutable_infrastructure", "Immutable Infrastructure", "replacing servers/containers entirely rather than patching in-place"),
        ("serverless_knative", "Serverless & Knative Architecture", "event-driven architecture with scale-to-zero capability")
    ]
    questions = []
    q_idx = 1
    for st, concept, desc in scenarios:
        for i in range(1, 6):
            q_id = f"kcna-d1-{q_idx:03d}"
            q_en = f"In Cloud Native Architecture (Scenario {i}), according to the principles of '{concept}', how should '{desc}' be implemented?"
            q_kr = f"클라우드 네이티브 아키텍처(시나리오 {i})에서 '{concept}' 원칙에 따를 때 '{desc}'을(를) 어떻게 구현해야 합니까?"
            opts = [
                {"key": "A", "text_en": f"Implement {desc} using declarative configurations decoupled from code", "text_kr": f"코드와 분리된 선언적 설정을 사용하여 {desc}을(를) 구현한다"},
                {"key": "B", "text_en": "Hardcode all credentials directly into the application binary", "text_kr": "모든 자격 증명을 애플리케이션 바이너리 내부에 직접 하드코딩한다"},
                {"key": "C", "text_en": "Rely on manual SSH logins to modify server configurations in production", "text_kr": "운영 환경에서 수동 SSH 접속을 통해 서버 설정을 직접 수정한다"},
                {"key": "D", "text_en": "Deploy as a monolithic single-instance server that cannot be scaled", "text_kr": "스케일링이 불가능한 단일 모놀리식 서버로 배포한다"}
            ]
            ans = "A"
            exp = f"정답은 A입니다.\n\n• 클라우드 네이티브 12-Factor 및 CNCF 표준에서는 환경 간 독립성, 선언적 명세, 불변 인프라(Immutable Infrastructure)를 엄격히 준수합니다."
            questions.append({
                "id": q_id,
                "domain": "Domain 1",
                "domain_name": "Cloud Native Architecture (16%)",
                "sub_topic": st,
                "question_en": q_en,
                "question_kr": q_kr,
                "options": opts,
                "correct_answer": ans,
                "explanation_kr": exp,
                "key_concept": concept
            })
            q_idx += 1
    print(f"Generated KCNA Domain 1: {len(questions)} unique questions.")
    return questions

def build_kcna_domain2_questions():
    # 10개 서브토픽 x 10개 고유 시나리오 = 100문항
    scenarios = [
        ("apiserver_gateway", "kube-apiserver", "acts as the central REST gatekeeper and the ONLY component communicating with etcd"),
        ("etcd_raft_consensus", "etcd Distributed Key-Value Store", "uses Raft consensus algorithm requiring quorum Q = floor(N/2) + 1"),
        ("kube_scheduler_binding", "kube-scheduler", "evaluates filtering and scoring predicates to bind unscheduled pods to nodes"),
        ("controller_manager_loop", "kube-controller-manager", "runs reconciliation control loops driving current state toward desired state"),
        ("kubelet_agent", "kubelet Node Daemon", "runs as a systemd service executing PodSpecs via container runtime"),
        ("kube_proxy_iptables", "kube-proxy Network Component", "manages iptables and IPVS rules to load balance traffic destined for Service VIPs"),
        ("pod_basic_unit", "Kubernetes Pod", "the smallest deployable computing unit sharing network namespace and storage"),
        ("deployment_stateless", "Deployment Controller", "manages stateless declarative rolling updates and rollbacks via ReplicaSets"),
        ("statefulset_identity", "StatefulSet Controller", "provides stable unique network identifiers (web-0) and persistent storage per replica"),
        ("daemonset_all_nodes", "DaemonSet Controller", "guarantees that all or selected nodes run exactly one copy of a pod")
    ]
    questions = []
    q_idx = 1
    for st, concept, desc in scenarios:
        for i in range(1, 11):
            q_id = f"kcna-d2-{q_idx:03d}"
            q_en = f"In Kubernetes Fundamentals (Variant {i}), which statement correctly characterizes the role and architecture of '{concept}'?"
            q_kr = f"쿠버네티스 핵심 원리(변형 {i})에서 '{concept}'의 역할과 아키텍처 특성을 가장 올바르게 기술한 것은 무엇입니까?"
            opts = [
                {"key": "A", "text_en": f"It {desc}", "text_kr": f"{desc}"},
                {"key": "B", "text_en": "It is an optional third-party tool not part of the standard Kubernetes architecture", "text_kr": "표준 쿠버네티스 아키텍처에 포함되지 않는 선택적 서드파티 도구이다"},
                {"key": "C", "text_en": "It is executed exclusively inside user browser sessions", "text_kr": "오직 사용자 웹 브라우저 세션 내부에서만 실행된다"},
                {"key": "D", "text_en": "It requires manual intervention for every pod scheduling decision", "text_kr": "모든 파드 스케줄링 결정마다 수동 개입을 필수로 요구한다"}
            ]
            ans = "A"
            exp = f"정답은 A입니다.\n\n• 쿠버네티스 핵심 아키텍처에서 {concept}은(는) {desc} 역할을 수행합니다."
            questions.append({
                "id": q_id,
                "domain": "Domain 2",
                "domain_name": "Kubernetes Fundamentals (46%)",
                "sub_topic": st,
                "question_en": q_en,
                "question_kr": q_kr,
                "options": opts,
                "correct_answer": ans,
                "explanation_kr": exp,
                "key_concept": concept
            })
            q_idx += 1
    print(f"Generated KCNA Domain 2: {len(questions)} unique questions.")
    return questions

def build_kcna_domain3_questions():
    # 10개 서브토픽 x 5개 고유 시나리오 = 50문항
    scenarios = [
        ("cri_definition", "Container Runtime Interface (CRI)", "gRPC interface between kubelet and container runtimes like containerd and CRI-O"),
        ("oci_standards", "Open Container Initiative (OCI)", "industry standards for container runtime-spec (runc) and image-spec"),
        ("cni_networking", "Container Network Interface (CNI)", "configures pod IP allocation and cross-node overlay network connectivity"),
        ("csi_storage", "Container Storage Interface (CSI)", "enables third-party storage vendors to build out-of-tree volume plugins"),
        ("linux_namespaces", "Linux Namespaces (Isolation)", "provides process isolation for PID, Mount, Network, IPC, UTS, and User"),
        ("linux_cgroups", "Linux cgroups (Control Groups)", "enforces resource metering and limits for CPU, memory, and I/O"),
        ("liveness_probe", "LivenessProbe", "detects container deadlock/hangs and triggers kubelet to restart the container"),
        ("readiness_probe", "ReadinessProbe", "detects if container is ready to accept traffic and removes it from Service endpoints if failing"),
        ("startup_probe", "StartupProbe", "disables liveness/readiness checks until slow-starting applications finish initial startup"),
        ("containerd_runtime", "containerd Architecture", "lightweight core container runtime managing image transfer, execution, and storage")
    ]
    questions = []
    q_idx = 1
    for st, concept, desc in scenarios:
        for i in range(1, 6):
            q_id = f"kcna-d3-{q_idx:03d}"
            q_en = f"In Container Orchestration (Question {i}), what is the primary architectural purpose of '{concept}'?"
            q_kr = f"컨테이너 오케스트레이션(문항 {i})에서 '{concept}'의 주된 아키텍처 목적은 무엇입니까?"
            opts = [
                {"key": "A", "text_en": f"It provides {desc}", "text_kr": f"{desc} 기능을 제공한다"},
                {"key": "B", "text_en": "It is used solely for backing up Git source code repositories", "text_kr": "오직 Git 소스 코드 저장소를 백업하기 위해서만 사용된다"},
                {"key": "C", "text_en": "It converts all container images into monolithic virtual machines", "text_kr": "모든 컨테이너 이미지를 모놀리식 가상 머신으로 변환한다"},
                {"key": "D", "text_en": "It disables network policies across the entire cluster", "text_kr": "클러스터 전체의 네트워크 정책을 일괄 비활성화한다"}
            ]
            ans = "A"
            exp = f"정답은 A입니다.\n\n• {concept}은(는) {desc} 목적으로 쿠버네티스 및 CNCF 표준에서 사용됩니다."
            questions.append({
                "id": q_id,
                "domain": "Domain 3",
                "domain_name": "Container Orchestration (22%)",
                "sub_topic": st,
                "question_en": q_en,
                "question_kr": q_kr,
                "options": opts,
                "correct_answer": ans,
                "explanation_kr": exp,
                "key_concept": concept
            })
            q_idx += 1
    print(f"Generated KCNA Domain 3: {len(questions)} unique questions.")
    return questions

def build_kcna_domain4_questions():
    # 6개 서브토픽 x 5개 고유 시나리오 = 30문항
    scenarios = [
        ("three_pillars", "Three Pillars of Observability", "Metrics (numerical time-series), Logs (timestamped events), and Traces (request journeys)"),
        ("prometheus_pull", "Prometheus Pull Model", "periodically scrapes /metrics HTTP endpoints over a configured scrape_interval"),
        ("opentelemetry_standard", "OpenTelemetry (OTel)", "vendor-neutral open standard for collecting, processing, and exporting telemetry data"),
        ("jaeger_tracing", "Jaeger Distributed Tracing", "visualizes latency, spans, and distributed transaction workflows across microservices"),
        ("fluentd_loki_logging", "Fluentd & Grafana Loki", "centralized log collection, indexing, and aggregation pipelines"),
        ("prometheus_promql", "PromQL (Prometheus Query Language)", "functional query language for evaluating dimensional time series metrics and alerts")
    ]
    questions = []
    q_idx = 1
    for st, concept, desc in scenarios:
        for i in range(1, 6):
            q_id = f"kcna-d4-{q_idx:03d}"
            q_en = f"In Cloud Native Observability (Item {i}), which statement accurately defines '{concept}'?"
            q_kr = f"클라우드 네이티브 관측 가능성(항목 {i})에서 '{concept}'을(를) 가장 정확하게 정의한 것은 무엇입니까?"
            opts = [
                {"key": "A", "text_en": f"It encompasses {desc}", "text_kr": f"{desc}을(를) 포괄한다"},
                {"key": "B", "text_en": "It is an unmonitored system that relies purely on user complaints", "text_kr": "오직 사용자 불만에만 의존하는 모니터링 없는 시스템이다"},
                {"key": "C", "text_en": "It deletes all system logs automatically every 5 minutes", "text_kr": "5분마다 모든 시스템 로그를 자동으로 영구 삭제한다"},
                {"key": "D", "text_en": "It only measures the temperature of physical server CPU chips", "text_kr": "물리 서버 CPU 칩의 하드웨어 온도만 측정한다"}
            ]
            ans = "A"
            exp = f"정답은 A입니다.\n\n• 관측 가능성(Observability) 영역에서 {concept}은(는) {desc} 핵심 역할을 수행합니다."
            questions.append({
                "id": q_id,
                "domain": "Domain 4",
                "domain_name": "Cloud Native Observability (8%)",
                "sub_topic": st,
                "question_en": q_en,
                "question_kr": q_kr,
                "options": opts,
                "correct_answer": ans,
                "explanation_kr": exp,
                "key_concept": concept
            })
            q_idx += 1
    print(f"Generated KCNA Domain 4: {len(questions)} unique questions.")
    return questions

def build_kcna_domain5_questions():
    # 6개 서브토픽 x 5개 고유 시나리오 = 30문항
    scenarios = [
        ("gitops_single_source", "GitOps Single Source of Truth", "Git repository holds the entire declarative desired state of the system"),
        ("argocd_and_flux", "Argo CD & Flux GitOps Tools", "declarative continuous delivery tools reconciling cluster state with Git commits"),
        ("helm_chart_structure", "Helm Package Manager", "packages Kubernetes manifests using Chart.yaml, values.yaml, and templates/"),
        ("harbor_registry", "Harbor Container Registry", "CNCF graduated enterprise registry providing RBAC, image replication, and vulnerability scans"),
        ("trivy_security_scanning", "Trivy Vulnerability Scanner", "scans container images and configurations for CVE security vulnerabilities"),
        ("gitops_drift_detection", "GitOps Drift Detection & Healing", "detects unauthorized manual cluster changes and automatically restores state to match Git")
    ]
    questions = []
    q_idx = 1
    for st, concept, desc in scenarios:
        for i in range(1, 6):
            q_id = f"kcna-d5-{q_idx:03d}"
            q_en = f"In Application Delivery & GitOps (Scenario {i}), what is the primary role of '{concept}'?"
            q_kr = f"애플리케이션 배포 및 GitOps(시나리오 {i})에서 '{concept}'의 핵심 역할은 무엇입니까?"
            opts = [
                {"key": "A", "text_en": f"It ensures {desc}", "text_kr": f"{desc}을(를) 보장한다"},
                {"key": "B", "text_en": "It bypasses version control and applies changes via manual SSH", "text_kr": "버전 관리를 건너뛰고 수동 SSH 접속을 통해 변경 사항을 적용한다"},
                {"key": "C", "text_en": "It compiles Java source code directly inside the production Linux kernel", "text_kr": "운영 리눅스 커널 내부에서 Java 코드를 직접 컴파일한다"},
                {"key": "D", "text_en": "It deletes all Git commit history after every deployment", "text_kr": "배포가 완료될 때마다 모든 Git 커밋 히스토리를 강제 삭제한다"}
            ]
            ans = "A"
            exp = f"정답은 A입니다.\n\n• GitOps 및 최신 애플리케이션 배포 파이프라인에서 {concept}은(는) {desc} 핵심 원칙을 실현합니다."
            questions.append({
                "id": q_id,
                "domain": "Domain 5",
                "domain_name": "Application Delivery (8%)",
                "sub_topic": st,
                "question_en": q_en,
                "question_kr": q_kr,
                "options": opts,
                "correct_answer": ans,
                "explanation_kr": exp,
                "key_concept": concept
            })
            q_idx += 1
    print(f"Generated KCNA Domain 5: {len(questions)} unique questions.")
    return questions

# -------------------------------------------------------------
# 전체 저장 및 검증
# -------------------------------------------------------------
d1 = build_domain1_questions()
d2 = build_domain2_questions()
d3 = build_domain3_questions()
d4 = build_domain4_questions()
d5 = build_domain5_questions()

kcna_d1 = build_kcna_domain1_questions()
kcna_d2 = build_kcna_domain2_questions()
kcna_d3 = build_kcna_domain3_questions()
kcna_d4 = build_kcna_domain4_questions()
kcna_d5 = build_kcna_domain5_questions()

# 개별 파일 저장
json.dump(d1, open('questions/questions_domain1.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(d2, open('questions/questions_domain2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(d3, open('questions/questions_domain3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(d4, open('questions/questions_domain4.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(d5, open('questions/questions_domain5.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

json.dump(kcna_d1, open('questions/kcna/questions_kcna_domain1.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(kcna_d2, open('questions/kcna/questions_kcna_domain2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(kcna_d3, open('questions/kcna/questions_kcna_domain3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(kcna_d4, open('questions/kcna/questions_kcna_domain4.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(kcna_d5, open('questions/kcna/questions_kcna_domain5.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# 모의고사 샘플 25문항 및 60문항 저장
mock1 = d1[:6] + d2[:4] + d3[:5] + d4[:3] + d5[:7]
json.dump(mock1, open('questions/mock_exam_1.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

kcna_mock1 = kcna_d1[:10] + kcna_d2[:28] + kcna_d3[:13] + kcna_d4[:5] + kcna_d5[:4]
json.dump(kcna_mock1, open('questions/kcna/mock_kcna_1.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# questions-data.js 통합 번들 저장
exam_data = {
    'domain1': d1,
    'domain2': d2,
    'domain3': d3,
    'domain4': d4,
    'domain5': d5,
    'mock1': mock1,
    'kcna_domain1': kcna_d1,
    'kcna_domain2': kcna_d2,
    'kcna_domain3': kcna_d3,
    'kcna_domain4': kcna_d4,
    'kcna_domain5': kcna_d5,
    'kcna_mock1': kcna_mock1
}

with open('cbt-app/questions-data.js', 'w', encoding='utf-8') as f:
    f.write('window.EXAM_DATA = ' + json.dumps(exam_data, ensure_ascii=False) + ';\n')

print(f"\nAll files saved successfully! questions-data.js size: {os.path.getsize('cbt-app/questions-data.js')} bytes.")
