import asyncio

from . import app
from fastapi.responses import JSONResponse
from firebase_models import Place
from fastapi import Request
from Util.parser import parse_place, parse_user


@app.get("/check-status")
async def status():
    return JSONResponse(content={"API is working": "True"}, status_code=200)


@app.post("/add-place")
async def add_place(request: Request):
    data = dict(await request.form())
    queried_place = parse_place(data)
    queried_place.save()
    return JSONResponse(content={"Received content": f"{queried_place.title} {queried_place.rating}"}, status_code=200)


@app.get("/get-place/{title}")
async def get_place_by_name(title: str):
    # Executing the query
    places_query = (
        Place.collection.filter("title", "==", "Kazan")
        .filter("rating", "==", 4.98)
    ).fetch()

    for p in places_query:
        print(p)


@app.post("/add-user")
async def add_user(request: Request):
    data = dict(await request.form())
    queried_user = parse_user(data)
    queried_user.save()
    return JSONResponse(content={"Received content": f"{queried_user.name}"}, status_code=200)


@app.get("/get-user/{title}")
async def get_user_by_name(title: str):
    # Executing the query
    places_user = (
        Place.collection.filter("name", "==", "Yigor")
    ).fetch()

    for p in places_user:
        print(p)
