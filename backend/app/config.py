import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

load_dotenv()


SERVICE_ACCOUNT_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not SERVICE_ACCOUNT_PATH:
    raise RuntimeError("Please set GOOGLE_APPLICATION_CREDENTIALS to the path of your service account JSON")


cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()


pyrebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
}


if not pyrebase_config["apiKey"]:
    firebase = None
else:
    firebase = pyrebase.initialize_app(pyrebase_config)
