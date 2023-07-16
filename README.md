# API

## Project description

The tourism crowdsourcing app is a comprehensive platform for tourists and guests, allowing them to search for tourist
places based on location, category, ratings, or popularity. Users can contribute by submitting information, including
location, description, ratings, reviews, and photos, to create a rich database of tourist destinations. Moderators
ensure the reliability and authenticity of the content. Users can rate, review, and filter search results based on
various parameters, aiding in decision-making. The app also provides navigation functionality, offering directions and
enhancing the exploration experience. Overall, it offers a user-friendly interface, promotes user contributions, and
facilitates informed travel decisions.
***

## Installation

- ### **Preparation**
    - Get [firebase](https://firebase.google.com/docs/) credentials for your application
        - Create file **admin-sdk.json** in root directory and paste received credentials inside it
    - Generate [secret token](https://docs.python.org/3/library/secrets.html) for using JWT
        - Create file **jwt-secret** in root directory and paste your secret inside it
    - Get [algolia](https://www.algolia.com) Application ID and API Key
        - Create file **algolia-api-key** in root directory and paste your API KEY inside it
        - Create file **algolia-app-id** in root directory and paste your APP ID inside it
- ### **Launch**
    - Set up virtual environment
    - Install requirements using **pip install -r requirements.txt**
    - Launch **run.py**
- ### **Postman collection**
    - Import [this](Tourism%20app.postman_collection.json) file to Postman

## Testing
#### If you do not want to install API on your machine, scan or click the QR.
<a href="https://drive.google.com/file/d/1I0OPUTGoFYJz71LWe0v576Ix1R9QKURR/view?usp=sharing"><img alt="apk_QR" height="250" src="https://i.imgur.com/hrrRK7l.png" width="250"/></a>

## What was done in Python?

The API is fully relies on python.

## Endpoints
- ### **Documentation**
    - [Docs](http://wensietyt.fvds.ru:8000/docs)

## Technological stack

### Programming language

- [Python 3.9](https://www.python.org/downloads/release/python-390/)

### API framework

- [FastAPI](https://fastapi.tiangolo.com/)

### Database

- [FireStore](https://firebase.google.com/docs/)
- [FireO](https://octabyte.io/FireO)

### Testing

- [Pytest](https://docs.pytest.org/)

### Moderation panel

- [React](https://react.dev/)

### Full-text search engine

- [Algolia](https://www.algolia.com)
