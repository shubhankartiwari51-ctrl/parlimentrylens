from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer
import math

# --- FIX: Import models and helpers from the new utils.py file ---
# Make sure you have created 'app/utils.py'
try:
    from ..utils import (
        sentiment_analyzer,
        summarizer,
        topic_model,
        summarizer_tokenizer,
        MODEL_MAX_LENGTH,
        calculate_average_sentiment,
        chunk_and_summarize
    )
except ImportError:
    # This path is for when you are in the same directory (like 'app')
    from utils import (
        sentiment_analyzer,
        summarizer,
        topic_model,
        summarizer_tokenizer,
        MODEL_MAX_LENGTH,
        calculate_average_sentiment,
        chunk_and_summarize
    )


router = APIRouter(prefix="/text", tags=["Text Analysis"])

class TextRequest(BaseModel):
    text: str

# --- All helper functions are now in 'utils.py' ---

@router.post("/analyze")
async def analyze_text(req: TextRequest):
    try:
        content = (req.text or "").strip()
        if not content:
            raise HTTPException(status_code=400, detail="Text is required")

        # --- 1. Stronger Sentiment (Averaging) ---
        content_length = len(content)
        
        # --- THIS IS THE FIX ---
        # We must use max(1, ...) to prevent a "division by zero" error
        # on very short text.
        step = max(1, content_length // 10)
        samples = [
            content[i : i + 512] # Sentiment model limit
            for i in range(0, content_length, step)
        ]
        
        sentiments = sentiment_analyzer(samples)
        final_sentiment = calculate_average_sentiment(sentiments)

        # --- 2. Stronger Summary (Recursive) ---
        first_pass_summary = chunk_and_summarize(content, max_length=120, min_length=30)

        if len(summarizer_tokenizer.encode(first_pass_summary)) > MODEL_MAX_LENGTH:
            final_summary_text = chunk_and_summarize(first_pass_summary, max_length=250, min_length=50)
        else:
            final_summary_text = first_pass_summary
            
        # --- 3. New Feature: Key Topics ---
        candidate_labels = [
            "Politics", "Law", "Economy", "Health", "Technology", 
            "Environment", "Education", "Sports", "Business", "International Relations"
        ]
        topic_results = topic_model(final_summary_text, candidate_labels, multi_label=True)
        key_topics = [
            {"label": label, "score": score}
            for label, score in zip(topic_results["labels"], topic_results["scores"])
            if score > 0.5
        ]
        key_topics = sorted(key_topics, key=lambda x: x["score"], reverse=True)

        # --- 4. Return the new, stronger response ---
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