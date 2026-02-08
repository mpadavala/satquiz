# AWS Deployment Guide

This guide covers deploying the SAT Vocabulary Learning App to AWS.

## Architecture Overview

```
┌─────────────┐
│  CloudFront │ (CDN for frontend)
└──────┬──────┘
       │
┌──────▼──────┐
│  S3 Bucket  │ (Frontend static files)
└─────────────┘

┌─────────────┐
│  ALB/API    │ (API Gateway)
└──────┬──────┘
       │
┌──────▼──────┐
│ ECS Fargate │ (FastAPI backend)
└──────┬──────┘
       │
┌──────▼──────┐
│ RDS Postgres│ (Database)
└─────────────┘

┌─────────────┐
│  S3 Bucket  │ (PDF storage)
└──────┬──────┘
       │
┌──────▼──────┐
│  Lambda     │ (PDF processing trigger)
└──────┬──────┘
       │
┌──────▼──────┐
│  SQS Queue  │ (Word processing queue)
└──────┬──────┘
       │
┌──────▼──────┐
│ ECS Worker  │ (Background word processor)
└─────────────┘
```

## Prerequisites

1. AWS CLI configured
2. Docker installed
3. Terraform (optional, for IaC)
4. AWS account with appropriate permissions

## Step 1: Database Setup (RDS PostgreSQL)

### Create RDS Instance

```bash
aws rds create-db-instance \
  --db-instance-identifier satquiz-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username postgres \
  --master-user-password YOUR_PASSWORD \
  --allocated-storage 20 \
  --vpc-security-group-ids sg-xxxxx \
  --db-subnet-group-name default \
  --backup-retention-period 7
```

### Get Connection String

```bash
aws rds describe-db-instances --db-instance-identifier satquiz-db
```

Update `DATABASE_URL` in your environment variables.

## Step 2: S3 Buckets

### Create Buckets

```bash
# Frontend bucket
aws s3 mb s3://satquiz-frontend --region us-east-1

# PDF storage bucket
aws s3 mb s3://satquiz-pdfs --region us-east-1
```

### Configure Frontend Bucket for Static Website

```bash
aws s3 website s3://satquiz-frontend \
  --index-document index.html \
  --error-document index.html
```

### Configure CORS for PDF Bucket

```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET", "PUT", "POST"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```

## Step 3: ECR (Elastic Container Registry)

### Create Repositories

```bash
# Backend API
aws ecr create-repository --repository-name satquiz-api

# Worker
aws ecr create-repository --repository-name satquiz-worker
```

### Build and Push Images

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build backend
cd backend
docker build -t satquiz-api .
docker tag satquiz-api:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/satquiz-api:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/satquiz-api:latest

# Build worker
cd worker
docker build -t satquiz-worker .
docker tag satquiz-worker:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/satquiz-worker:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/satquiz-worker:latest
```

## Step 4: ECS Fargate Setup

### Create ECS Cluster

```bash
aws ecs create-cluster --cluster-name satquiz-cluster
```

### Create Task Definitions

See `aws/ecs-task-definition-api.json` and `aws/ecs-task-definition-worker.json` for examples.

### Create ECS Service

```bash
aws ecs create-service \
  --cluster satquiz-cluster \
  --service-name satquiz-api \
  --task-definition satquiz-api \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

## Step 5: Application Load Balancer

### Create ALB

```bash
aws elbv2 create-load-balancer \
  --name satquiz-alb \
  --subnets subnet-xxx subnet-yyy \
  --security-groups sg-xxx
```

### Create Target Group

```bash
aws elbv2 create-target-group \
  --name satquiz-api-tg \
  --protocol HTTP \
  --port 8000 \
  --vpc-id vpc-xxx \
  --target-type ip \
  --health-check-path /health
```

### Create Listener

```bash
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...
```

## Step 6: CloudFront Distribution

### Create Distribution

```bash
aws cloudfront create-distribution \
  --origin-domain-name satquiz-frontend.s3.amazonaws.com \
  --default-root-object index.html
```

## Step 7: AWS Cognito (Google OAuth)

### Create User Pool

1. Go to AWS Cognito Console
2. Create User Pool
3. Configure Google as Identity Provider
4. Set up App Client
5. Configure Callback URLs

### Update Frontend

Update `frontend/src/api/auth.js` to use Cognito SDK.

## Step 8: SQS Queue

### Create Queue

```bash
aws sqs create-queue \
  --queue-name satquiz-word-queue \
  --attributes VisibilityTimeout=300
```

### Configure Worker Service

Update worker task definition to use SQS queue URL.

## Step 9: Secrets Manager

### Store Secrets

```bash
# Database password
aws secretsmanager create-secret \
  --name satquiz/db-password \
  --secret-string "YOUR_DB_PASSWORD"

# OpenAI API Key
aws secretsmanager create-secret \
  --name satquiz/openai-key \
  --secret-string "YOUR_OPENAI_KEY"
```

### Update Task Definitions

Reference secrets in ECS task definitions.

## Step 10: Lambda Function (PDF Processing)

### Create Lambda Function

```python
import json
import boto3

sqs = boto3.client('sqs')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extract words from PDF
    # Send to SQS queue
    pass
```

### Configure S3 Trigger

Set up S3 event notification to trigger Lambda on PDF upload.

## Step 11: Environment Variables

### Backend Environment Variables

```bash
DATABASE_URL=postgresql://user:pass@rds-endpoint:5432/satquiz
OPENAI_API_KEY=sk-...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
S3_BUCKET=satquiz-pdfs
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/.../satquiz-word-queue
```

## Step 12: Frontend Deployment

### Build Frontend

```bash
cd frontend
npm run build
```

### Upload to S3

```bash
aws s3 sync dist/ s3://satquiz-frontend --delete
```

### Invalidate CloudFront

```bash
aws cloudfront create-invalidation \
  --distribution-id E1234567890 \
  --paths "/*"
```

## CI/CD with GitHub Actions

See `.github/workflows/deploy.yml` for example workflow.

## Monitoring

### CloudWatch Logs

- ECS tasks automatically send logs to CloudWatch
- Set up log groups for API and Worker

### CloudWatch Metrics

- Monitor ECS service metrics
- Set up alarms for errors

## Cost Optimization

- Use Reserved Instances for RDS
- Use Spot Instances for worker (if using EC2)
- Enable S3 lifecycle policies
- Use CloudFront caching

## Security

- Use VPC for RDS (private subnets)
- Enable SSL/TLS for ALB
- Use IAM roles for ECS tasks
- Enable WAF on CloudFront
- Use Secrets Manager for sensitive data

## Troubleshooting

### Check ECS Task Logs

```bash
aws logs tail /ecs/satquiz-api --follow
```

### Check RDS Connection

```bash
psql -h rds-endpoint -U postgres -d satquiz
```

### Test API

```bash
curl https://api.yourdomain.com/health
```

## Next Steps

1. Set up monitoring and alerting
2. Configure auto-scaling
3. Set up backup strategy
4. Implement CI/CD pipeline
5. Add domain and SSL certificates
