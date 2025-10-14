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

variable "public_subnet_ids" {
  description = "List of public subnet IDs"
  type        = list(string)
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access ALB"
  type        = list(string)
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