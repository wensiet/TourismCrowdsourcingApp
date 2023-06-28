from fireo.models import Model
from fireo.fields import TextField, ListField, NumberField, BooleanField, GeoPoint
from google.cloud.firestore_v1._helpers import GeoPoint as GP
from typing import List


class Place(Model):
    title: TextField = TextField()
    rating: NumberField = NumberField()
    description: TextField = TextField()
    users_ids: ListField = ListField()
    geo_point: GeoPoint = GeoPoint()
    approved: BooleanField = BooleanField()
    image_references: ListField = ListField()

    def __init__(
            self,
            title: str = None,
            rating: float = None,
            description: str = None,
            user_ids: List[str] = None,
            geo_point: GP = None,
            approved: bool = None,
            image_references: List[str] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.title = title
        self.rating = rating
        self.description = description
        self.users_ids = user_ids
        self.geo_point = geo_point
        self.approved = approved
        self.image_references = image_references

    def __repr__(self):
        return f"Place(title={self.title}, rating={self.rating}, description={self.description}, " \
               f"interacted_users={self.users_ids}, geo_data={self.geo_point} {self.geo_point}, " \
               f"approved={self.approved}, photo_links={self.image_references})"

    def to_dict(self):
        result = {
            "id": self.id,
            "title": self.title,
            "rating": self.rating,
            "description": self.description,
            "interacted_users": self.users_ids,
            "geo_data": f"{self.geo_point.latitude}, {self.geo_point.longitude}",
            "approved": self.approved,
            "photo_links": self.image_references
        }

        return result