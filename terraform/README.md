# Vulnerability Chat RAG - AWS Infrastructure

This directory contains Terraform infrastructure-as-code for deploying the Vulnerability Chat RAG application to AWS using ECS Fargate.

## Architecture

The infrastructure creates the following AWS resources:

- **VPC**: Isolated network with public and private subnets across multiple AZs
- **ECR**: Repositories for backend and frontend container images  
- **ECS Fargate**: Containerized services for backend (FastAPI) and frontend (Next.js)
- **Application Load Balancer**: Routes traffic to services with health checks
- **IAM**: Roles and policies with least-privilege access
- **CloudWatch**: Centralized logging for all services

## Prerequisites

1. **AWS CLI configured** with appropriate credentials
2. **Terraform 1.6.0** installed (use `tfswitch` for version management)
3. **AWS Secrets Manager secret** containing Azure OpenAI credentials:
   ```json
   {
     "api_key": "your-azure-openai-api-key",
     "endpoint": "https://your-resource.openai.azure.com/",
     "embeddings_deployment": "text-embedding-ada-002", 
     "completions_deployment": "gpt-4o"
   }
   ```
4. **S3 backend** for Terraform state (configured via Atlantis)
5. **DynamoDB table** for state locking

## Deployment via Atlantis

This project uses [Atlantis](https://www.runatlantis.io/) for automated Terraform workflows.

### Supported Environments

- **dev**: Development environment with minimal resources
- **staging**: Pre-production environment for testing
- **prod**: Production environment with high availability

### Workflow

1. **Create/Update Azure OpenAI Secret**: Ensure the secret exists in AWS Secrets Manager
2. **Update Variables**: Modify `terraform/environments/{env}/{env}.tfvars` with correct values
3. **Create Pull Request**: Changes trigger automatic Atlantis plan
4. **Review Plan**: Atlantis posts plan output in PR comments
5. **Merge PR**: Triggers Atlantis apply to deploy infrastructure

### Manual Commands

If needed, you can run Atlantis commands manually:

```bash
# Plan for dev environment
atlantis plan -d terraform -p dev

# Apply for dev environment (after PR merge)
atlantis apply -d terraform -p dev
```

## Environment Configuration

### Development (dev)
- **Resources**: 1 backend task (512 CPU, 1GB RAM), 1 frontend task (256 CPU, 512MB RAM)
- **VPC**: 10.0.0.0/16 with 2 AZs
- **Cost**: ~$30-50/month

### Staging (staging)  
- **Resources**: 2 backend tasks (1 vCPU, 2GB RAM each), 2 frontend tasks (512 CPU, 1GB RAM each)
- **VPC**: 10.1.0.0/16 with 2 AZs  
- **Cost**: ~$80-120/month

### Production (prod)
- **Resources**: 3 backend tasks (2 vCPU, 4GB RAM each), 3 frontend tasks (1 vCPU, 2GB RAM each)
- **VPC**: 10.2.0.0/16 with 3 AZs
- **Cost**: ~$250-350/month

## Security Considerations

1. **Network Security**: 
   - ECS tasks run in private subnets with no direct internet access
   - ALB security group restricts access to HTTP (port 80) only
   - Consider restricting `allowed_cidr_blocks` in production

2. **Secret Management**:
   - Azure OpenAI credentials stored in AWS Secrets Manager
   - ECS tasks use IAM roles to access secrets (no hardcoded credentials)
   - Secrets are injected as environment variables at runtime

3. **Container Security**:
   - ECR repositories have vulnerability scanning enabled
   - Images are scanned on push for known vulnerabilities
   - Lifecycle policies clean up old/untagged images

4. **Access Control**:
   - IAM roles follow least-privilege principle
   - ECS execution and task roles have minimal required permissions
   - CloudTrail and CloudWatch monitor all API activity

## Cost Optimization

1. **Right-sizing**: Resource allocations optimized per environment
2. **Auto-scaling**: Can be added for production workloads  
3. **Spot instances**: Consider for non-production environments
4. **Image lifecycle**: ECR policies clean up unused images
5. **Monitoring**: CloudWatch Container Insights tracks resource utilization

## Troubleshooting

### Common Issues

1. **Task startup failures**: Check CloudWatch logs at `/ecs/vuln-chat-rag-{env}`
2. **ALB health checks failing**: Verify application health endpoints
3. **Secret access denied**: Check IAM permissions and secret ARN
4. **ECR access denied**: Ensure ECS has permissions to pull images

### Debugging Commands

```bash
# View ECS service status
aws ecs describe-services --cluster vuln-chat-rag-dev --services vuln-chat-rag-dev-backend

# Check task definitions  
aws ecs describe-task-definition --task-definition vuln-chat-rag-dev-backend

# View CloudWatch logs
aws logs tail /ecs/vuln-chat-rag-dev --follow

# Check ALB target health
aws elbv2 describe-target-health --target-group-arn <target-group-arn>
```

## Outputs

After successful deployment, Terraform outputs key information:

- `alb_dns_name`: Public URL to access the application
- `backend_ecr_repository_url`: ECR URL for pushing backend images
- `frontend_ecr_repository_url`: ECR URL for pushing frontend images
- `ecs_cluster_name`: ECS cluster name for deployments

## Next Steps

1. **Container Images**: Build and push Docker images to ECR repositories
2. **DNS**: Configure Route 53 or custom domain for ALB
3. **HTTPS**: Add SSL/TLS certificate to ALB listener
4. **Monitoring**: Set up CloudWatch dashboards and alarms
5. **Backup**: Configure database backup strategies for persistent data