from fireo.fields import TextField, NumberField
from fireo.models import Model


class Comment(Model):
    reference = TextField()
    text = TextField()
    rating = NumberField()

    def __int__(self,
                reference=None,
                text=None,
                rating=None,
                **kwargs):
        self.reference = reference
        self.text = text
        self.rating = rating

    def to_dict(self):
        return {
            "reference": self.reference,
            "text": self.text,
            "rating": self.rating
        }

    def __repr__(self):
        return f"Comment(reference={self.reference}, text={self.text}, rating={self.rating})"
