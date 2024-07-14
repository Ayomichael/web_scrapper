from flask import Flask, render_template, request, jsonify, send_file
import requests
from bs4 import BeautifulSoup
import csv
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    post_url = data.get('url')
    username = data.get('username')
    password = data.get('password')
    
    if not post_url or not username or not password:
        return jsonify({"error": "Invalid input"}), 400
    
    try:
        result = scrape_instagram(post_url, username, password)
        if result.get('error'):
            return jsonify(result), 400
        
        return jsonify({"message": "Data scraped successfully", "file": result['file']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def scrape_instagram(url, username, password):
    session = requests.Session()

    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.instagram.com/accounts/login/'
    })
    
    # Get CSRF token
    response = session.get('https://www.instagram.com/accounts/login/')
    csrf_token = response.cookies['csrftoken']
    
    login_data = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:&:{password}',
        'queryParams': {},
        'optIntoOneTap': False
    }
    session.headers.update({'X-CSRFToken': csrf_token})
    
    login_response = session.post(login_url, data=login_data, allow_redirects=True)
    if login_response.status_code != 200 or not login_response.json().get('authenticated'):
        return {"error": "Login failed"}
    
    response = session.get(url)
    if response.status_code != 200:
        return {"error": "Failed to load Instagram post"}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract static data as per the structure of the Instagram page
    likes = extract_likes(soup)
    comments = extract_comments(soup)
    
    # Save to CSV
    filename = save_to_csv(likes, comments)
    
    return {"message": "Data scraped and saved successfully", "file": filename}

def extract_likes(soup):
    likes = []
    try:
        
        likes_element = soup.select_one('div[role="dialog"] div.Igw0E.IwRSH.eGOV_._4EzTm') 
        if likes_element:
            for like_link in likes_element.find_all('a'):
                username = like_link.get('href').split('/')[1]
                likes.append(username)
            # likes_count = likes_element.text
            # likes.append(likes_count)
    except Exception as e:
        print(f"Error extracting likes: {e}")
    return likes

def extract_comments(soup):
    comments = []
    try:
        
        comment_elements = soup.select('ul.XQXOT li div.C4VMK') 
        for comment in comment_elements:
            username_element = comment.select_one('a.sqdOP.yWX7d._8A5w5.ZIAjV')
            comment_text_element = comment.select_one('span')
            if username_element and comment_text_element:
                username = username_element.text
                text = comment_text_element.text
                comments.append({"username": username, "comment": text})
    except Exception as e:
        print(f"Error extracting comments: {e}")
    return comments

def save_to_csv(likes, comments):
    filename = 'instagram_data.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Type', 'Username', 'Comment'])
        for like in likes:
            writer.writerow(['Like', like, ''])
        for comment in comments:
            writer.writerow(['Comment', comment['username'], comment['comment']])
    return filename

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
