# ⚡ Autonomous Research Grid Backend (Production Engine)

This is a professional, multi-agent research orchestration system built using **LangGraph** and **FastAPI**. It features a modular "Swarm" architecture where each agent specializes in a specific phase of the research lifecycle.

## 🏗 Architecture

The system follows **Clean Architecture** principles:
- **`core/agents/`**: Modular agent definitions with structured IO.
- **`core/llm_service.py`**: Singleton-pattern service managing Mock vs Production LLM modes.
- **`core/models.py`**: Pydantic models ensuring data integrity between agents.
- **`core/agent_manager.py`**: Orchestration logic using a Directed Acyclic Graph (DAG).

### Agents
1. **Researcher**: Deep-dive data gathering.
2. **Critic**: Adversarial analysis and bias detection.
3. **Synthesizer**: Integration of intelligence and feedback.
4. **Writer**: Professional Markdown reporting.

## 🚀 Installation & Setup

### 1. Environment Configuration
Create a `.env` file or export variables:
```bash
export GOOGLE_API_KEY=your_key_here  # Optional: Defaults to MOCK MODE if empty
export MOCK_MODE=false               # Set to true to force mock responses
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Engine
```bash
python3 main.py
```
*The server will start at `http://localhost:8000`*

## 📡 API Endpoints

- **GET `/api/research/stream?topic=...`**: Real-time Server-Sent Events (SSE) streaming of agent logs.
- **POST `/api/research`**: Synchronous JSON endpoint returning the final report.

## 🧪 Testing the Pipeline
You can test the orchestration directly via Python:
```python
from core.agent_manager import AgentManager
import asyncio

async def test():
    mgr = AgentManager()
    async for update in mgr.execute_task("Future of AI"):
        print(update)

asyncio.run(test())
```
