import os
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

class ResearchAgent:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables. Please check your .env file.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    async def execute(self, topic: str) -> str:
        """
        Gathers detailed research analysis using Gemini API.
        """
        logger.info(f"[ResearchAgent] Starting deep research on: '{topic}'")
        
        prompt = (
            f"Perform exhaustive research on the following topic: '{topic}'.\n"
            "Provide technical specifications, current trends, and a structured summary."
        )
        
        try:
            # Using async call for better backend performance
            response = await self.model.generate_content_async(prompt)
            logger.info("[ResearchAgent] Successfully generated research data.")
            return response.text
        except Exception as e:
            logger.error(f"[ResearchAgent] Error during research execution: {str(e)}")
            raise
