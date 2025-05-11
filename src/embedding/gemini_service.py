from google import genai
# from google.genai import types, errors
from typing import List, Optional
from src import setup_logger

log = setup_logger(__name__)

class GeminiEmbeddingService:
    DEFAULT_EMBEDDING_MODEL = "embedding-001"
    
    def __init__(self, api_key: str, embedding_model_name: str):
        try:
            self.client = genai.Client(api_key=api_key)
            log.info("Google Generative AI configured successfully.")
        except Exception as e:
            log.error(f"Failed to configure Google Generative AI: {e}")
            raise
        
        self.embedding_model = self._validate_model(embedding_model_name, "embedding", self.DEFAULT_EMBEDDING_MODEL)
        
    async def get_embedding(self, text: str) -> Optional[List[float]]:
        """get the embedding vector of the text"""
        try:
            result = await self.client.aio.models.embed_content(
                model=self.embedding_model,
                contents=[text],
                config={
                    'output_dimensionality': 64 #TODO: set the embedding dimension (config option & find a better value)
                }
            )
            log.debug(f"Embedding result: {result.embeddings[0].values}")
            return result.embeddings[0].values
        except Exception as e:
            log.error(f"Error getting embedding from Gemini: {e}", exc_info=True)
            return None
        
    def _validate_model(self, model_name: str, model_type: str, default_model: str) -> str:
        """check if the specified model is available, otherwise use the default model"""
        try:
            self.client.models.get(model=model_name)
            log.info(f"{model_type.capitalize()} model '{model_name}' validated successfully.")
            return model_name
        except:
            log.warning(
                f"{model_type.capitalize()} model '{model_name}' is not available. "
                f"Using default model '{default_model}'."
            )
            return default_model