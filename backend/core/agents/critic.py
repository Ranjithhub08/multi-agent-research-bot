import json
from .base import BaseAgent
from ..models import Criticism, ResearchOutput

class Critic(BaseAgent):
    async def process(self, research: ResearchOutput) -> Criticism:
        system_prompt = "You are an Adversarial Reviewer. Evaluate research quality and provide results in JSON."
        prompt = f"""
        Review this research:
        {research.model_dump_json()}
        
        Return a JSON object with:
        - logical_gaps: list of strings
        - missing_perspectives: list of strings
        - bias_score: float (0.0 to 1.0)
        - suggestions: list of strings
        """
        
        raw_response = await self.llm.generate(prompt, system_prompt)
        
        try:
            clean_json = raw_response.strip().replace("```json", "").replace("```", "")
            data = json.loads(clean_json)
            return Criticism(**data)
        except:
            return Criticism(
                logical_gaps=["Insufficient data on long-term impacts"],
                missing_perspectives=["Socio-economic analysis"],
                bias_score=0.2,
                suggestions=["Include case studies from emerging markets"]
            )
