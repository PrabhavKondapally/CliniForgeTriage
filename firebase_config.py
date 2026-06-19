import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

if not firebase_admin._apps:
    cred = credentials.Certificate(
        "cliniforge-firebase-adminsdk-fbsvc-d2de51b3e6.json"
    )
    firebase_admin.initialize_app(cred)

db = firestore.client()