# KrishiSathi Deployment Guide

This guide covers deployment procedures for both production AWS cloud environments and local hackathon demonstration environments.

---

## 1. Cloud Architecture & Deployment Targets

```
                                  ┌───────────────────────────────┐
                                  │      Vercel / AWS Amplify     │
                                  │  React + Vite Frontend (SPA)  │
                                  └───────────────┬───────────────┘
                                                  │ HTTPS
                                  ┌───────────────▼───────────────┐
                                  │      AWS App Runner / ECS     │
                                  │   FastAPI Backend Container   │
                                  └───────┬───────────────┬───────┘
                                          │               │
                         ┌────────────────┘               └────────────────┐
                         ▼                                                 ▼
             ┌────────────────────────┐                        ┌───────────────────────┐
             │     Amazon Bedrock     │                        │  Open-Meteo & IMD API │
             │  (Claude 3.5 / Titan)  │                        │ (Agro-Weather Radar)  │
             └────────────────────────┘                        └───────────────────────┘
```

---

## 2. Deploying Backend on AWS App Runner / ECS

### Option A: AWS App Runner (Fastest Container Deployment)
1. Push the backend Docker image to Amazon ECR:
   ```bash
   aws ecr create-repository --repository-name krishisathi-backend
   docker build -t krishisathi-backend .
   docker tag krishisathi-backend:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/krishisathi-backend:latest
   docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/krishisathi-backend:latest
   ```
2. In the AWS App Runner console, create a new service from the ECR image:
   - Port: `8000`
   - CPU: `1 vCPU`, Memory: `2 GB`
   - IAM Role: Attach policy granting `bedrock:InvokeModel` to your IAM role.
3. Configure environment variables in App Runner:
   - `AWS_REGION=us-east-1`
   - `BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0`
   - `FRONTEND_URL=https://your-frontend.vercel.app`

### Option B: AWS Bedrock AgentCore Deployment
Where supported by your AWS environment permissions, deploy the Krishi Orchestrator directly as a managed agent in Amazon Bedrock AgentCore.

---

## 3. Deploying Frontend to Vercel

1. Connect this GitHub repository (`https://github.com/CyborgX-hash/AWS-builder-Project`) to Vercel.
2. Root Directory: `./` (or `frontend`)
3. Build Command: `cd frontend && npm install && npm run build`
4. Output Directory: `frontend/dist`
5. Environment Variables:
   - `VITE_API_BASE_URL`: `https://your-backend-app-runner-url.awsapprunner.com`
6. Click **Deploy**.

---

## 4. Local Single-Command Deployment (Docker Compose)

Run the full-stack system locally using Docker Compose:
```bash
docker-compose up --build
```
- Frontend UI: `http://localhost:5173`
- Backend API Docs: `http://localhost:8000/docs`
