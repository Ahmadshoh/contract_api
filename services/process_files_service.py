from datetime import datetime
import os
import tempfile
from typing import Dict

from google.cloud import storage
from langchain_community.document_loaders import PyPDFLoader
from contract_manager.secrets import storage_config


class ProcessFilesService:
    def __init__(self):
        self.blobs: Dict[str, storage.Blob] = {}
        self.bucket: storage.Bucket = self._init_bucket()

    def upload_file(self, file, user_uuid):
        if file and file.filename.endswith('.pdf'):
            temp_file_path = os.path.join(tempfile.gettempdir(), file.filename)
            file.save(temp_file_path)

            blob_path = f"{user_uuid}/{datetime.now().strftime('%Y-%m-%d')}/{file.filename}"
            blob = self.bucket.blob(blob_path)
            blob.upload_from_filename(temp_file_path)

            self.blobs[file.filename] = blob
            os.remove(temp_file_path)
        else:
            raise TypeError("Invalid file format. Please provide a PDF file.")

    def delete_file(self, blob_name):
        blob = self.bucket.blob(blob_name)

        blob.reload()
        generation_match_precondition = blob.generation

        blob.delete(if_generation_match=generation_match_precondition)

    def to_json(self):
        return [{'name': filename, 'path': blob.public_url, 'blob_name': blob.name} for filename, blob in
                self.blobs.items()]

    @property
    def text(self):
        text = ''
        for filename, blob in self.blobs.items():
            loader = PyPDFLoader(blob.public_url)
            text += loader.load()[0].page_content
        return text

    @staticmethod
    def _init_bucket():
        client = storage.Client.from_service_account_info(storage_config)
        bucket_name = 'contract_files'
        return client.get_bucket(bucket_name)
