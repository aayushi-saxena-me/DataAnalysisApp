#!/bin/bash

# AWS ECS Deployment Script for Django Statistical Analysis Dashboard
# Usage: ./scripts/deploy.sh [environment]

set -e

# Configuration
REGION=${AWS_REGION:-us-east-1}
ENVIRONMENT=${1:-production}
APP_NAME="statistical-analysis-dashboard"
CLUSTER_NAME="statistical-analysis-cluster"
SERVICE_NAME="statistical-analysis-service"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting deployment for ${APP_NAME} to ${ENVIRONMENT}${NC}"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
if [ -z "$ACCOUNT_ID" ]; then
    echo -e "${RED}❌ Failed to get AWS account ID. Check your AWS credentials.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ AWS Account ID: ${ACCOUNT_ID}${NC}"

# ECR repository URI
ECR_REPOSITORY_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${APP_NAME}"

# Login to ECR
echo -e "${YELLOW}🔐 Logging in to Amazon ECR...${NC}"
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ECR_REPOSITORY_URI}

# Build Docker image
echo -e "${YELLOW}🏗️  Building Docker image...${NC}"
docker build -t ${APP_NAME}:latest .

# Tag image for ECR
IMAGE_TAG=$(date +%Y%m%d%H%M%S)-$(git rev-parse --short HEAD 2>/dev/null || echo "latest")
docker tag ${APP_NAME}:latest ${ECR_REPOSITORY_URI}:${IMAGE_TAG}
docker tag ${APP_NAME}:latest ${ECR_REPOSITORY_URI}:latest

echo -e "${GREEN}✅ Image tagged: ${ECR_REPOSITORY_URI}:${IMAGE_TAG}${NC}"

# Push to ECR
echo -e "${YELLOW}📤 Pushing image to ECR...${NC}"
docker push ${ECR_REPOSITORY_URI}:${IMAGE_TAG}
docker push ${ECR_REPOSITORY_URI}:latest

echo -e "${GREEN}✅ Image pushed successfully${NC}"

# Update ECS service
echo -e "${YELLOW}🔄 Updating ECS service...${NC}"
aws ecs update-service \
    --cluster ${CLUSTER_NAME} \
    --service ${SERVICE_NAME} \
    --force-new-deployment \
    --region ${REGION}

echo -e "${GREEN}✅ ECS service update initiated${NC}"

# Wait for deployment to complete
echo -e "${YELLOW}⏳ Waiting for deployment to complete...${NC}"
aws ecs wait services-stable \
    --cluster ${CLUSTER_NAME} \
    --services ${SERVICE_NAME} \
    --region ${REGION}

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"

# Get service status
SERVICE_STATUS=$(aws ecs describe-services \
    --cluster ${CLUSTER_NAME} \
    --services ${SERVICE_NAME} \
    --region ${REGION} \
    --query 'services[0].deployments[0].status' \
    --output text)

RUNNING_COUNT=$(aws ecs describe-services \
    --cluster ${CLUSTER_NAME} \
    --services ${SERVICE_NAME} \
    --region ${REGION} \
    --query 'services[0].runningCount' \
    --output text)

DESIRED_COUNT=$(aws ecs describe-services \
    --cluster ${CLUSTER_NAME} \
    --services ${SERVICE_NAME} \
    --region ${REGION} \
    --query 'services[0].desiredCount' \
    --output text)

echo -e "${GREEN}📊 Service Status: ${SERVICE_STATUS}${NC}"
echo -e "${GREEN}📊 Running Tasks: ${RUNNING_COUNT}/${DESIRED_COUNT}${NC}"

# Get load balancer URL
ALB_DNS=$(aws elbv2 describe-load-balancers \
    --names statistical-analysis-alb \
    --region ${REGION} \
    --query 'LoadBalancers[0].DNSName' \
    --output text 2>/dev/null || echo "N/A")

if [ "$ALB_DNS" != "N/A" ]; then
    echo -e "${GREEN}🌐 Application URL: http://${ALB_DNS}${NC}"
fi

echo -e "${GREEN}✨ Deployment script completed!${NC}" 