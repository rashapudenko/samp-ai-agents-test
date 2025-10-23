# 🚀 Generic Deployment Template

**The easiest way to deploy secure, scalable applications on Azure Kubernetes Service**

## 🎯 What This Template Does For You

This template automatically configures everything your application needs to run securely and reliably on AKS:

### 🔒 **Security First**
- Runs as non-root user with minimal permissions
- Integrates with Azure Key Vault for secrets
- Network policies to control traffic
- Security scanning and compliance built-in

### 🚀 **Production Ready**
- Auto-scaling based on CPU and memory usage
- Health checks to restart unhealthy pods
- High availability across multiple zones
- Rolling updates with zero downtime

### ⚙️ **Azure Optimized**
- Works seamlessly with AKS features
- Azure Container Registry integration
- Workload Identity for secure Azure access
- Optimized for Azure networking

## 🚀 I Just Want to Deploy My App!

**Skip to:** [Getting Started Guide](docs/GETTING_STARTED.md) - **5 minute setup**

## 📋 Prerequisites

**Essential** (you need these):
- [ ] An AKS cluster (ask your DevOps team)
- [ ] `kubectl` and `helm` installed
- [ ] Your Docker image in a registry

**Nice to have**:
- [ ] Azure Key Vault for secrets
- [ ] Custom domain name

> 💡 **Don't have these?** Your platform team can help you get set up!


## 📚 Documentation

### 👨‍💻 **For Developers** (Start Here!)
| Guide | What You'll Learn | Time |
|-------|------------------|------|
| 🚀 [**Getting Started**](docs/GETTING_STARTED.md) | Deploy your first app | 10 min |
| 📚 [**Examples**](docs/EXAMPLES.md) | Real-world configurations | 15 min |
| ⚙️ [**Configuration Reference**](docs/CONFIGURATION_REFERENCE.md) | All possible settings | 30 min |

### 🏗️ **For DevOps Teams**
| Guide | What You'll Learn | Time |
|-------|------------------|------|
| 🔒 [**Security Guide**](docs/SECURITY.md) | Secure configurations | 20 min |
| ✅ [**Production Checklist**](docs/PRODUCTION_CHECKLIST.md) | Go-live requirements | 15 min |

## 🎮 Common Scenarios

### Web Application
```yaml
# Basic web app (React, Vue, Angular)
image:
  repository: "myregistry.azurecr.io/my-webapp"
  tag: "v1.0.0"
service:
  containerPort: 3000
ingress:
  enabled: true
  hosts:
    - host: myapp.example.com
```

### REST API
```yaml
# Backend API service
image:
  repository: "myregistry.azurecr.io/my-api"
  tag: "v1.0.0"
service:
  containerPort: 8080
ingress:
  enabled: true
  hosts:
    - host: api.example.com
      paths:
        - path: /api
```

### Background Worker
```yaml
# Processing jobs/queues
image:
  repository: "myregistry.azurecr.io/worker"
  tag: "v1.0.0"
service:
  containerPort: 8080
ingress:
  enabled: false  # No external access needed
```

> 📖 **More examples**: Check the [Examples Guide](docs/EXAMPLES.md)

## 🔄 Updating Your Application

```bash
# Update to a new version
helm upgrade my-app . \
  --set image.tag=v1.1.0 \
  -f values.yaml -f values.prod.yaml

# Check deployment status
kubectl get pods
kubectl logs -f deployment/my-app
```
---

## 📋 Quick Commands

```bash
# Validate your configuration
helm template my-app . -f values.yaml -f values.dev.yaml

# Deploy to development
helm install my-app . -f values.yaml -f values.dev.yaml

# Check deployment status
kubectl get pods -l app.kubernetes.io/instance=my-app

# View logs
kubectl logs -f deployment/my-app

# Update your app
helm upgrade my-app . --set image.tag=v1.1.0 -f values.yaml -f values.prod.yaml
```
