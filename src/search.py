"""Module for searching pages"""
from typing import Any

from flask import render_template, Blueprint

from .classes import Manga, make_request
from .utility import get_genres, ordering, statuses, demographics, split_words

BASE_URL:str = 'https://api.mangadex.org'

ENDPOINT:str = '/manga'

bp = Blueprint('search', __name__)

def shorten(text: str, limit: int) -> str:
    """Shortens a title"""
    if len(text) < limit:
        return text
    return text[:limit] + '...'

@bp.route('/search')
def search_home():
    """Search page"""
    genres: list[str] = get_genres()
    return render_template('search.html', title='Search', genres=genres,
                           orders=ordering, status=statuses, demogr=demographics,
                           word_split=split_words)

@bp.route('/search/<query>')
def search_results(query: str):
    """Search results page"""
    name, included, excluded, \
    order, sort_dir, demo, status, limit = \
                [ el.strip() for el in query.split('+') ]
    search_result : list[Manga] = search_manga(name, int(limit),
                                               included_tags=included.split(','),
                                               excluded_tags=excluded.split(','),
                                               order={ order : sort_dir },
                                               status=status, demographic=demo)
    return render_template('result.html',
                           title=f'Results for {name if len(name) > 0 else 'ANY'}',
                           result=search_result, shorten=shorten)

def search_manga(title: str, limit: int, **args) -> list[Manga]:
    """Search manga"""
    tags: dict[str, Any] = make_request(f'{BASE_URL}/manga/tag').json_dict()
    params: dict[str, Any] = { 'limit' : limit }
    order_fix: dict[str, Any] = { f'order[{k}]' : v for k, v in args['order'].items() }
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
    response = make_request(BASE_URL + ENDPOINT, params=params)
    return [ mgn for m in response.json_dict()['data'] if (mgn := Manga(m)).title != '.' ]
