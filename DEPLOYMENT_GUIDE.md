# 🚀 Vulnerability Chat RAG - AWS Deployment Guide

This guide walks through deploying the Vulnerability Chat RAG application to AWS using the newly created Terraform infrastructure.

## 📋 Prerequisites Checklist

### ✅ **1. AWS Account & Credentials**
Ensure you have AWS credentials configured with the following minimum permissions:

<details>
<summary>Required AWS IAM Permissions</summary>

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:*",
        "ecs:*",
        "ecr:*",
        "elasticloadbalancing:*",
        "iam:*",
        "logs:*",
        "secretsmanager:GetSecretValue",
        "secretsmanager:CreateSecret",
        "secretsmanager:UpdateSecret",
        "secretsmanager:TagResource",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket",
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:DeleteItem"
      ],
      "Resource": "*"
    }
  ]
}
```
</details>

### ✅ **2. Terraform Backend Setup**

**Option A: Use Existing Backend (Recommended)**
If the S3 bucket and DynamoDB table exist:
```bash
aws s3api head-bucket --bucket app-builder-dplmt-tf-state
aws dynamodb describe-table --table-name app-builder-dplmt-tf-lock
```

**Option B: Create New Backend**
```bash
# Create S3 bucket for state
aws s3 mb s3://app-builder-dplmt-tf-state --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket app-builder-dplmt-tf-state \
  --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket app-builder-dplmt-tf-state \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# Create DynamoDB table for locking
aws dynamodb create-table \
  --table-name app-builder-dplmt-tf-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

### ✅ **3. Azure OpenAI Secret Setup**

Create a secret in AWS Secrets Manager containing your Azure OpenAI credentials:

```bash
# Create the secret
aws secretsmanager create-secret \
  --name "vuln-chat-rag/dev/azure-openai" \
  --description "Azure OpenAI credentials for vulnerability chat RAG dev environment" \
  --secret-string '{
    "api_key": "your-azure-openai-api-key",
    "endpoint": "https://your-resource.openai.azure.com/",
    "embeddings_deployment": "text-embedding-ada-002",
    "completions_deployment": "gpt-4o"
  }' \
  --tags '[
    {"Key": "Project", "Value": "vuln-chat-rag"},
    {"Key": "Environment", "Value": "dev"}
  ]' \
  --region us-east-1

# Get the secret ARN (you'll need this)
aws secretsmanager describe-secret --secret-id "vuln-chat-rag/dev/azure-openai" --query 'ARN' --output text
```

### ✅ **4. Update Configuration**

Update the secret ARN in your environment configuration:

```bash
# Edit terraform/environments/dev/dev.tfvars
# Replace the placeholder ARN with your actual secret ARN
azure_openai_secret_arn = "arn:aws:secretsmanager:us-east-1:YOUR-ACCOUNT:secret:vuln-chat-rag/dev/azure-openai-XXXXXX"
```

## 🚀 Deployment Methods

### **Method 1: Atlantis Workflow (Recommended)**

This method uses the configured Atlantis automation:

1. **Verify Prerequisites**: Ensure all the above prerequisites are met
2. **Commit Changes**: All Terraform code is already committed to this PR
3. **Atlantis Auto-Plan**: Atlantis will automatically run `terraform plan` on this PR
4. **Review Plan**: Check the plan output in PR comments
5. **Merge PR**: Merging will trigger `atlantis apply` to deploy infrastructure

### **Method 2: Manual Terraform (Alternative)**

If you prefer to run Terraform manually:

```bash
# Navigate to terraform directory
cd terraform

# Initialize Terraform (dev environment)
terraform init -backend-config=environments/dev/backend.tfvars

# Plan the deployment
terraform plan -var-file=environments/dev/dev.tfvars

# Apply the infrastructure (after review)
terraform apply -var-file=environments/dev/dev.tfvars

# View outputs
terraform output
```

## 📊 Infrastructure Overview

After deployment, you'll have:

### **Networking**
- VPC with CIDR 10.0.0.0/16
- 2 public subnets (10.0.1.0/24, 10.0.2.0/24) in us-east-1a, us-east-1b
- 2 private subnets (10.0.10.0/24, 10.0.20.0/24) in us-east-1a, us-east-1b
- Internet Gateway and NAT Gateways for internet access

### **Container Infrastructure**
- ECS Fargate cluster: `vuln-chat-rag-dev`
- ECR repositories:
  - `vuln-chat-rag-dev-backend` (for FastAPI backend)
  - `vuln-chat-rag-dev-frontend` (for Next.js frontend)

### **Load Balancing**
- Application Load Balancer with DNS name (output: `alb_dns_name`)
- Routing rules:
  - `/api/*` → Backend service
  - `/docs*`, `/openapi.json`, `/redoc*` → Backend service  
  - `/*` → Frontend service (default)

### **Security**
- ECS tasks run in private subnets (no direct internet access)
- IAM roles with least-privilege permissions
- Secrets Manager integration for Azure OpenAI credentials
- Security groups restricting traffic to necessary ports only

## 🏗️ Container Deployment

After infrastructure is deployed, you'll need to build and push container images:

### **Backend Container**
```bash
# Get ECR login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $(terraform output -raw backend_ecr_repository_url | cut -d/ -f1)

# Build and tag backend image
cd backend
docker build -t vuln-chat-rag-backend .
docker tag vuln-chat-rag-backend:latest $(terraform output -raw backend_ecr_repository_url):latest

# Push to ECR
docker push $(terraform output -raw backend_ecr_repository_url):latest
```

### **Frontend Container**
```bash
# Build and tag frontend image
cd ../frontend
docker build -t vuln-chat-rag-frontend .
docker tag vuln-chat-rag-frontend:latest $(terraform output -raw frontend_ecr_repository_url):latest

# Push to ECR
docker push $(terraform output -raw frontend_ecr_repository_url):latest
```

### **Update ECS Services**
```bash
# Force new deployment with updated images
aws ecs update-service \
  --cluster $(terraform output -raw ecs_cluster_name) \
  --service $(terraform output -raw ecs_backend_service_name) \
  --force-new-deployment

aws ecs update-service \
  --cluster $(terraform output -raw ecs_cluster_name) \
  --service $(terraform output -raw ecs_frontend_service_name) \
  --force-new-deployment
```

## 🔍 Verification & Testing

### **1. Check Deployment Status**
```bash
# Check ECS services
aws ecs describe-services \
  --cluster $(terraform output -raw ecs_cluster_name) \
  --services $(terraform output -raw ecs_backend_service_name) $(terraform output -raw ecs_frontend_service_name)

# Check ALB target health
aws elbv2 describe-target-health --target-group-arn <backend-target-group-arn>
aws elbv2 describe-target-health --target-group-arn <frontend-target-group-arn>
```

### **2. Access Application**
```bash
# Get ALB DNS name
echo "Application URL: http://$(terraform output -raw alb_dns_name)"

# Test backend API
curl http://$(terraform output -raw alb_dns_name)/api/health

# Test frontend (in browser)
open http://$(terraform output -raw alb_dns_name)
```

### **3. Monitor Logs**
```bash
# View backend logs
aws logs tail /ecs/vuln-chat-rag-dev --follow --filter-pattern="backend"

# View frontend logs  
aws logs tail /ecs/vuln-chat-rag-dev --follow --filter-pattern="frontend"
```

## 💰 Cost Management

### **Development Environment (~$30-50/month)**
- ECS Fargate: ~$15/month (1 backend + 1 frontend task)
- NAT Gateway: ~$32/month (data processing + hourly charge)
- ALB: ~$16/month + LCU charges
- ECR: ~$1/month (first 500MB free)
- CloudWatch: ~$1/month (basic logging)

### **Cost Optimization Tips**
1. **Shutdown Dev Environment**: Stop ECS services when not in use
2. **Right-Size Resources**: Adjust CPU/memory based on actual usage
3. **Use Spot for Non-Production**: Consider Fargate Spot pricing
4. **Monitor Usage**: Set up CloudWatch billing alarms

## 🛠️ Troubleshooting

### **Common Issues**

<details>
<summary><b>ECS Task Startup Failures</b></summary>

**Symptoms**: ECS tasks fail to start or immediately stop
**Solutions**:
1. Check CloudWatch logs: `/ecs/vuln-chat-rag-dev`
2. Verify secret ARN is correct in task definition
3. Ensure ECR images exist and are accessible
4. Check IAM permissions for task execution role
</details>

<details>
<summary><b>ALB Health Check Failures</b></summary>

**Symptoms**: ALB shows unhealthy targets
**Solutions**:
1. Verify application is listening on correct port (8000 for backend, 3000 for frontend)
2. Check health check paths (`/api/health` and `/`)
3. Review security group rules
4. Check container logs for startup errors
</details>

<details>
<summary><b>Secret Access Denied</b></summary>

**Symptoms**: ECS tasks can't access Azure OpenAI secret
**Solutions**:
1. Verify secret exists and has correct tags
2. Check IAM task role has `secretsmanager:GetSecretValue` permission
3. Ensure secret ARN format is correct in environment variables
</details>

### **Cleanup**

To destroy all infrastructure:
```bash
# Using Terraform
cd terraform
terraform destroy -var-file=environments/dev/dev.tfvars

# Or comment "atlantis destroy" on the PR (if supported)
```

## 🔗 Next Steps

1. **Custom Domain**: Set up Route 53 and custom domain
2. **HTTPS**: Add SSL certificate to ALB
3. **Monitoring**: Configure CloudWatch dashboards and alarms  
4. **Auto Scaling**: Add ECS service auto-scaling policies
5. **CI/CD**: Set up automated container builds and deployments
6. **Backup**: Configure database backup strategies

## 📞 Support

- **Terraform Documentation**: [terraform/README.md](terraform/README.md)
- **Application Architecture**: [README.md](README.md)
- **Issues**: Check CloudWatch logs and ECS service events