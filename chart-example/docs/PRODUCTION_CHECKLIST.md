# ✅ Production Readiness Checklist

**Before going live: Make sure your application is production-ready**

Use this checklist to ensure your application meets production standards for security, reliability, and observability.

## 🔒 Security Checklist

### Container Security
- [ ] **Non-root user**: App runs as non-root user (UID > 1000)
- [ ] **Read-only filesystem**: Root filesystem is read-only
- [ ] **No privileged escalation**: `allowPrivilegeEscalation: false`
- [ ] **Dropped capabilities**: All Linux capabilities dropped
- [ ] **Security context**: Proper security context configured

```yaml
# ✅ Example secure configuration
securityContext:
  runAsNonRoot: true
  runAsUser: 1001
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
```

### Network Security
- [ ] **Network policies**: Ingress and egress traffic restricted
- [ ] **TLS enabled**: All external traffic uses HTTPS
- [ ] **Service mesh**: Consider using Istio for service-to-service communication
- [ ] **Ingress controller**: Use trusted ingress controller (nginx, Azure Application Gateway)

```yaml
# ✅ Example network policy
networkPolicy:
  enabled: true
  policyTypes:
    - Ingress
    - Egress
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
```

### Secrets Management
- [ ] **Azure Key Vault**: Secrets stored in Azure Key Vault
- [ ] **Workload Identity**: Using Azure Workload Identity for authentication
- [ ] **No hardcoded secrets**: No secrets in container images or values.yaml
- [ ] **Secret rotation**: Automatic secret rotation configured

```yaml
# ✅ Example Azure Key Vault integration
azureKeyVault:
  enabled: true
  vaultName: "my-production-vault"
  clientId: "12345678-1234-1234-1234-123456789012"
  secrets:
    database-password: "DB_PASSWORD"
    api-key: "API_KEY"
```

## 🛡️ Reliability Checklist

### High Availability
- [ ] **Multiple replicas**: At least 3 replicas in production
- [ ] **Anti-affinity**: Pods spread across different nodes/zones
- [ ] **Pod disruption budget**: Minimum available pods during updates
- [ ] **Zone distribution**: Pods distributed across availability zones

```yaml
# ✅ Example HA configuration
replicaCount: 3
podDisruptionBudget:
  enabled: true
  minAvailable: 2
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          topologyKey: kubernetes.io/hostname
```

### Resource Management
- [ ] **Resource requests**: CPU and memory requests defined
- [ ] **Resource limits**: CPU and memory limits set
- [ ] **Right-sized resources**: Resources match actual usage
- [ ] **Quality of Service**: Guaranteed QoS class for critical apps

```yaml
# ✅ Example resource configuration
resources:
  requests:
    cpu: 200m
    memory: 256Mi
  limits:
    cpu: 1000m
    memory: 1Gi
```

### Health Checks
- [ ] **Liveness probe**: Detects and restarts unhealthy pods
- [ ] **Readiness probe**: Prevents traffic to unready pods
- [ ] **Startup probe**: Handles slow-starting applications
- [ ] **Probe endpoints**: Health check endpoints are lightweight

```yaml
# ✅ Example health check configuration
livenessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10
readinessProbe:
  httpGet:
    path: /ready
    port: http
  initialDelaySeconds: 5
  periodSeconds: 5
```

## 📊 Observability Checklist

### Monitoring
- [ ] **Metrics collection**: Prometheus metrics enabled
- [ ] **Service monitor**: ServiceMonitor configured
- [ ] **Dashboards**: Grafana dashboards created
- [ ] **SLIs defined**: Service Level Indicators identified

```yaml
# ✅ Example monitoring configuration
monitoring:
  enabled: true
  serviceMonitor:
    interval: 30s
    path: /metrics
    port: http
podAnnotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8080"
  prometheus.io/path: "/metrics"
```

### Logging
- [ ] **Structured logging**: JSON format preferred
- [ ] **Log aggregation**: Logs sent to centralized system
- [ ] **Log retention**: Appropriate retention policy
- [ ] **Log levels**: Production uses INFO or WARN level

```yaml
# ✅ Example logging configuration
env:
  enabled: true
  variables:
    LOG_LEVEL: "info"
    LOG_FORMAT: "json"
```

### Alerting
- [ ] **Error rate alerts**: High error rate triggers alerts
- [ ] **Latency alerts**: High response time triggers alerts
- [ ] **Resource alerts**: High CPU/memory usage triggers alerts
- [ ] **Availability alerts**: Service downtime triggers alerts

## 🚀 Performance Checklist

### Scaling
- [ ] **Horizontal Pod Autoscaler**: HPA configured for auto-scaling
- [ ] **Vertical Pod Autoscaler**: VPA configured for resource optimization
- [ ] **Cluster autoscaler**: Cluster can scale nodes automatically
- [ ] **Load testing**: Application tested under expected load

```yaml
# ✅ Example autoscaling configuration
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80
```

### Efficiency
- [ ] **Resource optimization**: Resources tuned based on actual usage
- [ ] **Image optimization**: Container images are minimal and efficient
- [ ] **Caching**: Appropriate caching strategies implemented
- [ ] **Database optimization**: Database queries optimized

## 🔄 Deployment Checklist

### CI/CD Pipeline
- [ ] **Automated testing**: Unit, integration, and e2e tests
- [ ] **Security scanning**: Container and dependency vulnerability scanning
- [ ] **Quality gates**: Code quality checks pass
- [ ] **Approval process**: Production deployments require approval

### Deployment Strategy
- [ ] **Rolling updates**: Zero-downtime deployment strategy
- [ ] **Blue-green deployment**: Consider for critical applications
- [ ] **Canary deployment**: Gradual rollout for risk mitigation
- [ ] **Rollback plan**: Quick rollback procedure documented

```yaml
# ✅ Example deployment strategy
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 25%
    maxSurge: 25%
```

### Environment Management
- [ ] **Environment parity**: Dev/staging/prod environments similar
- [ ] **Configuration management**: Environment-specific configurations
- [ ] **Database migrations**: Automated and tested
- [ ] **Feature flags**: Ability to enable/disable features

## 🌐 Infrastructure Checklist

### Networking
- [ ] **Load balancer**: External load balancer configured
- [ ] **DNS**: Custom domain names configured
- [ ] **CDN**: Content delivery network for static assets
- [ ] **Rate limiting**: API rate limiting implemented

### Storage
- [ ] **Persistent volumes**: Appropriate storage class selected
- [ ] **Backup strategy**: Data backup and recovery plan
- [ ] **Encryption**: Data encrypted at rest and in transit
- [ ] **Retention policy**: Data retention policy defined

### Disaster Recovery
- [ ] **Multi-region**: Consider multi-region deployment
- [ ] **Backup testing**: Regular backup restoration testing
- [ ] **RTO/RPO defined**: Recovery time and point objectives
- [ ] **Incident response**: Incident response plan documented

## 📋 Compliance Checklist

### Regulatory Compliance
- [ ] **GDPR compliance**: Data protection requirements met
- [ ] **SOC 2 compliance**: Security controls implemented
- [ ] **Industry standards**: Relevant industry standards followed
- [ ] **Audit logging**: Compliance audit logs enabled

### Security Compliance
- [ ] **Vulnerability scanning**: Regular security scans
- [ ] **Penetration testing**: Security testing performed
- [ ] **Security policies**: Security policies documented
- [ ] **Access controls**: Proper access controls implemented

## 🎯 Application-Specific Checklist

### Database Applications
- [ ] **Connection pooling**: Database connection pooling configured
- [ ] **Health checks**: Database connectivity checked
- [ ] **Migrations**: Database schema migrations automated
- [ ] **Backup verification**: Database backups tested

### API Applications
- [ ] **API documentation**: OpenAPI/Swagger documentation
- [ ] **Rate limiting**: API rate limiting implemented
- [ ] **Authentication**: Proper authentication mechanisms
- [ ] **Versioning**: API versioning strategy

### Web Applications
- [ ] **Static assets**: CDN for static assets
- [ ] **Compression**: Gzip compression enabled
- [ ] **Security headers**: Security headers configured
- [ ] **Performance monitoring**: Web performance monitoring

## 🔧 Pre-Deployment Validation

Run these commands before deploying to production:

```bash
# 1. Validate Helm template
helm template myapp . -f values.yaml -f values.prod.yaml

# 2. Lint the chart
helm lint . --values values.yaml --values values.prod.yaml

# 3. Check for security issues
trivy image myregistry.azurecr.io/myapp:v1.0.0

# 4. Validate Kubernetes resources
kubectl apply --dry-run=client -f rendered-manifests.yaml

# 5. Check resource quotas
kubectl describe quota -n production

# 6. Validate network policies
kubectl get networkpolicy -n production
```

## 📊 Post-Deployment Verification

After deployment, verify these items:

```bash
# 1. Check pod status
kubectl get pods -l app.kubernetes.io/instance=myapp

# 2. Check service endpoints
kubectl get endpoints myapp

# 3. Check ingress status
kubectl get ingress myapp

# 4. Test health endpoints
curl https://myapp.example.com/health

# 5. Check metrics
curl https://myapp.example.com/metrics

# 6. Check logs
kubectl logs -l app.kubernetes.io/instance=myapp --tail=20
```

## 🆘 Red Flags (Don't Deploy If...)

- ❌ **No health checks**: Application has no health check endpoints
- ❌ **No resource limits**: Containers have no resource limits
- ❌ **Running as root**: Application runs as root user
- ❌ **Hardcoded secrets**: Secrets are hardcoded in configuration
- ❌ **No monitoring**: No monitoring or alerting configured
- ❌ **Single replica**: Only one replica in production
- ❌ **No backups**: No backup strategy for persistent data
- ❌ **No rollback plan**: No plan for rolling back failed deployments

## 🎉 Ready for Production!

When you've completed this checklist, your application is ready for production deployment. Remember:

- 📈 **Monitor continuously**: Keep an eye on metrics and logs
- 🔄 **Iterate and improve**: Continuously improve your deployment
- 📚 **Document everything**: Keep deployment procedures documented
- 🤝 **Team knowledge**: Ensure team members know the deployment process

---

**Need help with any of these items?** Check the [Configuration Reference](CONFIGURATION_REFERENCE.md) for detailed settings or reach out to your platform team!
