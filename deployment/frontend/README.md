# Vulnerability RAG Frontend Helm Chart

This Helm chart deploys the Next.js frontend application for the Security Vulnerabilities RAG system.

## Overview

The frontend service is a **public-facing service** that:
- Provides the user interface for vulnerability search and chat
- Implements React components for security vulnerability queries
- Connects to the internal backend API service
- **Exposes ingress** for external user access

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- Azure Container Registry access
- Nginx Ingress Controller
- Cert-Manager for TLS certificates
- Sufficient cluster resources

## Installation

### Development Environment
```bash
helm install vulnerability-rag-frontend . \
  -f values.yaml \
  -f values.dev.yaml \
  -n frontend-dev \
  --create-namespace
```

### QA Environment
```bash
helm install vulnerability-rag-frontend . \
  -f values.yaml \
  -f values.qa.yaml \
  -n frontend-qa \
  --create-namespace
```

### Production Environment
```bash
helm install vulnerability-rag-frontend . \
  -f values.yaml \
  -f values.prod.yaml \
  -n frontend-prod \
  --create-namespace
```

## Configuration

### Environment-Specific Images

| Environment | Registry | Image Name | Tag |
|------------|----------|------------|-----|
| Development | mydevacr.azurecr.io | frontend-dev | dev |
| QA | myqaacr.azurecr.io | frontend-qa | qa |
| Production | myprodacr.azurecr.io | frontend-prod | prod |

### Environment-Specific Domains

| Environment | Domain |
|------------|---------|
| Development | vulnerability-rag.dev.example.com |
| QA | vulnerability-rag.qa.example.com |
| Production | vulnerability-rag.company.com |

### Key Configuration Options

- **Public Service**: Ingress enabled with TLS termination
- **Security**: Pod Security Standards enforced
- **Rate Limiting**: Production includes rate limiting
- **Health Checks**: Available at `/api/health` endpoint
- **Autoscaling**: HPA enabled for QA/Prod environments
- **Network Policies**: Allow ingress, restrict egress to backend

### Resource Requirements

| Environment | CPU Request | Memory Request | CPU Limit | Memory Limit |
|------------|-------------|----------------|-----------|--------------|
| Development | 50m | 128Mi | 200m | 512Mi |
| QA | 75m | 192Mi | 400m | 768Mi |
| Production | 100m | 256Mi | 500m | 1Gi |

## Backend Integration

The frontend connects to the backend service using internal Kubernetes DNS:

| Environment | Backend URL |
|------------|-------------|
| Development | http://vulnerability-rag-backend.backend-dev.svc.cluster.local |
| QA | http://vulnerability-rag-backend.backend-qa.svc.cluster.local |
| Production | http://vulnerability-rag-backend.backend-prod.svc.cluster.local |

## Security Features

- Non-root container execution
- Read-only root filesystem
- Security contexts with dropped capabilities
- Network policies for traffic isolation
- TLS encryption with Let's Encrypt certificates
- Rate limiting (production)
- Azure Key Vault integration (production)
- Workload Identity support

## Monitoring

The service includes:
- Health check endpoints at `/api/health`
- Prometheus metrics (optional)
- Audit logging (production)

## TLS Certificates

The chart uses cert-manager for automatic TLS certificate management:
- Development: Let's Encrypt staging
- QA: Let's Encrypt staging
- Production: Let's Encrypt production

## Uninstallation

```bash
helm uninstall vulnerability-rag-frontend -n <namespace>
```