from fastapi import APIRouter, HTTPException, UploadFile, File
import io
from .. import utils # <-- THE FIX

router = APIRouter(prefix="/video", tags=["Video/Audio File Analysis"])

@router.post("/analyze")
async def analyze_video_file(file: UploadFile = File(...)):
    try:
        file_data = await file.read()
        
        # --- Call API to get text ---
        content = utils.get_transcription_from_api(file_data) # <-- THE FIX
        if not content:
            raise HTTPException(status_code=400, detail="Could not extract any speech from the file.")
        
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
        raise HTTPException(status_code=500, detail=str(e))