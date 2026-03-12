from fastapi import APIRouter, HTTPException
from ..models.schemas import ExtractRequest
from ..services.extraction import extract_process

router = APIRouter(prefix="/extract", tags=["extract"])

@router.post("")
async def extract(req: ExtractRequest):
    try:
        data = extract_process(req.transcript, req.title, req.tone)
        return {"process": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
