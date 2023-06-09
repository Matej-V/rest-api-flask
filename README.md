REST API FLASK PYTHON 
=====================
REST API for movies database. The API allows GET, POST and PUT methods. The API is implemented in Python using `Flask framework` and uses `sqlite3` database.


## Run the server locally
```
$ python app.py
```

## Run the tests
Using `unittest` module. Prepared database `movies_database.db` is required to run the tests. Tests the basic functionality of the API including the GET, POST and PUT methods. Server needs to be activated.
```
$ python -m unittest test.RestApiTests
```

## Build a Docker image
```
$ docker build -t rest-api-flask .
```

## Run an image inside a container
```
$ docker run rest-api-flask
```

## Supported endpoints
### GET /movies
This endpoint returns a list of all the movies in the database.
Returned JSON object is in the following format:
```
[{
    'id': 1,
    'title': 'Interstellar',
    'description': 'When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.',
    'release_year': 2014
}]
```
### GET /movies/&lt;id&gt;
Endpoint returns details of a movie with the given id. If the
id is not found, returns a `404` status code. Format:
```
{
    'id': 1,
    'title': 'Interstellar',
    'description': 'When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.',
    'release_year': 2014
}
```
### POST /movies
Endpoint creates a new movie in the database. It accepts a
JSON object in the following format:
```
{
    'title': 'Oppenheimer',
    'description': 'The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.',
    'release_year': 2023}
}
```
The title and release_year fields are required. If either of these fields is missing, returns a `400 Bad Request` status code. Returned JSON object is in the same format as `GET /movies/<int:id>;`.
### PUT /movies/&lt;id&gt;
Endpoint updates a movie with the given id. It accepts a JSON object in the same format as the `POST /movies` endpoint. If the movie with the given id is not found, return a `404` status code. Returned JSON object is in the same format as `GET /movies/<int:id>`.

