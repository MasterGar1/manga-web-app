"""Utility function module"""
import base64

from typing import Any

from .classes import Manga, make_request

demographics: list[str] = ['any', 'shounen', 'shoujo', 'josei', 'seinen']
statuses: list[str] = ['any', 'ongoing', 'completed', 'haitus', 'cancelled']
ordering: list[str] = ['title', 'year', 'createdAt', 'updatedAt',
                       'latestUploadedChapter', 'relevance']

def encrypt(input_string: str, key: int = 69) -> str:
    """Encryption of given string"""
    enc: str = ''.join(chr(ord(c) ^ key) for c in input_string)
    return base64.urlsafe_b64encode(enc.encode()).decode()

def decrypt(input_string: str, key: int = 69) -> str:
    """Decription of given string"""
    dec: str = base64.urlsafe_b64decode(input_string.encode()).decode()
    return ''.join(chr(ord(c) ^ key) for c in dec)

def split_words(text: str) -> str:
    """Splits a text by words"""
    if text.count('_') > 0:
        text = ''.join([ word.capitalize() for word in text.split('_') ])
    words: list[str] = []
    last_word: int = 0
    for i, ch in enumerate(text):
        if ch.isupper() and i != 0:
            words.append(text[last_word:i])
            last_word = i
    words.append(text[last_word:])
    return ' '.join(words).capitalize()

def get_manga(manga_id: str) -> Manga:
    """Gets a manga by id"""
    manga_url: str = f'https://api.mangadex.org/manga/{manga_id}'
    response = make_request(manga_url)
    return Manga(response.json()['data'])

def get_genres() -> list[str]:
    """Gets all available generes"""
    tags: dict[str, Any] = make_request('https://api.mangadex.org/manga/tag').json()
    return sorted([ tag['attributes']['name']['en'] for tag in tags['data'] ])
