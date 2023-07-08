from faker import Faker
from firebase_models import User, Comment

fake = Faker()


def test_random_user_creation():
    email = fake.email()
    nickname = fake.first_name()
    gender = fake.random_element(elements=[True, False])
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=60)
    password = fake.password()
    status = fake.random_element(elements=["active", "inactive"])
    comments = [
        Comment(reference="ref1", text="Great user"),
        Comment(reference="ref2", text="Awesome!")
    ]

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


def test_random_user_to_dict():
    email = fake.email()
    nickname = fake.first_name()
    gender = fake.random_element(elements=[True, False])
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=60)
    password = fake.password()
    status = fake.random_element(elements=["active", "inactive"])
    comments = [
        Comment(reference="ref1", text="Great user"),
        Comment(reference="ref2", text="Awesome!")
    ]

    user = User(
        email=email,
        nickname=nickname,
        gender=gender,
        birth_date=birth_date,
        password=password,
        status=status,
        comments=comments,
    )

    user_dict = user.to_dict()

    expected_dict = result = {
        "nickname": nickname,
        "email": email,
        "gender": gender,
        "birth_date": {
            "year": birth_date.year,
            "month": birth_date.month,
            "day": birth_date.day
        },
        "password": password,
        "status": status,
        "comments": [{
            "reference": el.reference,
            "text": el.text
        } for el in comments]
    }

    assert user_dict == expected_dict


def test_random_user_repr():
    email = fake.email()
    nickname = fake.first_name()
    gender = fake.random_element(elements=[True, False])
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=60)
    password = fake.password()
    status = fake.random_element(elements=["active", "inactive"])
    comments = [
        Comment(reference="ref1", text="Great user"),
        Comment(reference="ref2", text="Awesome!")
    ]

    user = User(
        email=email,
        nickname=nickname,
        gender=gender,
        birth_date=birth_date,
        password=password,
        status=status,
        comments=comments,
    )

    user_repr = repr(user)

    expected_repr = f"User(email={email}, nickname={nickname}, gender={'male' if gender else 'female'}, " \
                    f"birth date={birth_date.year}.{birth_date.month}.{birth_date.day})"

    assert user_repr == expected_repr
