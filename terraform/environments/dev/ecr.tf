resource "aws_ecr_repository" "backend" {
  name                 = "aws-eks-backend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name        = "aws-eks-backend"
    Environment = "dev"
    Project     = "aws-eks-platform"
  }
}
