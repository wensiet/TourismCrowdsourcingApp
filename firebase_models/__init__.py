import os
from google.cloud import storage

# https://octabyte.io/FireO
# test issue #39
credentials_path = './admin-sdk.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
storage_client = storage.Client()

bucket = storage_client.bucket('crowdsourcing-app-f86b3.appspot.com')

blob = bucket.blob("test_name")

from firebase_models.places import Place
from firebase_models.users import User
from firebase_models.date import Date
from firebase_models.comment import Comment
from firebase_models.tags import Tags
from fireo import ListUnion
