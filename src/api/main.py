from fastapi import FastAPI, HTTPException
from schemas import TextRequest, TextResponse
from model import call_model_endpoint, call_mock_model
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Topic prediction API")

def get_model(text):
    # return call_model_endpoint
    return call_mock_model(text)

@app.post("/predict/", response_model=TextResponse, response_model_exclude_none=True)
async def predict(request: TextRequest):
    try:
        response = get_model(request.text)
        logger.info(f'Received prediction request for text: {request.text}...')
        
        if response.error:
            logger.error(f'Model returned an error: {response.error}')
            raise HTTPException(status_code=500, detail=response.error)
        
        logger.info('Prediction successful')
        
        logger.info(f"Response to be returned: {response}")
        return response
    
    except Exception as e:
        logger.exception('An unexpected error occurred')
        raise HTTPException(status_code=500, detail=str(e))