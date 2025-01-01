from typing import Any

import requests

from singleton import Manga

base_url = 'https://api.mangadex.org'

endpoint = '/manga'

def search(title : str, limit : int, **args) -> list[Manga]:
    tags : dict = requests.get(f'{base_url}/manga/tag').json()
    if args['included_tags'] == []:
        included_ids : list[str] = [ tag['id']
                            for tag in tags['data']
                            if tag['attributes']['name']['en'] in args['included_tags'][0] ]
    else: included_ids : list[str] = []

    if args['excluded_tags'] == []:
        excluded_ids : list[str] = [ tag['id']
                            for tag in tags['data']
                            if tag['attributes']['name']['en'] in args['excluded_tags'][0] ]
    else: excluded_ids : list[str] = []

    if args['order'] == []:
        order_fix : dict[str, str] = { f'order[{k}]' : v for k, v in args['order'].items() }
    else: order_fix : dict[str, str] = {}
    
    params : dict = {
        **{
            'title' : title,
            'limit' : limit,
            'includedTags[]' : included_ids,
            'excludedTags[]' : excluded_ids,
            'publicationDemographic[]' : args['demographic'],
            'status[]' : args['status'],
            'contentRating' : args['rating']
        },
        **order_fix
    }

    response = requests.get(base_url + endpoint, params=params)
    return [ Manga(m) for m in response.json()['data'] ]