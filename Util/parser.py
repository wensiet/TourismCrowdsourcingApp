from firebase_models import Place, User, Date, Comment
import json


def parse_place(data: dict) -> Place:
    title = data["title"]
    rating = float(data["rating"])
    description = data["description"]
    interacted_users = data["interacted_users"].split(" ")
    geo_data = [float(d) for d in data["geo_data"].split(" ")]
    approved = bool(data["approved"])
    photo_links = data["photo_links"].split(" ")

    queried_place = Place(title=title,
                          rating=rating,
                          description=description,
                          interacted_users=interacted_users,
                          geo_data=geo_data,
                          approved=approved,
                          photo_links=photo_links)

    return queried_place


def parse_user(data: dict) -> User:
    name = data["name"]
    surname = data["surname"]
    email = data["email"]
    gender = bool(data["gender"])
    birth_date = list(map(int, data["birth_date"].split(" ")))
    password = data["password"]
    status = data["status"]
    users_score = float(data["users_score"])
    comments_json = json.loads(data["comments"])
    comments = []
    for el in comments_json:
        comments.append(Comment(**el))

    queried_user = User(name=name,
                        surname=surname,
                        email=email,
                        gender=gender,
                        birth_date=Date(year=birth_date[0], month=birth_date[1], day=birth_date[2]),
                        password=password,
                        status=status,
                        users_score=users_score,
                        comments=comments)
    return queried_user
