import os

from . import app
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from firebase_models import Place, User, Date, Comment, Tags
from fastapi import Form, Depends, File
from Util import create_user, authenticate_user, create_access_token, get_current_user, \
    calculate_boundaries
from typing import Annotated, Optional
from fastapi.security import OAuth2PasswordBearer
from geopy.distance import geodesic
from google.cloud.firestore_v1._helpers import GeoPoint
from firebase_models import bucket
from algoliasearch.search_client import SearchClient
from API.docs_schemas import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

app.mount("/static", StaticFiles(directory="./build/static"), name="static")


@app.get("/check-status", tags=["Status"],
         summary="Check if API is working.",
         response_model=Message,
         responses={200: {"model": Message}})
async def status():
    """
    Retrieve the status of the API.

    Returns:
        dict: A JSON response containing the status message.

    Raises:
        HTTPException: If there is an error.
    """
    return JSONResponse(content={"message": "API is working!"}, status_code=200)


@app.get("/", tags=["React app"],
         summary="Moderation panel base root.")
async def root():
    return FileResponse("./build/index.html")


@app.get("/panel", tags=["React app"],
         summary="Moderation panel list root.")
async def root():
    return FileResponse("./build/index.html")


@app.post("/add-place", tags=["Places"],
          summary="Add new places in firestore.",
          response_model=Message,
          responses={200: {"model": Message}})
async def add_place(user: Annotated[User, Depends(get_current_user)], title: Annotated[str, Form()],
                    rating: Annotated[str, Form()], description: Annotated[str, Form()], tags: Annotated[str, Form()]):
    tags = tags.split(", ")
    tags_arg = Tags(
        historical=("historical" in tags),
        entertainment=("entertainment" in tags),
        residence=("residence" in tags),
        food=("food" in tags),
        art=("art" in tags),
        architecture=("architecture" in tags),
        sport=("sport" in tags),
        green_area=("green_area" in tags),
        nature=("nature" in tags),
        recommended=("recommended" in tags),
    )
    place = Place(
        title=title,
        rating=float(rating),
        description=description,
        user_ids=[user.id],
        tags=tags_arg
    )
    place.save()
    return JSONResponse(content={f"{place.id}": f"{title}"}, status_code=200)


@app.post("/update-place-location/{place_id}", tags=["Places"],
          summary="Update place's latitude and longitude.",
          response_model=Message,
          responses={200: {"model": Message}}
          )
async def update_location(place_id: str, lat: Annotated[str, Form()], lon: Annotated[str, Form()]):
    p = Place.collection.get(place_id)
    if p:
        p.geo_point = GeoPoint(latitude=float(lat), longitude=float(lon))
        p.save()
        return JSONResponse(content={"message": f"Place {place_id} location was updated to {lat}, {lon}"},
                            status_code=200)
    else:
        return JSONResponse(content={"message": f"Place {place_id} not found"}, status_code=404)


@app.get("/get-place/{place_id}", tags=["Places"],
         summary="Fetch place from firestore.",
         response_model=PlaceSchema,
         responses={200: {"model": PlaceSchema}})
async def get_place_by_id(place_id: str):
    place = Place.collection.get(place_id)
    if place:
        return JSONResponse(content=place.to_dict(), status_code=200)
    else:
        return JSONResponse(content={"message": f"Place {place_id} not found"}, status_code=404)


@app.get("/near-places", tags=["Places"],
         summary="Show places that are located in radius of 1.5km from entered latitude and longitude",
         response_model=NearSchema,
         responses={200: {"model": NearSchema}}
         )
async def get_near_places(user_lat: float, user_lon: float):
    # check documentation and postman request in notion for this one
    search_scope = calculate_boundaries(user_lat, user_lon, 1)

    places = Place.collection \
        .filter("geo_point", ">=", search_scope["minimal_point"]) \
        .filter("geo_point", "<=", search_scope["maximal_point"]) \
        .filter("approved", "==", True) \
        .limit(10).fetch()

    result = {}

    for p in places:
        distance = round(geodesic((user_lat, user_lon), (p.geo_point.latitude, p.geo_point.longitude)).meters)
        result[str(distance)] = p.to_dict()
    result = dict(sorted(result.items(), key=lambda item: int(item[0])))
    return JSONResponse(content=result, status_code=200)


@app.post("/register", tags=["Authentication"],
          summary="Register new user using email and password.",
          response_model=Message,
          responses={200: {"model": Message}}
          )
async def register(email: Annotated[str, Form()], password: Annotated[str, Form()]):
    existing_user = User.collection.filter("email", "==", email).get()
    if existing_user:
        return JSONResponse(content={"message": "User with such credentials already exists"}, status_code=400)
    create_user(User(email=email, password=password))
    return {"message": "User registered"}


@app.post("/login", tags=["Authentication"],
          summary="Login using existing credentials.",
          response_model=LoginSchema,
          responses={200: {"model": LoginSchema}}
          )
async def login(email: Annotated[str, Form()], password: Annotated[str, Form()]):
    user = authenticate_user(email, password)
    if not user:
        return JSONResponse(content={"message": "Invalid username or password"}, status_code=401)
    access_token = create_access_token(user)
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"}, status_code=200)


@app.get("/profile", tags=["Users"],
         summary="User data using authentication.",
         response_model=UserSchema,
         responses={200: {"model": UserSchema}}
         )
async def get_user(user: Annotated[User, Depends(get_current_user)]):
    return JSONResponse(content=user.to_dict(), status_code=200)


@app.post("/update-user-nickname", tags=["Users"],
          summary="Change user's nickname.",
          response_model=Message,
          responses={200: {"model": Message}}
          )
async def update_nickname(user: Annotated[User, Depends(get_current_user)],
                          nickname: Annotated[str, Form()],
                          ):
    """
    Parameters:
    - **nickname** (str): A nickname to reset for user.

    Returns:
    - **JSONResponse**: The answer form server.
    """

    user.nickname = nickname
    user.save()
    return JSONResponse(content={"message": f"User {user.id} changed nickname to {nickname}"}, status_code=200)


@app.post("/update-user-gender", tags=["Users"],
          summary="Change user's gender.",
          response_model=Message,
          responses={200: {"model": Message}})
async def update_gender(user: Annotated[User, Depends(get_current_user)], gender: Annotated[str, Form()]):
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


@app.post("/update-user-birthdate", tags=["Users"],
          summary="Change user's birth date.",
          response_model=Message,
          responses={200: {"model": Message}})
async def update_birthdate(user: Annotated[User, Depends(get_current_user)], birth_date: Annotated[str, Form()]):
    """
    Parameters:
    - **birth_date** (str): A birth date to reset for user, format: <DD.MM.YYYY>.

    Returns:
    - **JSONResponse**: The answer form server.
    """

    birth_date = birth_date.split(".")
    user.birth_date = Date(day=birth_date[0], month=birth_date[1], year=birth_date[2])
    user.save()
    return JSONResponse(
        content={
            "message": f"User {user.id} changed his birth date to {birth_date[0]}.{birth_date[1]}.{birth_date[2]}"},
        status_code=200)


@app.post("/update-user-phone-number", tags=["Users"],
          summary="Change user's birth phone number.",
          response_model=Message,
          responses={200: {"model": Message}})
async def update_phone_number(user: Annotated[User, Depends(get_current_user)], phone_number: Annotated[str, Form()]):
    """
    Parameters:
    - **phone_number** (str): A phone number to upload

    Returns:
    - **JSONResponse**: The answer form server.
    """

    user.phone_number = phone_number
    user.save()
    return JSONResponse(
        content={
            "message": f"User {user.id} changed his phone number to {phone_number}"},
        status_code=200)


@app.post("/add-comment/{place_id}", tags=["Users"],
          summary="Add new comments for places by particular user.",
          response_model=Message,
          responses={200: {"model": Message}})
async def add_comment(user: Annotated[User, Depends(get_current_user)], text: Annotated[str, Form()],
                      place_id: str, rating: Annotated[str, Form()]):
    place = Place.collection.get(place_id)
    rating = float(rating)
    if place:
        if user.id not in place.user_ids:
            if 1 <= rating <= 5:
                new_rating = min(((place.rating * len(place.user_ids)) + (rating * 1)) / (len(place.user_ids) + 1),
                                 5.00)
                place.rating = new_rating

                user.comments.append(Comment(reference=place_id, text=text, rating=rating))
                place.user_ids.append(user.id)

                place.save()
                user.save()
                return JSONResponse(content={
                    "message": f"User {user.id} rated place {place_id} with {rating} and commented with {text}"},
                    status_code=200)
            else:
                return JSONResponse(content={"message": f"Rating {rating} is not in range [1; 5]"}, status_code=400)
        else:
            return JSONResponse(content={"message": f"User {user.id} has already rated place {place_id}"},
                                status_code=400)
    else:
        return JSONResponse(content={"message": f"Place {place_id} not found"}, status_code=404)


@app.get("/add-to-favorites/{place_id}", tags=["Users"],
         summary="Add place to user's favorites",
         response_model=Message,
         responses={200: {"model": Message}})
async def add_to_favorites(user: Annotated[User, Depends(get_current_user)], place_id: str):
    place = Place.collection.get(place_id)
    if not place:
        return JSONResponse(
            content={"message": f"Place {place_id} not found"},
            status_code=404)
    if not place.approved:
        return JSONResponse(
            content={"message": f"Place {place_id} cannot be added to favorites, since it is not approved"},
            status_code=400)
    if place_id not in user.favorite_places:
        user.favorite_places.append(place_id)
        return JSONResponse(content={"message": f"User {user.id} added place {place_id} to favorites"}, status_code=200)


# pipeline test
@app.get("/remove-from-favorites/{place_id}", tags=["Users"],
         summary="Remove place user's favorites",
         response_model=Message,
         responses={200: {"model": Message}})
async def remove_from_favorites(user: Annotated[User, Depends(get_current_user)], place_id: str):
    place = Place.collection.get(place_id)
    if not place:
        return JSONResponse(
            content={"message": f"Place {place_id} not found"},
            status_code=404)
    if place_id in user.favorite_places:
        user.favorite_places.remove(place_id)
        return JSONResponse(content={"message": f"User {user.id} removed place {place_id} from favorites"},
                            status_code=200)


@app.get("/promote-to-moderator/{user_id}", tags=["Users"],
         summary="Promote another user to moderator. Can be called only by moderator.",
         response_model=Message,
         responses={200: {"model": Message}})
async def promote_to_moderator(user: Annotated[User, Depends(get_current_user)], user_id: str):
    if user.status == "moderator":
        another_user = User.collection.get(user_id)
        if another_user:
            if another_user.status != "moderator":
                another_user.status = "moderator"
                another_user.save()
                return JSONResponse(content={"message": f"Promoted {user_id} to moderator by {user.id}"})
            else:
                return JSONResponse(content={"message": f"Cannot promote {another_user.status} to moderator"},
                                    status_code=400)
        else:
            return JSONResponse(content={"message": f"User {user_id} not found"}, status_code=404)
    else:
        return JSONResponse(content={"message": f"You are not allowed to promote users"}, status_code=403)


@app.get("/moderation-places", tags=["Moderation"],
         summary="Places that are not approved by moderators.",
         response_model=ModerationPlacesSchema,
         responses={200: {"model": ModerationPlacesSchema}})
async def moderation_places():
    # TODO protect
    result = {
        "places": []
    }
    query = (Place.collection.filter("approved", "==", False)).fetch()
    for p in query:
        result["places"].append(p.id)
    return JSONResponse(content=result, status_code=200)


@app.get("/approve-place/{place_id}", tags=["Moderation"],
         summary="Moderation place approval.",
         response_model=Message,
         responses={200: {"model": Message}})
async def approve_place(place_id: str):
    # TODO protect
    place = Place.collection.get(place_id)
    if place:
        place.approved = True
        place.save()
        return JSONResponse(content={"message": f"Place {place_id} approved"}, status_code=200)
    else:
        return JSONResponse(content={"message": f"Place {place_id} not found"}, status_code=404)


@app.get("/reject-place/{place_id}", tags=["Moderation"],
         summary="Moderation place rejection.",
         response_model=Message,
         responses={200: {"model": Message}})
async def reject_place(place_id: str):
    # TODO protect
    place = Place.collection.get(place_id)
    if place:
        if not place.approved:
            Place.collection.delete(place.id)
            return JSONResponse(content={"message": f"Place {place_id} removed"}, status_code=200)
        else:
            return JSONResponse(content={"message": f"Place {place_id} cannot be removed, it was already approved."},
                                status_code=400)
    else:
        return JSONResponse(content={"message": f"Place {place_id} not found"}, status_code=404)


@app.post("/upload-image", tags=["Media"],
          summary="Upload image on Google Cloud Storage.",
          response_model=Message,
          responses={200: {"model": Message}})
async def upload_image(user: User = Depends(get_current_user), image: bytes = File(),
                       place_id: str = Form(), image_extension: str = Form()):
    blobs = bucket.list_blobs(prefix=place_id)
    s = sum(1 for _ in blobs)
    file_name = f"{place_id}/{s}.{image_extension}"
    blob = bucket.blob(file_name)
    blob.upload_from_string(image, content_type=f"image/{image_extension}")
    return JSONResponse(content={"message": f"Photo uploaded by {user.email} to {place_id}"})


@app.get("/get-images-list/{place_id}", tags=["Media"],
         summary="Get list of image names.",
         response_model=ImageListSchema,
         responses={200: {"model": ImageListSchema}})
async def get_images(place_id: str):
    result = {
        "image_ref": []
    }
    for b in bucket.list_blobs(prefix=place_id):
        filename = str(b.name)
        result["image_ref"].append(filename[filename.find("/") + 1:len(filename)])
    return JSONResponse(content=result, status_code=200)


@app.get("/images/{place_id}/{image_name}", tags=["Media"],
         summary="Display particular image.")
async def image_by_place_id(place_id: str, image_name: str):
    blob_name = f"{place_id}/{image_name}"
    blob = bucket.get_blob(blob_name)
    if blob:
        async def stream_image():
            yield blob.download_as_bytes()

        return StreamingResponse(stream_image(), media_type=blob.content_type, status_code=200)
    else:
        return JSONResponse({"message": f"Image {blob_name} not found"}, status_code=404)


@app.get("/remove-image/{place_id}/{image_name}", tags=["Media"],
         summary="Remove image from Google Storage.",
         response_model=Message,
         responses={200: {"model": Message}})
async def remove_image(user: User = Depends(get_current_user), place_id: str = str, image_name: str = str):
    if user.status == "moderator":
        blob_name = f"{place_id}/{image_name}"
        blob = bucket.get_blob(blob_name)
        if blob:
            blob.delete()
            return JSONResponse(content={"message": f"Image {blob_name} deleted"}, status_code=200)
        else:
            return JSONResponse(content={"message": f"Image {blob_name} not found"}, status_code=404)
    else:
        return JSONResponse(content={"message": "You cannot remove images"}, status_code=403)


@app.get("/remove-image-folder/{place_id}", tags=["Media"],
         summary="Remove places image folder.",
         response_model=Message,
         responses={200: {"model": Message}})
async def remove_image_folder(user: User = Depends(get_current_user), place_id: str = str):
    if user.status == "moderator":
        folder_name = f"{place_id}/"
        for b in bucket.list_blobs(prefix=folder_name):
            b.delete()
        return JSONResponse(content={"message": f"Removed folder {place_id}/"}, status_code=200)
    else:
        return JSONResponse(content={"message": "You cannot remove images"}, status_code=403)


@app.get("/get-comments/{place_id}", tags=["Places"],
         summary="Comments attached to some place",
         response_model=GetCommentsSchema,
         responses={200: {"model": GetCommentsSchema}})
async def get_place_comments(place_id: str):
    result = {}
    place = Place.collection.get(place_id)
    if place:
        if len(place.user_ids) > 1:
            for user_id in place.user_ids:
                user = User.collection.get(user_id)
                if user and user.comments:
                    text = None
                    rating = None
                    for comment in user.comments:
                        if comment.reference == place_id:
                            text = comment.text
                            rating = comment.rating
                            break
                    if text:
                        result[user_id] = {
                            "text": text,
                            "nickname": user.nickname,
                            "rating": rating
                        }
        else:
            return JSONResponse(content={"message": f"Place {place_id} has no comments"}, status_code=400)
        return JSONResponse(content=result, status_code=200)
    else:
        return JSONResponse(content={"message": f"Place {place_id} not found"}, status_code=404)


@app.post("/search-place-with-filters", tags=["Places"],
          summary='Search for places with filters. Priority:'
                  'title>description>latitude>longitude>rating.',
          response_model=FiltersSchema,
          responses={200: {"model": FiltersSchema}}
          )
async def search_places(
        text: Optional[str] = Form(None),
        latitude: Optional[str] = Form(None),
        longitude: Optional[str] = Form(None),
        tags: Optional[str] = Form(None),
        distance: Optional[str] = Form("1.5"),
        limit: Optional[str] = Form("10")
):
    """
    Parameters:
    - **text** (str, optional): Filter by text. Result of the filter will be places with given text
     appearing in title or description. Defaults to None.
    - **latitude** (str, optional): Filter by latitude. Defaults to None.
    - **longitude** (str, optional): Filter by longitude. Defaults to None.
    - **distance** (str, optional): Filter by distance in kilometers from a location (latitude, longitude).
     Defaults to 1.5km.
    - **tags** (str, optional): Filter by tags. Format: "tag1, tag2, tag3" Defaults to None.
    - **limit** (str, optional): Limit of given results. Defaults to 10. Limit cannot be increased in case no filters
     are provided.

    Returns:
    - **dict** : A dictionary containing the search results.
    """

    # Define the priority order of filters
    filter_field = next((field for field in [text, latitude, longitude, tags] if field is not None), None)
    if filter_field == text:
        algolia_client = SearchClient.create(os.environ["ALGOLIA_APP_ID"], os.environ["ALGOLIA_API_KEY"])

        algolia_index = algolia_client.init_index('search-engine-index')

        query = algolia_index.search(text, {
            "filters": "approved:true",
            'attributesToRetrieve': [
                'objectID'
            ]
        })

        results = [Place.collection.get(obj['objectID']).to_dict() for obj in query['hits']]

    else:
        query = Place.collection.filter("approved", "==", True)
        if filter_field == latitude and longitude:
            geo_boundaries = calculate_boundaries(float(latitude), float(longitude), float(distance))
            query = query.filter("geo_point", ">=", geo_boundaries["minimal_point"]) \
                .filter("geo_point", "<=", geo_boundaries["maximal_point"])
        elif filter_field == tags:
            for k in tags.split(', '):
                query = query.filter(f"tags.{k}", "==", True)
        if not filter_field:
            limit = min(int(limit), 100)
        else:
            limit = int(limit)

        results = [el.to_dict() for el in query.fetch(limit=limit)]

    # Apply additional filters to the fetched results
    filtered_results = {}
    for result in results:
        # Apply remaining filters
        if latitude and longitude and not geodesic((latitude, longitude),
                                                   (result.geo_point.latitude,
                                                    result.geo_point.longitude)).meters <= float(distance):
            continue
        # print(result)
        if tags and any(not result['tags'][tag] for tag in tags.split(', ')):
            continue
        # If the result passes all filters, add it to the filtered results
        filtered_results[result['id']] = result

    # Return the filtered results
    return filtered_results


@app.get("/delete-place-while-adding/{place_id}", tags=["Places"],
         summary="Delete place if user wants not to uploada it.",
         response_model=Message,
         responses={200: {"model": Message}})
async def delete_place_while_adding(user: User = Depends(get_current_user), place_id: str = str):
    place = Place.collection.get(place_id)
    if place:
        if user.id in place.user_ids[0]:
            Place.collection.delete(place_id)
            return JSONResponse(content={"message": f"Place {place_id} removed"}, status_code=200)
        else:
            return JSONResponse(content={"message": f"User {user.id} cannot remove place {place_id}"}, status_code=403)
    else:
        return JSONResponse(content={"message": f"Place {place_id} not found"}, status_code=404)


@app.get("/add-tag/{place_id}/{tag}", tags=["Users"],
         summary="Add tag to a place",
         response_model=Message,
         responses={200: {"model": Message}})
async def add_tag(user: Annotated[User, Depends(get_current_user)], place_id: str, tag: str):
    place = Place.collection.get(place_id)
    if not place:
        return JSONResponse(
            content={"message": f"Place {place_id} not found"},
            status_code=404)
    if not place.approved:
        return JSONResponse(
            content={"message": f"Place {place_id} cannot be tagged, since it is not approved"},
            status_code=400)
    if user.status == "moderator":
        if place.tags and not place.tags.get_by_name(tag):
            place.tags.set_by_name(tag, True)
            return JSONResponse(content={"message": f"User {user.id} added tag {tag} to a place {place_id}"},
                                status_code=200)


@app.get("/remove-tag/{place_id}/{tag}", tags=["Users"],
         summary="Add tag to a place",
         response_model=Message,
         responses={200: {"model": Message}})
async def remove_tag(user: Annotated[User, Depends(get_current_user)], place_id: str, tag: str):
    place = Place.collection.get(place_id)
    if not place:
        return JSONResponse(
            content={"message": f"Place {place_id} not found"},
            status_code=404)
    if not place.approved:
        return JSONResponse(
            content={"message": f"Place {place_id} cannot be un-tagged, since it is not approved"},
            status_code=400)
    if user.status == "moderator":
        if place.tags and place.tags.get_by_name(tag):
            place.tags.set_by_name(tag, False)
            return JSONResponse(content={"message": f"User {user.id} removed tag {tag} to a place {place_id}"},
                                status_code=200)
