from fastapi import APIRouter, UploadFile, HTTPException
from ..utils.files import save_upload
from ..utils.audio import extract_audio
from ..services.transcription import transcribe_with_azure, clean_transcript
from ..services.extraction import extract_process
from ..services.docx_builder import build_docx
import tempfile

router = APIRouter(prefix="/pipeline", tags=["pipeline"])

@router.post("")
async def full_pipeline(file: UploadFile, title: str | None = None, author: str | None = None):
    try:
        # 1) Save & extract audio
        path = save_upload(file)
        audio_path = extract_audio(path)

        # 2) Transcribe
        text = transcribe_with_azure(audio_path)
        text = clean_transcript(text)

        # 3) Extract process
        process = extract_process(text, title)

        # 4) Build docx temp and return paths & JSON
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            out = build_docx(process, author, path.name, tmp.name)

        return {
            "transcript": text,
            "process": process,
            "docx_temp_path": out,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
