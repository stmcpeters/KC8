# New York Times Technology News Scraper

### Overview of project
This project is a Python-based web application built with Flask that scrapes trending technology articles from the [New York Times](https://www.nytimes.com/section/technology) and fetches tech jokes from a [Joke API](https://github.com/15Dkatz/official_joke_api?tab=readme-ov-file). The app stores article data in a SQLite database called `tech_news` and random tech jokes in another database called `jokes_api`. The frontend is styled using Tailwind CSS, ensuring a clean and responsive user interface.

### Demo


https://github.com/user-attachments/assets/e3d835a8-f3a9-4762-ad87-736d8cf1ebd4



### Features
- Web Scraping: Collects news article data from online sources and stores it in the `tech_news` database.
- API Integration: Fetches random jokes from an API and stores them in the `jokes_api` database.
- Flask Framework: Lightweight and efficient backend handling.
- Tailwind Styling: Clean, responsive, and modern user interface.
- Unittest: Integrated testing of connections to databases and routes using Unittest and generates coverage report.
- Rate Limiting: Implements rate limiting to prevent excessive requests and ensure fair usage.
- Google OAuth: Enables users to sign in using Google for a seamless authentication experience.
- Google reCAPTCHA: Adds an extra layer of security to prevent bot access.
- Basic Search Functionality: Allows users to search for specific articles within the scraped database.
- Advanced Search Functionality: Allows users to search for specific articles matching multiple conditions (title AND description) within the scraped database.
- Pagination: Implements pagination for better navigation through articles.
- Data Export: Allows users to download a CSV file with the news article data scraped.


### Technologies Used
- Python
- Flask
- SQLite
- BeautifulSoup (for web scraping)
- Requests (for API calls)
- Tailwind Styling
- Unittest
- Flask-Limiter (for rate limiting)
- OAuthlib (for Google OAuth integration)
- Google reCAPTCHA
- FTS5 (Full-Text Search)

### Installation Instructions
#### Prerequisites 
Python 3.x


1. Clone the Repository:
`git clone https://github.com/yourusername/returning-grades.git <project-name>`
`cd KC5`
2. Create a Virtual Environment:
`python -m venv venv`
`source venv/bin/activate`  
3. Install Dependencies:
`pip install -r requirements.txt`
4. Get your OAuth 2.0 credentials from the Google API Console [here](https://developers.google.com/identity/protocols/oauth2#1.-obtain-oauth-2.0-credentials-from-the-dynamic_data.setvar.console_name.)
5. Set up Google reCAPTCHA [here](https://developers.google.com/recaptcha/docs/display)
6. Set up Environment Variables in the `.env` file<br/>
```GOOGLE_CLIENT_ID=your_google_client_id``` <br/>
```GOOGLE_CLIENT_SECRET=your_google_client_secret```<br/>
```SECRET_KEY=your_flask_secret_key```<br/>
```SITE_KEY=your_google_recaptcha_key```<br/>
7. Run the Application:
`python3 app.py`
The app will be available at `http://127.0.0.1:8000/`.

### Testing
Unittest coverage report can be generated using `coverage run -m unittest tests/test_app.py --v`
#### Current Tests
<img width="593" alt="Screenshot 2025-02-21 at 6 00 06 PM" src="https://github.com/user-attachments/assets/e097f218-6712-4452-b3ef-52ca3d2cdd1a" />

#### Additional unittest testing to be added include:
##### NYT Web Scraping
- Check if extracted article details (title, URL, summary) are correctly formatted.
- Ensure that empty or malformed HTML pages do not cause crashes.
##### API Integration Tests
- Test the handling of API failures (e.g., timeouts, invalid responses).
- Ensure the API data is correctly parsed and stored in database.
##### Flask Route Tests
- Verify the `/index` route triggers data scraping.
- Ensure the `/search` endpoint provides expected search results.
##### Google OAuth Tests
- Test that unauthenticated users cannot access restricted routes.
##### Rate Limiting Tests
- Test that the app correctly limits excessive requests from the same user.
- Verify that users receive appropriate error messages when exceeding limits
##### Google reCAPTCHA Tests
- Ensure that reCAPTCHA validation works and blocks automated requests.
- Test that form submissions fail when reCAPTCHA is not verified.
##### Form and Input Validation Tests
- Ensure that invalid search queries return appropriate responses/errors.
- Validate that required fields are properly handled.

### Screenshots of Databases
<img width="1030" alt="Screenshot 2025-02-19 at 10 53 34 PM" src="https://github.com/user-attachments/assets/f5732a77-2e07-4fb8-b61a-de8d00ad91d1" />
<img width="1030" alt="Screenshot 2025-02-19 at 10 53 12 PM" src="https://github.com/user-attachments/assets/dc1be9da-1f01-4e6e-bd82-6fa9c8e148d8" />

### Contributing
Contributions are welcomed to this project! If you have an idea for a new feature or a bug fix, please open an issue or a pull request.
