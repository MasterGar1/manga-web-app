import requests

class Chapter:
    def __init__(self, info : dict) -> None:
        self.id : str = info['id']
        self.title : str = info['attributes']['title']
        self.volume : float = info['attributes']['volume']
        self.number : float = info['attributes']['chapter']
        self.pages : int = info['attributes']['pages']
        self.release_date : str = info['attributes']['publishAt']
        self.language : str = info['attributes']['translatedLanguage']

    def __repr__(self) -> str:
        return f'Title: {self.title}\nID: {self.id} \
                \nVolume: {self.volume}\nChapter: {self.number} \
                \nPages: {self.pages}\nRelease Date: {self.release_date}\n'
    
    def __eq__(self, other) -> bool:
        return self.id == other.id
    
    def __ne__(self, other) -> bool:
        return self.id != other.id
    
    def images(self) -> list[str]:
        res = requests.get(f'https://api.mangadex.org/at-home/server/{self.id}')
        json : dict = res.json()
        return [ f'{json['baseUrl']}/data/{json['chapter']['hash']}/{img}' for img in json['chapter']['data'] ]

class Manga:
    def __init__(self, info : dict) -> None:
        self.id : str = info['id']
        self.title : str = info['attributes']['title']['en']
        self.description : str = info['attributes']['description']['en']
        self.tags : list[str] = [ tag['attributes']['name']['en'] for tag in info['attributes']['tags'] ]
        self.demographic : str = info['attributes']['publicationDemographic']
        # self.status : str = info['attributes']['completed']
        self.cover_art : str = [ el['id'] for el in info['relationships'] if el['type'] == 'cover_art' ][0]
        self.last_chapter : float = info['attributes']['lastChapter']
        self.last_volume : float = info['attributes']['lastVolume']
        self.chapters : list[Chapter] = self.load_chapters()

    def __repr__(self) -> str:
        return f'Title: {self.title}\nID: {self.id} \
                        \nDescription: {self.description} \
                        \nTags: {', '.join(self.tags)}\n'
    
    def __eq__(self, other) -> bool:
        return self.id == other.id
    
    def __ne__(self, other) -> bool:
        return self.id != other.id
    
    def load_chapters(self) -> list[Chapter]:
        res = requests.get(f'https://api.mangadex.org/manga/{self.id}/feed')
        return sorted(filter(lambda ch: ch.language == 'en', 
                       [ Chapter(ch) for ch in res.json()['data'] ]), 
                             key=lambda ch: ch.number)

    def cover(self) -> str:
        return f'https://uploads.mangadex.org/covers/{self.id}/{self.cover_art}'
        
    
class Book(Manga):
    def __init__(self, info : dict, chapter : int = 0) -> None:
        self.chapter = chapter
        super().__init__(info)

    def read_chapter(self) -> None:
        self.chapter += 1
    
    def __repr__(self):
        return super().__repr__() + f'Chaprers Read: {self.chapter}\n'

class Library:
    def __init__(self, mangas : list[Book]) -> None:
        self.books = mangas

    def add(self, manga : Manga) -> None:
        if not self.has(manga):
            self.books.append(manga)
    
    def remove(self, manga : Manga) -> None:
        self.books = [ book for book in self.books if book[0] != manga ]

    def has(self, manga : Manga) -> bool:
        return manga in [ book[0] for book in self.books ]
    
class User:
    def __init__(self, nick : str, password : str, lib : Library) -> None:
        pass
