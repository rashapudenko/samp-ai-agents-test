# Environment Configuration
environment = "staging"
aws_region  = "us-east-1"

# VPC Configuration
vpc_cidr             = "10.1.0.0/16"
availability_zones   = ["us-east-1a", "us-east-1b"]
public_subnet_cidrs  = ["10.1.1.0/24", "10.1.2.0/24"]
private_subnet_cidrs = ["10.1.10.0/24", "10.1.20.0/24"]

# Security Configuration
allowed_cidr_blocks = ["0.0.0.0/0"]

# Application Configuration  
backend_port         = 8000
frontend_port        = 3000
backend_health_path  = "/api/health"
frontend_health_path = "/"

# ECS Task Configuration (Staging - moderate resources)
backend_cpu_units    = 1024
backend_memory_mb    = 2048
frontend_cpu_units   = 512
frontend_memory_mb   = 1024

# ECS Service Configuration
backend_desired_count  = 2
frontend_desired_count = 2

# Secrets Configuration (Replace with actual ARN)
azure_openai_secret_arn = "arn:aws:secretsmanager:us-east-1:123456789012:secret:vuln-chat-rag/staging/azure-openai-XXXXXX"