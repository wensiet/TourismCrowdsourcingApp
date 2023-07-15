from pydantic import BaseModel


class Message(BaseModel):
    message: str


class TagsSchema(BaseModel):
    historical: bool
    entertainment: bool
    residence: bool
    food: bool
    art: bool
    architecture: bool
    sport: bool
    green_area: bool
    nature: bool
    recommended: bool


class PlaceSchema(BaseModel):
    id: str
    title: str
    rating: str
    description: str
    user_ids: list
    geo_point: str
    approved: bool
    tags: TagsSchema


class NearSchema(BaseModel):
    distance: PlaceSchema


class FiltersSchema(BaseModel):
    id: PlaceSchema


class LoginSchema(BaseModel):
    access_token: str
    token_type: str


class CommentSchema(BaseModel):
    reference: str
    text: str
    rating: float


class UserSchema(BaseModel):
    id: str
    nickname: str
    email: str
    gender: bool
    birth_date: str
    password: str
    status: str
    comments: list[CommentSchema]
    phone_number: str
    favorite_places: list[str]


class ModerationPlacesSchema(BaseModel):
    places: list[str]


class ImageListSchema(BaseModel):
    image_ref: list[str]


class GetCommentSchema(BaseModel):
    text: str
    nickname: str
    rating: float


class GetCommentsSchema(BaseModel):
    user_id: GetCommentSchema
