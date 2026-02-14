import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

class Synthesizer:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            self.llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
        else:
            self.llm = None

    async def run(self, research_data: str, critique: str):
        if not self.llm:
            return "Synthesizer [MOCK]: Merged research and critique into technical framework."
        
        prompt = f"""
        You are a Data Synthesizer. Merge the following Research Data and Critic Feedback into a cohesive technical framework.
        
        Research: {research_data}
        Critique: {critique}
        
        Ensure any conflicts are resolved and the framework is logically sound.
        """
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        return response.content
