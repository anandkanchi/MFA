# Cloud Run Quick Start

Deploy to Google Cloud Run in **5 minutes** ⚡

## Prerequisites
- Google Cloud student account (free $300 credits)
- `gcloud` CLI installed
- Docker installed
- This project cloned locally

## Quick Deploy (5 steps)

### 1. Authenticate & Set Project
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud auth configure-docker
```

### 2. Enable APIs
```bash
gcloud services enable run.googleapis.com containerregistry.googleapis.com
```

### 3. Build & Push
```bash
cd d:\CAPSTONE\MFA
docker build -t gcr.io/YOUR_PROJECT_ID/mfa:latest .
docker push gcr.io/YOUR_PROJECT_ID/mfa:latest
```

### 4. Deploy
```bash
gcloud run deploy mfa \
  --image gcr.io/YOUR_PROJECT_ID/mfa:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 512Mi
```

### 5. Get URL
```bash
gcloud run services describe mfa --region us-central1 --format='value(status.url)'
```

**View your app at the URL returned! 🎉**

## Custom Domain (Optional)

```bash
gcloud run services update mfa \
  --region us-central1 \
  --update-env-vars DOMAIN=your-domain.com
```

## Tear Down (Stop Charges)
```bash
gcloud run services delete mfa --region us-central1
```

---

For full deployment guide, see: [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
