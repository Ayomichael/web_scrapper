import unittest
import json
from app import app
import os

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Instagram Scraper', response.data)

    def test_scrape_post(self):
        payload = {
            "url": "https://www.instagram.com/example",
            "username": "xxxx",
            "password": "xxxxxxx"
        }
        response = self.app.post('/scrape',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', json.loads(response.data))

    def test_download_file(self):
        
        filename = 'instagram_data.csv'
        with open(filename, 'w') as f:
            f.write('username,comment\nuser1,comment1\nuser2,comment2')
        
        response = self.app.get(f'/download/{filename}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Disposition'],
                         f'attachment; filename={filename}')
        
        os.remove(filename)

if __name__ == "__main__":
    unittest.main()
