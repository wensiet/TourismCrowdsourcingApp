import os
from google.cloud import storage

# https://octabyte.io/FireO

credentials_path = './crowdsourcing-app-f86b3-firebase-adminsdk-1r7f5-52d53ab92b.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
storage_client = storage.Client()

from firebase_models.places import Place
from firebase_models.users import User, Comments, Date
