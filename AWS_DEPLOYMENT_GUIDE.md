# 🚀 AWS ECS Deployment Guide

Complete guide for deploying the Django Statistical Analysis Dashboard to AWS ECS using Docker.

## 📋 Prerequisites

- AWS CLI installed and configured
- Docker installed
- AWS account with appropriate permissions
- Domain name (optional, for custom domain)

## 🏗️ Architecture Overview

```
Internet → ALB → ECS Fargate → RDS PostgreSQL
                 ↓
               EFS (for media files)
                 ↓
            CloudWatch Logs
```

## 🛠️ Step-by-Step Deployment

### Step 1: Build and Test Docker Image Locally

```bash
# Build the Docker image
docker build -t statistical-analysis-dashboard .

# Test locally with Docker Compose
docker-compose up --build

# Access application at http://localhost:8000
```

### Step 2: Create AWS Resources

#### 2.1 Create ECR Repository
```bash
# Create ECR repository
aws ecr create-repository --repository-name statistical-analysis-dashboard

# Get login token and login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

#### 2.2 Create ECS Cluster
```bash
aws ecs create-cluster --cluster-name statistical-analysis-cluster
```

#### 2.3 Create RDS Database (Optional - for production database)
```bash
aws rds create-db-instance \
    --db-instance-identifier statistical-analysis-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username postgres \
    --master-user-password YOUR_PASSWORD \
    --allocated-storage 20 \
    --db-name statistical_analysis
```

#### 2.4 Create EFS for Media Files
```bash
aws efs create-file-system --tags Key=Name,Value=statistical-analysis-efs
```

#### 2.5 Create Secrets Manager Secrets
```bash
# Django Secret Key
aws secretsmanager create-secret \
    --name "django-secret-key" \
    --description "Django secret key for statistical analysis dashboard" \
    --secret-string "your-very-secure-secret-key-here"

# Database URL (if using RDS)
aws secretsmanager create-secret \
    --name "database-url" \
    --description "Database URL for statistical analysis dashboard" \
    --secret-string "postgresql://postgres:password@your-rds-endpoint:5432/statistical_analysis"
```

### Step 3: Build and Push Docker Image to ECR

```bash
# Tag the image for ECR
docker tag statistical-analysis-dashboard:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/statistical-analysis-dashboard:latest

# Push to ECR
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/statistical-analysis-dashboard:latest
```

### Step 4: Create IAM Roles

#### 4.1 ECS Task Execution Role
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Attach policies:
- `AmazonECSTaskExecutionRolePolicy`
- Custom policy for Secrets Manager access

#### 4.2 ECS Task Role
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "elasticfilesystem:DescribeFileSystems",
        "elasticfilesystem:DescribeAccessPoints"
      ],
      "Resource": "*"
    }
  ]
}
```

### Step 5: Update Task Definition

Edit `aws-ecs-task-definition.json` and replace:
- `YOUR_ACCOUNT_ID` with your AWS account ID
- `YOUR_ECR_REPOSITORY_URI` with your ECR repository URI
- `fs-YOUR_EFS_ID` with your EFS file system ID
- `fsap-YOUR_ACCESS_POINT_ID` with your EFS access point ID

### Step 6: Register Task Definition

```bash
aws ecs register-task-definition --cli-input-json file://aws-ecs-task-definition.json
```

### Step 7: Create Application Load Balancer

```bash
# Create ALB
aws elbv2 create-load-balancer \
    --name statistical-analysis-alb \
    --subnets subnet-12345678 subnet-87654321 \
    --security-groups sg-12345678

# Create target group
aws elbv2 create-target-group \
    --name statistical-analysis-tg \
    --protocol HTTP \
    --port 8000 \
    --vpc-id vpc-12345678 \
    --target-type ip \
    --health-check-path /

# Create listener
aws elbv2 create-listener \
    --load-balancer-arn arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/statistical-analysis-alb/1234567890123456 \
    --protocol HTTP \
    --port 80 \
    --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/statistical-analysis-tg/1234567890123456
```

### Step 8: Create ECS Service

```bash
aws ecs create-service \
    --cluster statistical-analysis-cluster \
    --service-name statistical-analysis-service \
    --task-definition statistical-analysis-dashboard:1 \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-12345678,subnet-87654321],securityGroups=[sg-12345678],assignPublicIp=ENABLED}" \
    --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/statistical-analysis-tg/1234567890123456,containerName=statistical-analysis-web,containerPort=8000
```

## 🔧 Environment Variables

Set these environment variables in your task definition:

| Variable | Description | Example |
|----------|-------------|---------|
| `DJANGO_SETTINGS_MODULE` | Django settings module | `statistical_analysis.settings_production` |
| `DEBUG` | Django debug mode | `False` |
| `SECRET_KEY` | Django secret key | (use Secrets Manager) |
| `DATABASE_URL` | Database connection URL | (use Secrets Manager) |
| `ALLOWED_HOSTS` | Allowed hosts | `your-domain.com,your-alb-dns-name` |

## 📊 Monitoring and Logging

### CloudWatch Logs
- Logs are automatically sent to CloudWatch
- Log group: `/ecs/statistical-analysis-dashboard`

### CloudWatch Metrics
- Monitor CPU, memory usage
- Set up alarms for high resource usage

### Health Checks
- ALB health checks on `/`
- Container health checks using curl

## 🔄 CI/CD Pipeline (Optional)

Create a GitHub Actions workflow:

```yaml
name: Deploy to ECS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Login to ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build and push image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: statistical-analysis-dashboard
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
      
      - name: Update ECS service
        run: |
          aws ecs update-service --cluster statistical-analysis-cluster --service statistical-analysis-service --force-new-deployment
```

## 💰 Cost Optimization

### Fargate Spot (for non-critical workloads)
```bash
aws ecs put-capacity-provider \
    --name FARGATE_SPOT \
    --capacity-provider-strategy capacityProvider=FARGATE_SPOT,weight=1
```

### Scheduled Scaling
- Scale down during off-hours
- Use Application Auto Scaling

## 🛡️ Security Best Practices

1. **Use Secrets Manager** for sensitive data
2. **Enable encryption** in transit and at rest
3. **Use least privilege** IAM roles
4. **Enable VPC Flow Logs**
5. **Use WAF** for web application firewall
6. **Enable GuardDuty** for threat detection

## 🔧 Troubleshooting

### Common Issues

#### Container Not Starting
```bash
# Check ECS service events
aws ecs describe-services --cluster statistical-analysis-cluster --services statistical-analysis-service

# Check CloudWatch logs
aws logs get-log-events --log-group-name /ecs/statistical-analysis-dashboard --log-stream-name ecs/statistical-analysis-web/TASK_ID
```

#### High Memory Usage
- Increase memory allocation in task definition
- Optimize Django application
- Use Redis for caching

#### Database Connection Issues
- Check security groups
- Verify database credentials in Secrets Manager
- Check VPC configuration

## 📚 Additional Resources

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)

## 🎉 Success!

Your Django Statistical Analysis Dashboard should now be running on AWS ECS!

Access your application at: `http://your-alb-dns-name` 