import os

import requests
import dotenv

import search
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

if __name__ == '__main__':
    res = search.search('Bleach', 4, included_tags=['Action'], 
                  excluded_tags=['Romance'], order={ 'rating' : 'desc' }, 
                  demographic=[], status=[], rating=[])
    for mgn in res:
        print(mgn)