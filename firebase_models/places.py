from fireo.models import Model
from fireo.fields import TextField, ListField, NumberField, BooleanField, GeoPoint
from google.cloud.firestore_v1._helpers import GeoPoint as GP
from typing import List


class Place(Model):
    title: TextField = TextField()
    rating: NumberField = NumberField()
    description: TextField = TextField()
    interacted_users: ListField = ListField()
    geo_data: GeoPoint = GeoPoint()
    approved: BooleanField = BooleanField()
    photo_links: ListField = ListField()

    def __init__(
            self,
            title: str = None,
            rating: float = None,
            description: str = None,
            interacted_users: List[str] = None,
            geo_data: GP = None,
            approved: bool = None,
            photo_links: List[str] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.title = title
        self.rating = rating
        self.description = description
        self.interacted_users = interacted_users
        self.geo_data = geo_data
        self.approved = approved
        self.photo_links = photo_links

    def __repr__(self):
        return f"Place(title={self.title}, rating={self.rating}, description={self.description}, " \
               f"interacted_users={self.interacted_users}, geo_data={self.geo_data.latitude} {self.geo_data.longitude}, " \
               f"approved={self.approved}, photo_links={self.photo_links})"

    def to_dict(self):
        result = {
            "title": self.title,
            "rating": self.rating,
            "description": self.description,
            "interacted_users": self.interacted_users,
            "geo_data": [self.geo_data.latitude, self.geo_data.longitude],
            "approved": self.approved,
            "photo_links": self.photo_links
        }

        return result
