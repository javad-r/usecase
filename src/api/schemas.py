from pydantic import BaseModel, Field
from typing import Dict
from typing import Optional

class TextRequest(BaseModel):
    text: str= Field(..., min_length=5, max_length=1000)

class TextResponse(BaseModel):
    topics: Optional[Dict[str, float]]
    error: Optional[str] = None