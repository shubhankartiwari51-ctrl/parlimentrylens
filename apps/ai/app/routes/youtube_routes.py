# C:\Users\prabh\Downloads\ParliamentLens\apps\ai\app\routes\youtube_routes.py
# (This is the UPDATED file)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    CouldNotRetrieveTranscript,
)
from urllib.parse import urlparse, parse_qs
import yt_dlp
import tempfile
import os
import re
import glob
from urllib.error import HTTPError
import math

# --- FIX: Import models and helpers from the new utils.py file ---
try:
    from ..utils import (
        sentiment_analyzer,
        summarizer,
        summarizer_tokenizer,
        MODEL_MAX_LENGTH,
        calculate_average_sentiment,
        chunk_and_summarize,
        get_topics_from_api  # <-- Import the new API function
    )
except ImportError:
    from utils import (
        sentiment_analyzer,
        summarizer,
        summarizer_tokenizer,
        MODEL_MAX_LENGTH,
        calculate_average_sentiment,
        chunk_and_summarize,
        get_topics_from_api  # <-- Import the new API function
    )

router = APIRouter(prefix="/youtube", tags=["YouTube Analysis"])

class AnalyzeReq(BaseModel):
    url: HttpUrl

# --- REMOVED all model loading and helper functions ---
# (Except for the ones specific to YouTube, which we keep)

# ----- Cookies support -----
COOKIES_PATH = os.environ.get("YT_COOKIES", os.path.join(os.getcwd(), "cookies.txt"))
COOKIES_ARG = COOKIES_PATH if os.path.exists(COOKIES_PATH) else None
print(f"Cookie file status: {'Loaded' if COOKIES_ARG else 'Not found'}")

# ----- Transcript-Fetching Helpers (Unchanged) -----
def _clean_text(t: str) -> str:
    return re.sub(r"\s+", " ", t or "").strip()

def _extract_video_id(url: str) -> str | None:
    pattern = (
        r"(?:youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/)|youtu\.be\/)"
        r"([a-zA-Z0-9_-]{11})"
    )
    match = re.search(pattern, url)
    return match.group(1) if match else None

def _read_vtt_file(path: str) -> str:
    out = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for ln in f:
            s = ln.strip()
            if not s or s.startswith("WEBVTT") or "-->" in s or s.isdigit():
                continue
            s = re.sub(r"<[^>]+>", "", s)
            if s:
                out.append(s)
    return _clean_text(" ".join(out))

def _get_text_via_yta(video_id: str) -> str:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=["en", "en-US", "en-GB"], cookies=COOKIES_ARG
        )
        text = " ".join(c.get("text", "") for c in transcript)
        if text:
            return _clean_text(text)
    except NoTranscriptFound:
        try:
            transcripts = YouTubeTranscriptApi.list_transcripts(video_id, cookies=COOKIES_ARG)
            for t in transcripts:
                if t.is_translatable:
                    t_en = t.translate("en")
                    text = " ".join(c.get("text", "") for c in t_en.fetch())
                    if text:
                        return _clean_text(text)
        except Exception:
            pass
    except Exception:
        pass
    return ""

def _get_text_via_ytdlp(url: str) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {
            "skip_download": True, "writesubtitles": True, "writeautomaticsub": True,
            "subtitlesformat": "vtt/best", "subtitleslangs": ["en", "en-US", "en-GB"],
            "quiet": True, "nocheckcertificate": True, "cookiefile": COOKIES_ARG,
            "paths": {"home": tmpdir}, "outtmpl": {"subtitle": "%(id)s.%(ext)s"},
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(url, download=True)
        except HTTPError as e:
            if getattr(e, "code", None) == 429:
                raise HTTPException(status_code=429, detail="YouTube rate-limited this IP (HTTP 429).")
            return ""
        except Exception as e:
            print(f"[yt-dlp Error]: {e}")
            return ""
        vtts = glob.glob(os.path.join(tmpdir, "*.vtt"))
        if not vtts:
            return ""
        preferred = None
        for p in vtts:
            n = os.path.basename(p).lower()
            if n.endswith(".en.vtt"): preferred = p; break
            if any(tag in n for tag in ["en-us", "en-gb", "en"]): preferred = p
        vtt_path = preferred or vtts[0]
        try:
            return _read_vtt_file(vtt_path) # <-- Corrected typo from your file
        except Exception:
            return ""

# ----- Route (Stronger Logic) -----
@router.post("/analyze")
async def analyze_youtube(req: AnalyzeReq):
    url = str(req.url)
    vid = _extract_video_id(url)
    if not vid:
        raise HTTPException(status_code=400, detail="Invalid YouTube video URL")

    text = ""
    last_error = None
    
    try:
        # --- 1. Get Transcript (Same as before) ---
        text = _get_text_via_yta(vid)
        if not text:
            text = _get_text_via_ytdlp(url)

        if not text:
            raise HTTPException(
                status_code=404,
                detail="No transcript could be fetched. This is often due to YouTube rate-limit/region blocks or subtitles being disabled. Try a different network (hotspot/VPN) or another video."
            )
        
        # --- 2. Start of "Strong Logic" (Copied from text_routes) ---
        content = text # Use transcript text as the content
        
        # Stronger Sentiment (Averaging)
        content_length = len(content)
        step = max(1, content_length // 10)
        samples = [
            content[i : i + 512] # Sentiment model limit
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
            
        # --- 3. FIX: Call the API for topics ---
        candidate_labels = [
            "Politics", "Law", "Economy", "Health", "Technology", 
            "Environment", "Education", "Sports", "Business", "International Relations"
        ]
        # This one line REPLACES the old code that loaded the giant model
        key_topics = get_topics_from_api(final_summary_text, candidate_labels)
        # ----------------------------------------

        # Return the new, stronger response
        return {
            "sentiment": final_sentiment,
            "summary": final_summary_text,
            "key_topics": key_topics[:5], # Return top 5 topics
        }

    # --- Error Handling (Same as before) ---
    except HTTPException as e:
        raise e
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        raise HTTPException(status_code=404, detail=f"Transcripts are disabled or not found: {e}")
    except CouldNotRetrieveTranscript as e:
        raise HTTPException(status_code=503, detail=f"Could not retrieve transcript: {e}")
    except HTTPError as e:
        if getattr(e, "code", None) == 429:
            raise HTTPException(status_code=429, detail="YouTube rate-limited this IP (HTTP 429).")
        raise HTTPException(status_code=502, detail=f"YouTube HTTP error: {e}")
    except Exception as e:
        print(f"Unhandled analysis error: {type(e).__name__}: {e}")
        raise HTTPException(status_code=502, detail=f"Transcript fetch failed: {type(e).__name__}: {e}")