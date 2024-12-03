import os
from fastapi import FastAPI, HTTPException, Depends, Header
from schemas import TextRequest, TextResponse
from model import call_model_endpoint, call_mock_model
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Topic Prediction API")

# Retrieve the API key from the environment variable
API_KEY = os.getenv("API_KEY")  # Make sure this matches the name used in app settings

# Dependency to verify the API key
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

@app.post("/predict/", response_model=TextResponse, 
           dependencies=[Depends(verify_api_key)], response_model_exclude_none=True)
async def predict(request: TextRequest):
    try:
        logger.info(f"Received prediction request for text: {request.text}")

        # Call the Azure ML model endpoint
        response = call_model_endpoint(request.text)

        if response.error:
            logger.error(f"Model returned an error: {response.error}")
            raise HTTPException(status_code=500, detail=response.error)

        logger.info(f"Prediction successful. Response: {response}")
        return response

    except Exception as e:
        logger.exception("An unexpected error occurred.")
        raise HTTPException(status_code=500, detail=str(e))
    