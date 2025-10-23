# Security Vulnerabilities Knowledge Base (vuln-kb) Helm Chart

This Helm chart deploys the Security Vulnerabilities Knowledge Base RAG application to Kubernetes. The application consists of a FastAPI backend and Next.js frontend that provides intelligent query capabilities over security vulnerability data.

## Prerequisites

- Kubernetes cluster (v1.19+)
- Helm 3.0+
- Default storage class configured (or custom storage class specified)
- Azure OpenAI API credentials

## Architecture

The chart deploys two main components:

### Backend (FastAPI)
- **Image**: `vuln-kb-backend:latest`
- **Port**: 8000
- **Health Check**: `/api/health`
- **Features**:
  - RAG (Retrieval-Augmented Generation) engine
  - Vector database integration
  - Security vulnerability scraping
  - Azure OpenAI integration

### Frontend (Next.js)
- **Image**: `vuln-kb-frontend:latest` 
- **Port**: 3000
- **Health Check**: `/`
- **Features**:
  - Interactive chat interface
  - Search and filter capabilities
  - Responsive web design

## Installation

### 1. Clone and prepare
```bash
git clone <repository-url>
cd helm-chart/vuln-kb
```

### 2. Configure values
Edit `values.yaml` and set required Azure OpenAI credentials:
```yaml
backend:
  secretEnv:
    AZURE_OPENAI_API_KEY: "your-api-key"
    AZURE_OPENAI_ENDPOINT: "https://your-openai.openai.azure.com/"
    AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT: "text-embedding-ada-002"
    AZURE_OPENAI_COMPLETIONS_DEPLOYMENT: "gpt-4o"
```

### 3. Install the chart
```bash
helm install vuln-kb . -f values.yaml
```

## Configuration

### Key Configuration Options

#### Backend Configuration
```yaml
backend:
  image:
    repository: vuln-kb-backend
    tag: latest
  
  replicaCount: 1
  
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 500m
      memory: 512Mi
  
  persistence:
    data:
      enabled: true
      size: 10Gi
    logs:
      enabled: true
      size: 5Gi
```

#### Frontend Configuration
```yaml
frontend:
  image:
    repository: vuln-kb-frontend
    tag: latest
  
  replicaCount: 1
  
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 250m
      memory: 256Mi
```

#### Ingress Configuration
```yaml
frontend:
  ingress:
    enabled: true
    className: "nginx"
    annotations:
      nginx.ingress.kubernetes.io/rewrite-target: /
    hosts:
      - host: vuln-kb.yourdomain.com
        paths:
          - path: /
            pathType: Prefix

backend:
  ingress:
    enabled: true
    className: "nginx"
    hosts:
      - host: vuln-kb-api.yourdomain.com
        paths:
          - path: /
            pathType: Prefix
```

## Persistence

The backend requires persistent storage for:

1. **Data Volume** (`/app/app/data`): Stores SQLite database and vector database
   - Default size: 10Gi
   - Contains vulnerability data and embeddings

2. **Logs Volume** (`/app/logs`): Application logs
   - Default size: 5Gi
   - Contains application and access logs

## Security Features

- **Non-root containers**: Both services run as non-root users
- **Security contexts**: Configured with security best practices
- **Secret management**: Sensitive credentials stored in Kubernetes secrets
- **Service accounts**: Dedicated service account with minimal privileges
- **Network policies**: Ready for network policy implementation

## Monitoring and Health Checks

### Health Endpoints
- **Backend**: `http://backend:8000/api/health`
- **Frontend**: `http://frontend:3000/`

### Probes Configuration
```yaml
backend:
  livenessProbe:
    httpGet:
      path: /api/health
      port: 8000
    initialDelaySeconds: 40
    periodSeconds: 30
  
  readinessProbe:
    httpGet:
      path: /api/health
      port: 8000
    initialDelaySeconds: 20
    periodSeconds: 10
```

## Scaling and Performance

### Horizontal Scaling
```yaml
backend:
  replicaCount: 3  # Scale backend pods

frontend:
  replicaCount: 2  # Scale frontend pods
```

### Resource Optimization
```yaml
backend:
  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 2000m
      memory: 2Gi
```

## Troubleshooting

### Common Issues

1. **Pod fails to start**: Check Azure OpenAI credentials
   ```bash
   kubectl logs deployment/vuln-kb-backend
   ```

2. **Storage issues**: Verify storage class exists
   ```bash
   kubectl get storageclass
   ```

3. **Service connectivity**: Check service endpoints
   ```bash
   kubectl get endpoints
   ```

### Debug Commands
```bash
# Check pod status
kubectl get pods -l app.kubernetes.io/name=vuln-kb

# View logs
kubectl logs -f deployment/vuln-kb-backend
kubectl logs -f deployment/vuln-kb-frontend

# Check services
kubectl get svc -l app.kubernetes.io/name=vuln-kb

# Describe problematic resources
kubectl describe pod <pod-name>
```

## Upgrading

```bash
helm upgrade vuln-kb . -f values.yaml
```

## Uninstalling

```bash
helm uninstall vuln-kb
```

**Note**: This will not delete persistent volume claims. To remove them:
```bash
kubectl delete pvc -l app.kubernetes.io/name=vuln-kb
```

## Development

### Local Development
For local development with port forwarding:
```bash
# Backend API
kubectl port-forward svc/vuln-kb-backend 8000:8000

# Frontend
kubectl port-forward svc/vuln-kb-frontend 3000:3000
```

### Custom Images
To use custom images:
```yaml
backend:
  image:
    repository: your-registry/vuln-kb-backend
    tag: v1.0.0

frontend:
  image:
    repository: your-registry/vuln-kb-frontend
    tag: v1.0.0
```

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Kubernetes events: `kubectl get events`
3. Check application logs
4. Verify configuration in `values.yaml`