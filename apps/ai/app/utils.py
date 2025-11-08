# C:\Users\prabh\Downloads\ParliamentLens\apps\ai\app\utils.py
# (This is the NEW "API-only" file)

import requests
import os
import time

# --- Hugging Face API setup ---
# We will get this from the Render secrets
HF_TOKEN = os.environ.get("HF_TOKEN") 
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# Define all the free API "phone numbers"
API_URLS = {
    "topics": "https://api-inference.huggingface.co/models/facebook/bart-large-mnli",
    "summary": "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-6-6",
    "sentiment": "https://api-inference.huggingface.co/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    "audio": "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
}

def make_api_call(api_url, data, is_json=True):
    """
    Handles all API calls, including the 503 "model loading" error.
    """
    if not HF_TOKEN:
        print("WARNING: HF_TOKEN not set. Skipping API call.")
        return None

    try:
        # Send the request
        if is_json:
            response = requests.post(api_url, headers=headers, json=data)
        else:
            response = requests.post(api_url, headers=headers, data=data) # For audio/image files

        # If model is loading, wait 15s and try again
        if response.status_code == 503:
            print(f"Model {api_url} is loading, waiting 15 seconds...")
            time.sleep(15) 
            response = requests.post(api_url, headers=headers, json=data if is_json else data)

        if response.status_code != 200:
            print(f"API Error ({api_url}): {response.status_code} - {response.text}")
            return None
        
        return response.json()

    except Exception as e:
        print(f"API Request failed ({api_url}): {e}")
        return None

# --- NEW API Helper Functions ---

def get_transcription_from_api(file_data: bytes) -> str:
    print("Calling ASR (Whisper) API...")
    data = make_api_call(API_URLS["audio"], data=file_data, is_json=False)
    if data and "text" in data:
        return data["text"]
    return ""

def get_sentiment_from_api(text: str) -> dict:
    print("Calling Sentiment API...")
    # Cut the text to 512 tokens for this model
    data = make_api_call(API_URLS["sentiment"], data={"inputs": text[:512]})
    if data and isinstance(data, list) and data[0]:
        label = data[0].get("label", "NEUTRAL").upper()
        if label not in {"POSITIVE", "NEGATIVE", "NEUTRAL"}:
             label = {"LABEL_0": "NEGATIVE", "LABEL_1": "POSITIVE"}.get(label, "NEUTRAL")
        return {"label": label, "score": data[0].get("score", 0.0)}
    return {"label": "NEUTRAL", "score": 0.0}

def get_summary_from_api(text: str) -> str:
    print("Calling Summary API...")
    data = make_api_call(API_URLS["summary"], data={"inputs": text})
    if data and isinstance(data, list) and data[0] and "summary_text" in data[0]:
        return data[0]["summary_text"]
    return "Summary API failed or text was too short."

def get_topics_from_api(text: str, labels: list) -> list:
    print("Calling Topics API...")
    payload = {"inputs": text, "parameters": {"candidate_labels": labels, "multi_label": True}}
    data = make_api_call(API_URLS["topics"], data=payload)
    if data and "labels" in data:
        topics = [
            {"label": label, "score": score}
            for label, score in zip(data["labels"], data["scores"])
            if score > 0.5
        ]
        return sorted(topics, key=lambda x: x["score"], reverse=True)
    return []