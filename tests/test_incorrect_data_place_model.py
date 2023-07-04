import pytest
from exceptions import EssentialInfoAbsent
from firebase_models import Place
from google.cloud.firestore_v1._helpers import GeoPoint as GP


def test_valid_input():
    place = Place(title="Title", rating=4.5, description="Description", users_ids=["1", "2"], geo_point=GP(1, 2),
                  approved=True, image_references=["image1.jpg"])
    assert isinstance(place, Place)


def test_missing_title():
    with pytest.raises(EssentialInfoAbsent):
        Place(rating=4.5, description="Description", users_ids=["1", "2"], geo_point=GP(1, 2), approved=True,
              image_references=["image1.jpg"])


def test_missing_geo_point():
    with pytest.raises(EssentialInfoAbsent):
        Place(title="Title", rating=4.5, description="Description", users_ids=["1", "2"], approved=True,
              image_references=["image1.jpg"])


def test_invalid_title_type():
    with pytest.raises(ValueError):
        Place(title=123, rating=4.5, description="Description", users_ids=["1", "2"], geo_point=GP(1, 2), approved=True,
              image_references=["image1.jpg"])


def test_invalid_geo_point_type():
    with pytest.raises(ValueError):
        Place(title="Title", rating=4.5, description="Description", users_ids=["1", "2"], geo_point="1,2", approved=True,
              image_references=["image1.jpg"])


def test_invalid_rating_type():
    with pytest.raises(ValueError):
        Place(title="Title", rating="4.5", description="Description", users_ids=["1", "2"], geo_point=GP(1, 2),
              approved=True, image_references=["image1.jpg"])


def test_invalid_description_type():
    with pytest.raises(ValueError):
        Place(title="Title", rating=4.5, description=123, users_ids=["1", "2"], geo_point=GP(1, 2), approved=True,
              image_references=["image1.jpg"])


def test_invalid_users_ids_type():
    with pytest.raises(ValueError):
        Place(title="Title", rating=4.5, description="Description", users_ids="1,2", geo_point=GP(1, 2), approved=True,
              image_references=["image1.jpg"])


def test_invalid_user_id_element_type():
    with pytest.raises(ValueError):
        Place(title="Title", rating=4.5, description="Description", users_ids=["1", 2], geo_point=GP(1, 2),
              approved=True, image_references=["image1.jpg"])


def test_invalid_approved_type():
    with pytest.raises(ValueError):
        Place(title="Title", rating=4.5, description="Description", users_ids=["1", "2"], geo_point=GP(1, 2),
              approved="true", image_references=["image1.jpg"])


def test_invalid_image_references_type():
    with pytest.raises(ValueError):
        Place(title="Title", rating=4.5, description="Description", users_ids=["1", "2"], geo_point=GP(1, 2),
              approved=True, image_references="image1.jpg")


def test_invalid_image_reference_element_type():
    with pytest.raises(ValueError):
        Place(title="Title", rating=4.5, description="Description", users_ids=["1", "2"], geo_point=GP(1, 2),
              approved=True, image_references=["image1.jpg", 2])
