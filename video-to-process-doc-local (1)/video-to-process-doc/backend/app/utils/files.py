import os
import uuid
from pathlib import Path
from fastapi import UploadFile

WORK_DIR = Path(os.getenv("WORK_DIR", "./data"))
WORK_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_VIDEO = {".mp4", ".mov", ".mkv", ".webm", ".avi"}
ALLOWED_AUDIO = {".mp3", ".wav", ".m4a", ".aac"}


def save_upload(file: UploadFile) -> Path:
    ext = Path(file.filename).suffix.lower()
    uid = uuid.uuid4().hex
    out = WORK_DIR / f"{uid}{ext}"
    with out.open("wb") as f:
        f.write(file.file.read())
    return out
