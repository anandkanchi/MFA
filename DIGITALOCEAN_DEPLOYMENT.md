# Deploy to DigitalOcean - Complete Guide

Get your app live with your **$200 free student credits**! 🎉

## 📋 Prerequisites Checklist
- ✅ Docker installed
- ✅ GitHub account with Student Pack ($200 credits)
- ✅ Project code ready
- ✅ This guide

---

## **Step 1: Push Code to GitHub** (5 minutes)

### 1.1 Create GitHub Repository
1. Go to: **https://github.com/new**
2. Name: **mfa** (or mutual-fund-analyzer)
3. Description: "Mutual Fund Data Analyzer"
4. Set to **Public** (DigitalOcean can access it)
5. Click **"Create repository"**
6. Copy the HTTPS URL (looks like: `https://github.com/YOUR_USERNAME/mfa.git`)

### 1.2 Push Your Code
Open PowerShell in your project folder:

```powershell
cd d:\CAPSTONE\MFA

# Initialize git
git init
git add .
git commit -m "Initial commit: Mutual Fund Analyzer with projections, charts, and export features"

# Add remote (replace with YOUR_USERNAME and repo name)
git remote add origin https://github.com/YOUR_USERNAME/mfa.git
git branch -M main
git push -u origin main

# When prompted:
# Username: YOUR_GITHUB_USERNAME
# Password: YOUR_GITHUB_TOKEN (see next section)
```

### 1.3 Create GitHub Personal Access Token
If you get "Authentication failed":

1. Go to: **https://github.com/settings/tokens**
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Name: `DigitalOcean`
4. Select scopes:
   - ✅ `repo` (full control of private repositories)
   - ✅ `read:user`
5. Click **"Generate token"**
6. **Copy the token** (you'll only see it once!)
7. Use this **as your password** when git asks

---

## **Step 2: Set Up DigitalOcean** (5 minutes)

### 2.1 Create DigitalOcean Account
1. Go to: **https://www.digitalocean.com/**
2. Click **"Sign in"** → **"GitHub"**
3. Click **"Authorize digitalocean"**
4. Verify your email (check inbox)
5. Complete profile setup

### 2.2 Activate Student Credits
1. Go to: **https://www.digitalocean.com/billing/account**
2. Click **"Billing"** (left menu)
3. Look for **"Student Developer Discount"** or **"Promo Code"**
4. If you have a code, enter it:
   - Paste your GitHub Student Pack **promo code** (check student benefits email)
   - Click **"Apply"**
5. You should see: **$200 Account Balance** ✅

### 2.3 Add Payment Method (Optional, but safe)
1. Go to: **Billing** → **Billing Settings**
2. Click **"Add Payment Method"**
3. Add credit card (only charged if you exceed $200 credit)
4. Click **"Save"**

---

## **Step 3: Deploy App to DigitalOcean** (10 minutes)

### 3.1 Create New App
1. Go to: **https://cloud.digitalocean.com/**
2. Click **"Apps"** (left sidebar)
3. Click **"Create App"** button

### 3.2 Select Repository
1. Choose: **"GitHub"**
2. Click **"Authorize"** (if prompted)
3. In dropdown, find your **mfa** repository
4. Select it
5. Branch: **main** (default)
6. Click **"Next"**

### 3.3 Configure App
DigitalOcean should auto-detect Dockerfile ✅

- **App Name:** `mfa` (or `mutual-fund-analyzer`)
- **Resource Type:** Docker (should be auto-selected)
- **Build Command:** (leave empty - Dockerfile has it)
- **Run Command:** (leave empty - Dockerfile has it)

Click **"Next"**

### 3.4 Select Plan
- **Basic Plan**: $12/month (covered by $200 credits for 16+ months)
- Or **Starter Plan**: Pay-as-you-go (even cheaper!)

Click **"Next"**

### 3.5 Review & Deploy
1. Review all settings
2. Click **"Create Resources"**
3. ⏳ **Wait 2-3 minutes** for deployment
4. Status changes from 🟡 "In Progress" to 🟢 "Active"

### 3.6 Get Your Live URL
1. Deployment complete! 🎉
2. Click on your app name
3. See **"Live App"** section
4. Click the **URL** (looks like: `https://mfa-xxxxx.ondigitalocean.app`)
5. **Share this URL!** Your app is LIVE! 🌍

---

## **Step 4: Verify Deployment** (2 minutes)

### Test Endpoints
Visit these URLs in your browser:

```
Health Check:
https://mfa-xxxxx.ondigitalocean.app/health

Homepage:
https://mfa-xxxxx.ondigitalocean.app/

API Test:
https://mfa-xxxxx.ondigitalocean.app/api/funds
```

All should return **200 OK** ✅

---

## **Step 5: Monitor & Update** (Ongoing)

### View Logs
1. App Dashboard → **"Logs"**
2. See real-time logs of your app running
3. Helps debug any issues

### Auto-Redeploy on Push
- Every time you push to GitHub main branch
- DigitalOcean **automatically redeploys** 🔄
- No manual work needed!

### Update Your Code
```powershell
# Make changes to your code
# Then:

git add .
git commit -m "Your changes here"
git push origin main

# DigitalOcean auto-deploys in 1-2 minutes!
```

---

## **Troubleshooting**

### Deployment Failed?
1. Check **Logs** → see error messages
2. Common issues:
   - **Port mismatch**: Make sure Dockerfile uses `8080`
   - **Missing dependencies**: Check `requirements.txt` is complete
   - **Timeout**: App takes too long to start

### App not responding?
1. Wait 5-10 minutes after deployment
2. Check **Components** → see health status
3. Restart the app: **App Settings** → **Restart App**

### How much do I owe?
- **Nothing!** (for typical usage)
- $200 free credits covers ~16 months
- You'll get email alert before credits run out
- Can add payment method anytime

---

## **Cost Breakdown**

| Service | Monthly Cost | Your Cost |
|---------|--------------|-----------|
| App Platform (1 Basic Container) | $12 | $0 (covered by credits) |
| Data transfer | ~$0.02/GB | $0 (low traffic) |
| **Total** | ~$12 | **$0 for 16+ months** |

---

## **Extra: Add Custom Domain** (Optional)

1. Buy domain from any registrar (e.g., Namecheap, GoDaddy)
2. DigitalOcean App → **Settings**
3. **Domains** section → Add your domain
4. Update DNS records (instructions provided)
5. SSL certificate auto-issued 🔒

---

## **Quick Checklist**

- [ ] Created GitHub repo with your code
- [ ] Pushed code using `git push`
- [ ] Created DigitalOcean account (used GitHub login)
- [ ] Activated $200 student credits
- [ ] Connected GitHub repo to DigitalOcean
- [ ] App deployed successfully
- [ ] Got your live URL
- [ ] Tested health endpoint
- [ ] App is live! 🎉

---

## **Next Steps**

✅ Your app is live!

Want to add more features?
- [ ] Custom domain name
- [ ] PostgreSQL database
- [ ] SSL certificate (auto-done)
- [ ] Environment variables
- [ ] Monitoring & alerts

---

**You're Done! 🎉 Share your URL: `https://mfa-xxxxx.ondigitalocean.app`**
