from faker import Faker
from firebase_models import User, Comment

fake = Faker()


def test_random_user_creation():
    email = fake.email()
    name = fake.first_name()
    surname = fake.last_name()
    gender = fake.random_element(elements=[True, False])
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=60)
    password = fake.password()
    status = fake.random_element(elements=["active", "inactive"])
    users_score = round(fake.pyfloat(min_value=1.0, max_value=5.0, right_digits=2), 2)
    comments = [
        Comment(reference="ref1", text="Great user"),
        Comment(reference="ref2", text="Awesome!")
    ]

    user = User(
        email=email,
        name=name,
        surname=surname,
        gender=gender,
        birth_date=birth_date,
        password=password,
        status=status,
        users_score=users_score,
        comments=comments,
    )

    assert user.email == email
    assert user.name == name
    assert user.surname == surname
    assert user.gender == gender
    assert user.birth_date == birth_date
    assert user.password == password
    assert user.status == status
    assert user.users_score == users_score
    assert len(user.comments) == 2
    assert user.comments[0].reference == "ref1"
    assert user.comments[0].text == "Great user"
    assert user.comments[1].reference == "ref2"
    assert user.comments[1].text == "Awesome!"


def test_random_user_to_dict():
    email = fake.email()
    name = fake.first_name()
    surname = fake.last_name()
    gender = fake.random_element(elements=[True, False])
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=60)
    password = fake.password()
    status = fake.random_element(elements=["active", "inactive"])
    users_score = round(fake.pyfloat(min_value=1.0, max_value=5.0, right_digits=2), 2)
    comments = [
        Comment(reference="ref1", text="Great user"),
        Comment(reference="ref2", text="Awesome!")
    ]

    user = User(
        email=email,
        name=name,
        surname=surname,
        gender=gender,
        birth_date=birth_date,
        password=password,
        status=status,
        users_score=users_score,
        comments=comments,
    )

    user_dict = user.to_dict()

    expected_dict = result = {
            "name": name,
            "surname": surname,
            "email": email,
            "gender": gender,
            "birth_date": {
                "year": birth_date.year,
                "month": birth_date.month,
                "day": birth_date.day
            },
            "password": password,
            "status": status,
            "users_score": users_score,
            "comments": [{
                "reference": el.reference,
                "text": el.text
            } for el in comments]
        }

    assert user_dict == expected_dict


def test_random_user_repr():
    email = fake.email()
    name = fake.first_name()
    surname = fake.last_name()
    gender = fake.random_element(elements=[True, False])
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=60)
    password = fake.password()
    status = fake.random_element(elements=["active", "inactive"])
    users_score = round(fake.pyfloat(min_value=1.0, max_value=5.0, right_digits=2), 2)
    comments = [
        Comment(reference="ref1", text="Great user"),
        Comment(reference="ref2", text="Awesome!")
    ]

    user = User(
        email=email,
        name=name,
        surname=surname,
        gender=gender,
        birth_date=birth_date,
        password=password,
        status=status,
        users_score=users_score,
        comments=comments,
    )

    user_repr = repr(user)

    expected_repr = f"User(email={email}, name={name} {surname}, gender={'male' if gender else 'female'}, " \
               f"birth date={birth_date.year}.{birth_date.month}.{birth_date.day}, users score={users_score})"
