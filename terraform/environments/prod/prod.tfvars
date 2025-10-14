# Environment Configuration
environment = "prod"
aws_region  = "us-east-1"

# VPC Configuration
vpc_cidr             = "10.2.0.0/16"
availability_zones   = ["us-east-1a", "us-east-1b", "us-east-1c"]
public_subnet_cidrs  = ["10.2.1.0/24", "10.2.2.0/24", "10.2.3.0/24"]
private_subnet_cidrs = ["10.2.10.0/24", "10.2.20.0/24", "10.2.30.0/24"]

# Security Configuration (Consider restricting in production)
allowed_cidr_blocks = ["0.0.0.0/0"]

# Application Configuration  
backend_port         = 8000
frontend_port        = 3000
backend_health_path  = "/api/health"
frontend_health_path = "/"

# ECS Task Configuration (Production - higher resources)
backend_cpu_units    = 2048
backend_memory_mb    = 4096
frontend_cpu_units   = 1024
frontend_memory_mb   = 2048

# ECS Service Configuration (Production - higher availability)
backend_desired_count  = 3
frontend_desired_count = 3

# Secrets Configuration (Replace with actual ARN)
azure_openai_secret_arn = "arn:aws:secretsmanager:us-east-1:123456789012:secret:vuln-chat-rag/prod/azure-openai-XXXXXX"