from .llm_enum import LLMEnum
from stores.llm.providers import OpenAIProvider

class LLMProviderFactory:
    def __init__(self, config: dict):
        self.config = config
    
    def create(self, provider_name: str):
        if provider_name == LLMEnum.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generate_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_name}")