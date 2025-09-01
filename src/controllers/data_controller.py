from .base_controller import BaseController
from .bucket_controller import BucketController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os

class DataController(BaseController):
    def __init__(self):
        super().__init__() 
        self.size_scale = 1048576 # convert MB to bytes
    
    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        return True, ResponseSignal.FILE_VALIDATION_SUCCESS.value

    def generate_unique_filename(self, original_filename: str, project_id: str):
        random_str = self.get_random_filename()
        project_dir = BucketController().get_project_bucket_path(project_id=project_id)
        cleaned_filename = self.clean_filename(original_filename)
        file_path = os.path.join(project_dir, f"{random_str}_{cleaned_filename}")

        while os.path.exists(file_path):
            random_str = self.get_random_filename()
            file_path = os.path.join(project_dir, f"{random_str}_{cleaned_filename}")
        return file_path, f"{random_str}_{cleaned_filename}"

    def clean_filename  (self, original_filename: str):
        cleaned_filename = re.sub(r'[^\w.]', '', original_filename.strip())
        return cleaned_filename