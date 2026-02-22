# Installation Guide - Docker & gcloud CLI

## 📦 Part 1: Install Docker Desktop

### Step 1: Download Docker Desktop
1. Go to: **https://www.docker.com/products/docker-desktop**
2. Click **"Download for Windows"** (Intel Chip recommended for most users)
3. Save the file to your Downloads folder
4. Wait for download to complete (~500MB)

### Step 2: Install Docker Desktop
1. Open your **Downloads** folder
2. Double-click **"Docker Desktop Installer.exe"**
3. Click **"OK"** when prompted for admin permissions
4. In installer window:
   - Keep defaults checked (WSL 2 backend recommended)
   - Click **"Install"**
   - Wait for installation (2-5 minutes)

### Step 3: Finish Installation
1. When complete, click **"Close"**
2. Your computer will **restart automatically** (save any work first!)
3. After restart, Docker will start automatically
4. Look for Docker icon in taskbar (whale icon 🐳)

### Step 4: Verify Docker Installation
Open **PowerShell** and run:
```powershell
docker --version
```

Expected output:
```
Docker version 25.x.x, build xxxxx
```

✅ If you see a version number, Docker is **installed successfully!**

---

## 🔧 Part 2: Install gcloud CLI

### Step 1: Download gcloud SDK
1. Go to: **https://cloud.google.com/sdk/docs/install-gcloud-cli**
2. Click **"Windows (64-bit)"** (or 32-bit if you have 32-bit Windows)
3. Download the **`.msi` installer file** (not the ZIP)
4. Save to Downloads folder
5. Wait for download (~200MB)

### Step 2: Install gcloud CLI
1. Open **Downloads** folder
2. Double-click **"google-cloud-sdk-xxx-windows-x86_64.msi"**
3. Click **"Next"** through the installer
4. Accept terms and click **"I Agree"**
5. Choose installation path (default is fine):
   - Default: `C:\Program Files\Google\Cloud SDK`
   - Click **"Install"**
6. Wait for installation (1-2 minutes)
7. Check the box: **"Start Google Cloud SDK Shell"**
8. Click **"Finish"**

### Step 3: Verify gcloud Installation
A new terminal window should open. Run:
```powershell
gcloud --version
```

Expected output:
```
Google Cloud SDK 470.0.0
bq-component version 2.0.x
core 2024.x.x
gsutil 5.x
```

✅ If you see version numbers, gcloud is **installed successfully!**

---

## 🔑 Part 3: Set Up Google Cloud Account

### Step 1: Create Google Cloud Account
1. Go to: **https://cloud.google.com/free/student**
2. Click **"Get started for free"**
3. Sign in or create Google account with your **student email** (e.g., `your.name@student.university.edu`)
4. Verify your student status:
   - Upload student ID **OR**
   - Verify with university email
   - Google will verify within 24 hours

### Step 2: Accept Free Credits
- You'll automatically receive:
  - **$300 free credits** (expires in 12 months)
  - **$50/month bonus** for 12 months
  - **Always-free tier** (Cloud Run: 2M requests/month)

### Step 3: Create New Project
1. Go to: **https://console.cloud.google.com/**
2. Click **"Select a Project"** (top left)
3. Click **"Create Project"**
4. Enter name: **"Mutual Fund Analyzer"**
5. Click **"Create"**
6. Wait 1-2 minutes for project to be created
7. **Copy your PROJECT_ID** (you'll need this!)
   - It looks like: `mutual-fund-analyzer-123456`

### Step 4: Set Up Billing
1. In Cloud Console, go to: **Billing** (left menu)
2. Click **"Link a billing account"**
3. Select your **Student account** with free credits
4. Click **"Link"**
5. You should see: "Free tier available" ✅

---

## 🔐 Part 4: Initialize gcloud CLI

### Step 1: Open PowerShell (new window)
- Press **Windows Key** + **R**
- Type: `powershell`
- Press **Enter**

### Step 2: Run gcloud init
```powershell
gcloud init
```

### Step 3: Follow the Prompts

**Question 1:** "Do you want to configure a default Compute Engine zone?"
```
Answer: Y (Yes)
```

**Question 2:** "Please enter numeric choice or text for an option from the list above:"
```
Scroll to find: us-central1
Type: us-central1
Press Enter
```

**Question 3:** Browser window opens for login
```
- Click your Google account
- Click "Allow" for permissions
- Close the browser window
```

**Question 4:** "Which Google Cloud project would you like to use?"
```
Select: mutual-fund-analyzer-xxxxx (your project)
Press Enter
```

### Step 4: Verify Configuration
```powershell
gcloud config list
```

You should see:
```
[core]
account = your.email@gmail.com
project = mutual-fund-analyzer-xxxxx
region = us-central1
```

✅ If you see this, gcloud is **configured successfully!**

---

## 🔑 Part 5: Authenticate Docker with gcloud

### Step 1: Run Authentication Command
```powershell
gcloud auth configure-docker
```

Expected output:
```
The following configurations will be added to your Docker config file located at [C:\Users\YourName\.docker\config.json]:
{
  "credHelpers": {
    "gcr.io": "gcloud"
  }
}

Do you want to continue (Y/n)?
```

### Step 2: Confirm
```
Type: Y
Press Enter
```

✅ Docker is now **authenticated with Google Cloud!**

---

## ✅ Final Verification

Run all three commands to confirm everything is installed:

```powershell
# Check Docker
docker --version

# Check gcloud
gcloud --version

# Check authentication
gcloud auth list
```

Expected outputs:
```
Docker version 25.x.x, build xxxxx
Google Cloud SDK x.x.x
gcloud
gcloud          ACTIVE
your.email@gmail.com

mutual-fund-analyzer-xxxxx
```

✅ **All tools installed and configured!**

---

## 🚨 If Something Goes Wrong

### Docker not found?
- Restart your computer
- Verify Docker Desktop is running (check taskbar)
- Reinstall Docker

### gcloud not found?
- Restart PowerShell
- Check PATH: `$env:Path | Select-String "google"`
- Reinstall gcloud SDK

### Authentication failed?
```powershell
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### Can't find your PROJECT_ID?
Go to: https://console.cloud.google.com/
Look at top left - it shows your project name and ID

---

## 📝 Quick Checklist

Complete these in order:

- [ ] Downloaded Docker Desktop
- [ ] Installed Docker Desktop
- [ ] Restarted computer
- [ ] Verified: `docker --version` works
- [ ] Created Google Cloud account (student email)
- [ ] Verified student status
- [ ] Created new project
- [ ] Copied PROJECT_ID somewhere safe
- [ ] Set up billing
- [ ] Downloaded gcloud CLI
- [ ] Installed gcloud CLI
- [ ] Ran `gcloud init`
- [ ] Answered all prompts (selected us-central1)
- [ ] Logged in via browser
- [ ] Selected your project
- [ ] Ran `gcloud config list` (saw your project)
- [ ] Ran `gcloud auth configure-docker`

---

## 💡 Pro Tips

1. **Keep your PROJECT_ID saved** - you'll use it many times
2. **Docker takes up ~10GB** - make sure you have space
3. **gcloud CLI is lightweight** - ~500MB
4. **Best to restart after installing both**
5. **Use PowerShell, not Command Prompt** - it's easier

---

**Once you complete these steps, come back and I'll deploy your app to the cloud! 🚀**
