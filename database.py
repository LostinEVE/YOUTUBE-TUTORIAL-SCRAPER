"""Database module for storing and retrieving tutorials"""

import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
import os


class TutorialDatabase:
    def __init__(self, db_path: str = None):
        # Use persistent storage path if available (for Render deployment)
        # Otherwise use local path for development
        if db_path is None:
            if os.path.exists('/app/data'):
                db_path = '/app/data/tutorials.db'
            else:
                db_path = 'tutorials.db'
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Create tutorials table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tutorials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    channel_name TEXT,
                    channel_id TEXT,
                    published_at TEXT,
                    duration_seconds INTEGER,
                    view_count INTEGER,
                    like_count INTEGER,
                    thumbnail_url TEXT,
                    video_url TEXT,
                    programming_language TEXT,
                    subject TEXT,
                    country_code TEXT,
                    added_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    is_favorite INTEGER DEFAULT 0,
                    is_watched INTEGER DEFAULT 0
                )
            """)

            # Create index for faster queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_language 
                ON tutorials(programming_language)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_subject 
                ON tutorials(subject)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_video_id 
                ON tutorials(video_id)
            """)

            conn.commit()

    def add_tutorial(self, tutorial: Dict[str, Any]) -> bool:
        """Add a tutorial to the database. Returns True if added, False if duplicate."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO tutorials (
                        video_id, title, description, channel_name, channel_id,
                        published_at, duration_seconds, view_count, like_count,
                        thumbnail_url, video_url, programming_language, subject,
                        country_code, added_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    tutorial.get('video_id'),
                    tutorial.get('title'),
                    tutorial.get('description'),
                    tutorial.get('channel_name'),
                    tutorial.get('channel_id'),
                    tutorial.get('published_at'),
                    tutorial.get('duration_seconds'),
                    tutorial.get('view_count'),
                    tutorial.get('like_count'),
                    tutorial.get('thumbnail_url'),
                    tutorial.get('video_url'),
                    tutorial.get('programming_language'),
                    tutorial.get('subject'),
                    tutorial.get('country_code'),
                    datetime.now().isoformat()
                ))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                # Duplicate video_id
                return False

    def get_tutorials_by_language(self, language: str) -> List[Dict[str, Any]]:
        """Get all tutorials for a specific programming language"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM tutorials 
                WHERE programming_language = ?
                ORDER BY view_count DESC
            """, (language,))
            return [dict(row) for row in cursor.fetchall()]

    def get_tutorials_by_subject(self, subject: str) -> List[Dict[str, Any]]:
        """Get all tutorials for a specific subject"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM tutorials 
                WHERE subject = ?
                ORDER BY view_count DESC
            """, (subject,))
            return [dict(row) for row in cursor.fetchall()]

    def get_all_tutorials(self) -> List[Dict[str, Any]]:
        """Get all tutorials"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tutorials ORDER BY added_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    def get_categories_summary(self) -> Dict[str, Any]:
        """Get a summary of tutorials by category"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Count by language
            cursor.execute("""
                SELECT programming_language, COUNT(*) as count 
                FROM tutorials 
                WHERE programming_language IS NOT NULL
                GROUP BY programming_language
                ORDER BY count DESC
            """)
            by_language = {row[0]: row[1] for row in cursor.fetchall()}

            # Count by subject
            cursor.execute("""
                SELECT subject, COUNT(*) as count 
                FROM tutorials 
                WHERE subject IS NOT NULL
                GROUP BY subject
                ORDER BY count DESC
            """)
            by_subject = {row[0]: row[1] for row in cursor.fetchall()}

            # Total count
            cursor.execute("SELECT COUNT(*) FROM tutorials")
            total = cursor.fetchone()[0]

            return {
                'total': total,
                'by_language': by_language,
                'by_subject': by_subject
            }

    def mark_watched(self, video_id: str):
        """Mark a tutorial as watched"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tutorials SET is_watched = 1 WHERE video_id = ?",
                (video_id,)
            )
            conn.commit()

    def mark_favorite(self, video_id: str, is_favorite: bool = True):
        """Mark a tutorial as favorite"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tutorials SET is_favorite = ? WHERE video_id = ?",
                (1 if is_favorite else 0, video_id)
            )
            conn.commit()

    def delete_tutorial(self, video_id: str):
        """Delete a tutorial from the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM tutorials WHERE video_id = ?", (video_id,))
            conn.commit()

    def search_tutorials(self, query: str) -> List[Dict[str, Any]]:
        """Search tutorials by title or description"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM tutorials 
                WHERE title LIKE ? OR description LIKE ?
                ORDER BY view_count DESC
            """, (f'%{query}%', f'%{query}%'))
            return [dict(row) for row in cursor.fetchall()]
