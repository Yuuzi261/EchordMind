from .chroma import ChromaVectorStore
from .base import VectorStoreInterface

def get_vector_store(vector_store_name: str, **kwargs) -> VectorStoreInterface:
    match vector_store_name:
        case "chroma":
            path = kwargs["path"]
            return ChromaVectorStore(path=path)
        case _:
            raise ValueError(f"Unknown vector store name: {vector_store_name}")
