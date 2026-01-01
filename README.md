# YouTube Programming Tutorial Scraper

A personal tool to scrape YouTube for programming tutorials, categorize them by language and subject, and filter out Shorts and India-based videos.

## Features

- 🔍 **Search YouTube** for programming tutorials by language or subject
- 📚 **Categorize** videos by programming language and topic
- 🚫 **Filter out** YouTube Shorts (videos < 2 minutes)
- 🚫 **Filter out** India-based content (Hindi and regional language tutorials)
- 💾 **Save** tutorials to a local SQLite database
- ⭐ **Favorite** tutorials for later viewing
- ✓ **Track** watched tutorials
- 📊 **View statistics** about your tutorial collection

## Setup

### 1. Get a YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable the **YouTube Data API v3**
4. Go to **Credentials** and create an **API Key**
5. Copy your API key

### 2. Install Dependencies

```bash
cd youtube-tutorial-scraper
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file in the project directory:

```
YOUTUBE_API_KEY=your_api_key_here
```

### 4. Run the App

```bash
python app.py
```

## Usage

The app provides an interactive menu:

1. **Scrape new tutorials** - Search YouTube for new programming tutorials
2. **Browse by programming language** - View tutorials organized by language (Python, JavaScript, etc.)
3. **Browse by subject** - View tutorials organized by topic (Web Dev, ML, etc.)
4. **View statistics** - See overview of your tutorial collection
5. **Search tutorials** - Search your saved tutorials by keyword
6. **View favorites** - See your favorited tutorials
7. **View all tutorials** - Browse all saved tutorials

## Configuration

Edit `config.py` to customize:

- `PROGRAMMING_LANGUAGES` - List of programming languages to search
- `PROGRAMMING_SUBJECTS` - List of subjects/topics to search
- `MIN_VIDEO_DURATION_SECONDS` - Minimum video length (filters Shorts)
- `MAX_RESULTS_PER_QUERY` - Results per search query
- `UPLOAD_DATE_FILTER` - Filter by upload date (month, week, year, etc.)

## Filtering Logic

### YouTube Shorts Filtering

- Videos under 2 minutes (configurable) are automatically filtered out
- Uses the `videoDuration=medium` parameter to prefer longer videos

### India Content Filtering

The app filters out videos with titles, descriptions, or channel names containing:

- Hindi language indicators (hindi, हिंदी, etc.)
- Regional Indian language indicators (Tamil, Telugu, Malayalam, etc.)
- Common phrases like "in hindi", "hindi tutorial", etc.

## Database

Tutorials are stored in `tutorials.db` (SQLite). The database includes:

- Video metadata (title, description, channel, duration, views)
- Categorization (language, subject)
- User flags (watched, favorite)
- Timestamps

## API Quota

The YouTube Data API has a daily quota (typically 10,000 units). Each search costs about 100 units, and fetching video details costs 1 unit per video. The app is designed to be efficient with quota usage.

## License

MIT - Personal use
