from app.utils.logger import get_logger
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from typing import Any
from app.config.config import get_settings
from app.utils.langfuse_tracing import build_langchain_config

settings = get_settings()

class LLMService:

    def __init__(self, llm_provider:str = None, llm_model: str = None, user_info: dict | None = None):
        self.logger = get_logger(__name__)
        self.user_info = user_info or {}

        self.llm_provider = llm_provider or settings.llm_provider
        self.llm_model = llm_model or settings.llm_model
        self.logger.info(f"LLMService initialized with {self.llm_provider} and {self.llm_model}")


    def generate_response(self, prompt: str,temperature:float=0.0) -> Any:
        self.logger.info(f"Generating LLM response with provider: {self.llm_provider}, model: {self.llm_model}")

        llm = self._get_llm(llm_provider= self.llm_provider , llm_model= self.llm_model,temperature=temperature)
        config = build_langchain_config(
            user_info=self.user_info,
            route="llm.generate_response",
            model=self.llm_model,
        )

        response = llm.invoke(prompt, config=config) if config else llm.invoke(prompt)

        self.logger.info(f"Response received from LLM: {response}")

        return response
        

    def _get_llm(self,llm_provider: str, llm_model: str,temperature: float):

        self.logger.info(f"Getting llm for provider : {self.llm_provider}, model: {self.llm_model}")
        try:
            if llm_provider == "vertex":
                return ChatGoogleGenerativeAI(model=llm_model, temperature=temperature)
            elif llm_provider == "openai":
                return  ChatOpenAI(model=llm_model, temperature=temperature)
            elif llm_provider == "ollama":
                return ChatOllama(model=llm_model,temperature=temperature)
            else:
                return ChatGoogleGenerativeAI(model=llm_model, temperature=temperature)
        except Exception as e:
            self.logger.error("Error while geting LLM for provider : {self.llm_provider}, model: {self.llm_model}")
            raise