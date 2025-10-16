terraform {
  required_version = "~> 1.6.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {}
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

# VPC Module
module "vpc" {
  source = "./modules/vpc"

  project_name = var.project_name
  environment  = var.environment
  aws_region   = var.aws_region
  
  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
}

# IAM Module
module "iam" {
  source = "./modules/iam"

  project_name = var.project_name
  environment  = var.environment
}

# ECR Module
module "ecr" {
  source = "./modules/ecr"

  project_name = var.project_name
  environment  = var.environment
}

# ALB Module
module "alb" {
  source = "./modules/alb"

  project_name = var.project_name
  environment  = var.environment
  
  vpc_id                = module.vpc.vpc_id
  public_subnet_ids     = module.vpc.public_subnet_ids
  allowed_cidr_blocks   = var.allowed_cidr_blocks
  backend_port          = var.backend_port
  frontend_port         = var.frontend_port
  backend_health_path   = var.backend_health_path
  frontend_health_path  = var.frontend_health_path
}

# ECS Module
module "ecs" {
  source = "./modules/ecs"

  project_name = var.project_name
  environment  = var.environment
  
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  
  ecs_task_execution_role_arn = module.iam.ecs_task_execution_role_arn
  ecs_task_role_arn          = module.iam.ecs_task_role_arn
  
  backend_ecr_repository_url  = module.ecr.backend_repository_url
  frontend_ecr_repository_url = module.ecr.frontend_repository_url
  
  backend_target_group_arn  = module.alb.backend_target_group_arn
  frontend_target_group_arn = module.alb.frontend_target_group_arn
  
  backend_port          = var.backend_port
  frontend_port         = var.frontend_port
  backend_health_path   = var.backend_health_path
  frontend_health_path  = var.frontend_health_path
  
  backend_cpu_units     = var.backend_cpu_units
  backend_memory_mb     = var.backend_memory_mb
  frontend_cpu_units    = var.frontend_cpu_units
  frontend_memory_mb    = var.frontend_memory_mb
  
  backend_desired_count  = var.backend_desired_count
  frontend_desired_count = var.frontend_desired_count
  
  azure_openai_secret_arn = var.azure_openai_secret_arn
  alb_dns_name           = module.alb.alb_dns_name
}