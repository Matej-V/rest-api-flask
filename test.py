import requests
import unittest


class RestApiTests(unittest.TestCase):
    _database = None
    # URI server runs on
    _URI = 'http://127.0.0.1:5000/'

    # save database state
    @classmethod
    def setUpClass(cls) -> None:
        # load database
        with open('movies_database.db', 'rb') as f:
            cls._database = f.read()

    # restore database state
    @classmethod
    def tearDownClass(cls) -> None:
        # restore database
        with open('movies_database.db', 'wb') as f:
            f.write(cls._database)

    def test_post(self) -> None:
        self.assertEqual(400, requests.post(self._URI + 'movies', json={'title': 'Oppenheimer'}).status_code)
        self.assertEqual(400, requests.post(self._URI + 'movies', json={'release_year': 2023}).status_code)
        response = requests.post(self._URI + 'movies', json={'title': 'Oppenheimer', 'release_year': 2023})
        self.assertEqual(201, response.status_code)
        self.assertEqual({'id': 4, 'title': 'Oppenheimer', 'description': None, 'release_year': 2023}, response.json())

    def test_get(self) -> None:
        self.assertEqual(200, requests.get(self._URI + 'movies/1').status_code)
        self.assertEqual({'id': 1, 'title': 'Interstellar',
                          'description': 'When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.',
                          'release_year': 2014}, requests.get(self._URI + "movies/1").json())
        self.assertEqual(404, requests.get(self._URI + 'movies/100').status_code)
        self.assertEqual(200, requests.get(self._URI + 'movies').status_code)

    def test_put(self) -> None:
        response = requests.put(self._URI + 'movies/4', json={
            'description': 'The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.'})
        self.assertEqual(200, response.status_code)
        self.assertEqual({'id': 4, 'title': 'Oppenheimer',
                          'description': 'The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.', 'release_year': 2023},
                         response.json())
