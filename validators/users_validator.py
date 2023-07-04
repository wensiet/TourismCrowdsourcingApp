from exceptions import EssentialInfoAbsent
import re


def users_init_validator(func):
    email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    def wrapper(*args, **kwargs):
        from firebase_models import Date

        for m in ["name", "password", "status"]:
            if m not in kwargs:
                raise EssentialInfoAbsent(f"Mandatory info about place ({m}) is not stated")

        name = kwargs["name"]
        password = kwargs["password"]
        status = kwargs["status"]

        if not isinstance(name, str):
            raise ValueError(f"Name has to be str, got {type(name)} instead.")

        if not isinstance(password, str):
            raise ValueError(f"Password has to be str, got {type(password)} instead.")

        if not isinstance(status, str):
            raise ValueError(f"Status has to be str, got {type(status)} instead.")

        if "users_score" in kwargs:
            users_score = kwargs["users_score"]
            if not isinstance(users_score, float):
                raise ValueError(f"Users_score has to be float, got {type(users_score)} instead.")

        if "surname" in kwargs:
            surname = kwargs["surname"]
            if not isinstance(surname, str):
                raise ValueError(f"Surname has to be str, got {type(surname)} instead.")

        if "comments" in kwargs:
            comments = kwargs["comments"]
            if not isinstance(comments, list) or any(not isinstance(x, str) for x in comments):
                raise ValueError(f"Comments has to be list of str, got {type(comments)} instead.")

        if "birth_date" in kwargs:
            birth_date = kwargs["birth_date"]
            if not isinstance(birth_date, Date):
                raise ValueError(f"Birth_date has to be Date, got {type(birth_date)} instead.")

        if "gender" in kwargs:
            gender = kwargs["gender"]
            if not isinstance(gender, bool):
                raise ValueError(f"Gender has to be bool, got {type(gender)} instead.")

        if "email" in kwargs:
            email = kwargs["email"]
            if not isinstance(email, str):
                raise ValueError(f"Email has to be str, got {type(email)} instead.")
            if not re.fullmatch(email_regex, email):
                raise ValueError(f"Email has to be valid")

        return func(*args, **kwargs)

    return wrapper
