from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from firebase_models import User
from passlib.context import CryptContext

import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# THIS IS A DEVELOPMENT SECRET KEY
secret_key = "7779d8f0291698afca259e4c7a9266e6232d5a60bf9412b6f24622609de7063a"


def create_access_token(user):
    payload = {
        "sub": str(user.id),
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }

    access_token = jwt.encode(payload,
                              secret_key,
                              algorithm="HS256")

    return access_token


def create_user(user_data: User):
    hashed_password = pwd_context.hash(user_data.password)
    user = User(
        email=user_data.email,
        name=user_data.name,
        surname=user_data.surname,
        password=hashed_password
    )
    user.save()
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(email, password):
    user = User.collection.filter("email", "==", email).get()
    if not user or not verify_password(password, user.password):
        return False
    return user


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = payload["sub"]
        # Fetch the user from the database based on the user_id
        user = User.collection.get(user_id)
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
