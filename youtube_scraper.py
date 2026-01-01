"""YouTube API scraper for programming tutorials"""

import os
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

from config import (
    PROGRAMMING_LANGUAGES,
    PROGRAMMING_SUBJECTS,
    EXCLUDED_COUNTRIES,
    MIN_VIDEO_DURATION_SECONDS,
    MAX_RESULTS_PER_QUERY,
    UPLOAD_DATE_FILTER,
)

load_dotenv()


class YouTubeScraper:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError(
                "YouTube API key is required. Set YOUTUBE_API_KEY in .env file "
                "or pass it directly."
            )
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

        # Patterns to identify India-based content
        self.india_indicators = [
            r'\b(hindi|हिंदी|हिन्दी)\b',
            r'\b(tamil|தமிழ்)\b',
            r'\b(telugu|తెలుగు)\b',
            r'\b(malayalam|മലയാളം)\b',
            r'\b(kannada|ಕನ್ನಡ)\b',
            r'\b(bengali|বাংলা)\b',
            r'\b(marathi|मराठी)\b',
            r'\b(gujarati|ગુજરાતી)\b',
            r'\b(punjabi|ਪੰਜਾਬੀ)\b',
            r'\bin hindi\b',
            r'\bhindi tutorial\b',
            r'\bhindi me\b',
            r'\bhindi mein\b',
        ]
        self.india_pattern = re.compile(
            '|'.join(self.india_indicators),
            re.IGNORECASE
        )

    def _parse_duration(self, duration: str) -> int:
        """Parse ISO 8601 duration to seconds"""
        # Format: PT#H#M#S or PT#M#S or PT#S
        match = re.match(
            r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?',
            duration
        )
        if not match:
            return 0

        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)

        return hours * 3600 + minutes * 60 + seconds

    def _is_short(self, duration_seconds: int) -> bool:
        """Check if video is a YouTube Short (typically under 60 seconds)"""
        return duration_seconds < MIN_VIDEO_DURATION_SECONDS

    def _is_india_content(self, title: str, description: str, channel_title: str) -> bool:
        """Check if content appears to be from India based on language indicators"""
        combined_text = f"{title} {description} {channel_title}"
        return bool(self.india_pattern.search(combined_text))

    def _get_video_details(self, video_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """Get detailed information for a list of video IDs"""
        if not video_ids:
            return {}

        details = {}

        # API allows max 50 IDs per request
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i+50]
            try:
                response = self.youtube.videos().list(
                    part='contentDetails,statistics,snippet',
                    id=','.join(batch_ids)
                ).execute()

                for item in response.get('items', []):
                    video_id = item['id']
                    content_details = item.get('contentDetails', {})
                    statistics = item.get('statistics', {})
                    snippet = item.get('snippet', {})

                    details[video_id] = {
                        'duration_seconds': self._parse_duration(
                            content_details.get('duration', 'PT0S')
                        ),
                        'view_count': int(statistics.get('viewCount', 0)),
                        'like_count': int(statistics.get('likeCount', 0)),
                        'country_code': snippet.get('defaultAudioLanguage', ''),
                        'tags': snippet.get('tags', []),
                    }
            except HttpError as e:
                print(f"Error fetching video details: {e}")

        return details

    def _get_channel_country(self, channel_id: str) -> Optional[str]:
        """Get the country of a channel"""
        try:
            response = self.youtube.channels().list(
                part='snippet',
                id=channel_id
            ).execute()

            items = response.get('items', [])
            if items:
                return items[0].get('snippet', {}).get('country')
        except HttpError:
            pass
        return None

    def search_tutorials(
        self,
        language: Optional[str] = None,
        subject: Optional[str] = None,
        max_results: int = MAX_RESULTS_PER_QUERY
    ) -> List[Dict[str, Any]]:
        """
        Search for programming tutorials on YouTube.

        Args:
            language: Programming language to search for
            subject: Programming subject/topic to search for
            max_results: Maximum number of results to return

        Returns:
            List of filtered tutorial dictionaries
        """
        # Build search query
        query_parts = []
        if language:
            query_parts.append(f"{language} programming")
        if subject:
            query_parts.append(subject)
        query_parts.append("tutorial")

        search_query = " ".join(query_parts)

        try:
            # Search for videos
            search_response = self.youtube.search().list(
                q=search_query,
                part='snippet',
                type='video',
                videoDuration='medium',  # Filter out very short videos
                relevanceLanguage='en',  # Prefer English content
                maxResults=max_results,
                order='relevance',
                publishedAfter=self._get_date_filter(),
                safeSearch='none',
                videoDefinition='high',  # Prefer HD videos
            ).execute()

            # Extract video IDs
            video_ids = [
                item['id']['videoId']
                for item in search_response.get('items', [])
            ]

            # Get detailed info for all videos
            video_details = self._get_video_details(video_ids)

            tutorials = []
            for item in search_response.get('items', []):
                video_id = item['id']['videoId']
                snippet = item['snippet']
                details = video_details.get(video_id, {})

                title = snippet.get('title', '')
                description = snippet.get('description', '')
                channel_title = snippet.get('channelTitle', '')
                channel_id = snippet.get('channelId', '')

                # Filter out Shorts
                duration = details.get('duration_seconds', 0)
                if self._is_short(duration):
                    continue

                # Filter out India content
                if self._is_india_content(title, description, channel_title):
                    continue

                # Check channel country (optional - uses extra API quota)
                # channel_country = self._get_channel_country(channel_id)
                # if channel_country in EXCLUDED_COUNTRIES:
                #     continue

                tutorial = {
                    'video_id': video_id,
                    'title': title,
                    'description': description[:500] if description else '',
                    'channel_name': channel_title,
                    'channel_id': channel_id,
                    'published_at': snippet.get('publishedAt'),
                    'duration_seconds': duration,
                    'view_count': details.get('view_count', 0),
                    'like_count': details.get('like_count', 0),
                    'thumbnail_url': snippet.get('thumbnails', {}).get(
                        'high', {}
                    ).get('url', ''),
                    'video_url': f"https://www.youtube.com/watch?v={video_id}",
                    'programming_language': language,
                    'subject': subject,
                    'country_code': details.get('country_code', ''),
                }

                tutorials.append(tutorial)

            return tutorials

        except HttpError as e:
            print(f"YouTube API error: {e}")
            return []

    def _get_date_filter(self) -> str:
        """Get the RFC 3339 formatted date for filtering"""
        from datetime import timedelta

        now = datetime.utcnow()

        if UPLOAD_DATE_FILTER == 'hour':
            delta = timedelta(hours=1)
        elif UPLOAD_DATE_FILTER == 'today':
            delta = timedelta(days=1)
        elif UPLOAD_DATE_FILTER == 'week':
            delta = timedelta(weeks=1)
        elif UPLOAD_DATE_FILTER == 'month':
            delta = timedelta(days=30)
        elif UPLOAD_DATE_FILTER == 'year':
            delta = timedelta(days=365)
        else:
            # 'any' - return a very old date
            delta = timedelta(days=365*10)

        filter_date = now - delta
        return filter_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    def scrape_all_categories(
        self,
        languages: Optional[List[str]] = None,
        subjects: Optional[List[str]] = None,
        progress_callback=None
    ) -> List[Dict[str, Any]]:
        """
        Scrape tutorials for all configured languages and subjects.

        Args:
            languages: List of programming languages (uses config if None)
            subjects: List of subjects (uses config if None)
            progress_callback: Optional callback function(current, total, message)

        Returns:
            List of all found tutorials
        """
        languages = languages or PROGRAMMING_LANGUAGES
        subjects = subjects or PROGRAMMING_SUBJECTS

        all_tutorials = []
        total_searches = len(languages) + len(subjects)
        current = 0

        # Search by language
        for lang in languages:
            current += 1
            if progress_callback:
                progress_callback(
                    current, total_searches,
                    f"Searching {lang} tutorials..."
                )

            tutorials = self.search_tutorials(language=lang)
            all_tutorials.extend(tutorials)

        # Search by subject
        for subj in subjects:
            current += 1
            if progress_callback:
                progress_callback(
                    current, total_searches,
                    f"Searching {subj} tutorials..."
                )

            tutorials = self.search_tutorials(subject=subj)
            all_tutorials.extend(tutorials)

        # Remove duplicates based on video_id
        seen_ids = set()
        unique_tutorials = []
        for tutorial in all_tutorials:
            if tutorial['video_id'] not in seen_ids:
                seen_ids.add(tutorial['video_id'])
                unique_tutorials.append(tutorial)

        return unique_tutorials
