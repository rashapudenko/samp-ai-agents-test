# 🚀 Getting Started - Your First Application

**Never used Helm before? This guide will get you deploying in 10 minutes!**

## What You'll Learn

By the end of this guide, you'll have:
- ✅ Deployed your first application to AKS
- ✅ Configured basic settings like ports and domains
- ✅ Learned how to update your application
- ✅ Know where to go for help

## Prerequisites

Make sure you have these installed:
- [ ] `kubectl` (to talk to Kubernetes)
- [ ] `helm` (to deploy applications)
- [ ] Access to an AKS cluster

> **Don't have these?** Your DevOps team can help you get set up!

## Step 1: Get the Template

Copy this template to your application folder:

```bash
# Go to your application folder
cd my-application/

# Copy the template
cp -r /path/to/this/template ./helm/

# Go to the template
cd helm/
```

## Step 2: Configure Your Application

Edit the `values.yaml` file and change these **essential** settings:

```yaml
# 🖼️ Your Docker image
image:
  repository: "your-registry.azurecr.io/your-app"
  tag: "v1.0.0"

# 🌐 Your app's port settings
service:
  port: 80              # Port that users will access
  containerPort: 8080   # Port your app listens on inside the container

# 🔗 Your domain (optional)
ingress:
  enabled: true
  hosts:
    - host: your-app.example.com
      paths:
        - path: /
```

> **💡 Quick tip**: Don't know your container port? Check your `Dockerfile` or ask your team!

## Step 3: Deploy Your Application

```bash
# Deploy to development environment
helm install my-app . -f values.yaml -f values.dev.yaml

# Check if it's running
kubectl get pods

# See the logs
kubectl logs -f deployment/my-app
```

That's it! Your app is now running on AKS! 🎉

## Step 4: Access Your Application

### If you enabled ingress (with a domain):
```bash
# Your app should be available at your domain
curl https://your-app.example.com
```

### If you didn't set up a domain:
```bash
# Create a temporary tunnel to your app
kubectl port-forward service/my-app 8080:80

# Now visit http://localhost:8080 in your browser
```

## Step 5: Update Your Application

When you have a new version:

```bash
# Update to version 1.1.0
helm upgrade my-app . \
  --set image.tag=v1.1.0 \
  -f values.yaml -f values.dev.yaml

# Check the rollout
kubectl rollout status deployment/my-app
```
