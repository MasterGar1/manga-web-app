"""Contains all classes and the make request function"""
from time import sleep
from typing import Any

import requests

class Chapter:
    """Class implementation for chapter"""
    def __init__(self, info: dict[str, Any]) -> None:
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
        """Returns a list of links to all chapter images"""
        res = make_request(f'https://api.mangadex.org/at-home/server/{self.id}')
        json: dict[str, Any] = res.json()
        return [ f'{json['baseUrl']}/data/{json['chapter']['hash']}/{img}'
                for img in json['chapter']['data'] ]

class Manga:
    """Class implementation for manga"""
    def __init__(self, info: dict[str, Any], from_dict: bool = False) -> None:
        if from_dict:
            self.id: str = info['id']
            self.title: str = info['title']
            self.description: str = info['description']
            self.tags: list[str] = info['tags']
            self.demographic: str = info['demographic']
            self.cover_art: str = info['cover_art']
            self.last_chapter: tuple[str, str] = (info['last_chapter'], info['last_volume'])
        else:
            self.id: str = info['id']
            self.title: str = info['attributes']['title'].get('en', '.')
            self.description: str = info['attributes']['description'].get('en', '.')
            self.tags: list[str] = [ tag['attributes']['name']['en']
                                    for tag in info['attributes']['tags'] ]
            self.demographic: str = info['attributes']['publicationDemographic']
            [self.cover_art] = [ el['id']
                                for el in info['relationships']
                                if el['type'] == 'cover_art' ]
            self.last_chapter: tuple[str, str] = (info['attributes']['lastChapter'],
                                                  info['attributes']['lastVolume'])

    def __repr__(self) -> str:
        return f'Title: {self.title}\nID: {self.id} \
                        \nDescription: {self.description} \
                        \nTags: {', '.join(self.tags)}\n'

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __ne__(self, other) -> bool:
        return self.id != other.id

    def to_dict(self) -> dict[str, Any]:
        """Convert object to dict"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'tags': self.tags,
            'demographic' : self.demographic,
            'cover_art' : self.cover_art,
            'last_chapter' : self.last_chapter[0],
            'last_volume' : self.last_chapter[1],
        }

    def chapters(self) -> list[Chapter]:
        """Return list of chapters"""
        res = make_request(f'https://api.mangadex.org/manga/{self.id}/feed')
        return sorted([ Chapter(ch) for ch in res.json()['data']
                       if ch['attributes']['translatedLanguage'] == 'en'],
                             key=lambda ch:
                             (float(ch.volume) if ch.volume else None,
                              float(ch.number) if ch.number else None))

    def cover(self) -> str:
        """Get cover image"""
        cover_response = make_request(f'https://api.mangadex.org/cover/{self.cover_art}')
        cover_filename: str = cover_response.json()['data']['attributes']['fileName']
        return f'https://uploads.mangadex.org/covers/{self.id}/{cover_filename}.256.jpg'

class Book(Manga):
    """Class implementation for a Book > Manga"""
    def __init__(self, info: dict[str, Any] | Manga, chapter: int = 0,
                 volume: int = 0, from_dict: bool = False) -> None:
        if from_dict:
            self.chapter: int = info.get('current_chapter', 0)
            self.volume: int = info.get('current_volume', 0)
        else:
            self.chapter: int = chapter
            self.volume: int = volume
        super().__init__(info, from_dict)

    def __repr__(self):
        return super().__repr__() + f'Chaprers Read: {self.chapter}\n'

    def to_dict(self) -> dict[str, Any]:
        """Convert object to dict"""
        return {
            **{
                'current_chapter' : self.chapter,
                'current_volume' : self.volume
            },
            **super().to_dict()
        }

    @staticmethod
    def properties() -> list[str]:
        """Get property list"""
        return ['id', 'title', 'last_chapter', 'current_chapter']

class Library:
    """Class implementation for a book library"""
    def __init__(self, mangas: list[Manga] | dict[str, Any], from_dict: bool = False) -> None:
        if from_dict:
            self.books: list[Book] = [ Book(bk, from_dict=True)
                                      for bk in mangas['books'] ]
        else:
            self.books: list[Book] = [ Book(mgn.to_dict(), from_dict=True)
                                      for mgn in mangas ]

    def get(self, key: str) -> Book:
        """Get book by key"""
        return [ bk for bk in self.books if bk.id == key ][0]

    def set(self, key: str, value: Book) -> None:
        """Set a book"""
        self.books = [ bk for bk in self.books if bk.id != key ] + [value]

    def to_dict(self) -> dict[str, Any]:
        """Convert object to dict"""
        return {
            'books' : [ bk.to_dict() for bk in self.books ]
        }

    def add(self, manga: Manga) -> None:
        """Add a new book"""
        if not self.has(manga):
            self.books.append(manga)

    def remove(self, manga: Manga) -> None:
        """Remove a book"""
        self.books = [ book for book in self.books if book.id != manga.id ]

    def has(self, manga: Manga) -> bool:
        """Check if book exists"""
        return manga.id in [ book.id for book in self.books ]

    def sort(self, prop: str, order: str) -> None:
        """Sort library"""
        ordir: bool = order == 'desc'
        if prop in Book.properties():
            if prop == 'last_chapter':
                self.books.sort(key=lambda bk: float(bk.to_dict()[prop][0]), reverse=ordir)
            elif prop == 'current_chapter':
                self.books.sort(key=lambda bk: float(bk.to_dict()[prop]), reverse=ordir)
            else:
                self.books.sort(key=lambda bk: bk.to_dict()[prop], reverse=ordir)

    def filter(self, genre: str) -> None:
        """Filter library"""
        if genre != 'Any':
            self.books = [ bk for bk in self.books
                          if genre in bk.tags ]

class User:
    """Class implementation for a User profile"""
    def __init__(self, json: dict[str, Any]) -> None:
        self.username: str = json['username']
        self.password: str = json['password']
        self.library: Library = Library(json['library'], True)

    def to_dict(self) -> dict[str, Any]:
        """Convert object to dict"""
        return {
            'username' : self.username,
            'password' : self.password,
            'library' : self.library.to_dict()
        }

    def update(self, manga: Manga, chapter: dict[str, Any]) -> None:
        """Update user"""
        self.library.set(manga.id,
                         Book(manga.to_dict() | chapter,
                              from_dict=True))

def make_request(url: str, params: dict[str, str] = None) -> Any:
    """Request maker"""
    if params is None:
        params = {}
    headers: dict[str, str] = {
        'User-Agent' : 'MangaApp/1.0 (https://github.com/MasterGar1/manga-web-app)'
    }
    try:
        response = requests.get(url, headers=headers,
                                params=params, timeout=10)
        if response.status_code == 429:
            print('Rate exceeded!')
            sleep(2)
            return make_request(url, params)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None
