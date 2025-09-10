from .vector_db_enum import VectorDBEnum
from stores.vectordb.providers import QdrantDBProvider
from controllers.base_controller import BaseController

class VectorDBProviderFactory:
    def __init__(self, config: dict):
        self.config = config
        self.base_controller = BaseController()
    
    def create(self, provider_name: str):
        if provider_name == VectorDBEnum.QDRANT.value:
            db_path = self.base_controller.get_database_path(database_name=self.config.VECTOR_DB_PATH)
            return QdrantDBProvider(
                db_path = db_path,
                distance_method = self.config.VECTOR_DB_DISTANCE_METHOD
            )
        else:
            return None