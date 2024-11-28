import requests
import os
from dotenv import load_dotenv
from schemas import TextResponse
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()  # Load environment variables from .env file

AZURE_ML_ENDPOINT = os.getenv("AZURE_ML_ENDPOINT")
# AZURE_ML_API_KEY = os.getenv("AZURE_ML_API_KEY")

def call_model_endpoint(text: str) -> TextResponse:
    payload = {"data": text}
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {AZURE_ML_API_KEY}"}

    try:
        response = requests.post(AZURE_ML_ENDPOINT, json=payload, headers=headers)

        if response.status_code == 200:
            return TextResponse(topics=response.json())
        else:
            return TextResponse(topics=None, error=f"Error: {response.status_code}, {response.text}")

    except Exception as e:
        return TextResponse(error=str(e))

    
    
def call_mock_model(text: str) -> TextResponse:
    try:
        topics = ['Soccer', 'Food', 'StockMarket', 'Travel', 'Fashion', 'Technology', 'Music', 'Art']
        probabilities = {topic: round(random.random(), 2) for topic in topics}
        
        sorted_topics = dict(sorted(probabilities.items(), key=lambda x: x[1], reverse=True))
        
        return TextResponse(topics=sorted_topics)  
    except Exception as e:
        return TextResponse(error=f"Error: Failed to use mock model. Details: {str(e)}")