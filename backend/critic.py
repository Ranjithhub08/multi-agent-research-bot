import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

class Critic:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            self.llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
        else:
            self.llm = None

    async def run(self, research_data: str):
        if not self.llm:
            return "Critic [MOCK]: Validated research data for biases."
        
        prompt = f"""
        You are an Adversarial Critic. Review the following research data for:
        1. Logical inconsistencies
        2. Potential biases or hallucinations
        3. Missing critical perspectives
        
        Data: {research_data}
        
        Provide a list of "Correction Directives" for the Synthesizer.
        """
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        return response.content
