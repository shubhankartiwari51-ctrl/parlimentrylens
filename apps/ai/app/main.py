from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ Import routers correctly
from app.routes import text_routes, youtube_routes, newspaper_routes

app = FastAPI(title="ParliamentLens AI API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://parlimentrylens.vercel.app",
    "https://parlimentrylens.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Make sure routers are included with the right prefix
app.include_router(text_routes.router, prefix="/text", tags=["Text Analysis"])
app.include_router(youtube_routes.router, prefix="/youtube", tags=["YouTube Analysis"])
app.include_router(newspaper_routes.router, prefix="/newspaper", tags=["Newspaper Analysis"])

@app.get("/")
def root():
    return {"message": "ParliamentLens AI API is running successfully 🚀"}
