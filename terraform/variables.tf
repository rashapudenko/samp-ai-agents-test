variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "vuln-chat-rag"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

# VPC Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.20.0/24"]
}

# Security Configuration
variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access ALB"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

# Application Configuration
variable "backend_port" {
  description = "Port for backend application"
  type        = number
  default     = 8000
}

variable "frontend_port" {
  description = "Port for frontend application"
  type        = number
  default     = 3000
}

variable "backend_health_path" {
  description = "Health check path for backend"
  type        = string
  default     = "/api/health"
}

variable "frontend_health_path" {
  description = "Health check path for frontend"
  type        = string
  default     = "/"
}

# ECS Task Configuration
variable "backend_cpu_units" {
  description = "CPU units for backend tasks"
  type        = number
  default     = 512
}

variable "backend_memory_mb" {
  description = "Memory MB for backend tasks"
  type        = number
  default     = 1024
}

variable "frontend_cpu_units" {
  description = "CPU units for frontend tasks"
  type        = number
  default     = 256
}

variable "frontend_memory_mb" {
  description = "Memory MB for frontend tasks"
  type        = number
  default     = 512
}

variable "backend_desired_count" {
  description = "Desired number of backend tasks"
  type        = number
  default     = 1
}

variable "frontend_desired_count" {
  description = "Desired number of frontend tasks"
  type        = number
  default     = 1
}

# Secrets Configuration
variable "azure_openai_secret_arn" {
  description = "ARN of AWS Secrets Manager secret containing Azure OpenAI credentials"
  type        = string
}