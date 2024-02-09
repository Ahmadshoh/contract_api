import firebase_admin
from firebase_admin import credentials, firestore
from contract_manager.secrets import firebase_config

cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)

db = firestore.client()
