import pytest
from fireo.fields import ListField, NestedModel

from API import app
from fastapi.testclient import TestClient

from firebase_models import User, Comment

TEST_DATA = {
    "TEST_PLACE": "",
    "ACCESS_TOKEN": "",
    "TEST_USER_CREDENTIALS": {
        "email": "api@unit.test",
        "password": "api_unit_test_password",
    }
}
client = TestClient(app)


def test_status():
    response = client.get(f"/check-status")
    assert response.status_code == 200
    assert response.json()["message"] == "API is working!"


def test_register_user():
    response = client.post(f"/register/", data=TEST_DATA["TEST_USER_CREDENTIALS"])
    assert response.status_code == 200 or response.status_code == 400


def test_login_user():
    response = client.post(f"/login", data=TEST_DATA["TEST_USER_CREDENTIALS"])
    assert response.status_code == 200
    TEST_DATA['ACCESS_TOKEN'] = response.json()["access_token"]


def test_user_update():
    headers = {"Authorization": f"Bearer {TEST_DATA['ACCESS_TOKEN']}"}
    username_json = {
        "nickname": "NewNickname"
    }
    username_response = client.post(f"/update-user-nickname", headers=headers, data=username_json)
    gender_json = {
        "gender": "male"
    }
    gender_response = client.post(f"/update-user-gender", headers=headers, data=gender_json)
    birth_json = {
        "birth_date": "10.05.1990"
    }
    birth_response = client.post(f"/update-user-birthdate", headers=headers, data=birth_json)
    phone_number_json = {
        "phone_number": "+79285034717"
    }
    phone_number_response = client.post(f"/update-user-phone-number", headers=headers, data=phone_number_json)
    assert username_response.status_code == 200
    assert gender_response.status_code == 200
    assert birth_response.status_code == 200
    assert phone_number_response.status_code == 200


def test_get_user():
    headers = {"Authorization": f"Bearer {TEST_DATA['ACCESS_TOKEN']}"}
    response = client.get(f"/profile", headers=headers)
    assert response.status_code == 200
    # Validate the response content as needed
    response_json = response.json()
    assert "email" in response_json
    assert "password" in response_json
    assert "nickname" in response_json
    assert "gender" in response_json
    assert "birth_date" in response_json
    assert "phone_number" in response_json
    assert response_json["email"] == "api@unit.test"
    assert response_json["nickname"] == "NewNickname"
    assert response_json["gender"] is True
    assert response_json["birth_date"] == "10.5.1990"
    assert response_json["phone_number"] == "+79285034717"


def test_add_place():
    headers = {"Authorization": f"Bearer {TEST_DATA['ACCESS_TOKEN']}"}
    json = {
        "title": "endpoints_test_place",
        "rating": "4.5",
        "description": "A wonderful place",
        "tags": "historical"
    }
    response = client.post(f"/add-place", headers=headers, data=json)
    assert response.status_code == 200
    place_id = list(response.json().keys())[0]
    assert response.json()[place_id] == "endpoints_test_place"
    TEST_DATA['TEST_PLACE'] = place_id


def test_update_location():
    place_id = TEST_DATA['TEST_PLACE']
    json = {
        "lat": "1.2345",
        "lon": "6.7890"
    }
    response = client.post(f"/update-place-location/{place_id}", data=json)
    assert response.status_code == 200
    assert response.json()["message"] == f"Place {place_id} location was updated to 1.2345, 6.7890"


def test_near_places():
    lat = 55.752222
    lon = 48.744546

    response = client.get(f"/near-places?user_lat={lat}&user_lon={lon}")

    assert response.status_code == 200


def test_upload_image():
    headers = {"Authorization": f"Bearer {TEST_DATA['ACCESS_TOKEN']}"}
    place_id = "test_directory"
    json = {
        "image": open("test-image.jpg", "rb"),
        "place_id": place_id,
        "image_extension": "jpg"
    }
    response = client.post(f"/upload-image", headers=headers, data=json)
    assert response.status_code == 200


def test_get_images_list():
    place_id = "test_directory"
    response = client.get(f"/get-images-list/{place_id}")
    assert response.status_code == 200
    assert "image_ref" in response.json()
    print(response.json()["image_ref"])


def test_image_by_place_id():
    place_id = "test_directory"
    response = client.get(f"/get-images-list/{place_id}")
    image_name = response.json()["image_ref"][0]
    response = client.get(f"/images/{place_id}/{image_name}")
    assert response.status_code == 200


def test_get_place_by_id():
    place_id = TEST_DATA['TEST_PLACE']
    response = client.get(f"/get-place/{place_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "endpoints_test_place"


def test_add_comment():
    place_id = TEST_DATA['TEST_PLACE']
    json = {
        "email": "api2@unit2.test2",
        "password": "2api_unit_test_password2",
    }
    client.post(f"/register/", data=json)
    response = client.post(f"/login", data=json)
    jwt = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {jwt}"}
    json = {
        "text": "Great place",
        "rating": "4.5"
    }
    response = client.post(f"/add-comment/{place_id}", headers=headers, data=json)
    assert response.status_code == 200


def test_get_comments():
    place_id = TEST_DATA['TEST_PLACE']
    response = client.get(f"/get-comments/{place_id}")
    assert response.status_code == 200


def test_promote_to_moderator():
    uid = "fS0tUzrY7a53zmmROF0a"
    json = {
        "email": "moderator@gmail.com",
        "password": "123456"
    }
    response = client.post(f"/login", data=json)
    jwt = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {jwt}"}
    response = client.get(f"/promote-to-moderator/{uid}", headers=headers)
    assert response.status_code == 200


def test_remove_image():
    headers = {"Authorization": f"Bearer {TEST_DATA['ACCESS_TOKEN']}"}
    place_id = "test_directory"
    response = client.get(f"/get-images-list/{place_id}")
    image_name = response.json()["image_ref"][0]
    response = client.get(f"/remove-image/{place_id}/{image_name}", headers=headers)
    assert response.status_code == 200


def test_remove_folder():
    test_upload_image()
    headers = {"Authorization": f"Bearer {TEST_DATA['ACCESS_TOKEN']}"}
    place_id = "test_directory"
    response = client.get(f"/remove-image-folder/{place_id}", headers=headers)
    assert response.status_code == 200


def test_delete_place():
    headers = {"Authorization": f"Bearer {TEST_DATA['ACCESS_TOKEN']}"}
    place_id = TEST_DATA['TEST_PLACE']
    response = client.get(f"/reject-place/{place_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == f"Place {place_id} removed"


def test_null_user():
    user = User.collection.get("fS0tUzrY7a53zmmROF0a")
    user.status = "user"
    user.comments = ListField(NestedModel(Comment)).empty_value_attributes
    user.birth_date = None
    user.nickname = None
    user.gender = None
    user.save()
    user = User.collection.get("Q1qkIXBiyNdErF7axr7y")
    user.status = "user"
    user.comments = ListField(NestedModel(Comment)).empty_value_attributes
    user.birth_date = None
    user.nickname = None
    user.gender = None
    user.save()



if __name__ == "__main__":
    pytest.main()
