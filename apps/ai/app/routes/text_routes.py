from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# --- Import our NEW API-only functions ---
try:
    from ..utils import (
        get_sentiment_from_api,
        get_summary_from_api,
        get_topics_from_api
    )
except ImportError:
    from utils import (
        get_sentiment_from_api,
        get_summary_from_api,
        get_topics_from_api
    )

router = APIRouter(prefix="/text", tags=["Text Analysis"])

class TextRequest(BaseModel):
    text: str

@router.post("/analyze")
async def analyze_text(req: TextRequest):
    try:
        content = (req.text or "").strip()
        if not content:
            raise HTTPException(status_code=400, detail="Text is required")

        # --- Call APIs for all 3 tasks ---
        final_sentiment = get_sentiment_from_api(content)
        final_summary_text = get_summary_from_api(content)
        
        candidate_labels = [
            "Politics", "Law", "Economy", "Health", "Technology", 
            "Environment", "Education", "Sports", "Business", "International Relations"
        ]
        key_topics = get_topics_from_api(final_summary_text, candidate_labels)
        
        return {
            "sentiment": final_sentiment,
            "summary": final_summary_text,
            "key_topics": key_topics[:5],
        }
        
    except Exception as e:
        print(f"Error in /text/analyze: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")