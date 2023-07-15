import os

file_path = './jwt-secret'
with open(file_path, 'r') as file:
    file_content = file.read().strip()
os.environ["SECRET_KEY"] = file_content


from Util.authorization import *
from Util.coordinates import *