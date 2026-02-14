import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import AsyncGenerator, List
import json
import asyncio
from app.orchestrator import ResearchOrchestrator

app = FastAPI(title="Autonomous Research Grid API", version="2.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    topic: str

@app.get("/")
async def root():
    return {"status": "online", "message": "Autonomous Research Grid Backend is active"}

@app.post("/api/research")
async def start_research(request: ResearchRequest):
    """
    Synchronous endpoint for simpler integration, 
    but it will call the orchestrator and return the final report.
    """
    orchestrator = ResearchOrchestrator()
    try:
        result = await orchestrator.run(request.topic)
        return {"finalReport": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/research/stream")
async def stream_research(topic: str):
    """
    Server-Sent Events endpoint to stream real-time agent logs to the frontend.
    """
    async def event_generator() -> AsyncGenerator[str, None]:
        orchestrator = ResearchOrchestrator()
        async for update in orchestrator.run_with_stream(topic):
            yield f"data: {json.dumps(update)}\n\n"
            
    from fastapi.responses import StreamingResponse
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
