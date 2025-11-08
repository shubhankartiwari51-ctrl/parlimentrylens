# C:\Users\prabh\Downloads\ParliamentLens\apps\ai\app\main.py
import os, sys
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your routes
from .routes import text_routes, youtube_routes, newspaper_routes

app = FastAPI(title="ParliamentLens AI API")

# ✅ Updated CORS configuration
origins = [
    "http://localhost:5173",                # Local Vite dev
    "http://127.0.0.1:5173",                # Local fallback
    "http://localhost:3000",                # In case of CRA
    "https://parliamentylens.vercel.app",   # Your frontend on Vercel
    "https://parliamentylens.onrender.com"  # Your backend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],   # Allow all headers
)

app.include_router(text_routes.router, prefix="/text", tags=["Text Analysis"])
app.include_router(youtube_routes.router, prefix="/youtube", tags=["YouTube Analysis"])
app.include_router(newspaper_routes.router, prefix="/newspaper", tags=["Newspaper Analysis"])

print("✅ All routers loaded successfully")

@app.get("/")
def read_root():
    return {"message": "ParliamentLens AI API is running successfully 🚀"}
