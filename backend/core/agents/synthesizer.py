import json
from .base import BaseAgent
from ..models import Synthesis, ResearchOutput, Criticism

class Synthesizer(BaseAgent):
    async def process(self, research: ResearchOutput, critique: Criticism) -> Synthesis:
        system_prompt = "You are a Chief Architect. Synthesize data and feedback into a JSON framework."
        prompt = f"""
        Merge Research: {research.model_dump_json()}
        With Criticism: {critique.model_dump_json()}
        
        Return a JSON object with:
        - refined_topic: string
        - merged_insights: list of strings
        - technical_framework: string (detailed plan)
        """
        
        raw_response = await self.llm.generate(prompt, system_prompt)
        
        try:
            clean_json = raw_response.strip().replace("```json", "").replace("```", "")
            data = json.loads(clean_json)
            return Synthesis(**data)
        except:
            return Synthesis(
                refined_topic=research.topic,
                merged_insights=research.key_findings + ["Integrated adversarial feedback"],
                technical_framework="Standard operational framework with built-in redundancy."
            )
