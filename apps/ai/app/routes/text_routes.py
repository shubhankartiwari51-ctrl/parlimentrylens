from fastapi import APIRouter, HTTPException, Request
from .. import utils

router = APIRouter()

@router.post("/analyze")
async def analyze_text(request: Request):
    try:
        # Try to parse incoming JSON safely
        body = await request.json()

        # The frontend might send either a dict {"text": "..."} or a plain string
        if isinstance(body, dict):
            text = body.get("text", "")
        elif isinstance(body, list):
            text = " ".join(body)
        else:
            text = str(body)

        if not text.strip():
            raise HTTPException(status_code=400, detail="Text input is empty.")

        # --- Call your utils functions ---
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
