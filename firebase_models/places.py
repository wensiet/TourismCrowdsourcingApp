from fireo.models import Model, NestedModel
from fireo.fields import TextField, ListField, NumberField, BooleanField, GeoPoint
from firebase_models.tags import Tags
from google.cloud.firestore_v1._helpers import GeoPoint as GP
from typing import List


class Place(Model):
    title: TextField = TextField()
    rating: NumberField = NumberField()
    description: TextField = TextField()
    user_ids: ListField = ListField(TextField())
    geo_point: GeoPoint = GeoPoint()
    approved: BooleanField = BooleanField()
    tags: NestedModel = NestedModel(Tags)

    def __init__(
            self,
            title: str = None,
            rating: float = None,
            description: str = None,
            user_ids: List[str] = ListField(TextField).empty_value_attributes,
            geo_point: GP = None,
            approved: bool = False,
            tags: Tags = Tags(),
            **kwargs
    ):
        super().__init__(**kwargs)
        self.title = title
        self.rating = rating
        self.description = description
        self.user_ids = user_ids
        self.geo_point = geo_point
        self.approved = approved
        self.tags = tags

    def __repr__(self):
        return f"Place(title={self.title}, rating={self.rating}, description={self.description}, " \
               f"user_ids={self.user_ids}, " \
               f"geo_point={self.geo_point.latitude if self.geo_point else None}," \
               f" {self.geo_point.longitude if self.geo_point else None}, " \
               f"approved={self.approved}, " \
               f"tags={self.tags.__repr__()})"

    def to_dict(self):
        result = {
            "id": self.id,
            "title": self.title,
            "rating": self.rating,
            "description": self.description,
            "user_ids": self.user_ids,
            "geo_point": f"{self.geo_point.latitude if self.geo_point else None}, "
                         f"{self.geo_point.longitude if self.geo_point else None}",
            "approved": self.approved,
            "tags": self.tags.to_dict() if self.tags else None
        }

        return result
