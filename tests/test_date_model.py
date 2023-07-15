# test_date_model.py
from firebase_models import Date


def test_date_creation():
    date = Date(day=1, month=1, year=1970)
    assert date.day == 1
    assert date.month == 1
    assert date.year == 1970


def test_date_to_dict():
    date = Date(day=1, month=1, year=1970)
    expected_dict = {
        "day": 1,
        "month": 1,
        "year": 1970
    }
    assert date.to_dict() == expected_dict


def test_date_representation():
    date = Date(day=1, month=1, year=1970)
    expected_repr = "1.1.1970"
    assert date.__repr__() == expected_repr
