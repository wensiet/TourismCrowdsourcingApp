# test_place_model.py
from firebase_models import Place, Tags
from google.cloud.firestore_v1._helpers import GeoPoint as GP


def test_place_creation():
    place = Place(title="Test Place", rating=4.5)
    assert place.title == "Test Place"
    assert place.rating == 4.5


def test_place_to_dict():
    place = Place(
        id="123",
        title="Test Place",
        rating=4.5,
        description="Sample description",
        user_ids=["user1", "user2"],
        geo_point=GP(latitude=123.456, longitude=987.654),
        approved=True,
        tags=Tags()
    )
    expected_dict = {
        "id": "123",
        "title": "Test Place",
        "rating": 4.5,
        "description": "Sample description",
        "user_ids": ["user1", "user2"],
        "geo_point": "123.456, 987.654",
        "approved": True,
        "tags": {
            "historical": False,
            "entertainment": False,
            "residence": False,
            "food": False,
            "art": False,
            "architecture": False,
            "sport": False,
            "green_area": False,
            "nature": False,
            "recommended": False
        }
    }
    assert place.to_dict() == expected_dict


def test_place_representation():
    place = Place(
        title="Test Place",
        rating=4.5,
        description="Sample description",
        user_ids=["user1", "user2"],
        geo_point=GP(latitude=123.456, longitude=987.654),
        approved=True,
        tags=Tags()
    )
    expected_repr = "Place(title=Test Place, rating=4.5, description=Sample description, " \
                    "user_ids=['user1', 'user2'], geo_point=123.456, 987.654, approved=True, tags=)"
    assert place.__repr__() == expected_repr
