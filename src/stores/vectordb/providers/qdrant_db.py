from qdrant_client import models, QdrantClient
from vector_db_interface import VectorDBInterface
import logging
from vector_db_enum import DistanceMethodEnum
from typing import List

class QdrantDBProvider(VectorDBInterface):

    def __init__(self, db_path: str, distance_method: str):
        self.client = None
        self.db_path = db_path
        self.distance_method = None
        
        if distance_method == DistanceMethodEnum.COSINE:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnum.DOT:
            self.distance_method = models.Distance.DOT
        else:
            self.distance_method = models.Distance.COSINE
        self.logger = logging.getLogger(__name__)


        def connect(self):
            self.client = QdrantClient(path = self.db_path)

        def disconnect(self):
            self.client = None

        def is_collection_exist(self, collection_name: str) -> bool:
            return self.client.collection_exists(collection_name)
         
        def lis_all_collection(self: str) -> List:
            return self.client.get_collections()

        def get_collection_info(self, collection_name: str) -> dict:
            return self.client.get_collection(collection_name)

        def delete_collection(self, collection_name: str):
            if self.is_collection_exist(collection_name):
                return self.client.delete_collection(collection_name)

        def create_collection(self, collection_name: str, embedding_size: int, do_reset: bool = False):
            if do_reset:
                _ = self.delete_collection(collection_name)
            if not self.is_collection_exist(collection_name):
                return self.client.create_collection(
                    collection_name = collection_name,
                    vectors_config = models.VectorParams(size = embedding_size, distance = self.distance_method),
                )

        def insert_one(self, collection_name: str, text: str,vector: list, metadata: dict = None, record_id: str = None):
            
            if not self.is_collection_exist(collection_name):
                self.logger.error(f"Collection {collection_name} does not exist.")  # Use the logger.
                return False
            
            try:
                _ = self.client.upload_records(
                    collection_name = collection_name,
                    recors = [
                        models.Record(
                            vector = vector,
                            id = record_id,
                            payload =  {
                                "text": text,
                                "metadata": metadata
                            }
                        )
                    ]
                )
            except Exception as e:
                self.logger.error(f"Error while inserting record: {e}")  # Use the logger.
                return False

            return True

        def insert_many(self, collection_name: str, texts: List, vectors: List, metadatas: List = None, record_ids: List = None, batch_size: int = 50):
            
            if not metadatas:
                metadatas = [None] * len(texts)

            if not record_ids:
                record_ids = [None] * len(texts)

            if not self.is_collection_exist(collection_name):
                self.logger.error(f"Collection {collection_name} does not exist.")  # Use the logger.
                return False
            
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i+batch_size]
                batch_vectors = vectors[i:i+batch_size]
                batch_metadatas = metadatas[i:i+batch_size]
                batch_records = [
                    models.Record(
                        payload =  {
                            "text": batch_texts[x],
                            "metadata": batch_metadatas[x]
                        }
                    )
                    for x in range(len(batch_texts))
                ]

            try:
                _ = self.client.upload_records(
                    collection_name = collection_name,
                    recors = batch_records
                )
            except Exception as e:
                self.logger.error(f"Error while inserting records: {e}")  # Use the logger.
                return False
            return True

        def search_by_vector(self, collection_name: str,vector: list, limit: int = 5):

            if not self.is_collection_exist(collection_name):
                self.logger.error(f"Collection {collection_name} does not exist.")  # Use the logger.
                return None

            try:
                return self.client.search(
                    query_vector = vector,
                    limit = limit
                )
            except Exception as e:
                self.logger.error(f"Error while searching by vector: {e}")  # Use the logger.
                return None