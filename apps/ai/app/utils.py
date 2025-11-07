# C:\Users\prabh\Downloads\ParliamentLens\apps\ai\app\utils.py
# (This is a NEW file)

from transformers import pipeline, AutoTokenizer
import math

# --- Load all models ONCE for all files to share ---
try:
    # 1. Sentiment (fast)
    sentiment_analyzer = pipeline("sentiment-analysis")
    
    # 2. Summarizer (fast)
    SUMMARIZER_MODEL = "sshleifer/distilbart-cnn-6-6"
    summarizer = pipeline("summarization", model=SUMMARIZER_MODEL)
    
    # 3. Topic model (for the "3-section" feel)
    topic_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    # 4. Tokenizer for chunking (matches summarizer)
    summarizer_tokenizer = AutoTokenizer.from_pretrained(SUMMARIZER_MODEL)
    # Get model's max size (usually 1024)
    MODEL_MAX_LENGTH = summarizer.model.config.max_position_embeddings # 1024
    
except Exception as e:
    raise RuntimeError(f"Model loading failed: {e}")


# --- "Strong Sentiment" Helper ---
def calculate_average_sentiment(sentiments: list) -> dict:
    if not sentiments:
        return {"label": "NEUTRAL", "score": 0.0}
    total_score = 0
    for sent in sentiments:
        score = sent["score"]
        if sent["label"] == "NEGATIVE":
            score = -score
        total_score += score
    avg_score = total_score / len(sentiments)
    final_label = "NEUTRAL"
    if avg_score > 0.15:
        final_label = "POSITIVE"
    elif avg_score < -0.15:
        final_label = "NEGATIVE"
    return {"label": final_label, "score": abs(avg_score)}

# --- "Recursive Summarizer" Helper ---
def chunk_and_summarize(text_to_summarize: str, max_length: int, min_length: int) -> str:
    """
    Handles text of any length by chunking it before sending to the summarizer.
    """
    try:
        tokens = summarizer_tokenizer.encode(text_to_summarize, add_special_tokens=False)
        chunk_size = MODEL_MAX_LENGTH - 50 # Give 50 tokens of buffer
        chunks = [
            tokens[i : i + chunk_size]
            for i in range(0, len(tokens), chunk_size)
        ]
        text_chunks = [
            summarizer_tokenizer.decode(chunk, skip_special_tokens=True)
            for chunk in chunks
        ]
        if not text_chunks:
            return ""
        summaries = summarizer(
            text_chunks, max_length=max_length, min_length=min_length, do_sample=False
        )
        return " ".join([s["summary_text"] for s in summaries])
    except Exception as e:
        print(f"Error during chunking/summarizing: {e}")
        return ""