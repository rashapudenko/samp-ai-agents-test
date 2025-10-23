# 🔒 Security Guide

**Keep your applications secure with these essential security practices**

This guide covers the key security features and best practices for deploying secure applications on AKS.

## 🎯 Security Quick Start

### Essential Security Settings

Add these to your `values.yaml` for basic security:

```yaml
# Run as non-root user
securityContext:
  runAsNonRoot: true
  runAsUser: 1001
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL

# Pod-level security
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1001
  runAsGroup: 1001
  fsGroup: 1001
  seccompProfile:
    type: RuntimeDefault

# Network security
networkPolicy:
  enabled: true
  policyTypes:
    - Ingress
    - Egress

# Use Azure Key Vault for secrets
azureKeyVault:
  enabled: true
  vaultName: "my-keyvault"
  clientId: "your-client-id"
  secrets:
    database-password: "DB_PASSWORD"
    api-key: "API_KEY"
```

## 🛡️ Security Features

### 1. Container Security

**Why it matters**: Prevents privilege escalation and limits attack surface

```yaml
# Secure container configuration
securityContext:
  # Don't run as root
  runAsNonRoot: true
  runAsUser: 1001
  runAsGroup: 1001
  
  # Make filesystem read-only
  readOnlyRootFilesystem: true
  
  # Prevent privilege escalation
  allowPrivilegeEscalation: false
  
  # Drop all Linux capabilities
  capabilities:
    drop:
      - ALL
```

**Common issues**:
- App writes to `/tmp` but filesystem is read-only
- App needs to write logs to `/var/log`

**Solution**: Add writable volumes
```yaml
volumes:
  - name: tmp
    emptyDir: {}
  - name: var-log
    emptyDir: {}

volumeMounts:
  - name: tmp
    mountPath: /tmp
  - name: var-log
    mountPath: /var/log
```

### 2. Network Security

**Why it matters**: Controls who can talk to your application

```yaml
# Network policy example
networkPolicy:
  enabled: true
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Only allow traffic from ingress controller
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080
  egress:
    # Only allow HTTPS to external services
    - to: []
      ports:
        - protocol: TCP
          port: 443
    # Allow DNS resolution
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: UDP
          port: 53
```

### 3. Secrets Management

**Why it matters**: Keeps sensitive data secure and rotatable

```yaml
# Azure Key Vault integration
azureKeyVault:
  enabled: true
  vaultName: "my-production-vault"
  clientId: "12345678-1234-1234-1234-123456789012"
  tenantId: "87654321-4321-4321-4321-210987654321"
  secrets:
    # Key Vault secret name -> Environment variable name
    database-connection-string: "DATABASE_URL"
    api-key: "API_KEY"
    jwt-secret: "JWT_SECRET"
    oauth-client-secret: "OAUTH_CLIENT_SECRET"
```

**Never do this**:
```yaml
❌ # Don't hardcode secrets
env:
  enabled: true
  variables:
    DATABASE_PASSWORD: "super-secret-password"
    API_KEY: "my-api-key-123"
```

### 4. Pod Security Standards

**Why it matters**: Enforces security policies across your cluster

```yaml
# Enable Pod Security Standards
podSecurityStandards:
  enabled: true
  enforceBaseline: true
  enforceRestricted: true
  runAsUser: 1001
  runAsGroup: 1001
  fsGroup: 1001
```

## 🔐 Azure Security Integration

### Workload Identity

**What it is**: Secure way to access Azure services without passwords

```yaml
# Enable Workload Identity
aks:
  workloadIdentity:
    enabled: true
    annotations:
      azure.workload.identity/client-id: "your-client-id"
    podLabels:
      azure.workload.identity/use: 'true'
```

### Azure Key Vault

**What it is**: Centralized secrets management

**Setup steps**:
1. Create Azure Key Vault
2. Add secrets to Key Vault
3. Create Azure AD identity
4. Grant identity access to Key Vault
5. Configure in your application

```yaml
# Key Vault configuration
azureKeyVault:
  enabled: true
  vaultName: "my-keyvault"
  clientId: "your-workload-identity-client-id"
  tenantId: "your-tenant-id"
  secrets:
    # Mapping: KeyVault-secret-name -> Environment-variable-name
    database-password: "DB_PASSWORD"
    redis-password: "REDIS_PASSWORD"
    sendgrid-api-key: "SENDGRID_API_KEY"
```

## 🚨 Security Compliance

### NIST Framework

For NIST compliance, enable these features:

```yaml
# NIST compliance configuration
compliance:
  enabled: true
  framework: "NIST"
  level: "moderate"
  auditLogging: true
  auditLogLevel: "info"
  encryptionAtRest: true
  
  # Required controls
  requirements:
    - id: "AC-2"
      name: "Account Management"
      status: "implemented"
    - id: "AC-3"
      name: "Access Enforcement"
      status: "implemented"
    - id: "SC-8"
      name: "Transmission Confidentiality"
      status: "implemented"
```

### SOC 2 Compliance

For SOC 2 compliance:

```yaml
# SOC 2 compliance configuration
compliance:
  enabled: true
  framework: "SOC2"
  level: "high"
  auditLogging: true
  
  # SOC 2 Type II requirements
  requirements:
    - id: "CC6.1"
      name: "Logical Access Security"
      status: "implemented"
    - id: "CC6.2"
      name: "Access Credentials"
      status: "implemented"
    - id: "CC6.3"
      name: "Network Access"
      status: "implemented"
```

## 🔍 Security Monitoring

### Audit Logging

**Why it matters**: Track who did what and when

```yaml
# Enable audit logging
compliance:
  enabled: true
  auditLogging: true
  auditLogLevel: "info"
  azureLogAnalytics:
    workspaceId: "your-workspace-id"
    sharedKey: "your-shared-key"
    logType: "KubernetesAuditLog"
```

### Security Monitoring

**Why it matters**: Detect security issues early

```yaml
# Enable security monitoring
monitoring:
  enabled: true
  serviceMonitor:
    interval: 30s
    path: /metrics
    port: http
    labels:
      security.monitoring: "enabled"

# Security-focused pod annotations
podAnnotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8080"
  prometheus.io/path: "/metrics"
  security.monitoring/enabled: "true"
```

## 🛠️ Security Best Practices

### 1. Image Security

**Use trusted base images**:
```yaml
# ✅ Good: Use official, minimal images
image:
  repository: "myregistry.azurecr.io/myapp"
  tag: "v1.0.0"  # Use specific version tags

# ❌ Bad: Using latest or unknown images
image:
  repository: "random-dockerhub-user/myapp"
  tag: "latest"
```

**Scan images for vulnerabilities**:
```bash
# Scan image before deployment
trivy image myregistry.azurecr.io/myapp:v1.0.0

# Scan during CI/CD
az acr task run --registry myregistry --name security-scan
```

### 2. Resource Security

**Set resource limits**:
```yaml
# Prevents resource exhaustion attacks
resources:
  limits:
    cpu: 1000m
    memory: 1Gi
    ephemeral-storage: 1Gi
  requests:
    cpu: 100m
    memory: 128Mi
    ephemeral-storage: 100Mi
```

### 3. Environment Security

**Development vs Production**:
```yaml
# Development (relaxed security)
# values.dev.yaml
podSecurityStandards:
  enabled: false
networkPolicy:
  enabled: false
securityContext:
  runAsNonRoot: false

# Production (strict security)
# values.prod.yaml
podSecurityStandards:
  enabled: true
  enforceRestricted: true
networkPolicy:
  enabled: true
securityContext:
  runAsNonRoot: true
  readOnlyRootFilesystem: true
```

## 🔧 Common Security Issues

### Issue 1: "Operation not permitted" errors

**Problem**: App can't write files due to read-only filesystem

**Solution**: Add writable volumes
```yaml
volumes:
  - name: tmp
    emptyDir: {}
  - name: cache
    emptyDir: {}

volumeMounts:
  - name: tmp
    mountPath: /tmp
  - name: cache
    mountPath: /var/cache
```

### Issue 2: Network connectivity issues

**Problem**: App can't connect to external services

**Solution**: Update network policy
```yaml
networkPolicy:
  enabled: true
  egress:
    # Allow HTTPS to external APIs
    - to: []
      ports:
        - protocol: TCP
          port: 443
    # Allow database access
    - to:
        - namespaceSelector:
            matchLabels:
              name: database
      ports:
        - protocol: TCP
          port: 5432
```

### Issue 3: Secret access issues

**Problem**: App can't access secrets from Key Vault

**Solution**: Check workload identity setup
```bash
# Verify workload identity is configured
kubectl get serviceaccount -o yaml | grep azure.workload.identity

# Check if secret provider class is created
kubectl get secretproviderclass

# Check if secrets are mounted
kubectl describe pod <pod-name> | grep -A10 volumes
```

## 📊 Security Validation

### Pre-Deployment Checks

Run these before deploying:

```bash
# 1. Scan container image
trivy image myregistry.azurecr.io/myapp:v1.0.0

# 2. Check security context
helm template myapp . -f values.yaml -f values.prod.yaml | grep -A10 securityContext

# 3. Validate network policies
kubectl apply --dry-run=client -f networkpolicy.yaml

# 4. Check RBAC permissions
kubectl auth can-i --list --as=system:serviceaccount:default:myapp
```

### Post-Deployment Verification

After deployment:

```bash
# 1. Check pod security context
kubectl get pod <pod-name> -o yaml | grep -A10 securityContext

# 2. Verify network policies
kubectl get networkpolicy

# 3. Check secret access
kubectl exec <pod-name> -- printenv | grep -E "(PASSWORD|KEY|SECRET)"

# 4. Test network connectivity
kubectl exec <pod-name> -- curl -I https://api.example.com
```

## 🆘 Security Incident Response

### If you suspect a security issue:

1. **Immediately**:
   - Scale down the affected deployment
   - Collect logs and pod information
   - Notify security team

2. **Investigation**:
   ```bash
   # Collect evidence
   kubectl logs <pod-name> > incident-logs.txt
   kubectl get events --sort-by='.metadata.creationTimestamp' > events.txt
   kubectl describe pod <pod-name> > pod-details.txt
   ```

3. **Recovery**:
   - Update container image if compromised
   - Rotate all secrets
   - Deploy patched version
   - Monitor for unusual activity

## 🎯 Security Checklist

Before going to production:

- [ ] Container runs as non-root
- [ ] Filesystem is read-only
- [ ] Resource limits are set
- [ ] Network policies are enabled
- [ ] Secrets are in Key Vault
- [ ] Workload identity is configured
- [ ] Security monitoring is enabled
- [ ] Images are scanned for vulnerabilities
- [ ] Compliance requirements are met
- [ ] Incident response plan is documented

---

**Need help with security?** Check the [Production Checklist](PRODUCTION_CHECKLIST.md) or reach out to your security team!
