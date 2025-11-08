# C:\Users\prabh\Downloads\ParliamentLens\apps\ai\app\routes\text_routes.py
# (This is the UPDATED file)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import math

# --- FIX: Import models and helpers from the new utils.py file ---
try:
    from ..utils import (
        sentiment_analyzer,
        summarizer,
        summarizer_tokenizer,
        MODEL_MAX_LENGTH,
        calculate_average_sentiment,
        chunk_and_summarize,
        get_topics_from_api  # <-- Import the new API function
    )
except ImportError:
    # This path is for when you are in the same directory (like 'app')
    from utils import (
        sentiment_analyzer,
        summarizer,
        summarizer_tokenizer,
        MODEL_MAX_LENGTH,
        calculate_average_sentiment,
        chunk_and_summarize,
        get_topics_from_api  # <-- Import the new API function
    )


router = APIRouter(prefix="/text", tags=["Text Analysis"])

class TextRequest(BaseModel):
    text: str

# --- REMOVED all model loading and helper functions ---

@router.post("/analyze")
async def analyze_text(req: TextRequest):
    try:
        content = (req.text or "").strip()
        if not content:
            raise HTTPException(status_code=400, detail="Text is required")

        # --- 1. Stronger Sentiment (Averaging) ---
        content_length = len(content)
        step = max(1, content_length // 10)
        samples = [
            content[i : i + 512] # Sentiment model limit
            for i in range(0, content_length, step)
        ]
        
        sentiments = sentiment_analyzer(samples)
        final_sentiment = calculate_average_sentiment(sentiments) # Use helper

        # --- 2. Stronger Summary (Recursive) ---
        first_pass_summary = chunk_and_summarize(content, max_length=120, min_length=30) # Use helper

        if len(summarizer_tokenizer.encode(first_pass_summary)) > MODEL_MAX_LENGTH:
            final_summary_text = chunk_and_summarize(first_pass_summary, max_length=250, min_length=50) # Use helper
        else:
            final_summary_text = first_pass_summary
            
        # --- 3. FIX: Call the API for topics ---
        candidate_labels = [
            "Politics", "Law", "Economy", "Health", "Technology", 
            "Environment", "Education", "Sports", "Business", "International Relations"
        ]
        # This one line REPLACES the old code that loaded the giant model
        key_topics = get_topics_from_api(final_summary_text, candidate_labels)
        # ----------------------------------------
        
        return {
            "sentiment": final_sentiment,
            "summary": final_summary_text,
            "key_topics": key_topics[:5], # Return top 5 topics
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in /text/analyze: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")