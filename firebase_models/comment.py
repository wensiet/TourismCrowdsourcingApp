from fireo.fields import TextField, ReferenceField
from fireo.models import Model
from firebase_models.places import Place


class Comment(Model):
    reference = ReferenceField(Place)
    text = TextField()

    def __int__(self,
                reference=None,
                text=None,
                **kwargs):
        self.reference = reference
        self.text = text
