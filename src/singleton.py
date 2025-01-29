import requests
from typing import Any
import base64
from time import sleep

type JSON = dict[str, Any]

demographics: list[str] = ['any', 'shounen', 'shoujo', 'josei', 'seinen']
statuses: list[str] = ['any', 'ongoing', 'completed', 'haitus', 'cancelled']
ordering: list[str] = ['title', 'year', 'createdAt', 'updatedAt', 'latestUploadedChapter', 'relevance']

def encrypt(input_string: str, key: int = 69) -> str:
    enc: str = ''.join(chr(ord(c) ^ key) for c in input_string)
    return base64.urlsafe_b64encode(enc.encode()).decode()

def decrypt(input_string: str, key: int = 69) -> str:
    dec: str = base64.urlsafe_b64decode(input_string.encode()).decode()
    return ''.join(chr(ord(c) ^ key) for c in dec)

def split_words(text: str) -> str:
    words: list[str] = []
    last_word : int = 0
    for i, ch in enumerate(text):
        if ch.isupper():
            words.append(text[last_word:i])
            last_word = i
    words.append(text[last_word:])
    return ' '.join(words).capitalize()

class Chapter:
    def __init__(self, info: JSON) -> None:
        self.id: str = info['id']
        self.title: str = info['attributes']['title']
        self.volume: str = info['attributes']['volume']
        self.number: str = info['attributes']['chapter']
        self.pages: str = info['attributes']['pages']
        self.release_date: str = info['attributes']['publishAt']
        self.language: str = info['attributes']['translatedLanguage']

    def __repr__(self) -> str:
        return f'Title: {self.title}\nID: {self.id} \
                \nVolume: {self.volume}\nChapter: {self.number} \
                \nPages: {self.pages}\nRelease Date: {self.release_date}\n'
    
    def __eq__(self, other) -> bool:
        return self.id == other.id
    
    def __ne__(self, other) -> bool:
        return self.id != other.id
    
    def images(self) -> list[str]:
        res = make_request(f'https://api.mangadex.org/at-home/server/{self.id}')
        json: dict[str, Any] = res.json()
        return [ f'{json['baseUrl']}/data/{json['chapter']['hash']}/{img}' for img in json['chapter']['data'] ]

class Manga:
    def __init__(self, info: JSON, from_dict: bool = False) -> None:
        if from_dict:
            self.id: str = info['id']
            self.title: str = info['title']
            self.description: str = info['description']
            self.tags: list[str] = info['tags']
            self.demographic: str = info['demographic']
            self.cover_art: str = info['cover_art']
            self.last_chapter: str = info['last_chapter']
            self.last_volume: str = info['last_volume']
        else:
            self.id: str = info['id']
            self.title: str = info['attributes']['title'].get('en', '.')
            self.description: str = info['attributes']['description'].get('en', '.')
            self.tags: list[str] = [ tag['attributes']['name']['en'] for tag in info['attributes']['tags'] ]
            self.demographic: str = info['attributes']['publicationDemographic']
            self.cover_art: str = [ el['id'] for el in info['relationships'] if el['type'] == 'cover_art' ][0]
            self.last_chapter: str = info['attributes']['lastChapter']
            self.last_volume: str = info['attributes']['lastVolume']

    def __repr__(self) -> str:
        return f'Title: {self.title}\nID: {self.id} \
                        \nDescription: {self.description} \
                        \nTags: {', '.join(self.tags)}\n'
    
    def to_dict(self) -> JSON:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'tags': self.tags,
            'demographic' : self.demographic,
            'cover_art' : self.cover_art,
            'last_chapter' : self.last_chapter,
            'last_volume' : self.last_volume,
        }
    
    def __eq__(self, other) -> bool:
        return self.id == other.id
    
    def __ne__(self, other) -> bool:
        return self.id != other.id
    
    def chapters(self) -> list[Chapter]:
        res = make_request(f'https://api.mangadex.org/manga/{self.id}/feed')
        return sorted([ Chapter(ch) for ch in res.json()['data'] if ch['attributes']['translatedLanguage'] == 'en'], 
                             key=lambda ch: 
                             (float(ch.volume) if ch.volume else None,
                              float(ch.number) if ch.number else None))

    def cover(self) -> str:
        cover_response = make_request(f'https://api.mangadex.org/cover/{self.cover_art}')
        cover_filename: str = cover_response.json()['data']['attributes']['fileName']
        return f'https://uploads.mangadex.org/covers/{self.id}/{cover_filename}.256.jpg'
 
class Book(Manga):
    def __init__(self, info: JSON, chapter: int = 0, volume: int = 0, from_dict: bool = False) -> None:
        if from_dict:
            self.chapter: int = info['current_chapter']
            self.volume: int = info['current_volume']
        else:
            self.chapter: int = chapter
            self.volume: int = volume
        super().__init__(info, from_dict)

    def to_dict(self) -> JSON:
        return {
            **{
                'current_chapter' : self.chapter,
                'current_volume' : self.volume
            },
            **super().to_dict()
        }
    
    @staticmethod
    def properties() -> list[str]:
        return ['id', 'title', 'demographic', 'last_chapter', 'current_chapter']

    def read_chapter(self) -> None:
        self.chapter += 1
    
    def __repr__(self):
        return super().__repr__() + f'Chaprers Read: {self.chapter}\n'

class Library:
    def __init__(self, mangas: list[Manga] | JSON, from_dict: bool = False) -> None:
        if from_dict:
            self.books: list[Book] = [ Book(bk, from_dict=True) for bk in mangas['books'] ]
        else:
            self.books: list[Book] = [ Book(mgn, 0) for mgn in mangas ]

    def get(self, key: str) -> Book:
        return [ bk for bk in self.books if bk.id == key ][0]
    
    def set(self, key: str, value: Book) -> None:
        self.books = [ bk for bk in self.books if bk.id != key ] + [value]

    def to_dict(self) -> JSON:
        return {
            'books' : [ bk.to_dict() for bk in self.books ]
        }

    def add(self, manga: Manga) -> None:
        if not self.has(manga):
            self.books.append(manga)
    
    def remove(self, manga: Manga) -> None:
        self.books = [ book for book in self.books if book.id != manga.id ]

    def has(self, manga: Manga) -> bool:
        return manga.id in [ book.id for book in self.books ]
    
    def sort(self, property: str, order: str) -> None:
        props: list[str] = Book.properties()
        if property in props:
            self.books.sort(key=lambda bk: bk.to_dict()[property], reverse=(order == 'desc'))
    
    def filter(self, genre: str) -> None:
        if genre != 'Any':
            self.books = [ bk for bk in self.books if genre in bk.tags ]

    
class User:
    def __init__(self, json: JSON) -> None:
        self.username: str = json['username']
        self.password: str = json['password']
        self.library: Library = Library(json['library'], True)

    def to_dict(self) -> JSON:
        return {
            'username' : self.username,
            'password' : self.password,
            'library' : self.library.to_dict()
        }
    
    def update(self, manga: Manga, chapter: JSON) -> None:
        self.library.set(manga.id,
                         Book(manga.to_dict() | chapter, 
                              from_dict=True))

def get_manga(id: str) -> Manga:
    manga_url: str = f'https://api.mangadex.org/manga/{id}'
    response = make_request(manga_url)
    return Manga(response.json()['data'])

def get_genres() -> list[str]:
    tags: JSON = make_request('https://api.mangadex.org/manga/tag').json()
    return sorted([ tag['attributes']['name']['en'] for tag in tags['data'] ])

def make_request(url: str, params: dict[str, str] = {}) -> Any:
    headers: dict[str, str] = {
        'User-Agent' : 'MangaApp/1.0 (https://github.com/MasterGar1/manga-web-app)'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 429:
            print('Rate exceeded!')
            sleep(2)
            return make_request(url, params)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None

