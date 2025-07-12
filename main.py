from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL
from fastapi.responses import StreamingResponse
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "✅ GoGrabify Python Backend is Running"}

@app.get("/download")
def download_video(url: str):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '-',
        'quiet': True
    }

    buffer = io.BytesIO()

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', 'video').replace(" ", "_")
        ydl.download([url])

    return {"message": f"Downloaded video: {title}"}
