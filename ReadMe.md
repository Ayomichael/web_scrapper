**Instagram Scraper (app.py)**
This Python Flask application scrapes data from public Instagram posts, including likes (usernames) and comments (username and text). It provides a simple web interface for entering post URLs and your Instagram credentials, then downloads the results as a CSV file.



**Features**
Scrapes usernames who liked a post.
Scrapes usernames and text of comments on a post.
Saves data as a CSV file for easy analysis.
Simple and user-friendly web interface.

**Prerequisites**
Python 3.x (Make sure you have pip installed)
A web browser
An Instagram account (to login and access content)
you can create a virtual environment to avoid dependency issues(optional) 

**Installation**

**Clone the Repository:**
git clone https://github.com/Ayomichael/web_scrapper.git
cd instagram-scraper

**Install Dependencies:**
pip install -r requirements.txt

**UnitTest:**
you can run unit test to confirm is properly setup (optional)
python -m unittest test_app.py

**Run the App:**
python app.py 

**Open Web Interface:**

Go to http://127.0.0.1:5000/ in your browser.
Provide your Instagram username and password.
Enter the URL of the Instagram post you want to scrape.

Click "Submit"

After scraping is complete, the instagram_data.csv file downloads automatically.