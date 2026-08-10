# AWS EKS Production Platform

A portfolio project demonstrating the design, provisioning, deployment,
security, observability, and operation of a containerized application on
Amazon EKS.

## Planned capabilities

- AWS infrastructure provisioned with Terraform
- Custom VPC with public and private subnets
- Amazon EKS managed node group
- Docker image stored in Amazon ECR
- Kubernetes application deployment
- Application Load Balancer ingress
- GitHub Actions CI/CD using AWS OIDC
- CloudWatch logging
- Prometheus and Grafana monitoring
- Horizontal Pod Autoscaling
- Pod disruption controls
- Security and incident-response documentation

## Project status

Current stage: Local application and Docker validation.

## Architecture

Architecture diagram will be added after the initial infrastructure is validated.

## Environments

- Development: in progress
- Production: not yet created

## Security

No AWS credentials, Terraform state files, Kubernetes secrets, or private
configuration files should be committed to this repository.