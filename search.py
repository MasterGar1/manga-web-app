from typing import Any

import requests
from flask import render_template, Blueprint, request

from singleton import Manga

base_url = 'https://api.mangadex.org'

endpoint = '/manga'

bp = Blueprint('searches', __name__)

demographics : list[str] = ['shounen', 'shoujo', 'josei', 'seinen']
statuses : list[str] = ['ongoing', 'completed', 'haitus', 'cancelled']
ordering : list[str] = ['title', 'year', 'createdAt', 'updatedAt', 'latestUploadedChapter', 'relevance']
genres : list[str] = ['Action', 'Adventure', 'Boys\' Love', 
                      'Comedy', 'Crime', 'Drama', 'Fantasy', 
                      'Girls\' Love', 'Historical', 'Horror', 
                      'Isekai', 'Magical Girls', 'Mecha', 'Medical', 
                      'Mystery', 'Philosophical', 'Psychological', 'Romance', 
                      'Sci-Fi', 'Slice of Life', 'Sports', 'Superhero', 
                      'Thriller', 'Tragedy', 'Wuxia']

@bp.route('/')
def search_home():
    return render_template('search.html', title='Search', genres=genres, 
                           orders=ordering, status=statuses, demogr=demographics)

@bp.route('/results')
def search_results():
    return render_template('results.html')

def search_manga(title : str, limit : int, **args) -> list[Manga]:
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
            'status[]' : args['status'],
            'publicationDemographic[]' : args['demographic'],
        },
        **order_fix
    }

    response = requests.get(base_url + endpoint, params=params)
    return [ Manga(m) for m in response.json()['data'] ]