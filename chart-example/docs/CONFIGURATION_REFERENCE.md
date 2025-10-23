# 📋 Complete Configuration Reference
 
**Everything you can configure in this Helm template**

This is your comprehensive guide to all configuration options available in `values.yaml`. Each section includes default values, descriptions, examples, and common use cases.

## Table of Contents

- [📊 Configuration Quick Reference Table](#-configuration-quick-reference-table)
- [🎯 Common Configuration Patterns](#-common-configuration-patterns)
- [📦 Application Basics](#-application-basics)
  - [Container Image Configuration](#container-image-configuration)
  - [Authentication for Private Registries](#authentication-for-private-registries)
  - [Application Naming](#application-naming)
  - [Replica Count](#replica-count)
- [🌐 Service & Networking](#-service--networking)
  - [Service Configuration](#service-configuration)
  - [Ingress Configuration](#ingress-configuration)
  - [Network Security](#network-security)
- [🔒 Security Settings](#-security-settings)
  - [Pod Security Context](#pod-security-context)
  - [Container Security Context](#container-security-context)
  - [Pod Security Standards](#pod-security-standards)
  - [Service Account](#service-account)
- [🔧 Resource Management](#-resource-management)
  - [Resource Limits and Requests](#resource-limits-and-requests)
  - [Resource Governance](#resource-governance)
- [📊 Scaling & Availability](#-scaling--availability)
  - [Horizontal Pod Autoscaler](#horizontal-pod-autoscaler)
  - [Pod Disruption Budget](#pod-disruption-budget)
- [🩺 Health Checks](#-health-checks)
  - [Liveness Probe](#liveness-probe)
  - [Readiness Probe](#readiness-probe)
  - [Startup Probe](#startup-probe)
- [🔷 Azure Integration](#-azure-integration)
  - [Azure Key Vault](#azure-key-vault)
  - [AKS-Specific Configuration](#aks-specific-configuration)
- [⚙️ Environment Variables](#-environment-variables)
  - [Application Configuration](#application-configuration)
  - [External Environment Sources](#external-environment-sources)
- [📁 Storage & Volumes](#-storage--volumes)
  - [Volume Configuration](#volume-configuration)
- [📊 Monitoring & Observability](#-monitoring--observability)
  - [Prometheus Integration](#prometheus-integration)
  - [Pod Annotations](#pod-annotations)
  - [Compliance and Governance](#compliance-and-governance)
- [🎛️ Advanced Configuration](#-advanced-configuration)
  - [Deployment Strategy](#deployment-strategy)
  - [Scheduling Configuration](#scheduling-configuration)
  - [DNS Configuration](#dns-configuration)
  - [Init Containers and Sidecars](#init-containers-and-sidecars)
- [🔧 Troubleshooting Quick Reference](#-troubleshooting-quick-reference)
- [Default Values Summary](#default-values-summary)
- [Configuration Validation](#configuration-validation)
- [📋 Environment Configuration Checklist](#-environment-configuration-checklist)

## 📊 Configuration Quick Reference Table

**The most important configuration options at a glance**

| Category | Setting | Default | Description | Example |
|----------|---------|---------|-------------|---------|
| **🚀 Essential** | | | | |
| | `image.repository` | `""` | Docker image location | `"myregistry.azurecr.io/app"` |
| | `image.tag` | `""` | Image version | `"v1.0.0"` |
| | `service.containerPort` | `8080` | Port your app listens on | `3000` |
| | `ingress.enabled` | `false` | Enable external access | `true` |
| | `ingress.hosts[0].host` | `""` | Your domain | `"myapp.example.com"` |
| **🔧 Resources** | | | | |
| | `resources.requests.cpu` | `100m` | Guaranteed CPU | `"200m"` |
| | `resources.requests.memory` | `128Mi` | Guaranteed memory | `"256Mi"` |
| | `resources.limits.cpu` | `500m` | Maximum CPU | `"1000m"` |
| | `resources.limits.memory` | `512Mi` | Maximum memory | `"1Gi"` |
| | `replicaCount` | `1` | Number of instances | `3` |
| **📈 Scaling** | | | | |
| | `autoscaling.enabled` | `false` | Enable auto-scaling | `true` |
| | `autoscaling.minReplicas` | `1` | Minimum instances | `2` |
| | `autoscaling.maxReplicas` | `10` | Maximum instances | `20` |
| | `autoscaling.targetCPUUtilizationPercentage` | `70` | CPU threshold | `80` |
| **🔒 Security** | | | | |
| | `podSecurityContext.runAsNonRoot` | `true` | Run as non-root user | `true` |
| | `podSecurityContext.runAsUser` | `1001` | User ID | `1001` |
| | `securityContext.readOnlyRootFilesystem` | `true` | Read-only filesystem | `true` |
| | `networkPolicy.enabled` | `false` | Enable network policies | `true` |
| **🔷 Azure** | | | | |
| | `azureKeyVault.enabled` | `false` | Enable Key Vault secrets | `true` |
| | `azureKeyVault.vaultName` | `""` | Key Vault name | `"myapp-secrets"` |
| | `azureKeyVault.clientId` | `""` | Workload Identity client ID | `"12345678-..."` |
| **🩺 Health** | | | | |
| | `livenessProbe.httpGet.path` | `"/health"` | Health check endpoint | `"/api/health"` |
| | `readinessProbe.httpGet.path` | `"/health"` | Ready check endpoint | `"/api/ready"` |
| | `startupProbe.httpGet.path` | `"/health"` | Startup check endpoint | `"/api/health"` |
| **📊 Monitoring** | | | | |
| | `monitoring.enabled` | `false` | Enable Prometheus metrics | `true` |
| | `monitoring.serviceMonitor.path` | `"/metrics"` | Metrics endpoint | `"/metrics"` |
| | `podAnnotations` | `{}` | Pod annotations | `{"app.version": "v1.0.0"}` |
| **⚙️ Environment** | | | | |
| | `env.enabled` | `false` | Enable environment variables | `true` |
| | `env.variables` | `{}` | Environment variables | `{"NODE_ENV": "production"}` |
| **📁 Storage** | | | | |
| | `volumes` | `[]` | Additional volumes | `[{"name": "data", "emptyDir": {}}]` |
| | `volumeMounts` | `[]` | Volume mounts | `[{"name": "data", "mountPath": "/data"}]` |

## 🎯 Common Configuration Patterns

**Pre-configured combinations for different scenarios**

| Scenario | Configuration | Use Case |
|----------|---------------|----------|
| **🚀 Development** | `replicaCount: 1`<br>`resources.requests.cpu: 50m`<br>`resources.requests.memory: 128Mi`<br>`ingress.enabled: false`<br>`networkPolicy.enabled: false` | Local development, testing |
| **🌐 Simple Web App** | `replicaCount: 2`<br>`service.containerPort: 3000`<br>`ingress.enabled: true`<br>`ingress.hosts[0].host: "myapp.com"`<br>`resources.requests.cpu: 100m`<br>`resources.requests.memory: 256Mi` | Static sites, simple web apps |
| **⚡ REST API** | `replicaCount: 3`<br>`service.containerPort: 8080`<br>`autoscaling.enabled: true`<br>`autoscaling.minReplicas: 2`<br>`autoscaling.maxReplicas: 10`<br>`monitoring.enabled: true` | RESTful APIs, microservices |
| **🔒 Production App** | `replicaCount: 3`<br>`autoscaling.enabled: true`<br>`podDisruptionBudget.enabled: true`<br>`networkPolicy.enabled: true`<br>`azureKeyVault.enabled: true`<br>`monitoring.enabled: true` | Production workloads |
| **🔄 Background Worker** | `replicaCount: 2`<br>`ingress.enabled: false`<br>`resources.requests.cpu: 200m`<br>`resources.requests.memory: 512Mi`<br>`autoscaling.enabled: true`<br>`autoscaling.targetCPUUtilizationPercentage: 80` | Queue processors, batch jobs |
| **🗄️ Database Client** | `replicaCount: 1`<br>`azureKeyVault.enabled: true`<br>`networkPolicy.enabled: true`<br>`volumes: [{"name": "data", "persistentVolumeClaim": {"claimName": "db-data"}}]`<br>`volumeMounts: [{"name": "data", "mountPath": "/var/lib/db"}]` | Database applications |

--- 

## 📦 Application Basics

### Container Image Configuration

**What it controls**: Which Docker image to deploy and how to pull it

```yaml
image:
  # Your Docker image location (REQUIRED)
  repository: "myregistry.azurecr.io/my-application"
  
  # Image version/tag (REQUIRED)
  tag: "v1.0.0"
  
  # When to pull the image
  # Options: Always | IfNotPresent | Never
  # Default: IfNotPresent
  pullPolicy: IfNotPresent
```

**Common configurations**:
```yaml
# ✅ Production: Use specific versions
image:
  repository: "prodregistry.azurecr.io/my-api"
  tag: "v2.1.0"
  pullPolicy: IfNotPresent

# ✅ Development: Always pull latest
image:
  repository: "devregistry.azurecr.io/my-api"
  tag: "dev-latest"
  pullPolicy: Always
```

### Authentication for Private Registries

**What it controls**: Access to private container registries

```yaml
# Default: No authentication
imagePullSecrets: []

# With authentication
imagePullSecrets:
  - name: acr-secret        # Azure Container Registry
  - name: dockerhub-secret  # Docker Hub
  - name: ghcr-secret       # GitHub Container Registry
```

### Application Naming

**What it controls**: How your application is named in Kubernetes

```yaml
# Partial name override (keeps release name prefix)
# Default: "" (uses Chart.name)
nameOverride: ""

# Full name override (replaces everything)
# Default: "" (uses release name + chart name)
fullnameOverride: "my-custom-app"

# Target namespace (optional)
# Default: "" (uses Helm release namespace)
namespace: "my-app-production"
```

**Examples**:
```yaml
# ✅ Simple override
nameOverride: "webapp"
# Results in: my-release-webapp

# ✅ Full control
fullnameOverride: "user-service-v2"
# Results in: user-service-v2

# ✅ Specific namespace
namespace: "production"
# Deploys to: production namespace
```

### Replica Count

**What it controls**: Number of application instances to run

```yaml
# Default: 1
replicaCount: 3

# Note: Ignored if autoscaling is enabled
```

**Guidelines**:
- **Development**: 1 replica
- **Staging**: 2-3 replicas
- **Production**: 3+ replicas (for high availability)

---

## 🌐 Service & Networking

### Service Configuration

**What it controls**: How your application is exposed within the cluster

```yaml
service:
  # Service type
  # Options: ClusterIP | NodePort | LoadBalancer
  # Default: ClusterIP
  type: ClusterIP
  
  # External port (what other services/users connect to)
  # Default: 80
  port: 80
  
  # Container port (what your app listens on)
  # Default: 8080 (MUST match your application)
  containerPort: 8080
  
  # Additional annotations
  annotations: {}
```

**Common configurations**:
```yaml
# ✅ Web application
service:
  type: ClusterIP
  port: 80
  containerPort: 3000

# ✅ API service
service:
  type: ClusterIP
  port: 8080
  containerPort: 8080

# ✅ Development with NodePort
service:
  type: NodePort
  port: 80
  containerPort: 8080
  nodePort: 30080  # Optional: specific port

# ✅ Load balancer with annotations
service:
  type: LoadBalancer
  port: 80
  containerPort: 8080
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"
```

### Ingress Configuration

**What it controls**: External access to your application via HTTP/HTTPS

```yaml
ingress:
  # Enable/disable external access
  # Default: false
  enabled: true
  
  # Ingress controller class
  # Options: nginx | azure-application-gateway | traefik
  # Default: nginx
  className: "nginx"
  
  # Ingress annotations for features
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
  
  # Domain configuration
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  
  # SSL/TLS configuration
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com
```

**Common configurations**:
```yaml
# ✅ Simple HTTP access
ingress:
  enabled: true
  hosts:
    - host: myapp-dev.internal.com
      paths:
        - path: /

# ✅ HTTPS with automatic certificates
ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com

# ✅ API with path-based routing
ingress:
  enabled: true
  hosts:
    - host: api.example.com
      paths:
        - path: /v1/users
          pathType: Prefix
        - path: /v1/orders
          pathType: Prefix

# ✅ Azure Application Gateway
ingress:
  enabled: true
  className: "azure-application-gateway"
  annotations:
    appgw.ingress.kubernetes.io/ssl-redirect: "true"
    appgw.ingress.kubernetes.io/backend-protocol: "http"
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
```

### Network Security

**What it controls**: Network traffic restrictions

```yaml
networkPolicy:
  # Enable network policies
  # Default: false
  enabled: true
  
  # Policy types to enforce
  policyTypes:
    - Ingress  # Control incoming traffic
    - Egress   # Control outgoing traffic
  
  # Custom ingress rules
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080
  
  # Custom egress rules
  egress:
    - to: []  # Allow all external HTTPS
      ports:
        - protocol: TCP
          port: 443
    - to:      # Allow database access
        - namespaceSelector:
            matchLabels:
              name: database
      ports:
        - protocol: TCP
          port: 5432
```

**Common configurations**:
```yaml
# ✅ Basic protection (recommended)
networkPolicy:
  enabled: true
  policyTypes:
    - Ingress
    - Egress

# ✅ Web application (ingress from load balancer)
networkPolicy:
  enabled: true
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
  egress:
    - to: []
      ports:
        - protocol: TCP
          port: 443  # HTTPS only

# ✅ Microservice (specific service access)
networkPolicy:
  enabled: true
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: api-gateway
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: database
      ports:
        - protocol: TCP
          port: 5432
```

---

### Basic Service Settings
**How your application is exposed within the cluster**

```yaml
service:
  # Service type
  # Options: ClusterIP, NodePort, LoadBalancer
  # Default: ClusterIP
  type: ClusterIP
  
  # External port (what other services connect to)
  # Default: 80
  port: 80
  
  # Container port (what your app listens on)
  # Default: 8080
  containerPort: 8080
  
  # Additional annotations
  # Default: {}
  annotations: {}
```

**Examples:**
```yaml
# Web application
service:
  type: ClusterIP
  port: 80
  containerPort: 3000

# API service
service:
  type: ClusterIP
  port: 8080
  containerPort: 8080
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"

# Database service
service:
  type: ClusterIP
  port: 5432
  containerPort: 5432
```

---

## Ingress & Networking

### Ingress Configuration
**External access to your application**

```yaml
ingress:
  # Enable/disable ingress
  # Default: false
  enabled: true
  
  # Ingress class name
  # Options: nginx, azure-application-gateway, traefik
  # Default: "nginx"
  className: "nginx"
  
  # Ingress annotations
  # Default: {}
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: letsencrypt-prod
  
  # Host configuration
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  
  # TLS configuration
  # Default: []
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com
```

**Common Patterns:**

```yaml
# Simple web app
ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: myapp.com
      paths:
        - path: /
          pathType: Prefix

# API with SSL
ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
  hosts:
    - host: api.example.com
      paths:
        - path: /api
          pathType: Prefix
  tls:
    - secretName: api-tls
      hosts:
        - api.example.com

# Multiple hosts/paths
ingress:
  enabled: true
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix
    - host: admin.example.com
      paths:
        - path: /admin
          pathType: Prefix
```

### Network Policies
**Controls network traffic to/from your application**

```yaml
networkPolicy:
  # Enable network policies
  # Default: false
  enabled: true
  
  # Custom ingress rules
  # Default: []
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - protocol: TCP
          port: 8080
  
  # Custom egress rules
  # Default: []
  egress:
    - to: []
      ports:
        - protocol: TCP
          port: 443
```

**Security Levels:**
```yaml
# Strict (production)
networkPolicy:
  enabled: true
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
  egress:
    - to: []
      ports:
        - protocol: TCP
          port: 443
        - protocol: UDP
          port: 53

# Permissive (development)
networkPolicy:
  enabled: false
```

---

## Security Settings

### Pod Security Context
**Security settings for the entire pod**

```yaml
podSecurityContext:
  # Run as non-root user
  # Default: true
  runAsNonRoot: true
  
  # User ID to run as
  # Default: 1001
  runAsUser: 1001
  
  # Group ID to run as
  # Default: 1001
  runAsGroup: 1001
  
  # File system group
  # Default: 1001
  fsGroup: 1001
  
  # Seccomp profile
  seccompProfile:
    type: RuntimeDefault
```

### Container Security Context
**Security settings for the application container**

```yaml
securityContext:
  # Prevent privilege escalation
  # Default: false
  allowPrivilegeEscalation: false
  
  # Drop all capabilities
  capabilities:
    drop:
    - ALL
  
  # Read-only root filesystem
  # Default: true
  readOnlyRootFilesystem: true
  
  # Run as non-root
  # Default: true
  runAsNonRoot: true
  
  # User ID
  # Default: 1001
  runAsUser: 1001
```

### Pod Security Standards
**Kubernetes Pod Security Standards enforcement**

```yaml
podSecurityStandards:
  # Enable Pod Security Standards
  # Default: true
  enabled: true
  
  # Enforce baseline standards
  # Default: true
  enforceBaseline: true
  
  # Enforce restricted standards
  # Default: true
  enforceRestricted: true
  
  # Security context defaults
  runAsUser: 1001
  runAsGroup: 1001
  fsGroup: 1001
```

### Service Account
**Kubernetes identity for your application**

```yaml
serviceAccount:
  # Create a service account
  # Default: true
  create: true
  
  # Mount service account token
  # Default: true
  automount: true
  
  # Service account annotations
  # Default: {}
  annotations: {}
  
  # Custom service account name
  # Default: "" (auto-generated)
  name: ""
```

---

## Resource Management

### Resource Limits and Requests
**CPU and memory allocation**

```yaml
resources:
  # Maximum resources (limits)
  limits:
    cpu: 500m        # 0.5 CPU cores
    memory: 512Mi    # 512 MB RAM
    ephemeral-storage: 1Gi  # Temporary storage
  
  # Guaranteed resources (requests)
  requests:
    cpu: 100m        # 0.1 CPU cores
    memory: 128Mi    # 128 MB RAM
    ephemeral-storage: 100Mi
```

**Resource Sizing Guidelines:**

```yaml
# Micro service
resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 50m
    memory: 128Mi

# Small web app
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 256Mi

# API service
resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 200m
    memory: 512Mi

# Large application
resources:
  limits:
    cpu: 2000m
    memory: 4Gi
  requests:
    cpu: 500m
    memory: 1Gi
```

### Resource Governance
**Namespace-level resource controls**

```yaml
resourceQuota:
  # Enable resource quotas
  # Default: false
  enabled: false
  
  # Request quotas
  requests:
    cpu: "4"
    memory: "8Gi"
  
  # Limit quotas
  limits:
    cpu: "8"
    memory: "16Gi"
  
  # Object count limits
  persistentvolumeclaims: "4"
  pods: "10"
  services: "5"
  secrets: "10"
  configmaps: "10"

limitRange:
  # Enable limit ranges
  # Default: false
  enabled: false
  
  # Container limits
  container:
    default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
    max:
      cpu: "2"
      memory: "4Gi"
    min:
      cpu: "10m"
      memory: "64Mi"
```

---

## Scaling & Availability

### Horizontal Pod Autoscaler
**Automatic scaling based on metrics**

```yaml
autoscaling:
  # Enable autoscaling
  # Default: false
  enabled: true
  
  # Minimum replicas
  # Default: 1
  minReplicas: 2
  
  # Maximum replicas
  # Default: 10
  maxReplicas: 20
  
  # CPU threshold (percentage)
  # Default: 70
  targetCPUUtilizationPercentage: 70
  
  # Memory threshold (percentage)
  # Default: 80
  targetMemoryUtilizationPercentage: 80
  
  # Custom metrics
  # Default: []
  metrics: []
  
  # Scaling behavior
  # Default: {} (uses optimized defaults)
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
```

**Scaling Examples:**
```yaml
# Conservative scaling
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 6
  targetCPUUtilizationPercentage: 80

# Aggressive scaling
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 50
  targetCPUUtilizationPercentage: 60
  targetMemoryUtilizationPercentage: 70

# Custom metrics scaling
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Pods
      pods:
        metric:
          name: custom_metric
        target:
          type: AverageValue
          averageValue: "30"
```

### Pod Disruption Budget
**Maintains availability during updates**

```yaml
podDisruptionBudget:
  # Enable PDB
  # Default: false
  enabled: true
  
  # Minimum available pods
  # Default: 1
  minAvailable: 2
  
  # OR maximum unavailable pods
  # maxUnavailable: 1
```

**Examples:**
```yaml
# High availability
podDisruptionBudget:
  enabled: true
  minAvailable: 2

# Percentage-based
podDisruptionBudget:
  enabled: true
  minAvailable: "50%"

# Maximum unavailable
podDisruptionBudget:
  enabled: true
  maxUnavailable: 1
```

---

## Health Checks

### Liveness Probe
**Checks if the application is running**

```yaml
livenessProbe:
  # HTTP check
  httpGet:
    path: /health
    port: http
    scheme: HTTP
  
  # Timing configuration
  failureThreshold: 3      # Failures before restart
  periodSeconds: 30        # Check interval
  successThreshold: 1      # Successes to be considered healthy
  timeoutSeconds: 5        # Timeout per check
  initialDelaySeconds: 30  # Wait before first check
```

### Readiness Probe
**Checks if the application can receive traffic**

```yaml
readinessProbe:
  httpGet:
    path: /health
    port: http
    scheme: HTTP
  failureThreshold: 3
  periodSeconds: 10
  successThreshold: 1
  timeoutSeconds: 5
  initialDelaySeconds: 5
```

### Startup Probe
**Checks if the application has started**

```yaml
startupProbe:
  httpGet:
    path: /health
    port: http
    scheme: HTTP
  failureThreshold: 30     # More failures allowed during startup
  periodSeconds: 10
  successThreshold: 1
  timeoutSeconds: 5
  initialDelaySeconds: 10
```

**Health Check Examples:**
```yaml
# Fast-starting app
livenessProbe:
  httpGet:
    path: /ping
    port: http
  initialDelaySeconds: 10
  periodSeconds: 10

# Slow-starting app
startupProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 60

# Database health check
livenessProbe:
  httpGet:
    path: /health/db
    port: http
  initialDelaySeconds: 60
  periodSeconds: 30
  timeoutSeconds: 10

# Custom port health check
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

---

## Azure Integration

### Azure Key Vault
**Secure secret management with Azure Key Vault**

```yaml
azureKeyVault:
  # Enable Azure Key Vault integration
  # Default: false
  enabled: true
  
  # Use VM managed identity (false = use workload identity)
  # Default: false
  useVMManagedIdentity: false
  
  # Key Vault name
  # Default: ""
  vaultName: "my-keyvault"
  
  # Azure client ID (for workload identity)
  # Default: ""
  clientId: "12345678-1234-1234-1234-123456789012"
  
  # Azure tenant ID
  # Default: ""
  tenantId: "87654321-4321-4321-4321-210987654321"
  
  # Secret mappings (Azure secret name -> environment variable)
  secrets:
    database-password: DB_PASSWORD
    api-key: API_KEY
    connection-string: CONNECTION_STRING
```

**Examples:**
```yaml
# Basic setup
azureKeyVault:
  enabled: true
  vaultName: "myapp-secrets"
  clientId: "your-client-id"
  tenantId: "your-tenant-id"
  secrets:
    db-password: DATABASE_PASSWORD

# Multiple secrets
azureKeyVault:
  enabled: true
  vaultName: "prod-secrets"
  clientId: "prod-client-id"
  tenantId: "your-tenant-id"
  secrets:
    database-url: DATABASE_URL
    redis-password: REDIS_PASSWORD
    jwt-secret: JWT_SECRET
    smtp-password: SMTP_PASSWORD
```

### AKS-Specific Configuration
**Azure Kubernetes Service optimizations**

```yaml
aks:
  # Linux node selector
  nodeSelector:
    kubernetes.io/os: linux
    # kubernetes.io/arch: amd64
  
  # System tolerations
  tolerations: []
  
  # Workload Identity configuration
  workloadIdentity:
    enabled: true
    annotations:
      azure.workload.identity/client-id: "your-client-id"
    podLabels:
      azure.workload.identity/use: 'true'
  
  # Zone-aware scheduling
  topologySpreadConstraints:
    enabled: true
    constraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app.kubernetes.io/name: myapp
```

---

## Environment Variables

### Application Configuration
**Environment variables for your application**

```yaml
env:
  # Enable environment variables
  # Default: false
  enabled: true
  
  # Environment variable definitions
  # Default: {}
  variables:
    NODE_ENV: "production"
    LOG_LEVEL: "info"
    API_TIMEOUT: "30000"
    CACHE_TTL: "3600"
```

### External Environment Sources
**Load environment variables from external sources**

```yaml
# Load from additional ConfigMaps or Secrets
# Default: []
extraEnvFrom:
  - secretRef:
      name: external-secret
  - configMapRef:
      name: shared-config

# Additional environment variables
# Default: []
extraEnv:
  - name: COMPUTED_VALUE
    value: "computed-$(date +%s)"
  - name: SECRET_VALUE
    valueFrom:
      secretKeyRef:
        name: my-secret
        key: secret-key
```

**Examples:**
```yaml
# Web application
env:
  enabled: true
  variables:
    NODE_ENV: "production"
    PORT: "3000"
    SESSION_SECRET: "generated-secret"

# API service
env:
  enabled: true
  variables:
    LOG_LEVEL: "info"
    DB_POOL_SIZE: "10"
    CACHE_ENABLED: "true"
    API_RATE_LIMIT: "1000"

# Microservice
env:
  enabled: true
  variables:
    SERVICE_NAME: "user-service"
    JAEGER_ENDPOINT: "http://jaeger:14268/api/traces"
    METRICS_PORT: "9090"
```

---

## Storage & Volumes

### Volume Configuration
**Persistent and temporary storage**

```yaml
# Additional volumes
# Default: []
volumes:
  - name: config-volume
    configMap:
      name: app-config
  - name: cache-volume
    emptyDir: {}
  - name: persistent-storage
    persistentVolumeClaim:
      claimName: app-storage

# Volume mounts
# Default: []
volumeMounts:
  - name: config-volume
    mountPath: /etc/config
    readOnly: true
  - name: cache-volume
    mountPath: /tmp/cache
  - name: persistent-storage
    mountPath: /data
```

**Storage Examples:**
```yaml
# Configuration files
volumes:
  - name: app-config
    configMap:
      name: myapp-config
volumeMounts:
  - name: app-config
    mountPath: /app/config
    readOnly: true

# Temporary storage
volumes:
  - name: temp-storage
    emptyDir:
      sizeLimit: 1Gi
volumeMounts:
  - name: temp-storage
    mountPath: /tmp

# Persistent data
volumes:
  - name: data-storage
    persistentVolumeClaim:
      claimName: myapp-data
volumeMounts:
  - name: data-storage
    mountPath: /var/lib/data

# Shared storage between containers
volumes:
  - name: shared-data
    emptyDir: {}
volumeMounts:
  - name: shared-data
    mountPath: /shared
```

---

## Monitoring & Observability

### Prometheus Integration
**Metrics collection and monitoring**

```yaml
monitoring:
  # Enable monitoring
  # Default: false
  enabled: true
  
  # ServiceMonitor configuration
  serviceMonitor:
    # Enable ServiceMonitor creation
    enabled: true
    
    # Metrics scraping interval
    # Default: 30s
    interval: 30s
    
    # Scraping timeout
    # Default: 10s
    timeout: 10s
    
    # Metrics endpoint path
    # Default: /metrics
    path: /metrics
    
    # Port to scrape (uses service port if not specified)
    port: http
    
    # Additional labels
    # Default: {}
    labels:
      release: prometheus
    
    # Additional annotations
    # Default: {}
    annotations: {}
```

### Pod Annotations
**Metadata and monitoring annotations**

```yaml
# Pod annotations
# Default: {}
podAnnotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8080"
  prometheus.io/path: "/metrics"

# Pod labels
# Default: {}
podLabels:
  version: "v1.0.0"
  team: "backend"
```

### Compliance and Governance
**Audit logging and compliance**

```yaml
compliance:
  # Enable compliance features
  # Default: false
  enabled: true
  
  # Compliance framework
  # Options: NIST, SOC2, PCI-DSS, HIPAA, GDPR
  # Default: "NIST"
  framework: "NIST"
  
  # Compliance level
  # Options: baseline, moderate, high
  # Default: "moderate"
  level: "high"
  
  # Audit logging
  # Default: false
  auditLogging: true
  
  # Audit log level
  # Default: "info"
  auditLogLevel: "info"
  
  # Azure Log Analytics integration
  azureLogAnalytics:
    workspaceId: "your-workspace-id"
    sharedKey: "your-shared-key"
    logType: "KubernetesAuditLog"
```

---

## Advanced Configuration

### Deployment Strategy
**How updates are rolled out**

```yaml
# Deployment strategy
# Default: RollingUpdate
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 25%
    maxSurge: 25%

# Lifecycle hooks
# Default: {}
lifecycle:
  preStop:
    exec:
      command: ["/bin/sh", "-c", "sleep 15"]

# Termination grace period
# Default: 30
terminationGracePeriodSeconds: 60
```

### Scheduling Configuration
**Where pods are placed**

```yaml
# Node selector
# Default: {}
nodeSelector:
  disktype: ssd
  node-size: large

# Tolerations
# Default: []
tolerations:
  - key: "dedicated"
    operator: "Equal"
    value: "app"
    effect: "NoSchedule"

# Affinity rules
# Default: {}
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/os
          operator: In
          values:
          - linux

# Topology spread constraints
# Default: []
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: myapp

# Priority class
# Default: ""
priorityClassName: "high-priority"
```

### DNS Configuration
**DNS resolution optimization**

```yaml
# DNS policy
# Default: ClusterFirst
dnsPolicy: ClusterFirst

# DNS configuration
dnsConfig:
  options:
    - name: ndots
      value: "2"
    - name: edns0
```

### Init Containers and Sidecars
**Additional containers**

```yaml
# Init containers
# Default: []
initContainers:
  - name: migration
    image: migrate/migrate
    command: ['migrate', '-path', '/migrations', '-database', 'postgres://...', 'up']

# Sidecar containers
# Default: []
sidecars:
  - name: log-shipper
    image: fluent/fluent-bit:1.9
    volumeMounts:
      - name: varlog
        mountPath: /var/log
```

---

## 🔧 Troubleshooting Quick Reference

**Common problems and their configuration fixes**

| Problem | Symptoms | Configuration Fix | Example |
|---------|----------|------------------|---------|
| **Pod won't start** | `ImagePullBackOff` | Check image repository and tag | `image.repository: "correct-registry.azurecr.io/app"` |
| **App crashes** | `CrashLoopBackOff` | Fix port mismatch | `service.containerPort: 3000` (match your app) |
| **Health checks fail** | Pod marked unhealthy | Fix health check path | `livenessProbe.httpGet.path: "/api/health"` |
| **Out of memory** | `OOMKilled` | Increase memory limits | `resources.limits.memory: "1Gi"` |
| **Slow startup** | Startup timeouts | Increase startup probe timeout | `startupProbe.initialDelaySeconds: 60` |
| **Can't access app** | Connection refused | Enable ingress | `ingress.enabled: true` |
| **SSL errors** | Certificate errors | Configure TLS | `ingress.tls: [{"secretName": "app-tls", "hosts": ["app.com"]}]` |
| **Permission denied** | File access errors | Fix security context | `podSecurityContext.fsGroup: 1000` |
| **Network blocked** | Connection timeouts | Allow network traffic | `networkPolicy.enabled: false` (or configure rules) |
| **Scaling issues** | Fixed replica count | Enable autoscaling | `autoscaling.enabled: true` |
| **Secret access** | Authentication failures | Configure Key Vault | `azureKeyVault.enabled: true` |
| **High CPU usage** | Performance issues | Increase CPU limits | `resources.limits.cpu: "1000m"` |
| **Storage issues** | Disk space errors | Add persistent volumes | `volumes: [{"name": "data", "persistentVolumeClaim": {...}}]` |
| **Monitoring missing** | No metrics | Enable ServiceMonitor | `monitoring.enabled: true` |
| **Environment vars** | Config not loaded | Enable env variables | `env.enabled: true` |

---

## Default Values Summary

### ✅ **Enabled by Default:**
- Pod Security Standards (Restricted)
- Security Contexts (Non-root, read-only filesystem)
- Resource limits and requests
- Health checks (liveness, readiness, startup)
- Service account creation
- DNS optimization

### ❌ **Disabled by Default:**
- Ingress
- Autoscaling
- Pod Disruption Budget
- Network Policies
- Azure Key Vault integration
- Monitoring/ServiceMonitor
- Compliance features

### 🔧 **Requires Configuration:**
- Image repository and tag
- Service ports
- Ingress hosts and domains
- Azure Key Vault secrets
- Environment variables
- Volume mounts

---

## Configuration Validation

Use these commands to validate your configuration:

```bash
# Check template rendering
helm template myapp . --values values.yaml --debug

# Validate against cluster
helm lint .

# Check resource requirements
kubectl apply --dry-run=client -f <(helm template myapp . --values values.yaml)

# Run validation script
./validate-aks.sh
```

---

## 📋 Environment Configuration Checklist

**Pre-deployment validation checklist for different environments**

| Configuration | Development | Staging | Production | Critical |
|---------------|-------------|---------|------------|----------|
| **🚀 Basic Setup** | | | | |
| `image.repository` | ✅ Required | ✅ Required | ✅ Required | **Must match your app** |
| `image.tag` | ✅ Required | ✅ Required | ✅ Required | **Use specific versions in prod** |
| `service.containerPort` | ✅ Required | ✅ Required | ✅ Required | **Must match your app's port** |
| **🔧 Resources** | | | | |
| `resources.requests.cpu` | ⚠️ Optional | ✅ Required | ✅ Required | **Size based on load testing** |
| `resources.requests.memory` | ⚠️ Optional | ✅ Required | ✅ Required | **Size based on load testing** |
| `resources.limits.cpu` | ⚠️ Optional | ✅ Required | ✅ Required | **Prevent resource starvation** |
| `resources.limits.memory` | ⚠️ Optional | ✅ Required | ✅ Required | **Prevent OOMKilled** |
| `replicaCount` | ⚠️ 1 is fine | ✅ 2+ required | ✅ 3+ required | **High availability** |
| **📈 Scaling** | | | | |
| `autoscaling.enabled` | ❌ Not needed | ✅ Recommended | ✅ Required | **Handle traffic spikes** |
| `podDisruptionBudget.enabled` | ❌ Not needed | ✅ Recommended | ✅ Required | **Zero-downtime updates** |
| **🔒 Security** | | | | |
| `podSecurityContext.runAsNonRoot` | ✅ Enabled | ✅ Enabled | ✅ Enabled | **Security best practice** |
| `networkPolicy.enabled` | ⚠️ Optional | ✅ Recommended | ✅ Required | **Network security** |
| `azureKeyVault.enabled` | ⚠️ Optional | ✅ Recommended | ✅ Required | **Secret management** |
| **🌐 Networking** | | | | |
| `ingress.enabled` | ⚠️ Optional | ✅ Required | ✅ Required | **External access** |
| `ingress.tls` | ❌ Not needed | ✅ Recommended | ✅ Required | **SSL/TLS encryption** |
| **🩺 Health Checks** | | | | |
| `livenessProbe` | ✅ Enabled | ✅ Enabled | ✅ Enabled | **Auto-restart unhealthy pods** |
| `readinessProbe` | ✅ Enabled | ✅ Enabled | ✅ Enabled | **Traffic routing** |
| `startupProbe` | ✅ Enabled | ✅ Enabled | ✅ Enabled | **Slow-starting apps** |
| **📊 Monitoring** | | | | |
| `monitoring.enabled` | ⚠️ Optional | ✅ Recommended | ✅ Required | **Observability** |
| `podAnnotations` | ⚠️ Optional | ✅ Recommended | ✅ Required | **Metadata and tracking** |
| **⚙️ Environment** | | | | |
| `env.enabled` | ⚠️ As needed | ✅ Usually needed | ✅ Usually needed | **App configuration** |
| `env.variables` | ⚠️ As needed | ✅ Environment-specific | ✅ Environment-specific | **Environment settings** |

### Legend:
- ✅ **Required** - Must be configured
- ✅ **Recommended** - Strongly recommended
- ⚠️ **Optional** - Configure if needed
- ❌ **Not needed** - Skip for this environment
