from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import math
from .. import utils # <-- THE FIX

router = APIRouter(prefix="/text", tags=["Text Analysis"])
class TextRequest(BaseModel): text: str

@router.post("/analyze")
async def analyze_text(req: TextRequest):
    try:
        content = (req.text or "").strip()
        if not content:
            raise HTTPException(status_code=400, detail="Text is required")

        # --- Call APIs for all 3 tasks ---
        final_sentiment = utils.get_sentiment_from_api(content) # <-- THE FIX
        final_summary_text = utils.get_summary_from_api(content) # <-- THE FIX
        
        candidate_labels = ["Politics", "Law", "Economy", "Health", "Technology"]
        key_topics = utils.get_topics_from_api(final_summary_text, candidate_labels) # <-- THE FIX
        
        return {
            "sentiment": final_sentiment,
            "summary": final_summary_text,
            "key_topics": key_topics[:5],
        }
    except Exception as e:
        print(f"Error in /text/analyze: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")