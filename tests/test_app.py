# import unittest module to use
import unittest
# import functions to be tested from app.py file
from app import app, news_db_connection, jokes_db_connection, index
# import sqlite module to use
import sqlite3

class TestFlaskApp(unittest.TestCase):
    
    # setUp method is called before each test to have a clean slate for every test
    def setUp(self):
      # create a test client for the flask app
      self.app = app.test_client()
      # testing mode = true
      self.app.testing = True

    def test_news_db_connection(self):
      """
      Tests function that connects app to the database storing the news articles
      """
      # call the function that connects to the database
      connection = news_db_connection()
      # assert that the connection is an instance of sqlite3.connection
      self.assertIsInstance(connection, sqlite3.Connection)
      # close the connection to database
      connection.close()


    def test_jokes_db_connection(self):
      """
      Tests function that connects app to the database storing the jokes
      """
      # call the function that connects to the database
      conn = jokes_db_connection()
      # assert that the connection is an instance of sqlite3.connection
      self.assertIsInstance(conn, sqlite3.Connection)
      # close the connection to database
      conn.close()
      
    def test_index(self):
      """
      Tests index page (index.html) renders
      correctly with a status code of 200 and displays the h1 tag 
      title for the page
      """
      response = self.app.get('/index')
      self.assertEqual(response.status_code, 200)
      self.assertIn(b'Top Tech Articles from the New York Times', response.data)

    def test_home(self):
      """
      Tests initial route/homepage (home.html) renders
      correctly with a status code of 200 and displays the h1 tag 
      title for the page
      """
      response = self.app.get('/')
      self.assertEqual(response.status_code, 200)
      self.assertIn(b'Welcome to my Knowledge Check 6', response.data)
    


if __name__ == '__main__':
    unittest.main()