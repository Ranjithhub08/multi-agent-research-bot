import os
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

class CriticAgent:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables. Please check your .env file.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    async def execute(self, research_data: str) -> str:
        """
        Evaluates research data for quality, gaps, and logical consistency.
        """
        logger.info("[CriticAgent] Analyzing research findings for gaps and inconsistencies.")
        
        prompt = (
            "Critically analyze the following research data. Identify any logical gaps, "
            "potential biases, or missing technical details. Provide constructive "
            f"criticism to improve the report:\n\n{research_data}"
        )
        
        try:
            response = await self.model.generate_content_async(prompt)
            logger.info("[CriticAgent] Completed critical evaluation.")
            return response.text
        except Exception as e:
            logger.error(f"[CriticAgent] Error during criticism execution: {str(e)}")
            raise
