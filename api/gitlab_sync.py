from datetime import datetime, timedelta
import logging
from .gitlab_api import GitLabAPI
from db.models import MongoDBManager
import schedule
import time
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, timedelta):
            return str(obj)
        return super().default(obj)

class GitLabSync:
    def __init__(self):
        self.gitlab_api = GitLabAPI()
        self.mongo_manager = MongoDBManager()
    
    def sync_all_data(self):
        """Sync all GitLab data to MongoDB"""
        try:
            logger.info("Starting GitLab data sync...")
            
            # Get all users
            users = self.mongo_manager.get_all_users()
            
            for user in users:
                user_id = user['user_id']
                logger.info(f"Syncing data for user: {user_id}")
                
                try:
                    # Get GitLab metrics
                    metrics = self.gitlab_api.get_developer_metrics(user_id)
                    if metrics:
                        # Convert to JSON-serializable format
                        metrics_json = json.loads(json.dumps(metrics, cls=DateTimeEncoder))
                        self.mongo_manager.save_gitlab_metrics(user_id, metrics_json)
                        logger.info(f"Saved metrics for user {user_id}")
                    
                    # Get recommendations from Gemini
                    recommendations = self.get_gemini_recommendations(metrics_json if metrics else None)
                    if recommendations:
                        # Ensure recommendations are JSON-serializable
                        recommendations_json = json.loads(json.dumps(recommendations, cls=DateTimeEncoder))
                        self.mongo_manager.save_recommendations(user_id, recommendations_json)
                        logger.info(f"Saved recommendations for user {user_id}")
                    
                    # Get telemetry data
                    telemetry = self.get_telemetry_data(user_id)
                    if telemetry:
                        # Convert to JSON-serializable format
                        telemetry_json = json.loads(json.dumps(telemetry, cls=DateTimeEncoder))
                        self.mongo_manager.save_telemetry(user_id, telemetry_json)
                        logger.info(f"Saved telemetry for user {user_id}")
                
                except Exception as e:
                    logger.error(f"Error processing user {user_id}: {str(e)}")
                    continue
            
            logger.info("GitLab data sync completed successfully")
            
        except Exception as e:
            logger.error(f"Error during GitLab sync: {str(e)}")
    
    def get_gemini_recommendations(self, metrics):
        """Get recommendations from Gemini API"""
        try:
            if not metrics:
                logger.warning("No metrics provided for recommendations")
                return None
                
            from ai.recommendations import GeminiRecommendations
            gemini = GeminiRecommendations("AIzaSyCBQSpRAR1Ua-nrTd_hAg2ohc195ceNhBk")
            recommendations = gemini.get_recommendations(metrics)
            
            if recommendations:
                # Add timestamp to recommendations
                recommendations['timestamp'] = datetime.utcnow().isoformat()
                return recommendations
            return None
            
        except Exception as e:
            logger.error(f"Error getting Gemini recommendations: {str(e)}")
            return None
    
    def get_telemetry_data(self, user_id):
        """Get telemetry data for user"""
        try:
            from utils.data_generator import get_telemetry_data
            telemetry = get_telemetry_data(user_id)
            
            if telemetry:
                # Add timestamp to telemetry
                telemetry['timestamp'] = datetime.utcnow().isoformat()
                return telemetry
            return None
            
        except Exception as e:
            logger.error(f"Error getting telemetry data: {str(e)}")
            return None

def run_sync():
    """Run the sync process"""
    sync = GitLabSync()
    sync.sync_all_data()

def schedule_sync():
    """Schedule daily sync"""
    # Run initial sync
    run_sync()
    
    # Schedule daily sync at midnight
    schedule.every().day.at("00:00").do(run_sync)
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except Exception as e:
            logger.error(f"Error in schedule loop: {str(e)}")
            time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    schedule_sync() 