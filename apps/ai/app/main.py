# C:\Users\prabh\Downloads\ParliamentLens\apps\ai\app\main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- Import this

# Import your routes
from .routes import text_routes, youtube_routes, newspaper_routes

app = FastAPI()

# --- THIS IS THE FIX ---
# Add this entire block to allow your website to connect
origins = [
    "http://localhost:5173",  # Your React app (Vite)
    "http://localhost:3000",  # (In case you use create-react-app)
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)
# -----------------------

# Include your routers
app.include_router(text_routes.router)
app.include_router(youtube_routes.router)
app.include_router(newspaper_routes.router)

@app.get("/")
def read_root():
    return {"message": "ParliamentLens AI API"}