from firebase_models import User, Comment, Date


def test_user_creation_static():
    email = "test@example.com"
    nickname = "John Doe"
    gender = True
    birth_date = Date(year=1990, month=5, day=20)
    password = "password123"
    status = "active"
    comments = [Comment(reference="ref1", text="Great user", rating=4),
                Comment(reference="ref2", text="Awesome!", rating=5)]
    phone_number = "+79285034717"
    favorite_places = ["place1", "place2"]

    user = User(
        email=email,
        nickname=nickname,
        gender=gender,
        birth_date=birth_date,
        password=password,
        status=status,
        comments=comments,
        phone_number=phone_number,
        favorite_places=favorite_places
    )

    assert user.email == email
    assert user.nickname == nickname
    assert user.gender == gender
    assert user.birth_date == birth_date
    assert user.password == password
    assert user.status == status
    assert len(user.comments) == 2
    assert user.comments[0].reference == "ref1"
    assert user.comments[0].text == "Great user"
    assert user.comments[1].reference == "ref2"
    assert user.comments[1].text == "Awesome!"
    assert user.comments[0].rating == 4
    assert user.comments[1].rating == 5
    assert user.phone_number == phone_number
    assert user.favorite_places[0] == "place1"
    assert user.favorite_places[1] == "place2"


def test_static_user_to_dict():
    user = User(
        email="test@example.com",
        nickname="John Doe",
        gender=True,
        birth_date=Date(year=1990, month=1, day=1),
        password="password123",
        status="active",
        comments=[
            Comment(reference="comment1", text="Great user!", rating=4),
            Comment(reference="comment2", text="Very helpful.", rating=5)
        ],
        phone_number="+79285034717",
        favorite_places=["place1", "place2"]
    )

    user_dict = user.to_dict()

    expected_dict = {
        "id": user.id,
        "nickname": "John Doe",
        "email": "test@example.com",
        "gender": True,
        "birth_date": "1.1.1990",
        "password": "password123",
        "status": "active",
        "comments": [
            {"reference": "comment1", "text": "Great user!", "rating": 4},
            {"reference": "comment2", "text": "Very helpful.", "rating": 5}
        ],
        "phone_number": "+79285034717",
        "favorite_places": ["place1", "place2"]
    }

    assert user_dict == expected_dict


def test_static_user_repr():
    user = User(
        email="test@example.com",
        nickname="John Doe",
        gender=True,
        birth_date=Date(year=1990, month=1, day=1),
        password="password123",
        status="active",
        comments=[
            Comment(reference="comment1", text="Great user!", rating=4),
            Comment(reference="comment2", text="Very helpful.", rating=5)
        ]
    )

    user_repr = repr(user)

    expected_repr = "User(email=test@example.com, nickname=John Doe, gender=male, birth date=1.1.1990)"

    assert user_repr == expected_repr
