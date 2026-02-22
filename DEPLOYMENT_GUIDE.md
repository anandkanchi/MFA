# Deployment Guide - Google Cloud Run

Complete guide to deploy the Mutual Fund Analyzer to Google Cloud Run with free student credits.

## Prerequisites

- Google Account with Student Email (`@student.` domain)
- Google Cloud Project created
- `gcloud` CLI installed
- `docker` installed (for local testing)
- Git account (optional, for CI/CD)

---

## Step 1: Set Up Google Cloud Account

### 1.1 Create Free Student Account
```bash
# Visit: https://cloud.google.com/free/student
# Sign up with your student email
# Verify with student verification (university email, student ID, etc.)
# Get $300 free credits + $50/month for 12 months
```

### 1.2 Create New Project
```bash
# Go to: https://console.cloud.google.com/
# Click "Select a Project" → "New Project"
# Name: "Mutual Fund Analyzer"
# Create the project
```

### 1.3 Set Up Billing
```bash
# Go to: Billing → Link to Student Account
# Enable billing (won't charge until credits run out)
```

---

## Step 2: Install & Configure gcloud

```bash
# Download from: https://cloud.google.com/sdk/docs/install

# Initialize gcloud
gcloud init

# Set default project
gcloud config set project YOUR_PROJECT_ID

# Authenticate Docker
gcloud auth configure-docker

# Enable required APIs
gcloud services enable \
  containerregistry.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  sql-component.googleapis.com
```

---

## Step 3: Local Testing with Docker

### 3.1 Build Docker Image
```bash
cd d:\CAPSTONE\MFA
docker build -t mfa:latest .
```

### 3.2 Run Locally
```bash
# Using docker-compose
docker-compose up

# Or manually
docker run -p 5000:8080 mfa:latest
```

Visit: `http://localhost:5000`

---

## Step 4: Deploy to Google Cloud Run

### 4.1 Push to Container Registry
```bash
# Set variables
$PROJECT_ID = "your-project-id"
$REGION = "us-central1"

# Build and push
docker build -t gcr.io/$PROJECT_ID/mfa:latest .
docker push gcr.io/$PROJECT_ID/mfa:latest
```

### 4.2 Deploy to Cloud Run
```bash
gcloud run deploy mfa \
  --image gcr.io/$PROJECT_ID/mfa:latest \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 120s \
  --max-instances 10 \
  --port 8080
```

**Success!** You'll get a URL like:
```
https://mfa-xxxxx.run.app
```

---

## Step 5: Set Up Custom Domain (Optional)

```bash
# Go to: Cloud Run → Services → mfa → Manage Custom Domains
# Add your custom domain (e.g., mfa.yourdomain.com)
# Follow DNS instructions from your domain registrar
# SSL certificate auto-issued by Google
```

---

## Step 6: Environment Variables

### 6.1 Create .env file in Cloud Run
```bash
gcloud run services update mfa \
  --update-env-vars \
  FLASK_ENV=production,DEBUG=False,LOG_LEVEL=INFO
```

### 6.2 Set Secrets (if needed)
```bash
# Create secret for API keys
echo -n "your-secret-value" | gcloud secrets create api-key --data-file=-

# Reference in service
gcloud run services update mfa \
  --set-env-vars="API_KEY=projects/YOUR_PROJECT_ID/secrets/api-key/versions/latest"
```

---

## Step 7: Database Setup (Optional - Cloud SQL)

### 7.1 Create Cloud SQL Instance
```bash
gcloud sql instances create mfa-db \
  --database-version POSTGRES_15 \
  --tier db-f1-micro \
  --region us-central1 \
  --availability-type zonal
```

### 7.2 Create Database
```bash
gcloud sql databases create mfa_prod --instance mfa-db
```

### 7.3 Connect from Cloud Run
```bash
# Install Cloud SQL Proxy in Dockerfile
# Update CONNECTION_STRING in Cloud Run environment
gcloud run services update mfa \
  --update-env-vars="DATABASE_URL=postgresql://user:password@/mfa_prod?host=/cloudsql/PROJECT_ID:REGION:mfa-db"
```

---

## Step 8: Continuous Deployment (CI/CD)

### 8.1 Connect GitHub Repository
```bash
# Go to: Cloud Build → Repository
# Connect your GitHub repo
# Select the branch to deploy
```

### 8.2 Set Up Trigger
```bash
gcloud builds create-github-trigger \
  --repo-name="your-repo" \
  --repo-owner="your-username" \
  --branch-pattern="^main$" \
  --build-config cloudbuild.yaml
```

### 8.3 Automatic Deployment
- Push to main branch
- Cloud Build automatically:
  1. Builds Docker image
  2. Pushes to Container Registry
  3. Deploys to Cloud Run
  4. No downtime (rolling deployment)

---

## Step 9: Monitoring & Logging

### 9.1 View Logs
```bash
gcloud run services logs read mfa --limit 50
```

### 9.2 Set Up Cloud Monitoring
```bash
# Go to: Monitoring → Dashboards
# Create dashboard with:
#   - Request rate
#   - Error rate
#   - Response time
#   - Memory usage
#   - CPU usage
```

### 9.3 Set Up Alerts
```bash
# Go to: Monitoring → Alerting → Create Policy
# Alert on: Error rate > 5% or Response time > 5s
```

---

## Step 10: Cost Optimization for Students

### 10.1 Always-Free Tier Usage
```
Cloud Run:
  - 180,000 vCPU-seconds/month (free)
  - 360,000 GiB-seconds/month (free)
  - 2 million requests/month (free)
  - $0.05 per GB outbound data

Cloud Storage:
  - 5 GB storage (free)
  - 50,000 class A operations
  - 500,000 class B operations

Cloud SQL:
  - 1 shared DB instance (db-f1-micro)
  - 10 GB storage (free)
```

### 10.2 Monitor Spending
```bash
# Go to: Billing → Budgets & Alerts
# Set budget alert at $50

# Check monthly usage
gcloud billing accounts describe YOUR_BILLING_ID
```

---

## Step 11: Security Best Practices

### 11.1 Enable IAM Roles
```bash
# Create service account
gcloud iam service-accounts create mfa-service \
  --display-name="Mutual Fund Analyzer Service"

# Grant roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:mfa-service@$PROJECT_ID.iam.gserviceaccount.com \
  --role roles/run.invoker
```

### 11.2 Enable HTTPS Only
```bash
# Cloud Run is HTTPS-only by default
# Enable ingress control
gcloud run services update mfa \
  --ingress internal-and-cloud-load-balancing
```

### 11.3 Restrict Access
```bash
# Allow only authenticated users (optional)
gcloud run services update mfa \
  --no-allow-unauthenticated

# Or specific IAM members
gcloud run services add-iam-policy-binding mfa \
  --member user:EMAIL@example.com \
  --role roles/run.invoker
```

---

## Step 12: Backup & Recovery

### 12.1 Export Data Regularly
```bash
# Backup to Cloud Storage
gcloud sql backups create \
  --instance mfa-db \
  --description "Daily backup"

# Automated backups
gcloud sql instances patch mfa-db \
  --backup-start-time "03:00"
```

### 12.2 Version Control
```bash
# Always commit to Git
git add .
git commit -m "Deploy version X.X.X"
git push origin main

# Cloud Build automatically deploys
```

---

## Troubleshooting

### Issue: Build fails with memory error
```bash
# Increase build machine
gcloud builds submit --config cloudbuild.yaml \
  --machine-type=N1_HIGHCPU_8
```

### Issue: Deployment timeout
```bash
# Increase Cloud Run timeout
gcloud run services update mfa --timeout 120
```

### Issue: Out of memory on runtime
```bash
# Increase memory allocation
gcloud run services update mfa --memory 512Mi --cpu 2
```

### Issue: Database connection fails
```bash
# Check proxy connection
gcloud sql connect mfa-db --user=postgres
```

---

## Final Checklist

- [ ] Google Cloud student account created
- [ ] Project created & billing enabled
- [ ] gcloud CLI installed & authenticated
- [ ] Docker image builds successfully
- [ ] Local Docker test passed
- [ ] Container pushed to Registry
- [ ] Deployed to Cloud Run
- [ ] Public URL verified
- [ ] Custom domain configured (optional)
- [ ] Environment variables set
- [ ] Database connected (if using)
- [ ] CI/CD pipeline configured
- [ ] Monitoring alerts set up
- [ ] Backup strategy in place
- [ ] Security settings configured

---

## Useful Links

- **Google Cloud Console:** https://console.cloud.google.com
- **Cloud Run Documentation:** https://cloud.google.com/run/docs
- **Cloud Run Pricing:** https://cloud.google.com/run/pricing
- **Student Benefits:** https://cloud.google.com/edu/students
- **gcloud CLI Reference:** https://cloud.google.com/sdk/gcloud/reference

---

## Support

For issues:
1. Check Cloud Logging: `gcloud run services logs read mfa`
2. Review Cloud Build: Cloud Build → History
3. Check service status: `gcloud run services describe mfa`
4. Review environment: `gcloud run services describe mfa --format=yaml`

Good luck! 🚀
