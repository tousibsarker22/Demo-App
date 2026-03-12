from fastapi import APIRouter, UploadFile, HTTPException
from ..utils.files import save_upload
from ..utils.audio import extract_audio
from ..services.transcription import transcribe_with_azure, clean_transcript

router = APIRouter(prefix="/transcribe", tags=["transcribe"])

@router.post("")
async def transcribe(file: UploadFile):
    path = save_upload(file)
    audio_path = extract_audio(path)
    try:
        text = transcribe_with_azure(audio_path)
        return {"transcript": clean_transcript(text)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
