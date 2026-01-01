"""Configuration for YouTube Tutorial Scraper"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure Cosmos DB Configuration
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT", "")
COSMOS_KEY = os.getenv("COSMOS_KEY", "")
COSMOS_DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME", "YouTubeTutorials")
COSMOS_CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME", "tutorials")

# Programming languages to search for
PROGRAMMING_LANGUAGES = [
    "Python",
    "JavaScript",
    "TypeScript",
    "Java",
    "C#",
    "C++",
    "Go",
    "Rust",
    "Ruby",
    "PHP",
    "Swift",
    "Kotlin",
    "SQL",
    "R",
    "Scala",
]

# Programming subjects/topics to search for
PROGRAMMING_SUBJECTS = [
    "Web Development",
    "Machine Learning",
    "Data Science",
    "Backend Development",
    "Frontend Development",
    "DevOps",
    "Cloud Computing",
    "Database",
    "API Development",
    "Mobile Development",
    "Game Development",
    "Algorithms",
    "Data Structures",
    "System Design",
    "Microservices",
    "Docker",
    "Kubernetes",
    "React",
    "Node.js",
    "Django",
    "Flask",
    "FastAPI",
    "Spring Boot",
    "REST API",
    "GraphQL",
]

# Countries to exclude (ISO 3166-1 alpha-2 codes)
EXCLUDED_COUNTRIES = ["IN"]  # India

# Minimum video duration in seconds (to filter out Shorts - typically < 60 seconds)
MIN_VIDEO_DURATION_SECONDS = 120  # 2 minutes minimum

# Maximum results per search query
MAX_RESULTS_PER_QUERY = 25

# Video upload date filter: 'any', 'hour', 'today', 'week', 'month', 'year'
UPLOAD_DATE_FILTER = "month"
