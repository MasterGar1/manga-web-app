import os

import requests
import dotenv
from flask import Flask, render_template, url_for

import search

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



# dotenv.load_dotenv()
# base_url = 'https://api.mangadex.org'

# endpoint = '/manga'

# params = {
#     'title' : 'Strongest',  
#     'limit' : 10,         
#     'order[relevance]' : 'desc'  
# }

# creds = {
#     'grant_type': 'password',
#     'username': 'Gar1',
#     'password': os.getenv('PASSWORD'),
#     'client_id': os.getenv('CLIENT_ID'),
#     'client_secret': os.getenv('CLIENT_SECRET')
# }

# r = requests.post(
#     'https://auth.mangadex.org/realms/mangadex/protocol/openid-connect/token',
#     data=creds
# )
# r_json = r.json()

# headers = {
#     'Authorization': f'Bearer {r_json['access_token']}'
# }

# api_response = requests.get(base_url + endpoint, headers=headers, params=params)

# resp_dict = api_response.json()

# titles = [el['attributes']['title']['en'] for el in resp_dict['data']]

# print(titles, flush=True)