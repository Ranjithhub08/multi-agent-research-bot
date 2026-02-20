from abc import ABC, abstractmethod
from typing import Any
from ..llm_service import LLMService

class BaseAgent(ABC):
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
        self.name = self.__class__.__name__

    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        pass
