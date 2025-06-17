import os
import logging
import google.generativeai as genai
from datetime import datetime, timezone
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiRecommendations:
    def __init__(self, api_key):
        """Initialize Gemini API with the provided API key"""
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            logger.info("Successfully configured Gemini model")
        except Exception as e:
            logger.error(f"Error configuring Gemini: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def get_recommendations(self, developer_data):
        """Get personalized recommendations using Gemini"""
        try:
            logger.info(f"Generating recommendations for developer: {developer_data.get('name', 'Unknown')}")
            
            # Format the prompt based on developer data
            prompt = f"""
            As an expert developer productivity analyst, analyze the following developer profile and provide actionable recommendations.
            
            Developer Profile:
            Name: {developer_data.get('name', 'Unknown')}
            Role: {developer_data.get('role', 'Unknown')}
            Recent Activity: {developer_data.get('recent_activity', [])}
            Skills: {developer_data.get('skills', [])}
            
            Please provide specific, actionable recommendations in the following format:
            
            <div class="recommendations-container">
                <div class="recommendation">
                    <h6>Recommendation Title</h6>
                    <p>Detailed explanation of the recommendation and why it's important.</p>
                    <ul>
                        <li>Step 1 to implement</li>
                        <li>Step 2 to implement</li>
                    </ul>
                </div>
            </div>
            
            Format each recommendation with proper HTML tags and ensure the content is clear and actionable.
            """
            
            logger.info("Sending prompt to Gemini")
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )
            logger.info("Received response from Gemini")
            
            if not response or not response.text:
                logger.error("Empty response from Gemini")
                raise Exception("Empty response from Gemini")
            
            # Parse the response into structured recommendations
            recommendations = []
            current_recommendation = None
            
            for line in response.text.split('\n'):
                if line.strip().startswith('<h6>'):
                    if current_recommendation:
                        recommendations.append(current_recommendation)
                    current_recommendation = {
                        'title': line.strip().replace('<h6>', '').replace('</h6>', ''),
                        'description': '',
                        'steps': []
                    }
                elif line.strip().startswith('<p>'):
                    if current_recommendation:
                        current_recommendation['description'] = line.strip().replace('<p>', '').replace('</p>', '')
                elif line.strip().startswith('<li>'):
                    if current_recommendation:
                        current_recommendation['steps'].append(line.strip().replace('<li>', '').replace('</li>', ''))
            
            if current_recommendation:
                recommendations.append(current_recommendation)
            
            return {
                'recommendations': recommendations,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            logger.error(traceback.format_exc())
            return {
                'recommendations': [],
                'error': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }

    def analyze_image_with_gemini(self, image_path, prompt):
        """Analyze an image using Gemini Vision"""
        try:
            logger.info(f"Analyzing image: {image_path}")
            
            # Load and process the image
            image = genai.upload_file(image_path)
            
            # Generate content with the image
            response = self.model.generate_content([prompt, image])
            
            if not response or not response.text:
                logger.error("Empty response from Gemini Vision")
                raise Exception("Empty response from Gemini Vision")
            
            return {
                'response': response.text,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            logger.error(traceback.format_exc())
            return {
                'error': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            } 