from .base_data_model import BaseDataModel
from .db_schemes import DataChunk
from .enums.database_enum import DatabaseEnum
from bson import ObjectId
from pymongo import InsertOne

class ChunkModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DatabaseEnum.COLLECTION_CHUNKS_NAME.value]

    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_one(chunk.model_dump())
        chunk.id = result.inserted_id
        return chunk
    
    async def get_chunk_by_id(self, chunk_id: str):
        record = await self.collection.find_one({"_id": ObjectId(chunk_id)})
        if record is None:
            return None
        return DataChunk(**record)
    
    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            operations = [InsertOne(chunk.model_dump()) for chunk in batch]
            self.collection.bulk_write(operations)

        return len(chunks)
