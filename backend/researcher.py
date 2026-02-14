import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

class Researcher:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            self.llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
        else:
            self.llm = None

    async def run(self, topic: str):
        if not self.llm:
            return f"Researcher [MOCK]: Gathered initial data on {topic}."
        
        prompt = f"""
        You are a Master Researcher. Provide a deep-dive, factual report on: {topic}.
        Search for technical specifications, historical context, and current industry trends.
        Format your response as raw data points for an analyst to process.
        """
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        return response.content
