import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

class Writer:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            self.llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
        else:
            self.llm = None

    async def run(self, topic: str, final_framework: str):
        if not self.llm:
            return f"# Report: {topic}\n\n[MOCK] Synthesis complete."
        
        prompt = f"""
        You are a Technical Writer. Convert this synthesized framework into a professional Markdown Research Report.
        Topic: {topic}
        Framework: {final_framework}
        
        Use sections, bullet points, and high-impact formatting.
        """
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        return response.content
