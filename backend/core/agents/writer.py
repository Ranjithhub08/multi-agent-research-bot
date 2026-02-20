import json
from .base import BaseAgent
from ..models import FinalReport, Synthesis

class Writer(BaseAgent):
    async def process(self, topic: str, synthesis: Synthesis) -> FinalReport:
        system_prompt = "You are a Technical Writer. Generate a Markdown report and metadata in JSON."
        prompt = f"""
        Project Topic: {topic}
        Final Synthesis: {synthesis.model_dump_json()}
        
        Return a JSON object with:
        - title: string
        - content_markdown: string (the actual full report)
        - word_count: integer
        - readability_score: string
        """
        
        raw_response = await self.llm.generate(prompt, system_prompt)
        
        try:
            clean_json = raw_response.strip().replace("```json", "").replace("```", "")
            data = json.loads(clean_json)
            return FinalReport(**data)
        except:
            return FinalReport(
                title=f"Advanced Analysis: {topic}",
                content_markdown=raw_response,
                word_count=len(raw_response.split()),
                readability_score="Professional"
            )
