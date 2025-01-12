import requests
from flask import render_template, Blueprint, request, session

from singleton import Manga, headers

base_url = 'https://api.mangadex.org'

endpoint = '/manga'

bp = Blueprint('search', __name__)

demographics : list[str] = ['shounen', 'shoujo', 'josei', 'seinen']
statuses : list[str] = ['ongoing', 'completed', 'haitus', 'cancelled']
ordering : list[str] = ['title', 'year', 'createdAt', 'updatedAt', 'latestUploadedChapter', 'relevance']
genres : list[str] = ['Action', 'Adventure', 'Boys Love', 
                      'Comedy', 'Crime', 'Drama', 'Fantasy', 
                      'Girls Love', 'Historical', 'Horror', 
                      'Isekai', 'Magical Girls', 'Mecha', 'Medical', 
                      'Mystery', 'Philosophical', 'Psychological', 'Romance', 
                      'Sci-Fi', 'Slice of Life', 'Sports', 'Superhero', 
                      'Thriller', 'Tragedy', 'Wuxia']

def split_words(text : str) -> str:
    words : list[str] = []
    last_word : int = 0
    for i, ch in enumerate(text):
        if ch.isupper():
            words.append(text[last_word:i])
            last_word = i
    words.append(text[last_word:])
    return ' '.join(words).capitalize()

def shorten(text : str, limit : int) -> str:
    if len(text) < limit:
        return text
    else:
        return text[:limit] + '...'

@bp.route('/search', methods=['GET', 'POST'])
def search_home():
    class_name = None
    if request.method == 'POST':
        class_name = request.args
    return render_template('search.html', title='Search', genres=genres, 
                           orders=ordering, status=statuses, demogr=demographics,
                           word_split=split_words, cls=class_name)

@bp.route('/search/<query>')
def search_results(query):
    name, included, excluded, order, sort_dir, demo, status, limit = query.split('+')
    search_result : list[Manga] = search_manga(name, int(limit),
                                               included_tags=included.split(','),
                                               excluded_tags=excluded.split(','),
                                               order={ order : sort_dir },
                                               status=status, demographic=demo)
    return render_template('result.html', title=f'Results for "{name}"', result=search_result, shorten=shorten)

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
            'status[]' : [args['status']],
            'publicationDemographic[]' : [args['demographic']],
        },
        **order_fix
    }

    response = requests.get(base_url + endpoint, params=params, headers=headers)
    return [ mgn for m in response.json()['data'] if (mgn := Manga(m)).title != '.' ]