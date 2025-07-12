from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL

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
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best',
            'outtmpl': '/tmp/%(title)s.%(ext)s'  # Save file to /tmp directory
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'video')
            return {"message": f"✅ Downloaded video: {title}"}

    except Exception as e:
        return {"error": str(e)}
