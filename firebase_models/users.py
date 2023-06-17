from enum import Enum

from fireo.models import Model
from fireo.fields import TextField, ListField, NumberField, BooleanField, GeoPoint, Field, ReferenceField
from google.cloud.firestore_v1._helpers import GeoPoint as GP
from typing import List


class Date(Field):
    year: NumberField
    month: NumberField
    day: NumberField

    def __int__(self,
                year: int,
                month: int,
                day: int):
        self.year = year
        self.month = month
        self.day = day


class Comments(Field):
    comments: list[dict[str: ReferenceField, str: TextField]]

    def __int__(self, comments):
        self.comments = comments


class User(Model):
    email: TextField = TextField()
    name: TextField = TextField(column_name="first name")
    surname: TextField = TextField()
    gender: BooleanField = BooleanField()
    birthDate: Date = Date()
    password: TextField = TextField()
    status: TextField = TextField()
    usersScore: NumberField = NumberField()
    comments: Comments = Comments()

    def __init__(
            self,
            email: str = None,
            name: str = None,
            surname: str = None,
            gender: bool = None,
            birth_date: Date = None,
            password: str = None,
            status: str = None,
            users_score: float = None,
            comments: Comments = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.email = email
        self.name = name
        self.surname = surname
        self.gender = gender
        self.birthDate = birth_date
        self.password = password
        self.status = status
        self.usersScore = users_score
        self.comments = comments

    def __repr__(self):
        return f"Place(email={self.email}, name={self.name} {self.surname}, gender={'male' if self.gender else 'female'}, " \
               f"birth date={self.birthDate.year}.{self.birthDate.month}.{self.birthDate.day}, users score={self.usersScore})"

    def to_dict(self):
        pass
