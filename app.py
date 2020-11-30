# a simple API connected to a local MySQL database
# 1. pip3 install Flask
# 2. pip3 install pymysql
# 3. pip3 install python-dotenv

from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from pathlib import Path
import pymysql


# explicitly providing path to '.env'
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


# connect to the local books MySQL database, created in the db.py file
def db_connection():
    connection = None
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user=os.getenv('MY_SQL_USER'),
            password=os.getenv('MY_SQL_PASSWORD'),
            db='books',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e:
        print(e)
    return connection


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_page_view():
    return "<h3>This is a simple REST API connected a local MySQL database.</h3> \n<p>At route '/books' you can get all the books in the database (GET) or create a new book (POST).</p> \n<p>At route '/book/id' you can get a book by its id (GET), update an existing book (PUT) or delete one (DELETE).</p>"


@app.route('/books', methods=['GET', 'POST'])
def books_view():
    connection = db_connection()
    cursor = connection.cursor()

    # GET: to read/get all the books
    if request.method == 'GET':
        cursor.execute('SELECT * FROM books')
        books = [dict(id=row['id'], author=row['author'], language=row['language'],
                      title=row['title']) for row in cursor.fetchall()]
        if books:
            return jsonify(books), 200
        else:
            return 'There are no books in the table yet.', 404

    # POST: to create a new book
    # to test it with Postman: POST / Body / form-data
    if request.method == 'POST':
        # iD is added to the table automatically
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']

        # parameterized query # an 'f string' would not work here
        # the '%s' is a placeholder to pass values dynamically
        insert_query = """ INSERT INTO books (author, language, title)
                           VALUES (%s, %s, %s) """
        cursor.execute(insert_query, (new_author, new_lang, new_title))

        connection.commit()  # save
        connection.close()

        return f'The book with the id: {cursor.lastrowid} created successfully.', 201


@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book_view(id):
    connection = db_connection()
    cursor = connection.cursor()

    # GET: to read/get a single book by its id
    if request.method == 'GET':
        cursor.execute(f'SELECT * FROM books WHERE id={id}')
        single_book = [dict(id=row['id'], author=row['author'], language=row['language'],
                            title=row['title']) for row in cursor.fetchall()]

        if single_book:
            return jsonify(single_book), 200
        else:
            return f'The book with id {id} is not found', 404

    # PUT: to update an existing book
    if request.method == 'PUT':
        author = request.form['author']
        language = request.form['language']
        title = request.form['title']

        # an 'f string' would not work here either
        update_query = """ UPDATE books
                           SET
                                author = %s,
                                language = %s,
                                title = %s
                           WHERE
                                id = %s """
        cursor.execute(update_query, (author, language, title, id))
        connection.commit()  # save

        cursor.execute(f'SELECT * FROM books WHERE id={id}')
        updated_book = [dict(id=row['id'], author=row['author'],
                             language=row['language'], title=row['title']) for row in cursor.fetchall()]
        if updated_book:
            return jsonify(updated_book), 200
        else:
            return 'Nothing Found', 404

    # DELETE: to delete a book
    if request.method == 'DELETE':
        # an 'f string' works here
        delete_query = f'''DELETE FROM books 
                           WHERE id = {id}'''
        cursor.execute(delete_query)

        connection.commit()  # save
        connection.close()

        return f'The book with id {id} has been deleted.', 200


if __name__ == '__main__':
    app.run(debug=True, port=5002)
