from exceptions import EssentialInfoAbsent
from google.cloud.firestore_v1._helpers import GeoPoint as GP


def places_init_validator(func):
    def wrapper(*args, **kwargs):
        for m in ["title", "geo_point"]:
            if m not in kwargs:
                raise EssentialInfoAbsent(f"Mandatory info about place ({m}) is not stated")

        title = kwargs["title"]
        geo_point = kwargs["geo_point"]

        if not isinstance(title, str):
            raise ValueError(f"Title has to be str, got {type(title)} instead.")

        if not isinstance(geo_point, GP):
            raise ValueError(f"Geo_point has to be GeoPoint, got {type(geo_point)} instead.")

        if "rating" in kwargs:
            rating = kwargs["rating"]
            if not isinstance(rating, float):
                raise ValueError(f"Rating has to be float, got {type(rating)} instead.")

        if "description" in kwargs:
            description = kwargs["description"]
            if not isinstance(description, str):
                raise ValueError(f"Description has to be str, got {type(description)} instead.")

        if "users_ids" in kwargs:
            users_ids = kwargs["users_ids"]
            if not isinstance(users_ids, list) or any(not isinstance(x, str) for x in users_ids):
                raise ValueError(f"Users_ids has to be list of str, got {type(users_ids)} instead.")

        if "approved" in kwargs:
            approved = kwargs["approved"]
            if not isinstance(approved, bool):
                raise ValueError(f"Approved has to be bool, got {type(approved)} instead.")

        if "image_references" in kwargs:
            image_references = kwargs["image_references"]
            if not isinstance(image_references, list) or any(not isinstance(x, str) for x in image_references):
                raise ValueError(f"Image_references has to be list of str, got {type(image_references)} instead.")

        return func(*args, **kwargs)

    return wrapper
