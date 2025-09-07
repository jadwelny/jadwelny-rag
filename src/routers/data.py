from bson import ObjectId
from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, BucketController, ProcessController
from models import ResponseSignal
import aiofiles
import os
import logging
from routers import ProcessRequest
from models.project_model import ProjectModel
from models.chunk_model import ChunkModel
from models.assets_model import AssetModel   
from models.db_schemes import DataChunk, Asset
from models.enums.assets_type_enum import AssetsTypeEnum

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["Data"],
)

@data_router.post("/upload/{project_id}")
async def upload_file(request: Request, project_id: str, file: UploadFile, app_settings:Settings=Depends(get_settings)):
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create(project_id=project_id)
    dataController = DataController()
    is_valid, message = dataController.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": message,
                "file_id": file_id,
                "project_id": str(project.id),
            }
        )
    
    project_dir_path  = BucketController().get_project_bucket_path(project_id=project_id)
    file_path, file_id = dataController.generate_unique_filename(original_filename=file.filename, project_id=project_id)

    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk) 
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value,

            }
        )
    
    # store the assets record in db
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
    assets_object = Asset(
        asset_project_id = str(project.id),
        asset_type  =  AssetsTypeEnum.DOCUMENT.value,
        asset_name = file_id,
        asset_size = file.size,
        # asset_config = ,
    )

    assets_record = await asset_model.create_asset(asset=assets_object)

    return JSONResponse(
        content={
            "signal": ResponseSignal.UPLOAD_SUCCESS.value,
            "file_path": file_path,
            "file_id": file_id
        }
    )

@data_router.post("/process/{project_id}")
async def process_file(request: Request,project_id: str, process_request: ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create(project_id=project_id)

    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

    process_controller = ProcessController(project_id=project_id)
    # get file content
    file_content = process_controller.get_file_content(file_id=file_id)
    #
    file_chunks = process_controller.process_file_content(file_content=file_content,file_id=file_id, chunk_size=chunk_size, overlap_size=overlap_size)

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_PROCESSING_FAILED.value,
            }
        )

    # save file chunks
    file_chunk_records= [
        DataChunk (
            chunk_text= chunk.page_content,
            chunk_metadata= chunk.metadata,
            chunk_order= i+1,
            chunk_project_id= project.id,
        )
        for i,chunk in enumerate(file_chunks)
    ]


    if do_reset:
        await chunk_model.delete_chunks_by_project_id(project_id=project.id)
     

    no_records = await chunk_model.insert_many_chunks(chunks=file_chunk_records)

    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_PROCESSING_SUCCESS.value,
            "file_id": file_id,
            "no_chunks": no_records,
            "project_id": str(project.id),
        }
    )