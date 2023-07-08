from firebase_models import User, Comment, Date


def test_user_creation_static():
    email = "test@example.com"
    nickname = "John Doe"
    gender = True
    birth_date = Date(year=1990, month=5, day=20)
    password = "password123"
    status = "active"
    comments = [Comment(reference="ref1", text="Great user"), Comment(reference="ref2", text="Awesome!")]

    user = User(
        email=email,
        nickname=nickname,
        gender=gender,
        birth_date=birth_date,
        password=password,
        status=status,
        comments=comments,
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


def test_static_user_to_dict():
    user = User(
        email="test@example.com",
        nickname="John Doe",
        gender=True,
        birth_date=Date(year=1990, month=1, day=1),
        password="password123",
        status="active",
        comments=[
            Comment(reference="comment1", text="Great user!"),
            Comment(reference="comment2", text="Very helpful.")
        ]
    )

    user_dict = user.to_dict()

    expected_dict = {
        "nickname": "John Doe",
        "email": "test@example.com",
        "gender": True,
        "birth_date": {
            "year": 1990,
            "month": 1,
            "day": 1
        },
        "password": "password123",
        "status": "active",
        "comments": [
            {"reference": "comment1", "text": "Great user!"},
            {"reference": "comment2", "text": "Very helpful."}
        ]
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
            Comment(reference="comment1", text="Great user!"),
            Comment(reference="comment2", text="Very helpful.")
        ]
    )

    user_repr = repr(user)

    expected_repr = "User(email=test@example.com, nickname=John Doe, gender=male, birth date=1990.1.1, users score=4.5)"

    assert user_repr == expected_repr
