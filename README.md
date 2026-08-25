# AWS EKS Production Platform

## Project Overview

This project demonstrates the design, provisioning, deployment, security, monitoring, and CI/CD automation of a containerized Python application running on Amazon EKS.

The platform was built as a hands-on DevOps portfolio project using AWS, Terraform, Docker, Kubernetes, GitHub Actions, Amazon ECR, Prometheus, and Grafana.

The environment is designed as a development/portfolio platform that demonstrates production-oriented DevOps practices such as Infrastructure as Code, multi-node Kubernetes deployment, secure AWS authentication with OIDC, observability, health checks, autoscaling, and automated application delivery.

---

<img width="1448" height="1086" alt="aws-eks-platform-architecture png" src="https://github.com/user-attachments/assets/d4076eff-9783-45a7-89f9-53c047eae5cd" />


## Architecture

The platform includes:

* Custom AWS VPC
* Public and private subnets across multiple Availability Zones
* Internet Gateway
* NAT Gateway
* Amazon EKS cluster
* EKS managed node group
* Two EC2 worker nodes distributed across Availability Zones
* Amazon ECR container registry
* Kubernetes Deployment with two backend replicas
* Kubernetes LoadBalancer Service
* Horizontal Pod Autoscaler
* Prometheus monitoring
* Grafana dashboards
* GitHub Actions CI/CD
* GitHub OIDC authentication to AWS
* Terraform remote state stored in Amazon S3

### Deployment Flow

```text
Developer
   |
   v
GitHub Repository
   |
   v
GitHub Actions
   |
   |-- CI
   |     |-- Python validation
   |     |-- Dependency installation
   |     |-- Docker build validation
   |
   |-- CD
         |
         v
   GitHub OIDC
         |
         v
       AWS IAM
         |
         v
     Amazon ECR
         |
         v
     Amazon EKS
         |
         v
 Kubernetes Deployment
         |
         v
  AWS Load Balancer
```

---

## Technology Stack

### Cloud

* Amazon Web Services
* Amazon EKS
* Amazon EC2
* Amazon ECR
* Amazon VPC
* IAM
* Elastic Load Balancing
* Amazon S3

### Infrastructure as Code

* Terraform

### Containers and Orchestration

* Docker
* Kubernetes
* Amazon EKS

### Application

* Python
* Flask
* Gunicorn

### CI/CD

* GitHub
* GitHub Actions
* AWS OIDC
* Amazon ECR

### Monitoring

* Prometheus
* Grafana
* kube-state-metrics
* Prometheus Node Exporter
* Metrics Server
* Alertmanager

---

## Infrastructure as Code

AWS infrastructure is provisioned with Terraform.

Terraform manages:

* VPC
* Public and private subnets
* Internet Gateway
* NAT Gateway
* Route tables
* IAM roles
* EKS cluster
* EKS managed node group
* Amazon ECR repository
* GitHub OIDC provider
* GitHub Actions IAM role
* EKS access entry and access policy

The Terraform state is stored remotely in an encrypted Amazon S3 backend.

Sensitive state files and local Terraform directories are excluded from Git through `.gitignore`.

---

## Amazon EKS Cluster

The development EKS cluster uses a managed node group with the following scaling configuration:

```text
Desired nodes: 2
Minimum nodes: 1
Maximum nodes: 3
```

The worker nodes use `t3.medium` EC2 instances.

The cluster currently operates with two worker nodes distributed across two Availability Zones.

Example:

```text
ip-10-0-11-124.ec2.internal   Ready
ip-10-0-12-6.ec2.internal     Ready
```

---

## Kubernetes Deployment

The backend application runs as a Kubernetes Deployment with two replicas.

The replicas are distributed across both EKS worker nodes.

Example:

```text
aws-eks-backend-xxxxx   Running   ip-10-0-11-124.ec2.internal
aws-eks-backend-yyyyy   Running   ip-10-0-12-6.ec2.internal
```

This demonstrates workload scheduling across multiple Kubernetes workers.

The application is exposed through a Kubernetes `LoadBalancer` Service backed by an AWS Elastic Load Balancer.

---

## Application Health Endpoints

The Flask backend provides operational endpoints including:

```text
/
```

Application root endpoint.

```text
/health
```

Returns application health status.

```text
/ready
```

Readiness validation endpoint.

```text
/info
```

Returns application metadata and pod hostname.

```text
/error
```

Generates a controlled HTTP 500 response for monitoring and alert testing.

Example successful health response:

```json
{
  "status": "healthy"
}
```

---

## CI/CD Pipeline

The project uses GitHub Actions for CI/CD.

The pipeline follows this workflow:

```text
Feature Branch
      |
      v
Pull Request
      |
      v
CI Validation
      |
      v
Merge to main
      |
      v
Docker Build
      |
      v
Amazon ECR
      |
      v
Amazon EKS Deployment
```

### Continuous Integration

Pull Requests targeting `main` execute:

* Repository checkout
* Python setup
* Dependency installation
* Python syntax validation
* Docker image build validation

Changes are merged only after CI checks succeed.

---

## Continuous Deployment

A push to the `main` branch triggers the deployment workflow.

The CD pipeline:

1. Authenticates to AWS using GitHub OIDC
2. Logs in to Amazon ECR
3. Builds the backend Docker image
4. Tags the image using the Git commit SHA
5. Pushes the image to Amazon ECR
6. Updates the EKS kubeconfig
7. Updates the Kubernetes Deployment image
8. Waits for Kubernetes rollout completion

Example deployed image:

```text
678494330006.dkr.ecr.us-east-1.amazonaws.com/aws-eks-backend:b6ae3544c16e8034cbdcf4ead85b7d65bcf76e5b
```

Using the Git commit SHA as the image tag provides traceability between source code and deployed containers.

---

## AWS Authentication with GitHub OIDC

The project does not store permanent AWS access keys in GitHub.

GitHub Actions authenticates to AWS using OpenID Connect.

The trust chain is:

```text
GitHub Actions
      |
      v
GitHub OIDC Token
      |
      v
AWS IAM OIDC Provider
      |
      v
GitHubActionsEKSRole
      |
      v
Amazon ECR / Amazon EKS
```

The IAM trust policy is restricted to the specific GitHub repository and the `main` branch.

This reduces the security risk associated with long-lived AWS credentials.

---

## EKS Access Control

The EKS cluster uses:

```text
API_AND_CONFIG_MAP
```

authentication mode.

The GitHub Actions IAM role is configured through an EKS Access Entry.

The deployment role receives `AmazonEKSEditPolicy` access limited to:

```text
namespace: default
```

This follows a least-privilege approach instead of granting full cluster administrator permissions.

---

## Monitoring and Observability

The cluster is monitored using the Prometheus and Grafana stack.

Monitoring components include:

* Prometheus
* Grafana
* Alertmanager
* kube-state-metrics
* Node Exporter
* Metrics Server

Grafana dashboards provide visibility into:

* CPU utilization
* Memory utilization
* Pod count
* Node count
* Namespace resource consumption
* Pod resource usage
* Worker node utilization
* HTTP application metrics

The environment currently monitors two EKS worker nodes.

Example observed cluster metrics:

```text
Nodes: 2
Pods: 16
```

Grafana also displays CPU and memory utilization independently for each Kubernetes worker node.

---

## Application Monitoring

The Flask application exposes Prometheus-compatible HTTP metrics.

The monitoring stack can track:

* HTTP request counts
* Successful HTTP 200 responses
* HTTP 500 errors
* Pod health
* Application availability

The `/error` endpoint was used to generate controlled HTTP 500 responses to validate monitoring behavior.

---

## Horizontal Pod Autoscaling

The project includes a Kubernetes Horizontal Pod Autoscaler manifest.

The HPA is designed to scale application replicas based on workload metrics.

This allows the platform to demonstrate Kubernetes autoscaling capabilities while maintaining configurable resource limits.

---

## High Availability

The development environment currently uses:

* Two EKS worker nodes
* Two Availability Zones
* Two backend application replicas
* Kubernetes scheduling across both worker nodes

This provides workload redundancy at the worker-node level.

This development environment should not be interpreted as a complete production high-availability design. Additional production controls would include stronger PodDisruptionBudgets, multi-NAT architecture, stricter network policies, ingress hardening, centralized secrets management, backup strategy, and broader resilience testing.

---

## Cost Optimization

Because this is a portfolio environment, infrastructure size is intentionally controlled.

The EKS managed node group supports:

```text
min_size     = 1
desired_size = 2
max_size     = 3
```

The environment can be reduced to one worker node when full multi-node testing is not required.

This allows cost reduction without destroying the entire EKS environment.

AWS Budgets is also used to monitor project spending.

---

## Security Practices

The project includes several security controls:

* AWS OIDC instead of permanent GitHub AWS credentials
* IAM role-based authentication
* Namespace-scoped EKS deployment access
* Terraform-managed IAM configuration
* Private EKS worker subnets
* Public/private network separation
* Git exclusion of Terraform state
* Git exclusion of local environment files
* Git exclusion of Kubernetes local configuration
* Container images stored in private Amazon ECR

---

## Troubleshooting and Engineering Challenges

Several real-world issues were encountered and resolved during the project.

### EKS Capacity Reduction

The development environment was temporarily reduced from two worker nodes to one to control AWS costs.

The node group was later scaled back to two nodes using Terraform for multi-node testing.

---

### Kubernetes Pod Distribution

After adding the second worker node, existing application pods remained scheduled on the original worker.

A controlled Kubernetes rollout restart allowed the scheduler to recreate the replicas and distribute them across both workers.

---

### Grafana Access

Grafana was accessed locally using Kubernetes port forwarding.

Port conflicts and WSL networking behavior required validation using:

```bash
curl -I http://127.0.0.1:3001
```

The Grafana service successfully returned an HTTP redirect to the login page.

---

### GitHub OIDC Authentication

The first GitHub Actions deployment failed during:

```text
Configure AWS credentials
```

The initial error was caused by an incorrectly configured role value.

A subsequent failure returned:

```text
Not authorized to perform sts:AssumeRoleWithWebIdentity
```

The trust policy was then corrected to use the repository-specific GitHub OIDC subject.

After the correction, the GitHub Actions CI/CD workflow completed successfully.

---

### Terraform Safety Validation

A Terraform plan initially attempted to replace the EKS cluster when changing the authentication mode.

The plan was reviewed before applying.

The configuration was corrected to preserve:

```text
bootstrap_cluster_creator_admin_permissions = true
```

A new Terraform plan then showed:

```text
2 to add
1 to change
0 to destroy
```

This prevented unnecessary destruction and recreation of the EKS cluster.

---

## Project Validation

The completed project has demonstrated:

* Terraform infrastructure provisioning
* EKS managed Kubernetes cluster
* Multi-node Kubernetes workloads
* Multi-AZ worker deployment
* Docker containerization
* Amazon ECR integration
* Kubernetes LoadBalancer exposure
* Application health checks
* Prometheus metrics
* Grafana dashboards
* Horizontal Pod Autoscaling configuration
* GitHub feature branch workflow
* Pull Request CI validation
* GitHub Actions CI/CD
* AWS OIDC authentication
* Automated Docker image delivery
* Automated EKS application rollout
* IAM least-privilege access controls
* AWS cost optimization

---

## Repository Structure

```text
aws-eks-platform/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── application/
│   └── backend/
│       ├── app.py
│       ├── Dockerfile
│       ├── requirements.txt
│       └── .env.example
├── kubernetes/
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── service.yaml
│   └── servicemonitor.yaml
├── terraform/
│   ├── bootstrap/
│   │   └── main.tf
│   └── environments/
│       └── dev/
│           ├── backend.tf
│           ├── ecr.tf
│           ├── eks.tf
│           ├── github_oidc.tf
│           ├── iam.tf
│           ├── network.tf
│           └── providers.tf
├── .gitignore
└── README.md
```

---

## Future Improvements

Potential next steps include:

* Kubernetes PodDisruptionBudget
* Topology spread constraints or pod anti-affinity
* Kubernetes NetworkPolicies
* AWS Secrets Manager integration
* HTTPS/TLS ingress
* AWS Load Balancer Controller
* Route 53 DNS
* ACM certificate management
* automated Terraform validation in CI
* container vulnerability scanning
* centralized logging
* additional application tests
* staging environment
* production environment
* improved alert notification integrations

---

## Project Status

**Development environment: Operational**

Validated capabilities include:

```text
Terraform
AWS EKS
Docker
Amazon ECR
Kubernetes
GitHub Actions
AWS OIDC
Prometheus
Grafana
Multi-node deployment
Automated CI/CD
```

 

