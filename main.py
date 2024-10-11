import os
import logging
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from o1_preview import o1_preview_extraction
from dotenv import load_dotenv

load_dotenv()       

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
from config import settings

app = FastAPI()

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class ChatResponse(BaseModel):
    message: str

class ProductSuggestion(BaseModel):
    name: str
    category: str
    price: str
    description: str
    productUrl: str
    graphicUrl: str

class Location(BaseModel):
    name: str
    address: str

class O1PreviewResponse(BaseModel):
    suggestions: List[ProductSuggestion]
    locations: List[Location]

@app.post("/process-chat", response_model=dict)
@limiter.limit("20/minute")
async def process_chat(chat_response: ChatResponse, request: Request):
    try:
        logger.info(f"Processing chat: {chat_response.message}")
        o1_preview_response, chat_reply = await o1_preview_extraction(chat_response.message)
        
        return {
            "chat_response": chat_reply,
            "products": [product.dict() for product in o1_preview_response.suggestions],
            "locations": [location.dict() for location in o1_preview_response.locations]
        }
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))