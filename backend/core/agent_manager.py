import logging
import datetime
import operator
from typing import Dict, List, Any, TypedDict, Optional, Annotated
from langgraph.graph import StateGraph, END

from .llm_service import LLMService
from .models import AgentLog, ResearchOutput, Criticism, Synthesis, FinalReport
from .agents.researcher import Researcher
from .agents.critic import Critic
from .agents.synthesizer import Synthesizer
from .agents.writer import Writer

logger = logging.getLogger(__name__)

class GraphState(TypedDict):
    topic: str
    research: Optional[ResearchOutput]
    critique: Optional[Criticism]
    synthesis: Optional[Synthesis]
    final_report: Optional[FinalReport]
    logs: Annotated[List[Dict[str, Any]], operator.add]

class AgentManager:
    def __init__(self):
        self.llm_service = LLMService()
        self.researcher = Researcher(self.llm_service)
        self.critic = Critic(self.llm_service)
        self.synthesizer = Synthesizer(self.llm_service)
        self.writer = Writer(self.llm_service)

    def _create_log(self, agent: str, message: str, type: str = "info") -> Dict[str, Any]:
        log = AgentLog(
            agent=agent,
            message=message,
            type=type,
            timestamp=datetime.datetime.now().strftime("%H:%M:%S")
        )
        logger.info(f"[{agent}] {message}")
        return log.model_dump()

    async def run_research(self, state: GraphState):
        log = self._create_log("Researcher", f"Initiating deep-scan for: {state['topic']}")
        res = await self.researcher.process(state["topic"])
        return {
            "research": res,
            "logs": [log]
        }

    async def run_critique(self, state: GraphState):
        log = self._create_log("Critic", "Analyzing research findings for logical gaps.")
        res = await self.critic.process(state["research"])
        return {
            "critique": res,
            "logs": [log]
        }

    async def run_synthesis(self, state: GraphState):
        log = self._create_log("Synthesizer", "Merging intelligence and adversarial feedback.")
        res = await self.synthesizer.process(state["research"], state["critique"])
        return {
            "synthesis": res,
            "logs": [log]
        }

    async def run_writer(self, state: GraphState):
        log_writer = self._create_log("Writer", "Drafting production-grade Markdown report.")
        res = await self.writer.process(state["topic"], state["synthesis"])
        log_system = self._create_log("System", "Mission complete.", "success")
        return {
            "final_report": res,
            "logs": [log_writer, log_system]
        }

    def _build_workflow(self):
        workflow = StateGraph(GraphState)
        
        workflow.add_node("research", self.run_research)
        workflow.add_node("critique", self.run_critique)
        workflow.add_node("synthesis", self.run_synthesis)
        workflow.add_node("writer", self.run_writer)
        
        workflow.set_entry_point("research")
        workflow.add_edge("research", "critique")
        workflow.add_edge("critique", "synthesis")
        workflow.add_edge("synthesis", "writer")
        workflow.add_edge("writer", END)
        
        return workflow.compile()

    async def execute_task(self, topic: str):
        app = self._build_workflow()
        initial_state = {
            "topic": topic,
            "research": None,
            "critique": None,
            "synthesis": None,
            "final_report": None,
            "logs": []
        }
        
        async for output in app.astream(initial_state):
            for node_name, node_output in output.items():
                # Yield each log entry produced by the node
                if "logs" in node_output:
                    for log in node_output["logs"]:
                        yield log
                
                # If the writer node finished, yield the final report as well
                if node_name == "writer":
                    yield {
                        "agent": "System",
                        "finalReport": node_output["final_report"].content_markdown,
                        "metadata": node_output["final_report"].model_dump()
                    }
