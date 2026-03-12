from fastapi import APIRouter, HTTPException
from ..models.schemas import DocxRequest
from ..services.docx_builder import build_docx
import tempfile
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/document", tags=["document"])

@router.post("")
async def generate_docx(req: DocxRequest):
    try:
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            out_path = build_docx(req.process, req.author, req.source_name, tmp.name)
        filename = (req.process.get('title') if isinstance(req.process, dict) else 'process') or 'process'
        filename = f"{filename}.docx"
        headers = {"Content-Disposition": f"attachment; filename="{filename}""}
        return FileResponse(out_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
