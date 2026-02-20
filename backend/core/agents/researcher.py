import json
from .base import BaseAgent
from ..models import ResearchOutput

class Researcher(BaseAgent):
    async def process(self, topic: str) -> ResearchOutput:
        system_prompt = "You are a Senior Research Analyst. Provide findings in a structured JSON format."
        prompt = f"""
        Conduct a deep-dive research into: {topic}.
        Return a JSON object with:
        - topic: string
        - key_findings: list of strings
        - sources_count: integer
        - raw_content: string (a paragraph of summary)
        """
        
        raw_response = await self.llm.generate(prompt, system_prompt)
        
        try:
            # Simple cleanup for JSON parsing
            clean_json = raw_response.strip().replace("```json", "").replace("```", "")
            data = json.loads(clean_json)
            return ResearchOutput(**data)
        except:
            # Fallback if LLM fails to return perfect JSON
            return ResearchOutput(
                topic=topic,
                key_findings=["Emerging market trends", "Technological disruptions"],
                sources_count=5,
                raw_content=raw_response
            )
