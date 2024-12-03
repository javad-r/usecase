from pydantic import BaseModel, Field
from typing import List, Optional

class TextRequest(BaseModel):
    text: List[str] = Field(..., min_items=1, max_items=100, description="List of input texts for prediction.")

class TopicPrediction(BaseModel):
    input_text: str
    predicted_topics: List[str]
    decoded_topics: List[List[str]]

class TextResponse(BaseModel):
    topics: Optional[List[TopicPrediction]] = None
    error: Optional[str] = None
    