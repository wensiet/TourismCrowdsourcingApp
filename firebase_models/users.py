from fireo.models import Model, NestedModel
from fireo.fields import TextField, BooleanField, ListField
from firebase_models.date import Date
from firebase_models.comment import Comment


class User(Model):
    email: TextField = TextField()
    nickname: TextField = TextField()
    gender: BooleanField = BooleanField()
    birth_date: NestedModel = NestedModel(Date)
    password: TextField = TextField()
    status: TextField = TextField()
    comments: ListField = ListField(NestedModel(Comment))
    phone_number: TextField = TextField()
    favorite_places: ListField(TextField())

    def __init__(
            self,
            email: str = None,
            nickname: str = None,
            gender: str = None,
            birth_date: str = None,
            password: str = None,
            status: str = "user",
            comments: list[Comment] = ListField(NestedModel(Comment)).empty_value_attributes,
            phone_number: str = None,
            favorite_places: list[str] = ListField(TextField()).empty_value_attributes,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.email = email
        self.nickname = nickname
        self.gender = gender
        self.birth_date = birth_date
        self.password = password
        self.status = status
        self.comments = comments
        self.phone_number = phone_number
        self.favorite_places = favorite_places

    def __repr__(self):
        return f"User(email={self.email}, nickname={self.nickname}, gender={'male' if self.gender else 'female'}, " \
               f"birth date={self.birth_date.__repr__() if self.birth_date else ''})"

    def to_dict(self):
        result = {
            "id": self.id,
            "nickname": self.nickname,
            "email": self.email,
            "gender": self.gender,
            "birth_date": self.birth_date.__repr__() if self.birth_date else None,
            "password": self.password,
            "status": self.status,
            "comments": [el.to_dict() for el in self.comments] if self.comments else None,
            "phone_number": self.phone_number,
            "favorite_places": self.favorite_places
        }

        return result
