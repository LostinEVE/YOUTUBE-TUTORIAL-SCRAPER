# 🚀 Deploy YouTube Tutorial Scraper to Render (Free)

This guide will help you deploy your YouTube Tutorial Scraper as a web application on Render.com for **FREE**.

## 📋 Prerequisites

- GitHub account
- YouTube API Key (from Google Cloud Console)
- 10 minutes of your time!

## 🎯 Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Initialize Git** (if not already done):

   ```bash
   git init
   git add .
   git commit -m "Initial commit - Web version"
   ```

2. **Create a GitHub repository**:
   - Go to <https://github.com/new>
   - Name it: `youtube-tutorial-scraper`
   - Make it Public or Private (both work)
   - Don't initialize with README (we already have files)

3. **Push your code to GitHub**:

   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/youtube-tutorial-scraper.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Get Your YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new project (if you don't have one)
3. Enable **YouTube Data API v3**
4. Create credentials → API Key
5. Copy the API key (you'll need it later)

### Step 3: Deploy to Render

1. **Sign up for Render**:
   - Go to <https://render.com>
   - Click "Get Started for Free"
   - Sign up with your GitHub account

2. **Create New Web Service**:
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub repository
   - Select `youtube-tutorial-scraper` repository

3. **Configure the Service**:
   - **Name**: `youtube-tutorial-scraper` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Runtime**: `Docker`
   - **Plan**: Select **Free**

4. **Add Environment Variables**:
   - Click "Advanced" or scroll to "Environment Variables"
   - Add the following:

   | Key | Value |
   |-----|-------|
   | `YOUTUBE_API_KEY` | Your API key from Step 2 |
   | `SECRET_KEY` | Any random string (e.g., `my-secret-key-123`) |
   | `PORT` | `10000` |

5. **Configure Disk Storage** (Important!):
   - Scroll to "Disks"
   - Click "Add Disk"
   - **Name**: `tutorial-data`
   - **Mount Path**: `/app/data`
   - **Size**: 1 GB (free tier)

6. **Deploy**:
   - Click "Create Web Service"
   - Wait 5-10 minutes for the first build
   - Render will automatically build and deploy your app

### Step 4: Update Database Path (Important!)

Since we're using persistent storage, we need to update the database path.

1. **Edit `database.py`** locally:

   ```python
   # Change this line in database.py __init__ method:
   def __init__(self, db_path: str = "/app/data/tutorials.db"):
   ```

2. **Commit and push**:

   ```bash
   git add database.py
   git commit -m "Update database path for Render deployment"
   git push
   ```

3. Render will automatically redeploy with the new changes!

## ✅ Access Your App

Once deployed, you'll get a URL like:

- `https://youtube-tutorial-scraper.onrender.com`

You can now access this from:

- ✅ Your phone browser
- ✅ Your laptop anywhere
- ✅ Any device with internet

## 📱 Add to Phone Home Screen (Optional)

### iPhone

1. Open Safari and go to your app URL
2. Tap the Share button
3. Select "Add to Home Screen"
4. Name it "Tutorial Scraper"

### Android

1. Open Chrome and go to your app URL
2. Tap the three dots menu
3. Select "Add to Home screen"
4. Name it "Tutorial Scraper"

## ⚙️ Important Notes

### Free Tier Limitations

- ✅ **750 hours/month** (enough for 24/7 usage!)
- ✅ **512 MB RAM** (sufficient for this app)
- ⚠️ **App sleeps after 15 minutes of inactivity** (wakes up in ~30 seconds)
- ✅ **1 GB persistent storage** (stores your database)

### First Visit After Sleep

- The first request after sleep takes 20-30 seconds to load
- Subsequent requests are instant
- Keep the app active if you're using it frequently

### Keeping It Running

If you want to prevent sleep, use a free uptime monitor like:

- [UptimeRobot](https://uptimerobot.com/) (free, pings your app every 5 minutes)
- [Cron-Job.org](https://cron-job.org/)

## 🔄 Updating Your App

Whenever you make changes:

```bash
git add .
git commit -m "Your change description"
git push
```

Render will automatically detect changes and redeploy!

## 🐛 Troubleshooting

### App Won't Start

- Check "Logs" tab in Render dashboard
- Verify all environment variables are set
- Make sure disk is properly mounted

### Database Not Persisting

- Verify disk mount path is `/app/data`
- Check `database.py` uses `/app/data/tutorials.db`

### YouTube API Errors

- Verify API key is correct
- Check API key has YouTube Data API v3 enabled
- Ensure you haven't exceeded free quota (10,000 requests/day)

## 💰 Cost Breakdown

### Completely Free

- ✅ Render Free Tier: $0/month
- ✅ YouTube API: $0 (free tier: 10,000 requests/day)
- ✅ GitHub: $0 (public/private repos)
- ✅ **Total: $0/month** 🎉

### If You Need More Later

- Render Hobby: $7/month (no sleep, better performance)
- Render Starter: $25/month (production-ready)

## 🎉 You're Done

Your YouTube Tutorial Scraper is now:

- 🌐 Accessible from anywhere
- 📱 Works on phone and laptop
- 💾 Saves your data permanently
- 🆓 Completely FREE
- 🔄 Auto-updates when you push to GitHub

**Enjoy your mobile-friendly tutorial scraper!** 🚀

---

## 📞 Need Help?

If you run into issues:

1. Check Render logs (Dashboard → Logs tab)
2. Review environment variables
3. Verify GitHub repository is connected
4. Check that disk storage is properly configured

## 🔗 Useful Links

- [Render Documentation](https://render.com/docs)
- [YouTube API Documentation](https://developers.google.com/youtube/v3)
- [Flask Documentation](https://flask.palletsprojects.com/)
