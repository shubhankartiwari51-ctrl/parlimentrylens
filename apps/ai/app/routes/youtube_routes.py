from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from youtube_transcript_api import (
    YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript
)
from urllib.parse import urlparse, parse_qs
import yt_dlp
import tempfile
import os
import re
import glob
from urllib.error import HTTPError
from .. import utils # <-- THE FIX

router = APIRouter(prefix="/youtube", tags=["YouTube Analysis"])
class AnalyzeReq(BaseModel): url: HttpUrl

# (All your helper functions _clean_text, _extract_video_id, etc. stay here)
# ...
COOKIES_CONTENT = os.environ.get("YT_COOKIES_CONTENT")
COOKIES_ARG = None
if COOKIES_CONTENT:
    try:
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as f:
            f.write(COOKIES_CONTENT); COOKIES_ARG = f.name
        print(f"Cookie file status: Loaded from secret")
    except Exception as e: print(f"Cookie file status: Failed to write secret - {e}")
else: print(f"Cookie file status: Not found (YT_COOKIES_CONTENT secret is not set)")
def _clean_text(t: str) -> str: return re.sub(r"\s+", " ", t or "").strip()
def _extract_video_id(url: str) -> str | None:
    pattern = (r"(?:youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})")
    match = re.search(pattern, url); return match.group(1) if match else None
def _read_vtt_file(path: str) -> str:
    out = [];
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for ln in f:
                s = ln.strip();
                if not s or s.startswith("WEBVTT") or "-->" in s or s.isdigit(): continue
                s = re.sub(r"<[^>]+>", "", s);
                if s: out.append(s)
    except Exception as e:
        print(f"Error reading VTT file: {e}")
        return ""
    return _clean_text(" ".join(out))
def _get_text_via_yta(video_id: str) -> str:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "en-US", "en-GB"], cookies=COOKIES_ARG)
        text = " ".join(c.get("text", "") for c in transcript);
        if text: return _clean_text(text)
    except NoTranscriptFound:
        try:
            transcripts = YouTubeTranscriptApi.list_transcripts(video_id, cookies=COOKIES_ARG)
            for t in transcripts:
                if t.is_translatable:
                    t_en = t.translate("en"); text = " ".join(c.get("text", "") for c in t_en.fetch())
                    if text: return _clean_text(text)
        except Exception: pass
    except Exception: pass
    return ""
def _get_text_via_ytdlp(url: str) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {"skip_download": True, "writesubtitles": True, "writeautomaticsub": True, "subtitlesformat": "vtt/best", "subtitleslangs": ["en", "en-US", "en-GB"], "quiet": True, "nocheckcertificate": True, "cookiefile": COOKIES_ARG, "paths": {"home": tmpdir}, "outtmpl": {"subtitle": "%(id)s.%(ext)s"},}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.extract_info(url, download=True)
        except HTTPError as e:
            if getattr(e, "code", None) == 429: raise HTTPException(status_code=429, detail="YouTube rate-limited this IP (HTTP 429).")
            return ""
        except Exception as e: print(f"[yt-dlp Error]: {e}"); return ""
        vtts = glob.glob(os.path.join(tmpdir, "*.vtt"));
        if not vtts: return ""
        preferred = None
        for p in vtts:
            n = os.path.basename(p).lower()
            if n.endswith(".en.vtt"): preferred = p; break
            if any(tag in n for tag in ["en-us", "en-gb", "en"]): preferred = p
        vtt_path = preferred or vtts[0]
        return _read_vtt_file(vtt_path)

@router.post("/analyze")
async def analyze_youtube(req: AnalyzeReq):
    url = str(req.url)
    vid = _extract_video_id(url)
    if not vid:
        raise HTTPException(status_code=400, detail="Invalid YouTube video URL")
    try:
        content = _get_text_via_yta(vid)
        if not content:
            content = _get_text_via_ytdlp(url)
        if not content:
            raise HTTPException(status_code=44, detail="No transcript could be fetched...")
        
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