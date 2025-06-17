import google.generativeai as genai
import os
from config import GEMINI_API_KEY
from datetime import datetime, timezone
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Use the correct model from the article
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    logger.info("Successfully configured Gemini model")
except Exception as e:
    logger.error(f"Error configuring Gemini: {str(e)}")
    logger.error(traceback.format_exc())

def get_adk_insights(developer_data):
    """Get insights using Gemini"""
    try:
        logger.info(f"Generating insights for developer: {developer_data.get('name')}")
        
        # Format the prompt based on developer data
        prompt = f"""
        As an expert developer productivity analyst, analyze the following developer profile and provide actionable insights.
        
        Developer Profile:
        Name: {developer_data.get('name', 'Unknown')}
        Role: {developer_data.get('role', 'Unknown')}
        Recent Activity: {developer_data.get('recent_activity', [])}
        Skills: {developer_data.get('skills', [])}
        
        Please provide a detailed analysis in the following HTML format:

        <div class="insights-container">
            <div class="section">
                <h6>Current Productivity Analysis</h6>
                <div class="content">
                    <h6>Key Strengths</h6>
                    <ul>
                        <li>Strength 1 with detailed explanation</li>
                        <li>Strength 2 with detailed explanation</li>
                    </ul>
                    <h6>Recent Achievements</h6>
                    <ul>
                        <li>Achievement 1 with impact</li>
                        <li>Achievement 2 with impact</li>
                    </ul>
                </div>
            </div>

            <div class="section">
                <h6>Areas for Improvement</h6>
                <div class="content">
                    <div class="improvement-item">
                        <h6>Area 1</h6>
                        <p>Detailed explanation of why this area needs attention</p>
                        <p>Impact of improvement</p>
                    </div>
                    <div class="improvement-item">
                        <h6>Area 2</h6>
                        <p>Detailed explanation of why this area needs attention</p>
                        <p>Impact of improvement</p>
                    </div>
                </div>
            </div>

            <div class="section">
                <h6>Specific Recommendations</h6>
                <div class="content">
                    <div class="recommendation">
                        <h6>Recommendation 1</h6>
                        <p>Detailed steps to implement</p>
                        <ul>
                            <li>Step 1</li>
                            <li>Step 2</li>
                        </ul>
                    </div>
                    <div class="recommendation">
                        <h6>Recommendation 2</h6>
                        <p>Detailed steps to implement</p>
                        <ul>
                            <li>Step 1</li>
                            <li>Step 2</li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="section">
                <h6>Learning Resources</h6>
                <div class="content">
                    <div class="resource-category">
                        <h6>Courses & Tutorials</h6>
                        <ul>
                            <li>Resource 1 with link</li>
                            <li>Resource 2 with link</li>
                        </ul>
                    </div>
                    <div class="resource-category">
                        <h6>Communities & Forums</h6>
                        <ul>
                            <li>Community 1 with link</li>
                            <li>Community 2 with link</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        Please analyze the developer profile and provide insights following this exact HTML structure. Use only h6 tags for all headings. Ensure all content is properly formatted with appropriate HTML tags and no special characters or emojis. Include specific, actionable recommendations and real examples where possible.
        """
        
        logger.info("Sending prompt to Gemini")
        # Get response from Gemini with basic configuration
        response = model.generate_content(
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
            
        return {
            'insights': response.text,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting insights: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            'insights': f"Unable to generate insights at this time. Error: {str(e)}",
            'timestamp': datetime.now(timezone.utc).isoformat()
        } 