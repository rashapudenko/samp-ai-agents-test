# GitHub Actions CI/CD Workflows

This directory contains the GitHub Actions workflows for the Security Vulnerabilities RAG application.

## Setup Instructions

⚠️ **Important**: Due to GitHub App permissions, these workflow files cannot be automatically placed in `.github/workflows/`. You need to manually copy them to the correct location.

### 1. Copy Workflow Files

```bash
# Create workflows directory if it doesn't exist
mkdir -p .github/workflows

# Copy workflow files
cp workflows/backend-ci-cd.yml .github/workflows/
cp workflows/frontend-ci-cd.yml .github/workflows/
```

### 2. Required Secrets

Configure the following secrets in your GitHub repository (`Settings > Secrets and variables > Actions`):

#### Development Environment
- `DEV_ACR_USERNAME` - Azure Container Registry username for dev
- `DEV_ACR_PASSWORD` - Azure Container Registry password for dev  
- `DEV_AZURE_CREDENTIALS` - Azure service principal credentials for dev
- `DEV_RESOURCE_GROUP` - Azure resource group for dev AKS cluster
- `DEV_AKS_CLUSTER` - Name of dev AKS cluster

#### QA Environment
- `QA_ACR_USERNAME` - Azure Container Registry username for qa
- `QA_ACR_PASSWORD` - Azure Container Registry password for qa
- `QA_AZURE_CREDENTIALS` - Azure service principal credentials for qa
- `QA_RESOURCE_GROUP` - Azure resource group for qa AKS cluster
- `QA_AKS_CLUSTER` - Name of qa AKS cluster

#### Production Environment
- `PROD_ACR_USERNAME` - Azure Container Registry username for prod
- `PROD_ACR_PASSWORD` - Azure Container Registry password for prod
- `PROD_AZURE_CREDENTIALS` - Azure service principal credentials for prod
- `PROD_RESOURCE_GROUP` - Azure resource group for prod AKS cluster
- `PROD_AKS_CLUSTER` - Name of prod AKS cluster

### 3. Environment Protection Rules

Configure environment protection rules in GitHub (`Settings > Environments`):

#### Development Environments
- `dev` (backend)
- `dev-frontend` (frontend)
- **No approval required** - automatic deployment

#### QA Environments
- `qa` (backend)
- `qa-frontend` (frontend)
- **Approval required** - add required reviewers

#### Production Environments
- `prod` (backend)
- `prod-frontend` (frontend)
- **Approval required** - add required reviewers
- **Deployment branches** - restrict to `main` branch only

## Workflow Overview

### Backend CI/CD Pipeline (`backend-ci-cd.yml`)

**Triggers:**
- Manual dispatch with environment selection
- Pull requests to `main` (build only)
- Push to `main` (build + deploy to dev)

**Stages:**
1. **Build** - Docker image build and push to ACR
2. **Deploy Dev** - Automatic deployment to dev environment
3. **Deploy QA** - Manual approval required
4. **Deploy Prod** - Manual approval required
5. **Security Scan** - Trivy vulnerability scanning

### Frontend CI/CD Pipeline (`frontend-ci-cd.yml`)

**Triggers:**
- Manual dispatch with environment selection  
- Pull requests to `main` (build only)
- Push to `main` (build + deploy to dev)

**Stages:**
1. **Build** - Next.js build, test, Docker image build and push
2. **Deploy Dev** - Automatic deployment to dev environment
3. **Deploy QA** - Manual approval required
4. **Deploy Prod** - Manual approval required
5. **Security Scan** - npm audit + Trivy scanning

## Company Standards Compliance

The workflows follow the company standards defined in `company-standards.txt`:

### Environment Configuration
| Environment | Registry | Image Suffix | Tag | Namespace Suffix |
|-------------|----------|--------------|-----|------------------|
| **dev** | mydevacr.azurecr.io | -dev | dev | -dev |
| **qa** | myqaacr.azurecr.io | -qa | qa | -qa |
| **prod** | myprodacr.azurecr.io | -prod | prod | -prod |

### Multistage Pipeline
- **Build Stage**: Docker image creation and testing
- **Deployment Stages**: Separate stages for each environment
- **Approval Gates**: QA and Production require manual approval

### Deployment Strategy
- **PR**: Build only, no deployment
- **Main Branch**: Build + automatic deploy to dev
- **Manual**: Deploy to any environment with approval

## Usage Examples

### Deploy to Development (Automatic)
Push to `main` branch or merge a PR - dev deployment happens automatically.

### Deploy to QA
1. Go to `Actions` tab in GitHub
2. Select `Backend CI/CD Pipeline` or `Frontend CI/CD Pipeline`
3. Click `Run workflow`
4. Select `qa` environment
5. Approve the deployment when prompted

### Deploy to Production
1. Go to `Actions` tab in GitHub
2. Select the appropriate pipeline
3. Click `Run workflow`
4. Select `prod` environment
5. Approve the deployment when prompted

## Monitoring and Troubleshooting

### Build Logs
- Build summaries are added to GitHub Actions summary
- Docker image details are displayed
- Deployment verification steps included

### Health Checks
- Kubernetes rollout status verification
- Pod status checks
- Application-specific health endpoints (configure as needed)

### Security
- Trivy vulnerability scanning for all images
- Results uploaded to GitHub Security tab
- npm audit for frontend dependencies

## Customization

### Adding Tests
- Backend: Add test commands in the build job
- Frontend: Tests are run before Docker build

### Adding Health Checks
- Update the verification steps in deployment jobs
- Add application-specific health check commands

### Environment-Specific Configuration
- Modify the Helm values files in `deployment/*/values.*.yaml`
- Update workflow environment variables as needed

## Troubleshooting

### Common Issues

1. **ACR Login Failures**
   - Verify registry credentials in secrets
   - Check ACR permissions for service principal

2. **AKS Access Issues**
   - Verify Azure credentials have AKS access
   - Check resource group and cluster names

3. **Helm Deployment Failures**
   - Check Helm chart syntax
   - Verify namespace permissions
   - Review pod logs for application issues

### Debug Commands

```bash
# Check pod status
kubectl get pods -n <namespace>

# View pod logs
kubectl logs -n <namespace> deployment/<app-name>

# Check Helm release status
helm status <release-name> -n <namespace>

# View Helm values
helm get values <release-name> -n <namespace>
```