# 🚀 Deploy YouTube Tutorial Scraper to Render (Free)

This guide will help you deploy your YouTube Tutorial Scraper as a web application on Render.com for **FREE** using **Azure Cosmos DB** for persistent storage.

## 📋 Prerequisites

- GitHub account
- YouTube API Key (from Google Cloud Console)
- Azure account (free tier available)
- 15 minutes of your time!

## 🎯 Step-by-Step Deployment

### Step 1: Set Up Azure Cosmos DB (FREE Forever!)

1. **Create Azure Account** (if you don't have one):
   - Go to [Azure Portal](https://portal.azure.com)
   - Sign up for free account ($200 credit + free services)

2. **Create Cosmos DB Account**:
   - In Azure Portal, search for "Azure Cosmos DB"
   - Click "Create" → "Azure Cosmos DB for NoSQL"
   - **Subscription**: Choose your subscription
   - **Resource Group**: Create new (e.g., "youtube-scraper-rg")
   - **Account Name**: Choose unique name (e.g., "youtube-tutorials-db")
   - **Location**: Choose closest region
   - **Capacity mode**: Select "Serverless" (FREE - no RU/s charges)
   - Click "Review + Create" → "Create"
   - Wait 5-10 minutes for deployment

3. **Get Connection Details**:
   - Go to your Cosmos DB account
   - Click "Keys" in left menu
   - Copy:
     - **URI** (endpoint)
     - **PRIMARY KEY**
   - Save these for Step 3!

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
   - Select `YOUTUBE-TUTORIAL-SCRAPER` repository

3. **Configure the Service**:
   - **Name**: `youtube-tutorial-scraper` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `master`
   - **Runtime**: `Docker`
   - **Plan**: Select **Free**

4. **Add Environment Variables**:
   - Click "Advanced" or scroll to "Environment Variables"
   - Add the following:

   | Key | Value | Description |
   |-----|-------|-------------|
   | `YOUTUBE_API_KEY` | Your YouTube API key | From Step 2 |
   | `SECRET_KEY` | Any random string | e.g., `my-secret-key-123` |
   | `PORT` | `10000` | Render default port |
   | `COSMOS_ENDPOINT` | Your Cosmos DB URI | From Step 1 |
   | `COSMOS_KEY` | Your Cosmos DB PRIMARY KEY | From Step 1 |
   | `COSMOS_DATABASE_NAME` | `YouTubeTutorials` | Database name |
   | `COSMOS_CONTAINER_NAME` | `tutorials` | Container name |

5. **Deploy**:
   - Click "Create Web Service"
   - Wait 5-10 minutes for the first build
   - Render will automatically build and deploy your app
   - Database and container will be created automatically on first run!


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

### Free Tier Benefits

**Azure Cosmos DB Serverless:**
- ✅ **Pay only for what you use** (no minimum charges)
- ✅ **1 million RU/s included** (plenty for this app)
- ✅ **25 GB storage** on free tier
- ✅ **Data persists forever** (no expiration)
- ✅ **Global distribution** available

**Render Free Tier:**
- ✅ **750 hours/month** (enough for 24/7 usage!)
- ✅ **512 MB RAM** (sufficient for this app)
- ⚠️ **App sleeps after 15 minutes of inactivity** (wakes up in ~30 seconds)

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
- Verify all environment variables are set correctly
- Ensure Azure Cosmos DB credentials are correct

### Database Connection Errors

- Verify `COSMOS_ENDPOINT` and `COSMOS_KEY` are correct
- Check Azure Cosmos DB firewall settings (should allow all networks for Render)
- Ensure database is in "Serverless" mode

### YouTube API Errors

- Verify API key is correct
- Check API key has YouTube Data API v3 enabled
- Ensure you haven't exceeded free quota (10,000 requests/day)

### Performance Issues

- Cosmos DB queries are optimized with partition keys
- Most queries (by language) are single-partition and very fast
- Cross-partition queries (by subject, search) may take slightly longer

## 💰 Cost Breakdown

### Completely Free (for small usage)

- ✅ Render Free Tier: $0/month
- ✅ YouTube API: $0 (free tier: 10,000 requests/day)
- ✅ GitHub: $0 (public/private repos)
- ✅ Azure Cosmos DB Serverless: **~$0-2/month** (with minimal usage)
- ✅ **Estimated Total: $0-2/month** 🎉

### Cosmos DB Pricing Details

- **Storage**: $0.25/GB per month (first 25 GB free on some plans)
- **Operations**: Charged per Request Unit (RU)
  - 1 read (1KB) = 1 RU ≈ $0.0000001
  - 1 write (1KB) = 5 RU ≈ $0.0000005
- **For 1000 tutorials**: Storage ~1 GB, Operations ~100K RU/month = **~$0.01-0.50/month**

### If You Need More Later

- Render Hobby: $7/month (no sleep, better performance)
- Cosmos DB Provisioned: ~$24/month for 400 RU/s (predictable costs)

## 🎉 You're Done!

Your YouTube Tutorial Scraper is now:

- 🌐 Accessible from anywhere
- 📱 Works on phone and laptop
- 💾 Saves your data permanently in Azure Cosmos DB
- 🔄 Globally distributed and scalable
- 🆓 Nearly FREE (serverless pricing)
- 🔄 Auto-updates when you push to GitHub

**Enjoy your mobile-friendly, globally-distributed tutorial scraper!** 🚀

## 🔧 Advanced: Local Development with Cosmos DB

To develop locally with Cosmos DB:

1. **Option 1: Use Azure Cosmos DB Emulator** (Windows/Docker):
   ```bash
   # Install emulator or run via Docker
   docker run -p 8081:8081 -p 10251:10251 mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator
   
   # Set environment variables
   export COSMOS_ENDPOINT="https://localhost:8081"
   export COSMOS_KEY="<emulator-key>"
   ```

2. **Option 2: Use your Azure Cosmos DB** (recommended):
   - Create a `.env` file in your project:
   ```
   COSMOS_ENDPOINT=https://your-account.documents.azure.com:443/
   COSMOS_KEY=your-primary-key
   COSMOS_DATABASE_NAME=YouTubeTutorials
   COSMOS_CONTAINER_NAME=tutorials
   YOUTUBE_API_KEY=your-youtube-api-key
   ```

---

## 📞 Need Help?

If you run into issues:

1. Check Render logs (Dashboard → Logs tab)
2. Review environment variables
3. Verify Azure Cosmos DB connection in Azure Portal
4. Check Cosmos DB metrics for request units and errors

## 🔗 Useful Links

- [Render Documentation](https://render.com/docs)
- [Azure Cosmos DB Documentation](https://learn.microsoft.com/azure/cosmos-db/)
- [YouTube API Documentation](https://developers.google.com/youtube/v3)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Azure Cosmos DB Emulator](https://learn.microsoft.com/azure/cosmos-db/emulator)
