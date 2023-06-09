from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
app.json.sort_keys = False  # Keep order of dictionary after passing to jsonify()

database = 'movies_database.db'


@app.route('/movies', methods=['GET'])
def get_movies():
    """
    Retrieve all movies from the database
    :return: JSON response
    """

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    # Get all the movies from databases
    cursor.execute('SELECT * FROM movies')

    # Prepare the response
    movie_list = []
    for movie in cursor.fetchall():
        movie_dict = {
            'id': movie[0],
            'title': movie[1],
            'description': movie[2],
            'release_year': movie[3]
        }
        movie_list.append(movie_dict)

    cursor.close()
    conn.close()

    return jsonify(movie_list)


@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id: int):
    """
    Retrieve with specified id from database
    :param movie_id: id of the movie to be retrieved from database
    :return: JSON response
    """

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Get the movie record
    movie = cursor.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()

    cursor.close()
    conn.close()

    if movie:
        # Prepare the response
        movie_dict = {
            'id': movie[0],
            'title': movie[1],
            'description': movie[2],
            'release_year': movie[3]
        }
        return jsonify(movie_dict)
    else:
        return jsonify({'message': f'Movie with id: {movie_id} not found'}), 404


@app.route('/movies', methods=['POST'])
def create_movie():
    """
    Create a new record of the movie
    :return: JSON response
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Extract movie information from the request
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', None)
    release_year = data.get('release_year')

    # Check if request data is valid
    if title is None or release_year is None:
        return jsonify({'message': 'Missing required field'}), 400

    # Insert the movie record into the database
    cursor.execute('INSERT INTO movies (title, description, release_year) VALUES (?, ?, ?)',
                   (title, description, release_year))
    conn.commit()

    # Retrieve the newly created movie
    movie = cursor.execute('SELECT * FROM movies WHERE id = ?', (cursor.lastrowid,)).fetchone()

    cursor.close()
    conn.close()

    movie_dict = {
        'id': movie[0],
        'title': movie[1],
        'description': movie[2],
        'release_year': movie[3]
    }
    return jsonify(movie_dict), 201


@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    """
    Update the movie in the database
    :param movie_id: id of the movie to be updated
    :return: JSON response
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Extract updated movie information from the request
    data = request.get_json()

    title = data.get('title')
    if title is not None:
        cursor.execute('UPDATE movies SET title=? WHERE id=?', (title, movie_id))
    description = data.get('description', None)
    if description is not None:
        cursor.execute('UPDATE movies SET description=? WHERE id=?', (description, movie_id))
    release_year = data.get('release_year')
    if release_year is not None:
        cursor.execute('UPDATE movies SET release_year=? WHERE id=?', (release_year, movie_id))

    conn.commit()

    # Retrieve the updated movie record
    movie = cursor.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()

    cursor.close()
    conn.close()

    if movie:
        # Prepare the response
        movie_dict = {
            'id': movie[0],
            'title': movie[1],
            'description': movie[2],
            'release_year': movie[3]
        }
        return jsonify(movie_dict), 200
    else:
        return jsonify({'message': f'Movie with id: {movie_id} not found'}), 404


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
