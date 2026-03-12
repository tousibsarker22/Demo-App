from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractRequest(BaseModel):
    transcript: str
    title: Optional[str] = None
    tone: str = Field(default="simple")

class Step(BaseModel):
    number: int
    action: str
    details: Optional[str] = None
    role: Optional[str] = None
    tools: Optional[List[str]] = None

class Decision(BaseModel):
    condition: str
    path_yes: Optional[str] = None
    path_no: Optional[str] = None

class ProcessModel(BaseModel):
    title: str
    summary: str
    purpose: str
    scope: Optional[str] = None
    roles: List[str] = []
    tools: List[str] = []
    steps: List[Step]
    decisions: List[Decision] = []
    notes: Optional[List[str]] = []

class DocxRequest(BaseModel):
    process: ProcessModel
    author: Optional[str] = None
    source_name: Optional[str] = None
