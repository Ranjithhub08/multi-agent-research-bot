import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import AsyncGenerator
import json
from .agent_manager import AgentManager

app = FastAPI(title="Autonomous Research Grid Engine", version="3.0.0")

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
    return {"status": "operational", "engine": "LangGraph Swarm"}

@app.get("/api/research/stream")
async def stream_research(topic: str):
    async def event_generator() -> AsyncGenerator[str, None]:
        manager = AgentManager()
        async for update in manager.run_with_stream(topic):
            yield f"data: {json.dumps(update)}\n\n"
            
    from fastapi.responses import StreamingResponse
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
