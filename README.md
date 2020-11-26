# books-flask-api-mysql

a simple Flask API connected to a local MySQL database

# quick start

1. pip3 install Flask
2. pip3 install pymysql
3. pip3 install python-dotenv
4. make sure you have MySQL installed and running on your computer
5. create a .env file with your MySQL user and password
6. run the command python3 db.py in your terminal to create the database: books
7. run the command python3 app.py in your terminal to start the app
8. make a post request with Postman (add and 'author', a 'language', and a 'title' of a book) at http://127.0.0.1:5002/books
9. try out a GET request with your browser or Postman at http://127.0.0.1:5002/books
10. try out GET, PUT or DELETE requests with Postman at http://127.0.0.1:5002/book/'id of a book you created'
