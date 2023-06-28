import os
from fireo.models import Model
from fireo.fields import TextField, ListField, NumberField, BooleanField, GeoPoint
from google.cloud.firestore_v1._helpers import GeoPoint as GP
from typing import List
from google.cloud import storage

"""
<a href="https://octabyte.io/FireO/">Documentation</a>
"""

# importing credentials
credentials_path = '../crowdsourcing-app-f86b3-firebase-adminsdk-1r7f5-52d53ab92b.json'
# to authenticate using google services, you need to use environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

storage_client = storage.Client()


# Creating model that extends by base class Model (fireo.models)
class Place(Model):
    title: TextField = TextField()
    rating: NumberField = NumberField()
    description: TextField = TextField()
    interacted_users: ListField = ListField()
    geo_data: GeoPoint = GeoPoint()
    approved: BooleanField = BooleanField()
    photo_links: ListField = ListField()

    def __init__(
            self,
            title: str = None,
            rating: float = None,
            description: str = None,
            interacted_users: List[str] = None,
            geo_data: List[float] = None,
            approved: bool = None,
            photo_links: List[str] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.title = title
        self.rating = rating
        self.description = description
        self.interacted_users = interacted_users
        self.geo_data = geo_data
        self.approved = approved
        self.photo_links = photo_links

    def __repr__(self):
        return f"{self.title} {self.rating} {self.approved}"


if __name__ == "__main__":
    # # inno = Place(title="Innopolis", rating=5.0, description="City of your ideas", interacted_users=[123, 456],
    # #              geo_data=GP(latitude=10, longitude=10), approved=True, photo_links=["https://yigor.com"])
    # # inno.save()
    #
    # # Declaring new place to be added
    # kazan = Place(
    #     title="Kazan",
    #     rating=4.98,
    #     description="City",
    #     geo_data=GP(latitude=55.796391, longitude=49.108891),
    #     interacted_users=[123, 234],
    #     approved=True,
    #     photo_links=["../001.jpg"],
    # )
    #
    # # Upload images to Cloud Storage and get the URLs
    # image_urls = []
    # for image_link in kazan.photo_links:
    #     if image_link != "empty":
    #         # Generate a unique filename for the image
    #         filename = f"{kazan.title}/{os.path.basename(image_link)}"
    #
    #         # Upload the image to Cloud Storage
    #         bucket = storage_client.bucket('crowdsourcing-app-f86b3.appspot.com')
    #         blob = bucket.blob(filename)
    #         blob.upload_from_filename(image_link)
    #
    #         # Get the public URL of the uploaded image
    #         image_url = blob.public_url
    #         image_urls.append(image_url)
    #
    # # Save the image URLs in Firestore
    # kazan.photo_links = image_urls
    # kazan.save()

    # Making a query for a place
    places = (
        Place.collection.filter("title", "==", "Kazan")
        .filter("rating", "==", 4.98)
        .fetch()
    )
    print(places)

    # Iterating through all found places
    for p in places:
        print(p)
