from firebase_models import Place, User, Date, Comments


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
    birth_date = map(int, data["birthDate"].split(" "))
    password = data["password"]
    status = data["status"]
    users_score = float(data["usersScore"])
    print(data["comments"])
    comments = [dict(x) if len(x) > 0 else {} for x in data["comments"].split(" ")]

    queried_user = User(name=name,
                        surname=surname,
                        email=email,
                        gender=gender,
                        birthDate=Date(*birth_date),
                        password=password,
                        status=status,
                        usersScore=users_score,
                        comments=Comments(comments))
    return queried_user

# email: TextField = TextField()
#     name: TextField = TextField()
#     surname: TextField = TextField()
#     gender: BooleanField = BooleanField()
#     birthDate: Date = Date()
#     password: TextField = TextField()
#     status: TextField = TextField()
#     usersScore: NumberField = NumberField()
#     comments: Comment = Comment()
