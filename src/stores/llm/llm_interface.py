from abc import ABC, abstractmethod
class LLMInterface(ABC):
    """
    Abstract class for Large Language Models (LLMs).
    """

    @abstractmethod
    def set_generation_model(self, model_id: str):
        """
        Set the model ID for the generation model
        """
        pass

    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        """
        Set the model ID for the embedding model
        """
        pass

    # temperature is between 0 and 1, when near to zero I need facts
    @abstractmethod
    def generate_text(self, prompt: str,chat_history: list =[] , max_output_tokens: int = None, temperature: float = None):
        """
        Generate text based on the given prompt and parameters
        """
        pass

    @abstractmethod
    def embed_text(self, text: str, document_type: str):
        """
        Embed the given text into a vector representation
        """
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        """
        Construct a prompt from the given prompt string and role string
        """
        pass
