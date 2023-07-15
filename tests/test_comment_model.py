# test_comment_model.py
from firebase_models import Comment


def test_comment_creation():
    comment = Comment(reference="some_reference", text="some_text", rating=4)
    assert comment.reference == "some_reference"
    assert comment.text == "some_text"
    assert comment.rating == 4


def test_comment_to_dict():
    comment = Comment(reference="some_reference", text="some_text", rating=4)
    expected_dict = {
        "reference": "some_reference",
        "text": "some_text",
        "rating": 4
    }
    assert comment.to_dict() == expected_dict


def test_comment_representation():
    comment = Comment(reference="some_reference", text="some_text", rating=4)
    expected_repr = "Comment(reference=some_reference, text=some_text, rating=4)"
    assert comment.__repr__() == expected_repr
