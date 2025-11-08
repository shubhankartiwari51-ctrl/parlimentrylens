from fastapi import APIRouter, HTTPException, UploadFile, File
import io

# --- Import our NEW API-only functions ---
# --- Import all helpers from utils.py ---
from utils import (
    sentiment_analyzer,
    summarizer,
    summarizer_tokenizer,
    MODEL_MAX_LENGTH,
    calculate_average_sentiment,
    chunk_and_summarize,
    get_topics_from_api,
    get_transcription_from_api # (This line is only needed in video_routes.py)
)
router = APIRouter(prefix="/video", tags=["Video/Audio File Analysis"])

@router.post("/analyze")
async def analyze_video_file(file: UploadFile = File(...)):
    try:
        file_data = await file.read()
        
        # --- Call API to get text ---
        content = get_transcription_from_api(file_data)
        if not content:
            raise HTTPException(status_code=400, detail="Could not extract any speech from the file.")
        
        # --- Call APIs for all 3 tasks ---
        final_sentiment = get_sentiment_from_api(content)
        final_summary_text = get_summary_from_api(content)
        candidate_labels = ["Politics", "Law", "Economy", "Health", "Technology"]
        key_topics = get_topics_from_api(final_summary_text, candidate_labels)
        
        return {
            "sentiment": final_sentiment,
            "summary": final_summary_text,
            "key_topics": key_topics[:5],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))