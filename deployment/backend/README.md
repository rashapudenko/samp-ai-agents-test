# Vulnerability RAG Backend Helm Chart

This Helm chart deploys the FastAPI backend service for the Security Vulnerabilities RAG system.

## Overview

The backend service is an **internal service** that:
- Provides FastAPI REST API endpoints for vulnerability queries
- Implements RAG (Retrieval-Augmented Generation) engine
- Handles data processing and embedding generation
- Connects to vector databases and external APIs
- **Does NOT expose ingress** (internal service only)

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- Azure Container Registry access
- Sufficient cluster resources

## Installation

### Development Environment
```bash
helm install vulnerability-rag-backend . \
  -f values.yaml \
  -f values.dev.yaml \
  -n backend-dev \
  --create-namespace
```

### QA Environment
```bash
helm install vulnerability-rag-backend . \
  -f values.yaml \
  -f values.qa.yaml \
  -n backend-qa \
  --create-namespace
```

### Production Environment
```bash
helm install vulnerability-rag-backend . \
  -f values.yaml \
  -f values.prod.yaml \
  -n backend-prod \
  --create-namespace
```

## Configuration

### Environment-Specific Images

| Environment | Registry | Image Name | Tag |
|------------|----------|------------|-----|
| Development | mydevacr.azurecr.io | backend-dev | dev |
| QA | myqaacr.azurecr.io | backend-qa | qa |
| Production | myprodacr.azurecr.io | backend-prod | prod |

### Key Configuration Options

- **Internal Service**: ClusterIP service type, no ingress
- **Security**: Pod Security Standards enforced
- **Monitoring**: Prometheus metrics at `/metrics`
- **Health Checks**: Available at `/health` endpoint
- **Autoscaling**: HPA enabled for QA/Prod environments
- **Network Policies**: Restrict traffic to/from frontend only

### Resource Requirements

| Environment | CPU Request | Memory Request | CPU Limit | Memory Limit |
|------------|-------------|----------------|-----------|--------------|
| Development | 100m | 256Mi | 500m | 1Gi |
| QA | 200m | 384Mi | 750m | 1.5Gi |
| Production | 250m | 512Mi | 1000m | 2Gi |

## Security Features

- Non-root container execution
- Read-only root filesystem
- Security contexts with dropped capabilities
- Network policies for traffic isolation
- Azure Key Vault integration (production)
- Workload Identity support

## Monitoring

The service exposes Prometheus metrics at `/metrics` endpoint and includes:
- ServiceMonitor for Prometheus scraping
- Health check endpoints
- Audit logging (production)

## Uninstallation

```bash
helm uninstall vulnerability-rag-backend -n <namespace>
```