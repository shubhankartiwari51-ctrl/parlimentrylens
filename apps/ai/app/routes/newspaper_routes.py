from fastapi import APIRouter, HTTPException, UploadFile, File
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter # <-- Import more image tools
import io

# Import your helper functions from utils.py
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
     from utils import (
        sentiment_analyzer,
        summarizer,
        topic_model,
        summarizer_tokenizer,
        MODEL_MAX_LENGTH,
        calculate_average_sentiment,
        chunk_and_summarize
    )

router = APIRouter(prefix="/newspaper", tags=["Newspaper Analysis"])

# This tells Python the exact path to your Tesseract program
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


@router.post("/analyze")
async def analyze_newspaper(file: UploadFile = File(...)):
    try:
        # 1. Read the uploaded image file
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        # --- 2. NEW "STRONG" IMAGE CLEANING ---
        # Convert to grayscale
        img_gray = image.convert('L')
        
        # Increase contrast
        enhancer = ImageEnhance.Contrast(img_gray)
        img_enhanced = enhancer.enhance(2.0) # 2.0 = 2x contrast
        
        # Apply a slight sharpen filter
        img_final = img_enhanced.filter(ImageFilter.SHARPEN)
        
        # You can uncomment this line to save the cleaned image
        # and see what Tesseract is "seeing"
        # img_final.save("cleaned_image.png") 
        # ----------------------------------------

        # 3. Use Tesseract to "scan" the CLEANED image
        extracted_text = pytesseract.image_to_string(img_final, lang='eng+hin')

        content = (extracted_text or "").strip()
        if not content:
            raise HTTPException(status_code=400, detail="Could not extract any text from the image. Try a clearer, higher-contrast image.")

        # --- 4. RE-USE YOUR "STRONG" AI LOGIC ---
        content_length = len(content)
        step = max(1, content_length // 10)
        samples = [
            content[i : i + 512]
            for i in range(0, content_length, step)
        ]
        sentiments = sentiment_analyzer(samples)
        final_sentiment = calculate_average_sentiment(sentiments)

        # Stronger Summary (Recursive)
        first_pass_summary = chunk_and_summarize(content, max_length=120, min_length=30)

        if len(summarizer_tokenizer.encode(first_pass_summary)) > MODEL_MAX_LENGTH:
            final_summary_text = chunk_and_summarize(first_pass_summary, max_length=250, min_length=50)
        else:
            final_summary_text = first_pass_summary

        # Key Topics
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

        return {
            "sentiment": final_sentiment,
            "summary": final_summary_text,
            "key_topics": key_topics[:5],
        }

    except HTTPException:
        raise
    except Exception as e:
        if "Tesseract is not installed" in str(e):
            raise HTTPException(
                status_code=500, 
                detail="Tesseract OCR is not installed or not found in your system's PATH."
            )
        print(f"Error in /newspaper/analyze: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")