import os
import logging
from typing import Any, Dict, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            logger.error("CRITICAL: GOOGLE_API_KEY not found. LLM service will fail.")
            self.client = None
        else:
            logger.info("Initializing in PRODUCTION MODE (Gemini API)")
            try:
                self.client = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash", 
                    google_api_key=self.api_key,
                    temperature=0.7
                )
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                self.client = None

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.client:
            raise ValueError("LLM client not initialized. Check your GOOGLE_API_KEY.")
            
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))
        
        try:
            response = await self.client.ainvoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            raise
