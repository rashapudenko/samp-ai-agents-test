variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs"
  type        = list(string)
}

variable "ecs_task_execution_role_arn" {
  description = "ARN of the ECS task execution role"
  type        = string
}

variable "ecs_task_role_arn" {
  description = "ARN of the ECS task role"
  type        = string
}

variable "backend_ecr_repository_url" {
  description = "URL of the backend ECR repository"
  type        = string
}

variable "frontend_ecr_repository_url" {
  description = "URL of the frontend ECR repository"
  type        = string
}

variable "backend_target_group_arn" {
  description = "ARN of the backend target group"
  type        = string
}

variable "frontend_target_group_arn" {
  description = "ARN of the frontend target group"
  type        = string
}

variable "backend_port" {
  description = "Port for backend application"
  type        = number
}

variable "frontend_port" {
  description = "Port for frontend application"
  type        = number
}

variable "backend_health_path" {
  description = "Health check path for backend"
  type        = string
}

variable "frontend_health_path" {
  description = "Health check path for frontend"
  type        = string
}

variable "backend_cpu_units" {
  description = "CPU units for backend tasks"
  type        = number
}

variable "backend_memory_mb" {
  description = "Memory MB for backend tasks"
  type        = number
}

variable "frontend_cpu_units" {
  description = "CPU units for frontend tasks"
  type        = number
}

variable "frontend_memory_mb" {
  description = "Memory MB for frontend tasks"
  type        = number
}

variable "backend_desired_count" {
  description = "Desired number of backend tasks"
  type        = number
}

variable "frontend_desired_count" {
  description = "Desired number of frontend tasks"
  type        = number
}

variable "azure_openai_secret_arn" {
  description = "ARN of AWS Secrets Manager secret containing Azure OpenAI credentials"
  type        = string
}

variable "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  type        = string
}