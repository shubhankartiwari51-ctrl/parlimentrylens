from fastapi import APIRouter, HTTPException, UploadFile, File
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
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

router = APIRouter(prefix="/newspaper", tags=["Newspaper Analysis"])
# We comment this out so it works on Render (Linux)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@router.post("/analyze")
async def analyze_newspaper(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        img_gray = image.convert('L')
        enhancer = ImageEnhance.Contrast(img_gray)
        img_enhanced = enhancer.enhance(2.0)
        img_final = img_enhanced.filter(ImageFilter.SHARPEN)
        
        content = pytesseract.image_to_string(img_final, lang='eng+hin')
        if not content:
            raise HTTPException(status_code=400, detail="Could not extract any text from the image.")

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