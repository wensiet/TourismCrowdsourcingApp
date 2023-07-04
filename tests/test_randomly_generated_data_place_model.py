from faker import Faker
from firebase_models import Place
from google.cloud.firestore_v1._helpers import GeoPoint as GP

fake = Faker()


def test_random_place_creation():
    title = fake.word()
    rating = fake.pyfloat(min_value=0, max_value=5)
    description = fake.text()
    user_ids = [fake.uuid4() for _ in range(fake.random_int(min=1, max=5))]
    latitude = fake.latitude()
    longitude = fake.longitude()
    approved = fake.boolean()
    image_references = [fake.url() for _ in range(fake.random_int(min=1, max=5))]

    place = Place(
        title=title,
        rating=rating,
        description=description,
        user_ids=user_ids,
        geo_point=GP(latitude=latitude, longitude=longitude),
        approved=approved,
        image_references=image_references
    )

    assert place.title == title
    assert place.rating == rating
    assert place.description == description
    assert place.user_ids == user_ids
    assert place.geo_point.latitude == latitude
    assert place.geo_point.longitude == longitude
    assert place.approved == approved
    assert place.image_references == image_references


def test_random_place_to_dict():
    place = Place(
        title=fake.word(),
        rating=fake.pyfloat(min_value=0, max_value=5),
        description=fake.text(),
        user_ids=[fake.uuid4() for _ in range(fake.random_int(min=1, max=5))],
        geo_point=GP(latitude=fake.latitude(), longitude=fake.longitude()),
        approved=fake.boolean(),
        image_references=[fake.url() for _ in range(fake.random_int(min=1, max=5))]
    )

    place_dict = place.to_dict()

    assert isinstance(place_dict, dict)
    assert "id" in place_dict
    assert place_dict["title"] == place.title
    assert place_dict["rating"] == place.rating
    assert place_dict["description"] == place.description
    assert place_dict["user_ids"] == place.user_ids
    assert place_dict["geo_point"] == f"{place.geo_point.latitude}, {place.geo_point.longitude}"
    assert place_dict["approved"] == place.approved
    assert place_dict["photo_links"] == place.image_references


def test_random_place_repr():
    title = fake.word()
    rating = fake.pyfloat(min_value=0, max_value=5)
    description = fake.text()
    user_ids = [fake.uuid4() for _ in range(fake.random_int(min=1, max=5))]
    latitude = fake.latitude()
    longitude = fake.longitude()
    approved = fake.boolean()
    image_references = [fake.url() for _ in range(fake.random_int(min=1, max=5))]

    place = Place(
        title=title,
        rating=rating,
        description=description,
        user_ids=user_ids,
        geo_point=GP(latitude=latitude, longitude=longitude),
        approved=approved,
        image_references=image_references
    )

    place_repr = repr(place)

    expected_repr = f"Place(title={title}, rating={rating}, description={description}, " \
                    f"user_ids={user_ids}, geo_point={latitude} {longitude}, " \
                    f"approved={approved}, photo_links={image_references})"

    assert place_repr == expected_repr
