import requests
from flask import render_template, Blueprint, request

from singleton import Manga, JSON, make_request

base_url = 'https://api.mangadex.org'

endpoint = '/manga'

bp = Blueprint('search', __name__)

demographics: list[str] = ['any', 'shounen', 'shoujo', 'josei', 'seinen']
statuses: list[str] = ['any', 'ongoing', 'completed', 'haitus', 'cancelled']
ordering: list[str] = ['title', 'year', 'createdAt', 'updatedAt', 'latestUploadedChapter', 'relevance']

def split_words(text: str) -> str:
    words: list[str] = []
    last_word : int = 0
    for i, ch in enumerate(text):
        if ch.isupper():
            words.append(text[last_word:i])
            last_word = i
    words.append(text[last_word:])
    return ' '.join(words).capitalize()

def shorten(text: str, limit: int) -> str:
    if len(text) < limit:
        return text
    else:
        return text[:limit] + '...'

@bp.route('/search', methods=['GET', 'POST'])
def search_home():
    class_name = None
    if request.method == 'POST':
        class_name = request.args
    tags: JSON = make_request(f'{base_url}/manga/tag').json()
    genres = sorted([ tag['attributes']['name']['en'] for tag in tags['data'] ])
    return render_template('search.html', title='Search', genres=genres, 
                           orders=ordering, status=statuses, demogr=demographics,
                           word_split=split_words, cls=class_name)

@bp.route('/search/<query>')
def search_results(query: str):
    name, included, excluded, order, sort_dir, demo, status, limit = [ el.strip() for el in query.split('+') ]
    search_result : list[Manga] = search_manga(name, int(limit),
                                               included_tags=included.split(','),
                                               excluded_tags=excluded.split(','),
                                               order={ order : sort_dir },
                                               status=status, demographic=demo)
    return render_template('result.html', title=f'Results for "{name}"', result=search_result, shorten=shorten)

def search_manga(title: str, limit: int, **args) -> list[Manga]:
    tags: JSON = make_request(f'{base_url}/manga/tag').json()

    params: JSON = {
        'limit' : limit
    }

    order_fix: JSON = { f'order[{k}]' : v for k, v in args['order'].items() }
    params |= order_fix

    if args['status'] != 'any':
        params |= { 'status[]' : [args['status']] }

    if args['demographic'] != 'any':
        params |= { 'publicationDemographic[]' : [args['demographic']] }

    if title != '':
        params |= { 'title' : title }

    if args['included_tags'] != ['']:
        params |= { 'includedTags[]' : [ tag['id']
                            for tag in tags['data']
                            if tag['attributes']['name']['en'] 
                            in args['included_tags'] ] }

    if args['excluded_tags'] != ['']:
        params |= { 'excludedTags[]' : [ tag['id']
                            for tag in tags['data']
                            if tag['attributes']['name']['en'] 
                            in args['excluded_tags'] ] }

    response = make_request(base_url + endpoint, params=params)
    return [ mgn for m in response.json()['data'] if (mgn := Manga(m)).title != '.' ]