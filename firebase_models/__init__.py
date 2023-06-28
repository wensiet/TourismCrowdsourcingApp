import os
from google.cloud import storage

# https://octabyte.io/FireO

credentials_path = './crowdsourcing-app-f86b3-firebase-adminsdk-1r7f5-52d53ab92b.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
storage_client = storage.Client()

bucket = storage_client.bucket('crowdsourcing-app-f86b3.appspot.com')

blob = bucket.blob("test_name")

from firebase_models.places import Place
from firebase_models.users import User
from firebase_models.date import Date
from firebase_models.comment import Comment
