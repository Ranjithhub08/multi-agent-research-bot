import os
import logging
import google.generativeai as genai
import asyncio
from agents.research_agent import ResearchAgent
from agents.critic_agent import CriticAgent

logger = logging.getLogger(__name__)

class SupervisorAgent:
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.critic_agent = CriticAgent()
        
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    async def run_pipeline(self, topic: str) -> str:
        """
        Orchestrates the multi-agent workflow: Research -> Critique -> Final Report.
        """
        logger.info(f"[SupervisorAgent] Starting pipeline for topic: '{topic}'")
        
        if not topic.strip():
            logger.warning("[SupervisorAgent] Empty query received.")
            return "Please provide a valid research topic."

        try:
            # 1. Trigger Research Agent
            research_content = await self.research_agent.execute(topic)
            logger.info("--- Intermediate Data: Research Phase Complete ---")
            
            # 2. Trigger Critic Agent
            await asyncio.sleep(2)
            critic_feedback = await self.critic_agent.execute(research_content)
            logger.info("--- Intermediate Data: Criticism Phase Complete ---")
            
            # 3. Final Synthesis by Supervisor
            await asyncio.sleep(2)
            logger.info("[SupervisorAgent] Synthesizing final report based on agent outputs.")
            
            synthesis_prompt = (
                "You are a Senior Research Supervisor. Using the research data and the "
                "criticism provided, generate a final, polished, production-ready "
                "research report that addresses all feedback and presents a unified analysis.\n\n"
                f"### RESEARCH DATA:\n{research_content}\n\n"
                f"### CRITIC FEEDBACK:\n{critic_feedback}\n\n"
                "### FINAL OUTPUT (Markdown):"
            )
            
            response = await self.model.generate_content_async(synthesis_prompt)
            logger.info("[SupervisorAgent] Pipeline execution successful.")
            
            return response.text
            
        except Exception as e:
            logger.error(f"[SupervisorAgent] Pipeline failed: {str(e)}")
            return f"Error: The research pipeline encountered a critical failure: {str(e)}"
