from .base_data_model import BaseDataModel
from .db_schemes import Project
from .enums.database_enum import DatabaseEnum

class ProjectModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DatabaseEnum.COLLECTION_PROJECTS_NAME.value]

    @classmethod 
    async def create_instance(cls, db_client: object): 
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DatabaseEnum.COLLECTION_PROJECTS_NAME.value not in all_collections:
            await self.db_client.create_collection(DatabaseEnum.COLLECTION_PROJECTS_NAME.value)
            # create indices
            indices = Project.get_indices()
            for index in indices:
                await self.collection.create_index(index["key"], name=index["name"], unique=index.get("unique", False))

    async def create_project(self, project: Project):
        result = await self.collection.insert_one(project.model_dump(by_alias=True, exclude_unset=True))
        project.id = result.inserted_id
        return project
    
    async def get_project_or_create(self, project_id: str) -> Project:
       record = await self.collection.find_one({"project_id": project_id})
       if record is None:
           project = Project(project_id=project_id)
           project = await self.create_project(project=project)
           return project
       
       return Project(**record)
    
    async def get_all_projects(self, page: int = 1, page_size: int = 10):
         # count total documents
        total_documents = await self.collection.count_documents({})
        total_pages = total_documents

        if total_documents % page_size > 0:
            total_pages += 1

        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        projects = []
        for doc in cursor:
            projects.append(Project(**doc))

        return {
            "projects": projects,
            "total_pages": total_pages,
            "current_page": page,
        }