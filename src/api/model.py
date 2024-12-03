import requests
import os
from dotenv import load_dotenv
from schemas import TextResponse, TopicPrediction
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Azure ML endpoint and API key
AZURE_ML_ENDPOINT = os.getenv("AZURE_ML_ENDPOINT")
AZURE_ML_API_KEY = os.getenv("AZURE_ML_API_KEY")

def call_model_endpoint(texts: list) -> TextResponse:
    """
    Calls the Azure ML model endpoint with the provided texts.

    Args:
        texts (list): List of input texts.

    Returns:
        TextResponse: Response with topics or error.
    """
    payload = {"text": texts}  # Request payload
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AZURE_ML_API_KEY}",
    }

    try:
        logger.info(f"Calling Azure ML endpoint: {AZURE_ML_ENDPOINT}")
        response = requests.post(AZURE_ML_ENDPOINT, json=payload, headers=headers)

        if response.status_code == 200:
            # Parse successful response
            logger.info("Model response received successfully.")
            response_json = response.json()
            
            # Map the response to the schema
            topics = [
                TopicPrediction(
                    input_text=item["input_text"],
                    predicted_topics=item["predicted_topics"],
                    decoded_topics=item["decoded_topics"]
                )
                for item in response_json
            ]
            return TextResponse(topics=topics)
        else:
            # Log and return error response
            logger.error(
                f"Error response from model: {response.status_code}, {response.text}"
            )
            return TextResponse(
                topics=None, error=f"Error: {response.status_code}, {response.text}"
            )
    except Exception as e:
        # Log exceptions
        logger.exception("Exception occurred while calling the model endpoint.")
        return TextResponse(topics=None, error=str(e))
    
    
def call_mock_model(text: str) -> TextResponse:
    try:
        topics = ['Soccer', 'Food', 'StockMarket', 'Travel', 'Fashion', 'Technology', 'Music', 'Art']
        probabilities = {topic: round(random.random(), 2) for topic in topics}
        
        sorted_topics = dict(sorted(probabilities.items(), key=lambda x: x[1], reverse=True))
        
        return TextResponse(topics=sorted_topics)  
    except Exception as e:
        return TextResponse(error=f"Error: Failed to use mock model. Details: {str(e)}")