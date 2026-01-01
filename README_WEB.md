# YouTube Tutorial Scraper - Web Version

A mobile-friendly web application for discovering and organizing programming tutorials from YouTube.

## 🌟 Features

- 🔍 **Scrape tutorials** by programming language or subject
- 📚 **Browse** by language, subject, or view all
- ⭐ **Favorite** tutorials for quick access
- ✅ **Mark as watched** to track your progress
- 🔎 **Search** through your saved tutorials
- 📊 **Statistics** dashboard
- 📱 **Mobile-responsive** design

## 🚀 Quick Start

### Local Development

1. **Clone the repository**:

   ```bash
   git clone https://github.com/YOUR_USERNAME/youtube-tutorial-scraper.git
   cd youtube-tutorial-scraper
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file:

   ```
   YOUTUBE_API_KEY=your_api_key_here
   SECRET_KEY=your_secret_key
   ```

4. **Run the app**:

   ```bash
   python web_app.py
   ```

5. **Open in browser**:
   - Go to `http://localhost:5000`

### Deploy to Render (Free!)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed step-by-step instructions to deploy this app for **FREE** on Render.com.

**Key benefits of deploying:**

- ✅ Access from any device (phone, laptop, tablet)
- ✅ No need to keep your computer on
- ✅ Completely FREE forever
- ✅ Mobile-friendly interface
- ✅ Automatic updates via GitHub

## 📱 Mobile Access

Once deployed, you can:

- Access from any web browser
- Add to your phone's home screen for app-like experience
- Use on the go when you're away from home

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with persistent storage
- **Frontend**: Bootstrap 5 + Bootstrap Icons
- **API**: YouTube Data API v3
- **Deployment**: Docker + Render.com

## 📂 Project Structure

```
youtube-tutorial-scraper/
├── web_app.py              # Flask application
├── app.py                  # Original CLI version (still works!)
├── youtube_scraper.py      # YouTube API integration
├── database.py             # SQLite database management
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── render.yaml            # Render deployment config
├── DEPLOYMENT.md          # Deployment instructions
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── tutorials.html
│   ├── scrape.html
│   └── ...
└── README.md             # This file
```

## 🔑 Getting a YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new project
3. Enable **YouTube Data API v3**
4. Create credentials → API Key
5. Copy the key and add it to your `.env` file

## 💻 CLI Version

The original CLI version is still available! Run:

```bash
python app.py
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests

## 📝 License

This project is open source and available under the MIT License.

## ⚠️ Important Notes

- **YouTube API Quota**: Free tier provides 10,000 requests/day
- **Render Free Tier**: App sleeps after 15 min of inactivity (wakes in ~30 sec)
- **Storage**: Free tier includes 1 GB persistent storage

## 🎉 Get Started Now

Follow the [DEPLOYMENT.md](DEPLOYMENT.md) guide to get your app running in the cloud for FREE within 10 minutes!
