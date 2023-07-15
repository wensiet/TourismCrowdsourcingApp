import os

file_path = './algolia-app-id'
with open(file_path, 'r') as file:
    file_content = file.read().strip()
os.environ["ALGOLIA_APP_ID"] = file_content

file_path = './algolia-api-key'
with open(file_path, 'r') as file:
    file_content = file.read().strip()
os.environ["ALGOLIA_API_KEY"] = file_content

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from . import routes
