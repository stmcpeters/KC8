# import Flask from flask to create the app
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, send_file
# import Limiter from flask_limiter to limit the number of requests
from flask_limiter import Limiter
# import get_remote_address from flask_limiter.util to get the user's IP address
from flask_limiter.util import get_remote_address
# import flask-login
from flask_login import login_required
# import sqlite3 to connect to the database
import sqlite3
# import OAuth from authlib to authenticate users
from authlib.integrations.flask_client import OAuth
# import dotenv and os module to access environment variables
from dotenv import load_dotenv
# import os module to access environment variables
import os
# import csv
import csv

# load environment variables from .env file
# assign the environment variables to variables to be used
load_dotenv()
SECRET_KEY = 'secret'
SITE_KEY = os.getenv('SITE_KEY')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

# create a new instance of Flask
app = Flask(__name__)
app.secret_key = SECRET_KEY

# OAuth config
oauth = OAuth(app)
# create a new instance of OAuth
google = oauth.register(
        name="google",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        # access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        # authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={'scope': 'email profile'},
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        redirect_uri='http://localhost:8000/authorize'
)

# flask-limiter config
limiter = Limiter(
# use the user's IP address for rate limiting
    get_remote_address, 
    app=app,
    # sets a global rate limit (e.g., 15 requests per hour)
    default_limits=["15 per hour"], 
)

# error handling for exceeding rate limit
@app.errorhandler(429)
def ratelimit_error(e):
    # allows you to render a template from a string
    return render_template_string('''
        <html>
        <head>
            <script type="text/javascript">
                alert("You have exceeded your request limit! Please try again later.");
                window.history.back();  // returns to landing ('/') page
            </script>
        </head>
        <body></body>
        </html>
    '''), 429


# use a route decorator to create a route redirecting to the google login page
@app.route('/login')
@limiter.limit("15 per minute") # limits to 15 req/min
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


# use a route decorator to create a route for redirecting after successful login
@app.route('/authorize')
@limiter.limit("15 per minute") # limits to 15 req/min
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    # print(f'token: {token}')
    resp = google.get('userinfo')
    # resp.raise_for_status()
    user_info = resp.json()
    # print(f'user_info: {user_info}')
    session['email'] = user_info['email']
    # will redirect to the index.html after successful login
    return redirect(url_for('index'))

# starter page
@app.route('/')
@limiter.limit("15 per minute") # limits to 15 req/min
def home():
    return render_template('home.html', SITE_KEY=SITE_KEY)

# use a route decorator to create a route for logging out
@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return render_template('logout.html')

# create connection to database tech_news.db
def news_db_connection():
    # connect to database
    connection = sqlite3.connect('tech_news.db')
    # allows us to access the columns of the database by name like a Python dictionary
    connection.row_factory = sqlite3.Row
    # access the database using a cursor object
    return connection

# create connection to database jokes_api.db
def jokes_db_connection():
    # connect to database
    conn = sqlite3.connect('jokes_api.db')
    # allows us to access the columns of the database by name like a Python dictionary
    conn.row_factory = sqlite3.Row
    # access the database using a cursor object
    return conn

# create a route for the home page
# login_required makes sure user auth is successful before showing data
@login_required
@app.route('/index', methods=['GET'])
@limiter.limit("15 per minute") # limits to 15 req/min
def index():
    # get the session email
    email = dict(session).get('email', None)
    # opens connection to database
    connection = news_db_connection()
    conn = jokes_db_connection()
    # fetch data from articles table
    data = connection.execute('''SELECT * FROM articles''').fetchall()
    joke = conn.execute('''SELECT * FROM tech_jokes LIMIT 1''').fetchone()
    # pagination for articles data
    page = request.args.get('page', 1, type=int)
    per_page = 2
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(data) + per_page - 1) // per_page
    items_on_page = data[start:end]
    # close database connection
    connection.close()
    conn.close()
    # render articles data in index.html and pass data in order to display
    return render_template('index.html', items_on_page=items_on_page, joke=joke, page=page, total_pages=total_pages)

@app.route('/add', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        # opens the database connection
        connection = news_db_connection()
        # form data from the user
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        link = request.form['article_link']
        # adds the data to the articles table 
        connection.execute('''INSERT INTO articles (title, author, description, article_link) VALUES (?, ?, ?, ?)''', (title, author, description, link))
        # saves the changes
        connection.commit()
        # closes database connection
        connection.close()
        # redirects to the index.html page
        return redirect(url_for('index'))
    else:
        return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_article(id):
    # open connection to database 
    connection = news_db_connection()
    if request.method == "POST":
        # form data from user
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        link = request.form['article_link']
        # updates data from specified id in the articles table
        connection.execute('''UPDATE articles SET title = ?, author = ?, description = ?, article_link = ? WHERE id = ?''', (title, author, description, link, id))
        # commit the changes
        connection.commit()
        # close database connection
        connection.close()
        # redirect to home page
        return redirect(url_for('index'))
    else:
        # will populate the article's info to be edited in the form
        article = connection.execute('''SELECT * FROM articles WHERE id = ?''', (id,)).fetchone()
        # close the connection to database
        connection.close()
        # will render the edit.html template with article info
        return render_template('edit.html', article=article)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_article(id):
    # open connection to database
    connection = news_db_connection()
    # query to delete specified id from the articles table
    article = connection.execute('''DELETE FROM articles WHERE id = ?''',(id,))
    # commit the changes 
    connection.commit()
    # close the database connection
    connection.close()
    # render deletion template to confirm article was deleted
    return render_template('delete.html', article=article)

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        # opens the database connection
        connection = news_db_connection()
        # create a cursor object to execute SQL queries
        cursor = connection.cursor()
        # drop table if it already exists
        cursor.execute('DROP TABLE IF EXISTS articles_fts')
        # create virtual table for FTS5
        create_vtable = connection.execute('''CREATE VIRTUAL TABLE articles_fts USING FTS5(title, author, description, article_link)''')
        # insert data into virtual table
        insert_data = connection.execute('''INSERT INTO articles_fts SELECT title, author, description, article_link FROM articles''')
        # form data from the user (search query)
        search = request.form['search']
        # searches the data from the articles table using FTS5 MATCH and returns any matches to titles in the database
        data = connection.execute('''SELECT * FROM articles_fts WHERE title MATCH ?''', (search,)).fetchall()
        # pagination for search results data
        page = int(request.form.get('page', 1))
        per_page = 2
        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (len(data) + per_page - 1) // per_page
        items_on_page = data[start:end]
        # closes database connection
        connection.close()
        # renders the search.html page
        return render_template('search.html', data=data, total_pages=total_pages, page=page, items_on_page=items_on_page, search=search)
    else:
        return render_template('search.html')
    
@app.route('/advanced_search', methods=['GET', 'POST'])
def advanced_search():
    if request.method == 'POST':
        # opens the database connection
        connection = news_db_connection()
        # create a cursor object to execute SQL queries
        cursor = connection.cursor()
        # drop table if it already exists
        cursor.execute('DROP TABLE IF EXISTS articles_fts')
        # create virtual table for FTS5
        create_vtable = connection.execute('''CREATE VIRTUAL TABLE articles_fts USING FTS5(title, author, description, article_link)''')
        # insert data into virtual table
        insert_data = connection.execute('''INSERT INTO articles_fts SELECT title, author, description, article_link FROM articles''')
        # form data from the user (search query)
        search = request.form['search']
        # advanced search query using FTS5 MATCH with multiple conditions (title AND description)
        data = connection.execute('''SELECT * FROM articles_fts WHERE articles_fts MATCH ? AND description MATCH ?''', (search, search)).fetchall()
        # pagination for search results data
        page = int(request.form.get('page', 1))
        per_page = 2
        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (len(data) + per_page - 1) // per_page
        items_on_page = data[start:end]
        # closes database connection
        connection.close()
        # renders the advanced_search.html page
        return render_template('advanced_search.html', data=data, total_pages=total_pages, page=page, items_on_page=items_on_page, search=search)
    else:
        return render_template('advanced_search.html')

# convert article database data into CSV file
@app.route('/export')
def export_data():
    # create connection to sqlite database
    connection = sqlite3.connect('tech_news.db')
    # create a cursor object to execute SQL queries
    cursor = connection.cursor()
    # opens connection to database
    connection = news_db_connection()
    # fetch data from articles table
    data = connection.execute('''SELECT * FROM articles''').fetchall()
    # create path to CSV file
    csv_file_path = os.path.join(os.getcwd(), "articles.csv")
    # write database data to CSV file
    with open(csv_file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Title', 'Author(s)', 'Description', 'Article Link'])
        writer.writerows(data)
    print(f"Data exported successfully to {csv_file_path}")
    # return csv to be downloaded by user
    return send_file(csv_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)