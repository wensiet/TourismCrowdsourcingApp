from fireo.fields import BooleanField
from fireo.models import Model


class Tags(Model):
    historical: BooleanField = BooleanField()
    entertainment: BooleanField = BooleanField()
    residence: BooleanField = BooleanField()
    food: BooleanField = BooleanField()
    art: BooleanField = BooleanField()
    architecture: BooleanField = BooleanField()
    sport: BooleanField = BooleanField()
    green_area: BooleanField = BooleanField()
    nature: BooleanField = BooleanField()
    recommended: BooleanField = BooleanField()

    def __init__(self,
                 historical: bool = False,
                 entertainment: bool = False,
                 residence: bool = False,
                 food: bool = False,
                 art: bool = False,
                 architecture: bool = False,
                 sport: bool = False,
                 green_area: bool = False,
                 nature: bool = False,
                 recommended: bool = False,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.historical = historical
        self.entertainment = entertainment
        self.residence = residence
        self.food = food
        self.art = art
        self.architecture = architecture
        self.sport = sport
        self.green_area = green_area
        self.nature = nature
        self.recommended = recommended

    def __repr__(self):
        res = " "
        if self.historical:
            res += 'historical '
        if self.entertainment:
            res += 'entertainment '
        if self.residence:
            res += 'residence '
        if self.food:
            res += 'food '
        if self.art:
            res += 'art '
        if self.architecture:
            res += 'architecture '
        if self.sport:
            res += 'sport '
        if self.green_area:
            res += 'green_area '
        if self.nature:
            res += 'nature '
        if self.recommended:
            res += 'recommended '
        return res[:-1]

    def to_dict(self):
        return {
            "historical": self.historical,
            "entertainment": self.entertainment,
            "residence": self.residence,
            "food": self.food,
            "art": self.art,
            "architecture": self.architecture,
            "sport": self.sport,
            "green_area": self.green_area,
            "nature": self.nature,
            "recommended": self.recommended
        }

    def get_by_name(self, name: str):
        if name == "historical":
            return self.historical
        if name == "entertainment":
            return self.entertainment
        if name == "residence":
            return self.residence
        if name == "food":
            return self.food
        if name == "art":
            return self.art
        if name == "architecture":
            return self.architecture
        if name == "sport":
            return self.sport
        if name == "green_area":
            return self.green_area
        if name == "nature":
            return self.nature
        if name == "recommended":
            return self.recommended

    def set_by_name(self, name: str, value: bool):
        if name == "historical":
            self.historical = value
        if name == "entertainment":
            self.entertainment = value
        if name == "residence":
            self.residence = value
        if name == "food":
            self.food = value
        if name == "art":
            self.art = value
        if name == "architecture":
            self.architecture = value
        if name == "sport":
            self.sport = value
        if name == "green_area":
            self.green_area = value
        if name == "nature":
            self.nature = value
        if name == "recommended":
            self.recommended = value
