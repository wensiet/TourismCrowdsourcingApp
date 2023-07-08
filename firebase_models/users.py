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

    def __init__(
            self,
            email=None,
            nickname=None,
            gender=None,
            birth_date=None,
            password=None,
            status=None,
            comments=None,
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

    def __repr__(self):
        return f"User(email={self.email}, nickname={self.nickname}, gender={'male' if self.gender else 'female'}, " \
               f"birth date={self.birth_date.year}.{self.birth_date.month}.{self.birth_date.day})"

    def to_dict(self):
        result = {
            "nickname": self.nickname,
            "email": self.email,
            "gender": self.gender,
            "birth_date": f"{self.birth_date.day}.{self.birth_date.month}.{self.birth_date.year}",
            "password": self.password,
            "status": self.status,
            "comments": [{
                "reference": el.reference,
                "text": el.text
            } for el in self.comments]
        }

        return result
