from . import app
from fastapi.responses import JSONResponse, StreamingResponse
from firebase_models import Place, User, Date, Comment
from fastapi import Form, Depends, File
from Util import create_user, authenticate_user, create_access_token, get_current_user, \
    calculate_boundaries
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from geopy.distance import geodesic
from google.cloud.firestore_v1._helpers import GeoPoint
from firebase_models import bucket, ListUnion

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@app.get("/check-status", tags=["Status"], summary="Check if API is working.")
async def status():
    print("Pipeline test")
    return JSONResponse(content={"message": "API is working!"}, status_code=200)


@app.post("/add-place", tags=["Places"], summary="Add new places in firestore.")
async def add_place(user: Annotated[User, Depends(get_current_user)], title: Annotated[str, Form()],
                    rating: Annotated[str, Form()], description: Annotated[str, Form()]):
    place = Place(
        title=title,
        rating=float(rating),
        description=description,
        user_ids=[user.id]
    )
    place.save()
    return JSONResponse(content={f"{place.id}": f"{title}"}, status_code=200)


@app.post("/update-place-location/{place_id}", tags=["Places"],
          summary="Update place's latitude and longitude.")
async def update_location(place_id: str, lat: Annotated[str, Form()], lon: Annotated[str, Form()]):
    p = (Place.collection.filter("id", "==", place_id)).get()
    if p:
        p.geo_point = GeoPoint(latitude=float(lat), longitude=float(lon))
        p.save()
        return JSONResponse(content={"message": f"Place {place_id} location was updated to {lat}, {lon}"},
                            status_code=200)
    else:
        return JSONResponse(content={"message": f"Place {place_id} not found"}, status_code=404)


@app.get("/get-place/{place_id}", tags=["Places"], summary="Fetch place from firestore.")
async def get_place_by_name(place_id: str):
    place = Place.collection.filter("id", "==", place_id).get()
    if place:
        return JSONResponse(content=place.to_dict(), status_code=200)
    else:
        return JSONResponse(content={"message": f"Place {place_id} not found"}, status_code=404)


@app.post("/upload-image", tags=["Media"], summary="Upload image on Google Cloud Storage.")
async def upload_image(user: User = Depends(get_current_user), image: bytes = File(),
                       place_id: str = Form(), image_extension: str = Form()):
    blobs = bucket.list_blobs(prefix=place_id)
    s = sum(1 for _ in blobs)
    file_name = f"{place_id}/{s}.{image_extension}"
    blob = bucket.blob(file_name)
    blob.upload_from_string(image, content_type=f"image/{image_extension}")
    return JSONResponse(content={"message": f"Photo uploaded by {user.email} to {place_id}"})


@app.get("/get-images-list/{place_id}", tags=["Media"], summary="Get list of image names.")
async def get_images(place_id: str):
    result = {
        "image_ref": []
    }
    for b in bucket.list_blobs(prefix=place_id):
        filename = str(b.name)
        result["image_ref"].append(filename[filename.find("/") + 1:len(filename)])
    return result


@app.get("/images/{place_id}/{image_name}", tags=["Media"], summary="Display particular image.")
async def image_by_place_id(place_id: str, image_name: str):
    for b in bucket.list_blobs(prefix=place_id):
        byte_file = b.download_as_bytes()
        filename = str(b.name)
        current_name = filename[filename.find("/") + 1:len(filename)]
        if current_name == image_name:
            async def stream_image():
                yield byte_file

            return StreamingResponse(stream_image(), media_type=b.content_type)


@app.get("/profile", tags=["Users"], summary="User data using authentication.")
async def get_user(user: Annotated[User, Depends(get_current_user)]):
    return user.to_dict()


@app.post("/register", tags=["Authentication"], summary="Register new user using email and password.")
async def register(email: Annotated[str, Form()], password: Annotated[str, Form()]):
    existing_user = User.collection.filter("email", "==", email).get()
    if existing_user:
        return JSONResponse(content={"message": "User with such credentials already exists"}, status_code=400)
    create_user(User(email=email, password=password))
    return {"message": "User registered"}


@app.post("/login", tags=["Authentication"], summary="Login using existing credentials.")
async def login(email: Annotated[str, Form()], password: Annotated[str, Form()]):
    user = authenticate_user(email, password)
    if not user:
        return JSONResponse(content={"message": "Invalid username or password"}, status_code=401)
    access_token = create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected", tags=["Authentication"], summary="Access to protected route using JSON Web Token.")
async def protected_route(user: User = Depends(get_current_user)):
    return {"message": f"Hello, {user.name}! This is a protected route."}


@app.get("/near-places", tags=["Places"],
         summary="Show places that are located in radius of 1.5km from entered latitude and longitude")
async def get_near_places(user_lat: float, user_lon: float):
    # check documentation and postman request in notion for this one
    search_scope = calculate_boundaries(user_lat, user_lon, 1)

    places = Place.collection \
        .filter("geo_point", ">=", search_scope["minimal_point"]) \
        .filter("geo_point", "<=", search_scope["maximal_point"]) \
        .fetch()

    result = {}

    for p in places:
        result[p.id] = geodesic((user_lat, user_lon), (p.geo_point.latitude, p.geo_point.longitude)).meters

    return result


@app.get("/search-place-by-rating/{rating_range}", tags=["Places"],
         summary="Search places with rating that is >= than passed parameters.")
async def search_by_rating(rating_range: int):
    queried_places = Place.collection.filter("rating", ">=", rating_range).fetch()
    result = {}
    for place in queried_places:
        result[place.id] = place.rating

    return result


@app.post("/update-user-nickname", tags=["Users"], summary="Change user's nickname.")
async def update_location(user: Annotated[User, Depends(get_current_user)],
                          nickname: Annotated[str, Form()]):
    """
    Parameters:
    - **nickname** (str): A nickname to reset for user.

    Returns:
    - **JSONResponse**: The answer form server.
    """

    user.nickname = nickname
    user.save()
    return JSONResponse(content={"message": f"User {user.id} changed nickname to {nickname}"}, status_code=200)


@app.post("/update-user-gender", tags=["Users"], summary="Change user's gender.")
async def update_location(user: Annotated[User, Depends(get_current_user)], gender: Annotated[str, Form()]):
    """
    Parameters:
    - **gender** (str): A gender to reset for user.

    Returns:
    - **JSONResponse**: The answer form server.
    """
    if gender == "male":
        user.gender = True
    elif gender == "female":
        user.gender = False
    else:
        return JSONResponse(content={"message": f"Invalid gender {gender}, use male/female"}, status_code=400)
    user.save()
    return JSONResponse(content={"message": f"User {user.id} changed gender to {gender}"}, status_code=200)


@app.post("/update-user-birthdate", tags=["Users"], summary="Change user's birth date.")
async def update_location(user: Annotated[User, Depends(get_current_user)], birthdate: Annotated[str, Form()]):
    """
    Parameters:
    - **birthdate** (str): A birthdate to reset for user, format: <YYYY.MM.DD>.

    Returns:
    - **JSONResponse**: The answer form server.
    """

    birthdate = birthdate.split(".")
    user.birthdate = Date(year=birthdate[0], month=birthdate[1], day=birthdate[2])
    user.save()
    return JSONResponse(
        content={"message": f"User {user.id} changed his birth date to {birthdate[2]}.{birthdate[1]}.{birthdate[0]}"},
        status_code=200)


@app.post("/add-comment/{place_id}", tags=["Users"],
          summary="Add new comments for places by particular user.")
async def update_location(user: Annotated[User, Depends(get_current_user)], text: Annotated[str, Form()],
                          place_id: str):
    """
    Parameters:
    - **text** (str): A text of comment.
    - **place_id** (str): A reference to commented place.

    Returns:
    - **JSONResponse**: The answer form server.
    """
    if (Place.collection.filter("id", "==", place_id)).get():
        new_comment = Comment(reference=place_id, text=text)
        user.comments = ListUnion(new_comment)
        user.save()
        return JSONResponse(content={"message": f"User {user.id} commented {place_id}"}, status_code=200)
    else:
        return JSONResponse(content={"message": f"Place {place_id} not found"}, status_code=404)
