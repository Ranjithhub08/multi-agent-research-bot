import os
import asyncio
from typing import List, Dict, Any, TypedDict, Annotated, Sequence
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
import operator
from pydantic import BaseModel, Field

# Define the state of our research swarm
class ResearchState(TypedDict):
    topic: str
    research_data: List[str]
    analysis: str
    critique: str
    final_report: str
    logs: List[Dict[str, str]]

class ResearchOrchestrator:
    def __init__(self):
        # Configure the LLM
        # Note: Users should set GOOGLE_API_KEY in their environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            self.llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
        else:
            # Fallback/Placeholder logic could go here
            self.llm = None 

    def _create_log(self, agent: str, message: str, type: str = "info"):
        return {
            "agent": agent,
            "message": message,
            "type": type,
            "timestamp": "now" # Frontend handles actual timestamping if needed
        }

    async def researcher_node(self, state: ResearchState):
        topic = state["topic"]
        print(f"Researcher working on: {topic}")
        
        # In a real app, this would call a search tool (Tavily, SerpApi, etc.)
        # For this challenge, we simulate high-quality research gathering
        if self.llm:
            prompt = f"Provide a detailed list of key facts and current developments about {topic}. Focus on technical details and recent breakthroughs."
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            research_data = [response.content]
        else:
            research_data = [f"Simulated research data for {topic}: Emerging trends in AI orchestration and multi-agent systems."]
            await asyncio.sleep(2) # Simulate work

        return {
            "research_data": research_data,
            "logs": state.get("logs", []) + [self._create_log("Researcher", f"Gathered intelligence on {topic}")]
        }

    async def analyst_node(self, state: ResearchState):
        data = state["research_data"]
        print("Analyst processing data...")
        
        if self.llm:
            prompt = f"Analyze the following research data and identify key patterns and contradictions: {data}"
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            analysis = response.content
        else:
            analysis = "Analysis: The data suggests a shift towards autonomous agentic workflows with decentralized memory."
            await asyncio.sleep(2)

        return {
            "analysis": analysis,
            "logs": state.get("logs", []) + [self._create_log("Analyst", "Completed deep-dive analysis of gathered data")]
        }

    async def critic_node(self, state: ResearchState):
        analysis = state["analysis"]
        print("Critic reviewing analysis...")
        
        if self.llm:
            prompt = f"Review this analysis for biases, logical gaps, and missing perspectives: {analysis}"
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            critique = response.content
        else:
            critique = "Critique: The analysis is solid but could benefit from more focus on security implications."
            await asyncio.sleep(2)

        return {
            "critique": critique,
            "logs": state.get("logs", []) + [self._create_log("Critic", "Validated analysis and identified optimization points")]
        }

    async def writer_node(self, state: ResearchState):
        topic = state["topic"]
        analysis = state["analysis"]
        critique = state["critique"]
        print("Writer crafting final report...")
        
        if self.llm:
            prompt = f"Write a comprehensive professional research report on {topic} based on this analysis: {analysis} and incorporating this critique: {critique}. Use professional Markdown formatting."
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            report = response.content
        else:
            report = f"# Research Report: {topic}\n\n## 1. Overview\nSynthesized findings from the autonomous swarm.\n\n## 2. Technical Details\n{analysis}\n\n## 3. Critique Integration\n{critique}"
            await asyncio.sleep(2)

        return {
            "final_report": report,
            "logs": state.get("logs", []) + [self._create_log("Writer", "Finalized production-ready research report")]
        }

    def _build_graph(self):
        workflow = StateGraph(ResearchState)

        # Add nodes
        workflow.add_node("researcher", self.researcher_node)
        workflow.add_node("analyst", self.analyst_node)
        workflow.add_node("critic", self.critic_node)
        workflow.add_node("writer", self.writer_node)

        # Build edges
        workflow.set_entry_point("researcher")
        workflow.add_edge("researcher", "analyst")
        workflow.add_edge("analyst", "critic")
        workflow.add_edge("critic", "writer")
        workflow.add_edge("writer", END)

        return workflow.compile()

    async def run(self, topic: str):
        app = self._build_graph()
        final_state = await app.ainvoke({"topic": topic, "logs": [], "research_data": [], "analysis": "", "critique": "", "final_report": ""})
        return final_state["final_report"]

    async def run_with_stream(self, topic: str):
        """
        Runs the workflow and yields progress updates for SSE.
        """
        app = self._build_graph()
        state = {"topic": topic, "logs": [], "research_data": [], "analysis": "", "critique": "", "final_report": ""}
        
        # Initial log
        yield {"agent": "System", "message": f"Initializing research swarm for: {topic}", "type": "info"}
        
        async for output in app.astream(state):
            # output is a dict where keys are node names
            for node_name, node_output in output.items():
                if "logs" in node_output:
                    # Send only the last log entry added
                    last_log = node_output["logs"][-1]
                    yield last_log
                
                if node_name == "writer":
                    yield {"agent": "System", "message": "Research complete", "type": "success", "finalReport": node_output["final_report"]}
