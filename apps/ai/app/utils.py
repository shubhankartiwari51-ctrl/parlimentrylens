# C:\Users\prabh\Downloads\ParliamentLens\apps\ai\app\utils.py
# (This is a NEW file)

from transformers import pipeline, AutoTokenizer
import math
import requests  # <-- New library
import os       # <-- New library

# --- Load only the models that fit in memory ---
try:
    # 1. Sentiment (fast)
    sentiment_analyzer = pipeline("sentiment-analysis")
    
    # 2. Summarizer (fast)
    SUMMARIZER_MODEL = "sshleifer/distilbart-cnn-6-6"
    summarizer = pipeline("summarization", model=SUMMARIZER_MODEL)

    # 4. Tokenizer for chunking (matches summarizer)
    summarizer_tokenizer = AutoTokenizer.from_pretrained(SUMMARIZER_MODEL)
    MODEL_MAX_LENGTH = summarizer.model.config.max_position_embeddings # 1024
    
    # --- 3. REMOVED the "topic_model" ---
    # We will call the API for this instead to save memory.
    
except Exception as e:
    raise RuntimeError(f"Model loading failed: {e}")

# --- NEW: Hugging Face API setup ---
HF_TOKEN = os.environ.get("HF_TOKEN") # Reads the secret from Render
TOPIC_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}


# --- NEW API Helper Function ---
def get_topics_from_api(text: str, labels: list) -> list:
    """
    Offloads the "Key Topics" task to the free Hugging Face API.
    This saves a huge amount of memory.
    """
    if not HF_TOKEN:
        print("WARNING: HF_TOKEN not set. Skipping topic analysis.")
        return []
        
    try:
        response = requests.post(
            TOPIC_API_URL, 
            headers=headers, 
            json={
                "inputs": text,
                "parameters": {"candidate_labels": labels, "multi_label": True}
            }
        )
        if response.status_code != 200:
            # If the API is busy (503 error), it's not a crash. Just return empty.
            print(f"HF API Error: {response.status_code} - {response.text}")
            return [] # Return empty on error
        
        data = response.json()
        if not isinstance(data, dict) or "labels" not in data:
             print(f"HF API returned invalid data: {data}")
             return []
             
        topics = [
            {"label": label, "score": score}
            for label, score in zip(data["labels"], data["scores"])
            if score > 0.5 # Only show topics with > 50% confidence
        ]
        return sorted(topics, key=lambda x: x["score"], reverse=True)
    except Exception as e:
        print(f"HF API Request failed: {e}")
        return []

# --- "Strong Sentiment" Helper (Unchanged) ---
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

# --- "Recursive Summarizer" Helper (Unchanged) ---
def chunk_and_summarize(text_to_summarize: str, max_length: int, min_length: int) -> str:
    try:
        tokens = summarizer_tokenizer.encode(text_to_summarize, add_special_tokens=False)
        chunk_size = MODEL_MAX_LENGTH - 50 
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