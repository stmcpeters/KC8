# import requests module for HTTP requests
import requests
# import beautifulsoup 
from bs4 import BeautifulSoup
# import sqlite3 for database
import sqlite3
import json

url = 'https://www.nytimes.com/section/technology'
api_url = 'https://official-joke-api.appspot.com/jokes/programming/ten'

################## fetching and storing data from jokes API ##################
try:
  # uses requests module to make a HTTP request to the API
  api_response = requests.get(api_url)
  # checks to see that the connection is 200
  if api_response.status_code == requests.codes.ok:
      # parses the response received from API into json
      jokes = api_response.json()
      # list comprehension to select all the values of 'setup' from each dictionary within jokes 
      setups = [joke['setup'] for joke in jokes]
      # list comprehension to select all the values of 'setup' from each dictionary within jokes
      punchlines = [joke['punchline'] for joke in jokes]

      # create connection to the database
      conn = sqlite3.connect('jokes_api.db')
      # cursor to execute SQL queries
      c = conn.cursor()

      # drop table if it already exists
      c.execute('''DROP TABLE IF EXISTS tech_jokes''')

      # create tech_jokes table schema
      jokes_table = '''CREATE TABLE tech_jokes(
                id INTEGER PRIMARY KEY,
                setup TEXT,
                punchline TEXT
                )'''
      
      # create the table
      c.execute(jokes_table)
      # message to confirm table was made
      print('jokes table has been created')

      # insert the setups and punchlines data into the tech_jokes table
      # zip() inserts the data in one command, best practice for matching data
      for setup, punchline in zip(setups, punchlines):
        c.execute('''INSERT INTO tech_jokes (setup, punchline) VALUES (?, ?)''', (setup, punchline))
      # commit the changes
      conn.commit()

      # select all the data from the table
      c.execute('''SELECT * FROM tech_jokes''')
      # fetch data from the table
      result = c.fetchall()
      # prints table data
      print(result)
      # close the connection
      conn.close()
  else:
      print("Error:", api_response.status_code, api_response.text)

############# error handling ###############
# error handling for HTTP requests
except requests.exceptions.RequestException as e:
  print(f'error fetching data from {url}: {e}')

# error handling for sqlite 
except sqlite3.Error as e:
  print(f'database error: {e}')

# catch all error handling
except Exception as e:
  print(f'an error occurred: {e}')

########### close database connection ############
# closes connection to database whether data is successful or error is thrown
finally:
  if 'connection' in locals():
    conn.close()

##########################################################################################

############ webscraping NYT articles ################
try:
  # uses the requests module to fetch HTML content from specified URL
  response = requests.get(url)

  # parse the HTML content using BeautifulSoup
  soup = BeautifulSoup(response.content, "html.parser")
  # print(soup.prettify())

  # find all elements needed to display articles (title, paragraph and links)
  titles = soup.find_all('h3', class_="css-1j88qqx e15t083i0")
  # for title in titles:
  #   print(title.text)
  descriptions = soup.find_all('p', class_="css-1pga48a e15t083i1")
  # for description in descriptions:
  #   print(description.text)
  links = soup.find_all('a', class_="css-8hzhxf")
  # for link in links:
  #   print(link.get('href'))
  authors = soup.find_all('span', class_="css-1n7hynb")
  # for author in authors:
  #   print(author.text)

# ######### creating database and table ############
  # create connection to sqlite database, if it doesn't exist it will be created
  connection = sqlite3.connect('tech_news.db')
  # create a cursor object to execute SQL queries
  cursor = connection.cursor()

  # drop table if it already exists
  cursor.execute('DROP TABLE IF EXISTS articles')

  # articles database schema
  table = '''CREATE TABLE articles (
              ID INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT,
              author TEXT,
              description TEXT,
              article_link TEXT
              );'''
  # creates table in database
  cursor.execute(table)
  # 'commits' table being created
  connection.commit()
  # message to console showing table has been created
  print('articles table has been created')

  # iterate through data and insert into articles table
  # zip() inserts all data in one command (best practice for matching data)
  for title, author, description, article_link in zip(titles, authors, descriptions, links):
    cursor.execute('''INSERT INTO articles (title, author, description, article_link) VALUES (?, ?, ?, ?)''', (title.text, author.text, description.text, article_link.get('href')))
  # commit changes
  connection.commit()

  # select all data from articles table
  cursor.execute('''SELECT * FROM articles''')
  # fetch data from table
  result = cursor.fetchall()
  # message in console to confirm database data has been fetched
  print(f'database data has been fetched: {result}')


############# error handling ###############
# error handling for HTTP requests
except requests.exceptions.RequestException as e:
  print(f'error fetching data from {url}: {e}')

# # error handling for sqlite 
except sqlite3.Error as e:
  print(f'database error: {e}')

# catch all error handling
except Exception as e:
  print(f'an error occurred: {e}')

# ########### close database connection ############
# closes connection to database whether data is successful or error is thrown
finally:
  if 'connection' in locals():
    connection.close()