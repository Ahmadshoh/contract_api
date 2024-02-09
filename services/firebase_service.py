from typing import Dict, Any
from google.cloud.firestore_v1 import DocumentSnapshot
from contract_manager import db


class FirebaseService:
    def __init__(self, user_uuid):
        self._init_user(user_uuid)
        self.company = FirebaseCompany(self.user_collection)
        self.contract = FirebaseContract(self.user_collection)
        self.file = FirebaseFile(self.user_collection)

    def _init_user(self, user_uuid):
        self.user_collection = db.collection('users').document(user_uuid)
        user_data = {'uuid': user_uuid}
        self.user_collection.set(user_data, merge=True)


class FirebaseModel:
    def __init__(self, user_collection):
        self.collection = user_collection.collection(self._collection_name())

    def find_or_create_by(self, field, value, data) -> DocumentSnapshot:
        query = self.collection.where(field, '==', value).limit(1)
        existing_items = list(query.stream())

        if existing_items:
            return existing_items[0]
        else:
            _, reference = self.collection.add(data)
            return reference.get()

    def create(self, data: Dict[str, Any]):
        return self.collection.add(data)

    def _collection_name(self) -> str:
        raise NotImplementedError


class FirebaseCompany(FirebaseModel):
    def _collection_name(self):
        return 'companies'


class FirebaseContract(FirebaseModel):
    def _collection_name(self):
        return 'contracts'


class FirebaseFile(FirebaseModel):
    def _collection_name(self):
        return 'files'
