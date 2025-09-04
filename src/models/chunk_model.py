from .base_data_model import BaseDataModel
from .db_schemes import DataChunk
from .enums.database_enum import DatabaseEnum
from bson import ObjectId
from pymongo import InsertOne

class ChunkModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DatabaseEnum.COLLECTION_CHUNKS_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object): 
        instance = cls(db_client)
        await instance.init_collection()
        return instance
    
    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DatabaseEnum.COLLECTION_CHUNKS_NAME.value not in all_collections:
            await self.db_client.create_collection(DatabaseEnum.COLLECTION_CHUNKS_NAME.value)
            # create indices
            indices = DataChunk.get_indices()
            for index in indices:
                await self.collection.create_index(index["key"], name=index["name"], unique=index.get("unique", False))
        

    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_one(chunk.model_dump(by_alias=True, exclude_unset=True)) # if it have alias it will be used, eclude unset to not include None values
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
            operations = [InsertOne(chunk.model_dump(by_alias=True, exclude_unset=True)) for chunk in batch]
            self.collection.bulk_write(operations)

        return len(chunks)
    
    async def delete_chunks_by_project_id(self, project_id: ObjectId):
        result = await self.collection.delete_many({"chunk_project_id": project_id})
        return result.deleted_count
