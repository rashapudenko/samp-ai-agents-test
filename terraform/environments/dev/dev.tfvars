# Environment Configuration
environment = "dev"
aws_region  = "us-east-1"

# VPC Configuration
vpc_cidr             = "10.0.0.0/16"
availability_zones   = ["us-east-1a", "us-east-1b"]
public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
private_subnet_cidrs = ["10.0.10.0/24", "10.0.20.0/24"]

# Security Configuration
allowed_cidr_blocks = ["0.0.0.0/0"]

# Application Configuration  
backend_port         = 8000
frontend_port        = 3000
backend_health_path  = "/api/health"
frontend_health_path = "/"

# ECS Task Configuration (Development - lower resources)
backend_cpu_units    = 512
backend_memory_mb    = 1024
frontend_cpu_units   = 256
frontend_memory_mb   = 512

# ECS Service Configuration
backend_desired_count  = 1
frontend_desired_count = 1

# Secrets Configuration (Replace with actual ARN)
# TODO: Update with the actual ARN of your Azure OpenAI secret in AWS Secrets Manager
azure_openai_secret_arn = "arn:aws:secretsmanager:us-east-1:123456789012:secret:vuln-chat-rag/dev/azure-openai-XXXXXX"