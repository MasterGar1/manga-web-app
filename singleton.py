class Manga:
    def __init__(self, info : dict) -> None:
        self.id : str = info['id']
        self.title : str = info['attributes']['title']['en']
        self.description : str = info['attributes']['description']['en']
        self.tags : list[str] = [ tag['attributes']['name']['en'] for tag in info['attributes']['tags'] ]

    def __repr__(self) -> str:
        return f'Title: {self.title}\nID: {self.id}\nDescription: {self.description}\nTags: {', '.join(self.tags)}\n'
    
    def __eq__(self, other) -> bool:
        return self.title == other.title
    
    def __ne__(self, other) -> bool:
        return self.title != other.title
    
class Book(Manga):
    def __init__(self, info : dict, chapter : int = 0) -> None:
        self.chapter = chapter
        super().__init__(info)

    def read_chapter(self) -> None:
        self.chapter += 1
    
    def __repr__(self):
        return super().__repr__() + f'Chaprers Read: {self.chapter}'

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
