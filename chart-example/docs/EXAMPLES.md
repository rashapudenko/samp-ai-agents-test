# 📚 Examples Guide

**Real-world examples for common use cases**

This guide provides copy-paste ready configurations for the most common deployment scenarios.

## 📋 Table of Contents

- [🚀 Recommended Configuration](#recommended-configuration)
  - [Development](#development)
  - [Production](#production)
- [📚 Samples](#samples)
  [🌐 Basic Web Application](#basic-web-application)
  - [⚡ REST API Service](#rest-api-service)
  - [🗄️ Microservice with Database](#microservice-with-database)
  - [📄 Static Website](#static-website)
  - [🔄 Background Worker](#background-worker)
  - [📦 Multi-Container Application](#multi-container-application)
  - [🏆 High Availability Setup](#high-availability-setup)
- [🚀 Deployment Commands](#-deployment-commands)
  - [Basic Deployment](#basic-deployment)
  - [Advanced Deployment](#advanced-deployment)
  - [Testing Configuration](#testing-configuration)
- [💡 Tips for Success](#-tips-for-success)

---

# Recommended configuration

## Development

```yaml
# -- Development namespace
namespace: development

# -- Single replica for development
replicaCount: 1

# -- Development image configuration
image:
  # -- Always pull latest for development
  pullPolicy: Always
  # -- Use development tag or leave empty for latest
  tag: "dev"

# -- Development ingress configuration
ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-staging
  hosts:
    - host: myapp.dev.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-dev-tls
      hosts:
        - myapp.dev.example.com

# -- Development resource limits (lower for cost optimization)
resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 50m
    memory: 128Mi

# -- Development environment variables
env:
  enabled: true
  variables:
    ASPNETCORE_ENVIRONMENT: "Development"

# -- Disabled autoscaling for development
autoscaling:
  enabled: false

# -- Disabled PDB for development
podDisruptionBudget:
  enabled: false

# -- Development network policy (more permissive)
networkPolicy:
  enabled: true
  ingress:
    - from: []  # Allow all ingress in development
  egress:
    - to: []    # Allow all egress in development

# -- Development security (relaxed for debugging)
podSecurityStandards:
  enabled: true
  enforceBaseline: true
  enforceRestricted: false  # Relaxed for development

# -- Development compliance (disabled)
compliance:
  enabled: false

# -- Development resource governance (disabled)
resourceQuota:
  enabled: false

limitRange:
  enabled: false

# -- Development AKS configuration
aks:
  workloadIdentity:
    enabled: true
    annotations:
      azure.workload.identity/client-id: "YOUR_WORKLOAD_IDENTITY_CLIENT_ID"

# -- Development Azure integration
azureKeyVault:
  enabled: true
  vaultName: "prod-keyvault"
  clientId: "YOUR_CLIENT_ID"
  tenantId: "YOUR_TENANT_ID"
  secrets:
    database-password: DB_PASSWORD
    api-key: API_KEY
    connection-string: CONNECTION_STRING
```

## Production

```yaml
# -- Production namespace
namespace: production

# -- High availability replica count
replicaCount: 3

# -- Production image configuration
image:
  # -- Never pull unless not present
  pullPolicy: IfNotPresent
  # -- Use specific version tag in production
  tag: "v1.0.0"

# -- Production ingress configuration
ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-prod-tls
      hosts:
        - myapp.example.com

# -- Production resource limits
resources:
  limits:
    cpu: 1000m
    memory: 2Gi
    ephemeral-storage: 2Gi
  requests:
    cpu: 500m
    memory: 1Gi
    ephemeral-storage: 1Gi

# -- Production environment variables
env:
  enabled: true
  variables:
    ASPNETCORE_ENVIRONMENT: "Production"

# -- Production health checks
livenessProbe:
  initialDelaySeconds: 30
  periodSeconds: 30
  failureThreshold: 3
  successThreshold: 1
  timeoutSeconds: 10

readinessProbe:
  initialDelaySeconds: 10
  periodSeconds: 10
  failureThreshold: 3
  successThreshold: 1
  timeoutSeconds: 5

startupProbe:
  initialDelaySeconds: 10
  periodSeconds: 10
  failureThreshold: 30
  successThreshold: 1
  timeoutSeconds: 5

# -- Production autoscaling
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80
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
      - type: Pods
        value: 4
        periodSeconds: 15

# -- Production PDB for high availability
podDisruptionBudget:
  enabled: true
  minAvailable: 2

# -- Production network policy (strict)
networkPolicy:
  enabled: true
  ingress:
    # Allow only from ingress controller
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080
    # Allow from monitoring namespace
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - protocol: TCP
          port: 8080
  egress:
    # Allow DNS resolution
    - to: []
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
    # Allow HTTPS to external services
    - to: []
      ports:
        - protocol: TCP
          port: 443
    # Allow database connections
    - to:
        - namespaceSelector:
            matchLabels:
              name: database
      ports:
        - protocol: TCP
          port: 5432

# -- Production monitoring (full)
monitoring:
  enabled: true
  serviceMonitor:
    enabled: true
    interval: 30s
    timeout: 10s
    path: /metrics
    labels:
      release: prometheus

# -- Production security (full enforcement)
podSecurityStandards:
  enabled: true
  enforceBaseline: true
  enforceRestricted: true

# -- Production compliance (Experimental)
compliance:
  enabled: true
  framework: "NIST"
  level: "high"
  auditLogging: true
  auditLogLevel: "info"
  auditDestinations:
    - type: "azureLogAnalytics"
      workspaceId: "YOUR_WORKSPACE_ID"
      sharedKey: "YOUR_SHARED_KEY"
  requirements:
    - id: "AC-2"
      name: "Account Management"
      description: "Manage information system accounts"
      status: "implemented"
      evidence: "RBAC and service accounts configured"
    - id: "AC-3"
      name: "Access Enforcement"
      description: "Enforce approved authorizations"
      status: "implemented"
      evidence: "Network policies and RBAC enforced"
    - id: "SC-8"
      name: "Transmission Confidentiality"
      description: "Protect communications"
      status: "implemented"
      evidence: "TLS encryption for all communications"
  encryptionAtRest: true

# -- Production resource governance (Experimental)
resourceQuota:
  enabled: true
  requests:
    cpu: "10"
    memory: "20Gi"
  limits:
    cpu: "20"
    memory: "40Gi"
  persistentvolumeclaims: "10"
  pods: "50"
  services: "20"
  secrets: "50"
  configmaps: "50"

limitRange:
  enabled: true
  container:
    default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
    max:
      cpu: "4"
      memory: "8Gi"
    min:
      cpu: "10m"
      memory: "64Mi"
  pod:
    max:
      cpu: "8"
      memory: "16Gi"
    min:
      cpu: "10m"
      memory: "64Mi"

# -- Production AKS configuration
aks:
  workloadIdentity:
    enabled: true
    annotations:
      azure.workload.identity/client-id: "YOUR_WORKLOAD_IDENTITY_CLIENT_ID"
  topologySpreadConstraints:
    enabled: true
    constraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app.kubernetes.io/name: myapp

# -- Production Azure integration
azureKeyVault:
  enabled: true
  useVMManagedIdentity: false
  vaultName: "prod-keyvault"
  clientId: "YOUR_CLIENT_ID"
  tenantId: "YOUR_TENANT_ID"
  secrets:
    database-password: DB_PASSWORD
    api-key: API_KEY
    connection-string: CONNECTION_STRING

# -- Production priority class
priorityClassName: "high-priority"

# -- Production termination grace period
terminationGracePeriodSeconds: 60

```

# Samples

## Basic Web Application

**Use case**: Simple web app (React, Vue, Angular, etc.)

```yaml
# values.yaml
image:
  repository: "myregistry.azurecr.io/my-webapp"
  tag: "v1.0.0"

service:
  port: 80
  containerPort: 3000

ingress:
  enabled: true
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80
```

**Deploy**:
```bash
helm install my-webapp . -f values.yaml -f values.prod.yaml
```

---

## REST API Service

**Use case**: Backend API (Node.js, Python, Java, etc.)

```yaml
# values.yaml
image:
  repository: "myregistry.azurecr.io/my-api"
  tag: "v2.1.0"

service:
  port: 8080
  containerPort: 8080

ingress:
  enabled: true
  className: "nginx"
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/cors-allow-origin: "*"
    nginx.ingress.kubernetes.io/enable-cors: "true"
  hosts:
    - host: api.example.com
      paths:
        - path: /api
          pathType: Prefix

# Health checks for API
livenessProbe:
  httpGet:
    path: /api/health
    port: http
  initialDelaySeconds: 30

readinessProbe:
  httpGet:
    path: /api/ready
    port: http
  initialDelaySeconds: 5

# Environment variables
env:
  enabled: true
  variables:
    NODE_ENV: "production"
    API_VERSION: "v1"
    PORT: "8080"

resources:
  requests:
    cpu: 200m
    memory: 256Mi
  limits:
    cpu: 1000m
    memory: 1Gi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80
```

---

## Microservice with Database

**Use case**: Service that connects to external database

```yaml
# values.yaml
image:
  repository: "myregistry.azurecr.io/user-service"
  tag: "v1.5.0"

service:
  port: 8080
  containerPort: 8080

# Database secrets from Azure Key Vault
azureKeyVault:
  enabled: true
  vaultName: "my-production-vault"
  clientId: "12345678-1234-1234-1234-123456789012"
  tenantId: "87654321-4321-4321-4321-210987654321"
  secrets:
    database-password: "DB_PASSWORD"
    database-url: "DATABASE_URL"
    jwt-secret: "JWT_SECRET"

# Environment configuration
env:
  enabled: true
  variables:
    DB_HOST: "postgres.example.com"
    DB_PORT: "5432"
    DB_NAME: "userdb"
    DB_USER: "api_user"
    REDIS_HOST: "redis.example.com"
    REDIS_PORT: "6379"

# Health checks that verify database connectivity
livenessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 60
  timeoutSeconds: 5

readinessProbe:
  httpGet:
    path: /health/ready
    port: http
  initialDelaySeconds: 30
  timeoutSeconds: 3

# Resource limits for database connections
resources:
  requests:
    cpu: 300m
    memory: 512Mi
  limits:
    cpu: 1500m
    memory: 2Gi

# Network policy for database access
networkPolicy:
  enabled: true
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

## Static Website

**Use case**: Static site (HTML, CSS, JS files)

```yaml
# values.yaml
image:
  repository: "nginx"
  tag: "alpine"

service:
  port: 80
  containerPort: 80

ingress:
  enabled: true
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
  hosts:
    - host: www.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: example-tls
      hosts:
        - www.example.com

# Health checks for nginx
livenessProbe:
  httpGet:
    path: /
    port: http
  initialDelaySeconds: 10

readinessProbe:
  httpGet:
    path: /
    port: http
  initialDelaySeconds: 5

# Minimal resources for static content
resources:
  requests:
    cpu: 50m
    memory: 64Mi
  limits:
    cpu: 200m
    memory: 256Mi

# Volume for static files
volumes:
  - name: static-content
    configMap:
      name: static-files

volumeMounts:
  - name: static-content
    mountPath: /usr/share/nginx/html
    readOnly: true
```

---

## Background Worker

**Use case**: Processing jobs, queues, scheduled tasks

```yaml
# values.yaml
image:
  repository: "myregistry.azurecr.io/worker"
  tag: "v1.0.0"

# No service needed for background workers
service:
  port: 8080
  containerPort: 8080

# Different deployment strategy for workers
strategy:
  type: Recreate

# Queue configuration
env:
  enabled: true
  variables:
    QUEUE_URL: "redis://redis.example.com:6379/0"
    WORKER_CONCURRENCY: "4"
    LOG_LEVEL: "info"

# No ingress for background workers
ingress:
  enabled: false

# Health checks for worker processes
livenessProbe:
  exec:
    command:
      - /bin/sh
      - -c
      - "ps aux | grep worker"
  initialDelaySeconds: 30

readinessProbe:
  exec:
    command:
      - /bin/sh
      - -c
      - "test -f /tmp/ready"
  initialDelaySeconds: 10

# Resource limits for processing
resources:
  requests:
    cpu: 500m
    memory: 1Gi
  limits:
    cpu: 2000m
    memory: 4Gi

# Autoscaling based on queue length
autoscaling:
  enabled: true
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: External
      external:
        metric:
          name: queue_length
        target:
          type: AverageValue
          averageValue: "5"
```

---

## Multi-Container Application

**Use case**: App with sidecar containers (logging, monitoring, etc.)

```yaml
# values.yaml
image:
  repository: "myregistry.azurecr.io/main-app"
  tag: "v1.0.0"

# Sidecar containers
sidecars:
  - name: log-forwarder
    image: fluent/fluent-bit:1.9
    resources:
      requests:
        cpu: 10m
        memory: 32Mi
      limits:
        cpu: 100m
        memory: 128Mi
    volumeMounts:
      - name: logs
        mountPath: /var/log/app
        readOnly: true

# Shared volumes
volumes:
  - name: logs
    emptyDir: {}
  - name: config
    configMap:
      name: app-config

volumeMounts:
  - name: logs
    mountPath: /var/log/app
  - name: config
    mountPath: /etc/app/config
    readOnly: true

# Service for main container
service:
  port: 8080
  containerPort: 8080

resources:
  requests:
    cpu: 200m
    memory: 256Mi
  limits:
    cpu: 1000m
    memory: 1Gi
```

---

## High Availability Setup

**Use case**: Critical production service with maximum uptime

```yaml
# values.yaml
image:
  repository: "myregistry.azurecr.io/critical-app"
  tag: "v1.0.0"

# High replica count
replicaCount: 5

service:
  port: 80
  containerPort: 8080

# Pod disruption budget
podDisruptionBudget:
  enabled: true
  minAvailable: 60%  # Always keep 60% of pods running

# Aggressive autoscaling
autoscaling:
  enabled: true
  minReplicas: 5
  maxReplicas: 50
  targetCPUUtilizationPercentage: 50  # Scale earlier
  targetMemoryUtilizationPercentage: 60

# Zone distribution
aks:
  topologySpreadConstraints:
    enabled: true
    constraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule

# Anti-affinity to spread across nodes
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
              - key: app.kubernetes.io/name
                operator: In
                values:
                  - critical-app
          topologyKey: kubernetes.io/hostname

# Resource guarantees
resources:
  requests:
    cpu: 500m
    memory: 1Gi
  limits:
    cpu: 2000m
    memory: 4Gi

# Robust health checks
livenessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: http
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 2

# Monitoring
monitoring:
  enabled: true
  serviceMonitor:
    interval: 15s
    timeout: 10s
    path: /metrics
```

---

## 🚀 Deployment Commands

### Basic Deployment
```bash
# Development
helm install myapp . -f values.yaml -f values.dev.yaml

# Production
helm install myapp . -f values.yaml -f values.prod.yaml

# Staging
helm install myapp . -f values.yaml -f values.staging.yaml
```

### Advanced Deployment
```bash
# Override specific values
helm install myapp . \
  -f values.yaml -f values.prod.yaml \
  --set image.tag=v1.2.0 \
  --set replicaCount=5

# Dry run first
helm install myapp . \
  -f values.yaml -f values.prod.yaml \
  --dry-run --debug

# Upgrade with rollback safety
helm upgrade myapp . \
  -f values.yaml -f values.prod.yaml \
  --atomic --timeout 10m
```

### Testing Configuration
```bash
# Validate template
helm template myapp . -f values.yaml -f values.prod.yaml

# Check differences
helm diff upgrade myapp . -f values.yaml -f values.prod.yaml

# Test connection
kubectl port-forward service/myapp 8080:80
```

---

## 💡 Tips for Success

1. **Start Simple**: Begin with basic configuration and add complexity gradually
2. **Use Environment Files**: Keep environment-specific settings in separate files
3. **Test Locally**: Always use `helm template` before deploying
4. **Monitor Everything**: Enable health checks and monitoring from day one
5. **Document Changes**: Keep notes about what you changed and why
6. **Plan for Scale**: Consider autoscaling and resource limits early
7. **Security First**: Enable security features before going to production

