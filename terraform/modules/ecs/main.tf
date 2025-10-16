# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-cluster"
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/${var.project_name}-${var.environment}"
  retention_in_days = 30

  tags = {
    Name = "${var.project_name}-${var.environment}-ecs-logs"
  }
}

# ECS Security Group
resource "aws_security_group" "ecs_tasks" {
  name_prefix = "${var.project_name}-${var.environment}-ecs-"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = var.backend_port
    to_port     = var.backend_port
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"] # VPC CIDR
  }

  ingress {
    from_port   = var.frontend_port
    to_port     = var.frontend_port
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"] # VPC CIDR
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-ecs-sg"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Backend Task Definition
resource "aws_ecs_task_definition" "backend" {
  family                   = "${var.project_name}-${var.environment}-backend"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.backend_cpu_units
  memory                   = var.backend_memory_mb
  execution_role_arn       = var.ecs_task_execution_role_arn
  task_role_arn           = var.ecs_task_role_arn

  container_definitions = jsonencode([
    {
      name  = "backend"
      image = "${var.backend_ecr_repository_url}:latest"
      
      essential = true
      
      portMappings = [
        {
          containerPort = var.backend_port
          protocol      = "tcp"
        }
      ]
      
      environment = [
        {
          name  = "API_HOST"
          value = "0.0.0.0"
        },
        {
          name  = "API_PORT"
          value = tostring(var.backend_port)
        },
        {
          name  = "API_PREFIX"
          value = "/api"
        },
        {
          name  = "DATABASE_PATH"
          value = "app/data/vulnerabilities.db"
        },
        {
          name  = "VECTOR_DB_PATH"
          value = "app/data/vector_db"
        },
        {
          name  = "SNYK_BASE_URL"
          value = "https://security.snyk.io/vuln/pip/"
        },
        {
          name  = "SCRAPER_PAGES_TO_FETCH"
          value = "10"
        },
        {
          name  = "WORKERS"
          value = "1"
        },
        {
          name  = "ALLOWED_ORIGINS"
          value = "http://${var.alb_dns_name},https://${var.alb_dns_name}"
        }
      ]
      
      secrets = [
        {
          name      = "AZURE_OPENAI_API_KEY"
          valueFrom = "${var.azure_openai_secret_arn}:api_key::"
        },
        {
          name      = "AZURE_OPENAI_ENDPOINT"
          valueFrom = "${var.azure_openai_secret_arn}:endpoint::"
        },
        {
          name      = "AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT"
          valueFrom = "${var.azure_openai_secret_arn}:embeddings_deployment::"
        },
        {
          name      = "AZURE_OPENAI_COMPLETIONS_DEPLOYMENT"
          valueFrom = "${var.azure_openai_secret_arn}:completions_deployment::"
        }
      ]
      
      healthCheck = {
        command = [
          "CMD-SHELL",
          "curl -f http://localhost:${var.backend_port}${var.backend_health_path} || exit 1"
        ]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
      
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs.name
          "awslogs-region"        = data.aws_region.current.name
          "awslogs-stream-prefix" = "backend"
        }
      }
    }
  ])

  tags = {
    Name      = "${var.project_name}-${var.environment}-backend-task"
    Component = "backend"
  }
}

# Frontend Task Definition
resource "aws_ecs_task_definition" "frontend" {
  family                   = "${var.project_name}-${var.environment}-frontend"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.frontend_cpu_units
  memory                   = var.frontend_memory_mb
  execution_role_arn       = var.ecs_task_execution_role_arn
  task_role_arn           = var.ecs_task_role_arn

  container_definitions = jsonencode([
    {
      name  = "frontend"
      image = "${var.frontend_ecr_repository_url}:latest"
      
      essential = true
      
      portMappings = [
        {
          containerPort = var.frontend_port
          protocol      = "tcp"
        }
      ]
      
      environment = [
        {
          name  = "NODE_ENV"
          value = "production"
        },
        {
          name  = "PORT"
          value = tostring(var.frontend_port)
        },
        {
          name  = "NEXT_TELEMETRY_DISABLED"
          value = "1"
        },
        {
          name  = "API_URL"
          value = "http://backend:${var.backend_port}"
        },
        {
          name  = "NEXT_PUBLIC_API_URL"
          value = "http://${var.alb_dns_name}"
        }
      ]
      
      healthCheck = {
        command = [
          "CMD-SHELL",
          "curl -f http://localhost:${var.frontend_port}${var.frontend_health_path} || exit 1"
        ]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 30
      }
      
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs.name
          "awslogs-region"        = data.aws_region.current.name
          "awslogs-stream-prefix" = "frontend"
        }
      }
    }
  ])

  tags = {
    Name      = "${var.project_name}-${var.environment}-frontend-task"
    Component = "frontend"
  }
}

# Backend ECS Service
resource "aws_ecs_service" "backend" {
  name            = "${var.project_name}-${var.environment}-backend"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.backend.arn
  desired_count   = var.backend_desired_count
  launch_type     = "FARGATE"

  network_configuration {
    security_groups  = [aws_security_group.ecs_tasks.id]
    subnets          = var.private_subnet_ids
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = var.backend_target_group_arn
    container_name   = "backend"
    container_port   = var.backend_port
  }

  depends_on = [
    var.backend_target_group_arn
  ]

  tags = {
    Name      = "${var.project_name}-${var.environment}-backend-service"
    Component = "backend"
  }
}

# Frontend ECS Service
resource "aws_ecs_service" "frontend" {
  name            = "${var.project_name}-${var.environment}-frontend"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.frontend.arn
  desired_count   = var.frontend_desired_count
  launch_type     = "FARGATE"

  network_configuration {
    security_groups  = [aws_security_group.ecs_tasks.id]
    subnets          = var.private_subnet_ids
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = var.frontend_target_group_arn
    container_name   = "frontend"
    container_port   = var.frontend_port
  }

  depends_on = [
    var.frontend_target_group_arn
  ]

  tags = {
    Name      = "${var.project_name}-${var.environment}-frontend-service"
    Component = "frontend"
  }
}

# Data source for current AWS region
data "aws_region" "current" {}