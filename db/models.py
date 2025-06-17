from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.server_api import ServerApi
from datetime import datetime, timezone
import logging
import os
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional
from bson import ObjectId
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

class MongoDBManager:
    def __init__(self):
        """Initialize MongoDB connection"""
        try:
            # Get MongoDB URI from environment variable
            mongo_uri = os.getenv('MONGODB_URI')
            if not mongo_uri:
                raise ValueError("MONGODB_URI environment variable is not set")
                
            self.client = MongoClient(mongo_uri, server_api=ServerApi('1'))
            
            # Send a ping to confirm successful connection
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB!")
            
            self.db = self.client['gitlab_analytics']
            
            # Initialize collections
            self.users = self.db['users']
            self.achievements = self.db['achievements']
            self.gitlab_metrics = self.db['gitlab_metrics']
            self.recommendations = self.db['recommendations']
            self.telemetry = self.db['telemetry']
            
            # Drop existing indexes to avoid conflicts
            self._drop_indexes()
            
            # Create indexes
            self._create_indexes()
            
            # Initialize default data if collections are empty
            self._initialize_default_data()
            
            logger.info("MongoDB connection initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing MongoDB: {str(e)}")
            raise
    
    def _drop_indexes(self):
        """Drop existing indexes"""
        try:
            self.users.drop_indexes()
            self.achievements.drop_indexes()
            self.gitlab_metrics.drop_indexes()
            self.recommendations.drop_indexes()
            self.telemetry.drop_indexes()
            logger.info("Dropped existing indexes")
        except Exception as e:
            logger.error(f"Error dropping indexes: {str(e)}")
    
    def _create_indexes(self):
        """Create indexes for collections"""
        try:
            # Users collection
            self.users.create_index([('user_id', ASCENDING)], unique=True)
            
            # GitLab metrics collection
            self.gitlab_metrics.create_index([('user_id', ASCENDING), ('timestamp', DESCENDING)])
            
            # Recommendations collection
            self.recommendations.create_index([('user_id', ASCENDING), ('timestamp', DESCENDING)])
            
            # Telemetry collection
            self.telemetry.create_index([('user_id', ASCENDING), ('timestamp', DESCENDING)])
            
            # Achievements collection - handle null achievement_id
            self.achievements.create_index([
                ('user_id', ASCENDING),
                ('achievement_id', ASCENDING)
            ], sparse=True)  # Use sparse index to handle null values
            
            logger.info("Created MongoDB indexes")
            
        except Exception as e:
            logger.error(f"Error creating indexes: {str(e)}")
    
    def _initialize_default_data(self):
        """Initialize default data if collections are empty"""
        try:
            # Initialize users if empty
            if self.users.count_documents({}) == 0:
                default_users = [
                    {'user_id': 'dev1', 'name': 'Developer 1', 'role': 'developer'},
                    {'user_id': 'dev2', 'name': 'Developer 2', 'role': 'developer'},
                    {'user_id': 'admin', 'name': 'Admin User', 'role': 'admin'}
                ]
                self.users.insert_many(default_users)
                logger.info("Initialized default users")
            
            # Initialize achievements if empty
            if self.achievements.count_documents({}) == 0:
                default_achievements = [
                    {
                        'achievement_id': 'first_commit',
                        'name': 'First Commit',
                        'description': 'Made your first commit',
                        'points': 10,
                        'category': 'development'
                    },
                    {
                        'achievement_id': 'code_review',
                        'name': 'Code Reviewer',
                        'description': 'Completed 10 code reviews',
                        'points': 20,
                        'category': 'collaboration'
                    }
                ]
                self.achievements.insert_many(default_achievements)
                logger.info("Initialized default achievements")
            
        except Exception as e:
            logger.error(f"Error initializing default data: {str(e)}")
    
    def get_all_users(self):
        """Get all users"""
        try:
            return list(self.users.find({}, {'_id': 0}))
        except Exception as e:
            logger.error(f"Error getting users: {str(e)}")
            return []
    
    def get_user_achievements(self, user_id):
        """Get user achievements"""
        try:
            # Get all achievements and user's earned achievements
            all_achievements = list(self.achievements.find({}, {'_id': 0}))
            user_achievements = list(self.db['user_achievements'].find(
                {'user_id': user_id},
                {'_id': 0}
            ))
            
            # Combine achievements with user progress
            for achievement in all_achievements:
                achievement['earned'] = any(
                    ua['achievement_id'] == achievement['achievement_id']
                    for ua in user_achievements
                )
            
            return all_achievements
            
        except Exception as e:
            logger.error(f"Error getting user achievements: {str(e)}")
            return []
    
    def get_latest_gitlab_metrics(self, user_id):
        """Get latest GitLab metrics for user"""
        try:
            return self.gitlab_metrics.find_one(
                {'user_id': user_id},
                sort=[('timestamp', DESCENDING)],
                projection={'_id': 0}
            )
        except Exception as e:
            logger.error(f"Error getting GitLab metrics: {str(e)}")
            return None
    
    def get_latest_recommendations(self, user_id):
        """Get latest recommendations for user"""
        try:
            return self.recommendations.find_one(
                {'user_id': user_id},
                sort=[('timestamp', DESCENDING)],
                projection={'_id': 0}
            )
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            return None
    
    def get_telemetry_data(self, user_id):
        """Get telemetry data for user"""
        try:
            return self.telemetry.find_one(
                {'user_id': user_id},
                sort=[('timestamp', DESCENDING)],
                projection={'_id': 0}
            )
        except Exception as e:
            logger.error(f"Error getting telemetry data: {str(e)}")
            return None
    
    def save_gitlab_metrics(self, user_id, metrics):
        """Save GitLab metrics"""
        try:
            metrics['user_id'] = user_id
            metrics['timestamp'] = datetime.now(timezone.utc).isoformat()
            # Convert to JSON-serializable format
            metrics_json = json.loads(json.dumps(metrics, cls=DateTimeEncoder))
            self.gitlab_metrics.insert_one(metrics_json)
            logger.info(f"Saved GitLab metrics for user {user_id}")
        except Exception as e:
            logger.error(f"Error saving GitLab metrics: {str(e)}")
    
    def save_recommendations(self, user_id, recommendations):
        """Save recommendations"""
        try:
            recommendations['user_id'] = user_id
            recommendations['timestamp'] = datetime.now(timezone.utc).isoformat()
            # Convert to JSON-serializable format
            recommendations_json = json.loads(json.dumps(recommendations, cls=DateTimeEncoder))
            self.recommendations.insert_one(recommendations_json)
            logger.info(f"Saved recommendations for user {user_id}")
        except Exception as e:
            logger.error(f"Error saving recommendations: {str(e)}")
    
    def save_telemetry(self, user_id, telemetry):
        """Save telemetry data"""
        try:
            telemetry['user_id'] = user_id
            telemetry['timestamp'] = datetime.now(timezone.utc).isoformat()
            # Convert to JSON-serializable format
            telemetry_json = json.loads(json.dumps(telemetry, cls=DateTimeEncoder))
            self.telemetry.insert_one(telemetry_json)
            logger.info(f"Saved telemetry for user {user_id}")
        except Exception as e:
            logger.error(f"Error saving telemetry: {str(e)}")
    
    def close(self):
        """Close MongoDB connection"""
        try:
            self.client.close()
            logger.info("MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {str(e)}")

def main():
    # Test MongoDB connection
    mongo_manager = MongoDBManager()
    
    # Test user data
    user_data = {
        "user_id": "test_user",
        "name": "Test User",
        "email": "test@example.com"
    }
    
    # Save user
    mongo_manager.save_user(user_data)
    
    # Get user
    user = mongo_manager.get_user("test_user")
    print(f"User: {user}")
    
    # Close connection
    mongo_manager.close()

if __name__ == "__main__":
    main() 