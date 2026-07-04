terraform {
  required_version = ">= 1.9.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Wire modules per environment — never monolithic root module
# module "networking" { source = "../../modules/networking" }
# module "database"   { source = "../../modules/database" }
