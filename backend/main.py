import os
from core.config import settings
import json
import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import AsyncGenerator
from dotenv import load_dotenv

# Initialize environment
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AutonomousGrid")

from core.agent_manager import AgentManager

app = FastAPI(title="Autonomous Research Grid - Production Engine", version="3.0.0")

# Security configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    topic: str

@app.get("/health")
async def health_check():
    return {"status": "operational", "engine": "LangGraph V3", "mode": "MOCK" if not settings.GOOGLE_API_KEY else "LIVE"}

@app.post("/api/research")
async def start_research(request: ResearchRequest):
    """Simple POST endpoint for immediate results."""
    manager = AgentManager()
    # We use execute_task but gather it for a final response
    final_report = ""
    async for update in manager.execute_task(request.topic):
        if "finalReport" in update:
            final_report = update["finalReport"]
    
    if not final_report:
        raise HTTPException(status_code=500, detail="Failed to generate report")
    
    return {"finalReport": final_report}

@app.get("/api/research/stream")
async def stream_research(topic: str):
    """Premium SSE endpoint for real-time agent coordination logs."""
    async def event_generator() -> AsyncGenerator[str, None]:
        manager = AgentManager()
        try:
            async for update in manager.execute_task(topic):
                yield f"data: {json.dumps(update)}\n\n"
        except Exception as e:
            logger.error(f"Stream Error: {e}")
            yield f"data: {json.dumps({'agent': 'Error', 'message': str(e), 'type': 'warning'})}\n\n"
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    port = settings.PORT
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
