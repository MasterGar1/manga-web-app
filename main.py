import requests
import dotenv
import os

dotenv.load_dotenv()
API_KEY : str = os.getenv('API_KEY')

base_url = 'https://api.mangadex.org'

endpoint = '/manga'

params = {
    'title' : 'I am the',  
    'limit' : 5,         
    'order[relevance]' : 'desc'  
}

creds = {
    'grant_type': 'password',
    'username': 'Gar1',
    'password': os.getenv('PASSWORD'),
    'client_id': os.getenv('CLIENT_ID'),
    'client_secret': os.getenv('CLIENT_SECRET')
}

r = requests.post(
    'https://auth.mangadex.org/realms/mangadex/protocol/openid-connect/token',
    data=creds
)
r_json = r.json()

headers = {
    "Authorization": f"Bearer {r_json['access_token']}"
}

api_response = requests.get(base_url + endpoint, headers=headers, params=params)

print(api_response.status_code)