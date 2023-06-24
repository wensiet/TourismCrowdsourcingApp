from fireo.fields import NumberField
from fireo.models import Model


class Date(Model):
    year = NumberField()
    month = NumberField()
    day = NumberField()

    def __int__(self,
                year: int,
                month: int,
                day: int,
                **kwargs):
        self.year = year
        self.month = month
        self.day = day
