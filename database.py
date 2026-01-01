"""Database module for storing and retrieving tutorials using Azure Cosmos DB"""

from azure.cosmos import CosmosClient, PartitionKey, exceptions
from datetime import datetime
from typing import List, Optional, Dict, Any
import os
import config


class TutorialDatabase:
    def __init__(self):
        """Initialize connection to Azure Cosmos DB"""
        # Get configuration from environment variables
        endpoint = config.COSMOS_ENDPOINT
        key = config.COSMOS_KEY
        database_name = config.COSMOS_DATABASE_NAME
        container_name = config.COSMOS_CONTAINER_NAME

        if not endpoint or not key:
            raise ValueError(
                "Azure Cosmos DB credentials not configured. "
                "Please set COSMOS_ENDPOINT and COSMOS_KEY environment variables."
            )

        # Initialize Cosmos Client
        self.client = CosmosClient(endpoint, key)
        self.database_name = database_name
        self.container_name = container_name

        # Initialize database and container
        self._init_db()

    def _init_db(self):
        """Initialize the database and container with proper partitioning"""
        # Create database if it doesn't exist
        self.database = self.client.create_database_if_not_exists(
            id=self.database_name)

        # Create container with partition key
        # Using /programming_language as primary partition for even distribution
        # This allows efficient queries by language
        partition_key = PartitionKey(path="/programming_language", kind="Hash")

        # Note: offer_throughput is not specified for serverless accounts
        # Serverless accounts automatically scale based on usage
        self.container = self.database.create_container_if_not_exists(
            id=self.container_name,
            partition_key=partition_key
        )

    def add_tutorial(self, tutorial: Dict[str, Any]) -> bool:
        """
        Add a tutorial to the database. Returns True if added, False if duplicate.
        """
        try:
            # Prepare the item for Cosmos DB
            item = {
                'id': tutorial.get('video_id'),  # Use video_id as unique id
                'video_id': tutorial.get('video_id'),
                'title': tutorial.get('title'),
                'description': tutorial.get('description'),
                'channel_name': tutorial.get('channel_name'),
                'channel_id': tutorial.get('channel_id'),
                'published_at': tutorial.get('published_at'),
                'duration_seconds': tutorial.get('duration_seconds'),
                'view_count': tutorial.get('view_count'),
                'like_count': tutorial.get('like_count'),
                'thumbnail_url': tutorial.get('thumbnail_url'),
                'video_url': tutorial.get('video_url'),
                'programming_language': tutorial.get('programming_language'),
                'subject': tutorial.get('subject'),
                'country_code': tutorial.get('country_code'),
                'added_at': datetime.now().isoformat(),
                'is_favorite': False,
                'is_watched': False
            }

            # Try to create the item
            self.container.create_item(body=item)
            return True

        except exceptions.CosmosResourceExistsError:
            # Item with this id already exists
            return False
        except Exception as e:
            print(f"Error adding tutorial: {e}")
            return False

    def get_tutorials_by_language(self, language: str) -> List[Dict[str, Any]]:
        """Get all tutorials for a specific programming language"""
        query = """
            SELECT * FROM c 
            WHERE c.programming_language = @language
            ORDER BY c.view_count DESC
        """

        parameters = [{"name": "@language", "value": language}]

        try:
            items = list(self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=False  # Single partition query
            ))
            return items
        except Exception as e:
            print(f"Error querying by language: {e}")
            return []

    def get_tutorials_by_subject(self, subject: str) -> List[Dict[str, Any]]:
        """Get all tutorials for a specific subject"""
        query = """
            SELECT * FROM c 
            WHERE c.subject = @subject
            ORDER BY c.view_count DESC
        """

        parameters = [{"name": "@subject", "value": subject}]

        try:
            items = list(self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True  # Cross-partition query
            ))
            return items
        except Exception as e:
            print(f"Error querying by subject: {e}")
            return []

    def get_all_tutorials(self) -> List[Dict[str, Any]]:
        """Get all tutorials"""
        query = "SELECT * FROM c ORDER BY c.added_at DESC"

        try:
            items = list(self.container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            return items
        except Exception as e:
            print(f"Error getting all tutorials: {e}")
            return []

    def get_categories_summary(self) -> Dict[str, Any]:
        """Get a summary of tutorials by category"""
        try:
            # Count by language
            language_query = """
                SELECT c.programming_language, COUNT(1) as count
                FROM c
                WHERE IS_DEFINED(c.programming_language)
                GROUP BY c.programming_language
            """
            by_language = {}
            for item in self.container.query_items(
                query=language_query,
                enable_cross_partition_query=True
            ):
                by_language[item['programming_language']] = item['count']

            # Count by subject
            subject_query = """
                SELECT c.subject, COUNT(1) as count
                FROM c
                WHERE IS_DEFINED(c.subject)
                GROUP BY c.subject
            """
            by_subject = {}
            for item in self.container.query_items(
                query=subject_query,
                enable_cross_partition_query=True
            ):
                by_subject[item['subject']] = item['count']

            # Total count
            total_query = "SELECT VALUE COUNT(1) FROM c"
            total = list(self.container.query_items(
                query=total_query,
                enable_cross_partition_query=True
            ))[0]

            return {
                'total': total,
                'by_language': by_language,
                'by_subject': by_subject
            }
        except Exception as e:
            print(f"Error getting categories summary: {e}")
            return {'total': 0, 'by_language': {}, 'by_subject': {}}

    def mark_watched(self, video_id: str):
        """Mark a tutorial as watched"""
        try:
            # Read the item first to get partition key
            item = self.container.read_item(
                item=video_id,
                partition_key=self._get_partition_key(video_id)
            )

            # Update the item
            item['is_watched'] = True
            self.container.replace_item(item=item['id'], body=item)

        except exceptions.CosmosResourceNotFoundError:
            print(f"Tutorial {video_id} not found")
        except Exception as e:
            print(f"Error marking as watched: {e}")

    def mark_favorite(self, video_id: str, is_favorite: bool = True):
        """Mark a tutorial as favorite"""
        try:
            # Read the item first to get partition key
            item = self.container.read_item(
                item=video_id,
                partition_key=self._get_partition_key(video_id)
            )

            # Update the item
            item['is_favorite'] = is_favorite
            self.container.replace_item(item=item['id'], body=item)

        except exceptions.CosmosResourceNotFoundError:
            print(f"Tutorial {video_id} not found")
        except Exception as e:
            print(f"Error marking as favorite: {e}")

    def delete_tutorial(self, video_id: str):
        """Delete a tutorial from the database"""
        try:
            self.container.delete_item(
                item=video_id,
                partition_key=self._get_partition_key(video_id)
            )
        except exceptions.CosmosResourceNotFoundError:
            print(f"Tutorial {video_id} not found")
        except Exception as e:
            print(f"Error deleting tutorial: {e}")

    def search_tutorials(self, query: str) -> List[Dict[str, Any]]:
        """Search tutorials by title or description"""
        search_query = """
            SELECT * FROM c 
            WHERE CONTAINS(LOWER(c.title), LOWER(@query))
               OR CONTAINS(LOWER(c.description), LOWER(@query))
            ORDER BY c.view_count DESC
        """

        parameters = [{"name": "@query", "value": query}]

        try:
            items = list(self.container.query_items(
                query=search_query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))
            return items
        except Exception as e:
            print(f"Error searching tutorials: {e}")
            return []

    def _get_partition_key(self, video_id: str) -> str:
        """
        Get the partition key value for a given video_id.
        This requires reading the item to get its programming_language.
        """
        # For point operations, we need the partition key
        # We'll query to find it
        query = "SELECT c.programming_language FROM c WHERE c.id = @video_id"
        parameters = [{"name": "@video_id", "value": video_id}]

        try:
            results = list(self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))
            if results:
                return results[0]['programming_language']
        except Exception as e:
            print(f"Error getting partition key: {e}")

        return ""
