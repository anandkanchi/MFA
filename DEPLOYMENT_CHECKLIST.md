# Google Cloud Deployment Checklist

## ☑️ Pre-Deployment Setup

### Account & Project Setup
- [ ] Sign up for Google Cloud with student email: https://cloud.google.com/free/student
- [ ] Verify student status (provide student ID/university email)
- [ ] Receive $300 free credits + $50/month bonus
- [ ] Go to: https://console.cloud.google.com/
- [ ] Create new project: "mutual-fund-analyzer"
- [ ] Note your PROJECT_ID (you'll need this)

### Install Tools
- [ ] **gcloud CLI**: https://cloud.google.com/sdk/docs/install
  - Download for Windows
  - Run installer
  - Restart PowerShell
  - Verify: `gcloud --version`

- [ ] **Docker Desktop**: https://www.docker.com/products/docker-desktop
  - Install for Windows
  - Enable WSL 2 backend (recommended)
  - Verify: `docker --version`

- [ ] **Git** (optional): https://git-scm.com/
  - For future CI/CD automation

---

## 🚀 Deployment Steps

### Step 1: Initialize gcloud
```powershell
gcloud init
```
- Choose: Create new configuration
- Login with your Google account
- Select your PROJECT_ID
- Select default region: `us-central1`

### Step 2: Enable Required APIs
```powershell
gcloud services enable `
  containerregistry.googleapis.com `
  run.googleapis.com `
  cloudbuild.googleapis.com
```

### Step 3: Authenticate Docker
```powershell
gcloud auth configure-docker
```

### Step 4: Set Project Variables
```powershell
$PROJECT_ID = "your-project-id"  # Replace with your project ID
$REGION = "us-central1"
$IMAGE_NAME = "mfa"

gcloud config set project $PROJECT_ID
```

### Step 5: Build & Push Docker Image
```powershell
cd d:\CAPSTONE\MFA

# Build locally (optional, for testing)
docker build -t mfa:latest .

# Tag for Google Container Registry
docker tag mfa:latest gcr.io/$PROJECT_ID/mfa:latest

# Push to registry
docker push gcr.io/$PROJECT_ID/mfa:latest
```

### Step 6: Deploy to Cloud Run
```powershell
gcloud run deploy mfa `
  --image gcr.io/$PROJECT_ID/mfa:latest `
  --region $REGION `
  --platform managed `
  --allow-unauthenticated `
  --memory 512Mi `
  --cpu 1 `
  --timeout 120 `
  --max-instances 10 `
  --port 8080
```

### Step 7: Get Your Public URL
```powershell
gcloud run services describe mfa `
  --region $REGION `
  --format='value(status.url)'
```

**Share this URL with the world!** 🌍

---

## ✅ Post-Deployment

### Verify Deployment
```powershell
# Check service status
gcloud run services describe mfa --region $REGION

# View recent logs
gcloud run services logs read mfa --limit 50

# Test health endpoint
curl https://mfa-xxxxx.run.app/health
```

### Monitor Performance
1. Go to: https://console.cloud.google.com/run
2. Click service: `mfa`
3. View: Metrics, Logs, Executions

### Set Up Custom Domain (Optional)
1. Console → Cloud Run → mfa → Manage Custom Domains
2. Add domain name: `yourdomain.com`
3. Update DNS records (provided by Google)
4. SSL certificate auto-issued

---

## 💰 Cost Monitoring

```powershell
# View current billing
gcloud billing accounts list

# Check budget
gcloud billing budgets describe --billing-account=YOUR_ACCOUNT_ID
```

Go to: https://console.cloud.google.com/billing

Set up budget alerts at $50/month

---

## 🐛 Troubleshooting

### Build fails
```powershell
gcloud builds log --stream
gcloud builds submit --config cloudbuild.yaml --machine-type=N1_HIGHCPU_8
```

### Deployment timeout
```powershell
gcloud run services update mfa --timeout 180
```

### Out of memory
```powershell
gcloud run services update mfa --memory 1Gi --cpu 2
```

### Permission denied
```powershell
gcloud auth login
gcloud config set project $PROJECT_ID
```

---

## 📊 Success Indicators

- [ ] Deployment completes without errors
- [ ] Cloud Run shows service as "OK"
- [ ] Public URL is accessible
- [ ] `/health` endpoint returns `{"status": "healthy"}`
- [ ] Homepage loads in browser
- [ ] Can fetch mutual fund data
- [ ] PDF/Excel export works
- [ ] Charts display correctly

---

## 🎯 Commands Quick Reference

| Task | Command |
|------|---------|
| Initialize | `gcloud init` |
| Set project | `gcloud config set project $PROJECT_ID` |
| Enable APIs | `gcloud services enable run.googleapis.com` |
| Authenticate Docker | `gcloud auth configure-docker` |
| Build image | `docker build -t gcr.io/$PROJECT_ID/mfa:latest .` |
| Push image | `docker push gcr.io/$PROJECT_ID/mfa:latest` |
| Deploy | `gcloud run deploy mfa --image gcr.io/$PROJECT_ID/mfa:latest ...` |
| View logs | `gcloud run services logs read mfa` |
| Get URL | `gcloud run services describe mfa --format='value(status.url)'` |
| Update service | `gcloud run services update mfa ...` |
| Delete service | `gcloud run services delete mfa` |

---

## 📞 Getting Help

- **Stuck?** Check logs: `gcloud run services logs read mfa --limit 100`
- **Build error?** Check build logs: `gcloud builds log --stream`
- **Permission issue?** Re-run: `gcloud auth login`
- **Documentation**: https://cloud.google.com/run/docs

---

**Ready to deploy? Follow the steps above! 🚀**
