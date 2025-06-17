"""
Configuration settings for the application
"""

import os

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_API_VERSION = "v1beta"
GEMINI_MODEL_NAME = "gemini-2.0-flash"
GEMINI_API_BASE_URL = f"https://generativelanguage.googleapis.com/{GEMINI_API_VERSION}/models/{GEMINI_MODEL_NAME}:generateContent"

# API Request Headers
API_HEADERS = {
    'Content-Type': 'application/json'
}

# Default API Request Payload Structure
DEFAULT_PAYLOAD = {
    "contents": [
        {
            "parts": [
                {
                    "text": ""
                }
            ]
        }
    ]
} 