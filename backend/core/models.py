from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class AgentLog(BaseModel):
    agent: str
    message: str
    type: str = "info"
    timestamp: str

class ResearchOutput(BaseModel):
    topic: str
    key_findings: List[str]
    sources_count: int
    raw_content: str

class Criticism(BaseModel):
    logical_gaps: List[str]
    missing_perspectives: List[str]
    bias_score: float = Field(..., ge=0, le=1)
    suggestions: List[str]

class Synthesis(BaseModel):
    refined_topic: str
    merged_insights: List[str]
    technical_framework: str

class FinalReport(BaseModel):
    title: str
    content_markdown: str
    word_count: int
    readability_score: str
