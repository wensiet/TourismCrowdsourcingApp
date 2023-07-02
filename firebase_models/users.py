from fireo.models import Model, NestedModel
from fireo.fields import TextField, NumberField, BooleanField, ListField
from firebase_models.date import Date
from firebase_models.comment import Comment


class User(Model):
    email: TextField = TextField()
    name: TextField = TextField()
    surname: TextField = TextField()
    gender: BooleanField = BooleanField()
    birth_date: NestedModel = NestedModel(Date)
    password: TextField = TextField()
    status: TextField = TextField()
    users_score: NumberField = NumberField()
    comments: ListField = ListField(NestedModel(Comment))


    def __init__(
            self,
            email=None,
            name=None,
            surname=None,
            gender=None,
            birth_date=None,
            password=None,
            status=None,
            users_score=None,
            comments=None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.email = email
        self.name = name
        self.surname = surname
        self.gender = gender
        self.birth_date = birth_date
        self.password = password
        self.status = status
        self.users_score = users_score
        self.comments = comments

    def __repr__(self):
        return f"User(email={self.email}, name={self.name} {self.surname}, gender={'male' if self.gender else 'female'}, " \
               f"birth date={self.birth_date.year}.{self.birth_date.month}.{self.birth_date.day}, users score={self.users_score})"

    def to_dict(self):
        result = {
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "gender": self.gender,
            "birth_date": {
                "year": self.birth_date.year,
                "month": self.birth_date.month,
                "day": self.birth_date.day
            },
            "password": self.password,
            "status": self.status,
            "users_score": self.users_score,
            "comments": [{
                "reference": el.reference,
                "text": el.text
            } for el in self.comments]
        }

        return result
