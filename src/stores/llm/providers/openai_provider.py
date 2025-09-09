from llm_interface import LLMInterface
from openai import OpenAI
from llm_enum import OpenAIEnum 
import logging


class openai_provider(LLMInterface):
    def __init__(self, api_key: str, api_url: str = None, default_input_max_characters: int = 1000, default_output_max_characters: int = 1000,
                 default_generate_temperature: float = 0.1):
        self.api_key = api_key
        self.api_url = api_url
        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_characters = default_output_max_characters
        self.default_generate_temperature = default_generate_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(
            api_key=self.api_key,
            api_url=self.api_url
        )

        self.logger = logging.getLogger(__name__)

        def set_generation_model(self, model_id: str):
            self.generation_model_id = model_id

        def set_embedding_model(self, model_id: str, embedding_size: int):
            self.embedding_model_id = model_id
            self.embedding_size = embedding_size

        def process_text(self, text: str):
            return text[:self.default_input_max_characters].strip()

        def generate_text(self, prompt: str, chat_history: list, max_output_tokens: int, temperature: float):
            if not self.client:
                self.logger.error("OpenAI client is not initialized.")
                return None
            
            if not self.generation_model_id:
                self.logger.error("Generation model is not set.")
                return None
            
            max_output_tokens = max_output_tokens if max_output_tokens else self.default_output_max_characters
            temperature = temperature if temperature else self.default_generate_temperature

            chat_history.append(self.construct_prompt(prompt, OpenAIEnum.USER.value))
            
            response = self.client.completions.create(
                model = self.generation_model_id,
                messages = chat_history,
                max_tokens = max_output_tokens,
                temperature = temperature
            )

            if not response or not response.choices or len(response.choices) == 0 or not response.choices[0] or not response.choices[0].message or not response.choices[0].message.content:
                self.logger.error("Error while generating text.")
                return None
            
            return response.choices[0].message.content 

        def embed_text(self, text: str, document_type: str):
            if not self.client:
                self.logger.error("OpenAI client is not initialized.")
                return None
            
            if not self.embedding_model_id:
                self.logger.error("Embedding model is not set.")
                return None
            
            response = self.client.embeddings.create(
                model = self.embedding_model_id,
                input = text
            )

            if not response or not response["data"] or len(response["data"]) == 0 or not response["data"][0] or not response["data"][0]["embedding"]:
                self.logger.error("Error while embedding text.")
                return None
            
            return response["data"][0]["embedding"]

        def construct_prompt(self, prompt: str, role: str):
            self.process_text(prompt)
            return {
                "role": role,
                "content": prompt
            }

