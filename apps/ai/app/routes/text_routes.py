from fastapi import APIRouter, HTTPException
from .. import utils

router = APIRouter()

@router.post("/analyze")
async def analyze_text(request: dict):
    text = request.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Text input required")

    try:
        sentiment = utils.get_sentiment_from_api(text)
        summary = utils.get_summary_from_api(text)
        topics = utils.get_topics_from_api(summary, ["Politics", "Law", "Economy", "Health", "Technology"])
        return {
            "sentiment": sentiment,
            "summary": summary,
            "topics": topics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
