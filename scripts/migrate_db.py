import json
import os
from datetime import datetime
from mongodb_models import MongoDBManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_data():
    """Migrate existing GitLab data to MongoDB"""
    try:
        # Initialize MongoDB manager
        mongo = MongoDBManager()
        
        # Migrate recommendations
        recommendation_files = [f for f in os.listdir('.') if f.startswith('recommendations_') and f.endswith('.json')]
        for file in recommendation_files:
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    user_id = data.get('user_id', 'dev1')
                    mongo.save_recommendations(user_id, data)
                logger.info(f"Migrated recommendations from {file}")
            except Exception as e:
                logger.error(f"Error migrating {file}: {str(e)}")
        
        # Migrate GitLab metrics
        metrics_files = [f for f in os.listdir('.') if f.startswith('gitlab_metrics_') and f.endswith('.json')]
        for file in metrics_files:
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    user_id = data.get('user_id', 'dev1')
                    mongo.save_gitlab_metrics(user_id, data)
                logger.info(f"Migrated metrics from {file}")
            except Exception as e:
                logger.error(f"Error migrating {file}: {str(e)}")
        
        # Migrate telemetry data
        telemetry_files = [f for f in os.listdir('.') if f.startswith('telemetry_') and f.endswith('.json')]
        for file in telemetry_files:
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    user_id = data.get('user_id', 'dev1')
                    mongo.save_telemetry(user_id, data)
                logger.info(f"Migrated telemetry from {file}")
            except Exception as e:
                logger.error(f"Error migrating {file}: {str(e)}")
        
        logger.info("Migration completed successfully")
        
    except Exception as e:
        logger.error(f"Error during migration: {str(e)}")
    finally:
        mongo.close()

if __name__ == '__main__':
    migrate_data() 