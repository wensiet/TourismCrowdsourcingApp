import pytest
from exceptions import EssentialInfoAbsent
from firebase_models import User, Date


def test_valid_input():
    user = User(
        email="test@example.com",
        name="John",
        surname="Doe",
        gender=True,
        birth_date=Date(year=1990, month=1, day=1),
        password="password",
        status="active",
        users_score=4.5,
        comments=["Comment 1", "Comment 2"]
    )
    assert isinstance(user, User)


def test_missing_name():
    with pytest.raises(EssentialInfoAbsent):
        User(email="test@example.com", surname="Doe", gender=True, birth_date=Date(year=1990, month=1, day=1), password="password",
             status="active", users_score=4.5, comments=["Comment 1", "Comment 2"])


def test_missing_password():
    with pytest.raises(EssentialInfoAbsent):
        User(email="test@example.com", name="John", surname="Doe", gender=True, birth_date=Date(year=1990, month=1, day=1),
             status="active", users_score=4.5, comments=["Comment 1", "Comment 2"])


def test_missing_status():
    with pytest.raises(EssentialInfoAbsent):
        User(email="test@example.com", name="John", surname="Doe", gender=True, birth_date=Date(year=1990, month=1, day=1),
             password="password", users_score=4.5, comments=["Comment 1", "Comment 2"])


def test_invalid_name_type():
    with pytest.raises(ValueError):
        User(email="test@example.com", name=123, surname="Doe", gender=True, birth_date=Date(year=1990, month=1, day=1),
             password="password", status="active", users_score=4.5, comments=["Comment 1", "Comment 2"])


def test_invalid_password_type():
    with pytest.raises(ValueError):
        User(email="test@example.com", name="John", surname="Doe", gender=True, birth_date=Date(year=1990, month=1, day=1),
             password=123, status="active", users_score=4.5, comments=["Comment 1", "Comment 2"])


def test_invalid_status_type():
    with pytest.raises(ValueError):
        User(email="test@example.com", name="John", surname="Doe", gender=True, birth_date=Date(year=1990, month=1, day=1),
             password="password", status=123, users_score=4.5, comments=["Comment 1", "Comment 2"])


def test_invalid_users_score_type():
    with pytest.raises(ValueError):
        User(email="test@example.com", name="John", surname="Doe", gender=True, birth_date=Date(year=1990, month=1, day=1),
             password="password", status="active", users_score="4.5", comments=["Comment 1", "Comment 2"])


def test_invalid_surname_type():
    with pytest.raises(ValueError):
        User(email="test@example.com", name="John", surname=123, gender=True, birth_date=Date(year=1990, month=1, day=1),
             password="password", status="active", users_score=4.5, comments=["Comment 1", "Comment 2"])


def test_invalid_comments_type():
    with pytest.raises(ValueError):
        User(email="test@example.com", name="John", surname="Doe", gender=True, birth_date=Date(year=1990, month=1, day=1),
             password="password", status="active", users_score=4.5, comments="Comment")


def test_invalid_comments_element_type():
    with pytest.raises(ValueError):
        User(email="test@example.com", name="John", surname="Doe", gender=True, birth_date=Date(year=1990, month=1, day=1),
             password="password", status="active", users_score=4.5, comments=["Comment 1", 2])


def test_invalid_birth_date_type():
    with pytest.raises(ValueError):
        User(email="test@example.com", name="John", surname="Doe", gender=True, birth_date="1990-01-01",
             password="password", status="active", users_score=4.5, comments=["Comment 1", "Comment 2"])


def test_invalid_gender_type():
    with pytest.raises(ValueError):
        User(email="test@example.com", name="John", surname="Doe", gender="true", birth_date=Date(year=1990, month=1, day=1),
             password="password", status="active", users_score=4.5, comments=["Comment 1", "Comment 2"])


def test_invalid_email_type():
    with pytest.raises(ValueError):
        User(email=123, name="John", surname="Doe", gender=True, birth_date=Date(year=1990, month=1, day=1), password="password",
             status="active", users_score=4.5, comments=["Comment 1", "Comment 2"])


def test_invalid_email_format():
    with pytest.raises(ValueError):
        User(email="test@example", name="John", surname="Doe", gender=True, birth_date=Date(year=1990, month=1, day=1),
             password="password", status="active", users_score=4.5, comments=["Comment 1", "Comment 2"])
