# Main Terraform configuration for Penetration Testing Toolset
# Infrastructure as Code with Security as Code principles

terraform {
  required_version = ">= 1.6.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.0"
    }
  }
  
  backend "s3" {
    bucket = "penetration-tools-terraform-state"
    key    = "infrastructure/terraform.tfstate"
    region = "us-west-2"
    
    # Enable state locking and encryption
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}

# Provider configuration
provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "penetration-tools"
      Environment = var.environment
      ManagedBy   = "terraform"
      Owner       = "security-team"
    }
  }
}

# VPC and Networking
module "vpc" {
  source = "./modules/vpc"
  
  environment = var.environment
  vpc_cidr    = var.vpc_cidr
  
  # Security: Private subnets for application
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets
  
  # Enable VPC Flow Logs for security monitoring
  enable_flow_logs = true
  flow_log_retention_days = 30
}

# EKS Cluster
module "eks" {
  source = "./modules/eks"
  
  environment = var.environment
  cluster_name = "penetration-tools-${var.environment}"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
  
  # Security: Node groups with security hardening
  node_groups = {
    app = {
      desired_capacity = var.app_node_desired_capacity
      max_capacity     = var.app_node_max_capacity
      min_capacity     = var.app_node_min_capacity
      
      instance_types = ["t3.medium", "t3.large"]
      
      # Security: Use latest Amazon Linux 2 EKS optimized AMI
      ami_type = "AL2_x86_64"
      
      # Security: Enable encryption at rest
      disk_size = 50
      disk_type = "gp3"
      
      # Security: IAM roles with least privilege
      iam_role_additional_policies = [
        "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
        "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
        "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
      ]
    }
  }
  
  # Security: Enable cluster logging
  cluster_enabled_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
  
  # Security: Enable encryption at rest
  cluster_encryption_config = {
    provider_key_arn = module.kms.kms_key_arn
    resources        = ["secrets"]
  }
}

# KMS for encryption
module "kms" {
  source = "./modules/kms"
  
  environment = var.environment
  key_description = "KMS key for Penetration Tools ${var.environment} environment"
  
  # Security: Enable key rotation
  enable_key_rotation = true
  
  # Security: Define key administrators and users
  key_administrators = var.kms_administrators
  key_users          = var.kms_users
}

# RDS Database
module "rds" {
  source = "./modules/rds"
  
  environment = var.environment
  cluster_name = "penetration-tools-${var.environment}"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
  
  # Security: Use encryption
  storage_encrypted = true
  kms_key_id       = module.kms.kms_key_arn
  
  # Security: Use private subnets only
  publicly_accessible = false
  
  # Security: Enable deletion protection in production
  deletion_protection = var.environment == "production"
  
  # Security: Enable automated backups
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  # Security: Enable performance insights
  performance_insights_enabled = true
  performance_insights_retention_period = 7
}

# ElastiCache Redis
module "redis" {
  source = "./modules/redis"
  
  environment = var.environment
  cluster_name = "penetration-tools-${var.environment}"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
  
  # Security: Use encryption at rest and in transit
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  
  # Security: Use private subnets only
  security_group_ids = [module.vpc.default_security_group_id]
}

# Application Load Balancer
module "alb" {
  source = "./modules/alb"
  
  environment = var.environment
  name = "penetration-tools-${var.environment}"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.public_subnet_ids
  
  # Security: Use HTTPS only
  enable_https = true
  certificate_arn = module.acm.certificate_arn
  
  # Security: Enable WAF
  enable_waf = true
  waf_rules = [
    {
      name = "RateLimit"
      priority = 1
      action = "block"
      rate_limit = 2000
    },
    {
      name = "SQLInjection"
      priority = 2
      action = "block"
    },
    {
      name = "XSS"
      priority = 3
      action = "block"
    }
  ]
}

# ACM Certificate
module "acm" {
  source = "./modules/acm"
  
  domain_name = var.domain_name
  environment = var.environment
}

# CloudWatch Logs
module "cloudwatch" {
  source = "./modules/cloudwatch"
  
  environment = var.environment
  
  # Security: Define log retention policies
  log_groups = {
    application = {
      name = "/aws/eks/penetration-tools-${var.environment}/application"
      retention_in_days = 30
    }
    security = {
      name = "/aws/eks/penetration-tools-${var.environment}/security"
      retention_in_days = 90
    }
    audit = {
      name = "/aws/eks/penetration-tools-${var.environment}/audit"
      retention_in_days = 365
    }
  }
}

# Security Hub
module "security_hub" {
  source = "./modules/security_hub"
  
  environment = var.environment
  
  # Security: Enable all security standards
  enable_cis_aws_foundations_benchmark = true
  enable_pci_dss = var.environment == "production"
  enable_aws_foundational_security_best_practices = true
}

# GuardDuty
module "guardduty" {
  source = "./modules/guardduty"
  
  environment = var.environment
  
  # Security: Enable all GuardDuty features
  enable_finding_publishing = true
  enable_s3_protection = true
  enable_kubernetes_protection = true
  enable_malware_protection = true
}

# Outputs
output "cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
}

output "cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

output "database_endpoint" {
  description = "RDS cluster endpoint"
  value       = module.rds.cluster_endpoint
  sensitive   = true
}

output "redis_endpoint" {
  description = "ElastiCache Redis endpoint"
  value       = module.redis.endpoint
  sensitive   = true
}

output "alb_dns_name" {
  description = "Application Load Balancer DNS name"
  value       = module.alb.dns_name
}

output "kms_key_arn" {
  description = "KMS key ARN"
  value       = module.kms.kms_key_arn
  sensitive   = true
} 