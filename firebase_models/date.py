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

    def __repr__(self):
        return f"{self.day}.{self.month}.{self.year}"

    def to_dict(self):
        return {
            "day": self.day,
            "month": self.month,
            "year": self.year
        }
