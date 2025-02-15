"""Unittests for the classes module"""
import unittest
from typing import Any

from src.classes import Manga, Chapter, Library, User

class TestManga(unittest.TestCase):
    """Tests for manga class"""
    def setUp(self) -> None:
        self.manga_info: dict[str, Any] = {
            'id': '1',
            'attributes': {
                'title': {'en': 'Test Manga'},
                'description': {'en': 'Test Description'},
                'tags': [{'attributes': {'name': {'en': 'Action'}}}],
                'publicationDemographic': 'shounen',
                'lastChapter': '10',
                'lastVolume': '1'
            },
            'relationships': [{'id': 'cover1', 'type': 'cover_art'}]
        }
        self.manga: Manga = Manga.from_res(self.manga_info)

    def test_manga_initialization(self) -> None:
        """Test case for manga initialization"""
        self.assertEqual(self.manga.id, '1')
        self.assertEqual(self.manga.title, 'Test Manga')
        self.assertEqual(self.manga.description, 'Test Description')
        self.assertEqual(self.manga.tags, ['Action'])
        self.assertEqual(self.manga.demographic, 'shounen')
        self.assertEqual(self.manga.cover_art, 'cover1')
        self.assertEqual(self.manga.last_chapter, ('10', '1'))

class TestChapter(unittest.TestCase):
    """Tests for chapter class"""
    def setUp(self) -> None:
        self.chapter_info: dict[str, Any] = {
            'id': '1',
            'attributes': {
                'title': 'Chapter 1',
                'volume': '1',
                'chapter': '1',
                'pages': '20',
                'publishAt': '2021-01-01',
                'translatedLanguage': 'en'
            }
        }
        self.chapter = Chapter(self.chapter_info)

    def test_chapter_initialization(self) -> None:
        """Test case for chapter initialization"""
        self.assertEqual(self.chapter.id, '1')
        self.assertEqual(self.chapter.title, 'Chapter 1')
        self.assertEqual(self.chapter.volume, '1')
        self.assertEqual(self.chapter.number, '1')
        self.assertEqual(self.chapter.pages, '20')
        self.assertEqual(self.chapter.release_date, '2021-01-01')
        self.assertEqual(self.chapter.language, 'en')

class TestLibrary(unittest.TestCase):
    """Tests for Library class"""
    def setUp(self) -> None:
        self.manga_info: dict[str, Any] = {
            'id': '1',
            'attributes': {
                'title': {'en': 'Test Manga'},
                'description': {'en': 'Test Description'},
                'tags': [{'attributes': {'name': {'en': 'Action'}}}],
                'publicationDemographic': 'shounen',
                'lastChapter': '10',
                'lastVolume': '1'
            },
            'relationships': [{'id': 'cover1', 'type': 'cover_art'}]
        }
        self.manga: Manga = Manga.from_res(self.manga_info)
        self.library: Library = Library.from_list([self.manga])

    def test_library_add(self) -> None:
        """Test case for library item add"""
        new_manga = Manga.from_res(self.manga_info)
        self.library.add(new_manga)
        self.assertTrue(self.library.has(new_manga))

    def test_library_remove(self) -> None:
        """Test case for library item remove"""
        self.library.remove(self.manga)
        self.assertFalse(self.library.has(self.manga))

    def test_library_sort(self) -> None:
        """Test case for library sort"""
        manga_info_2: dict[str, Any] = {
            'id': '2',
            'attributes': {
                'title': {'en': 'Another Manga'},
                'description': {'en': 'Another Description'},
                'tags': [{'attributes': {'name': {'en': 'Adventure'}}}],
                'publicationDemographic': 'shounen',
                'lastChapter': '5',
                'lastVolume': '1'
            },
            'relationships': [{'id': 'cover2', 'type': 'cover_art'}]
        }
        manga_2: Manga = Manga.from_res(manga_info_2)
        self.library.add(manga_2)
        self.library.sort('title', 'asc')
        self.assertEqual(self.library.books[0].title, 'Another Manga')
        self.library.sort('title', 'desc')
        self.assertEqual(self.library.books[0].title, 'Test Manga')

    def test_library_filter(self) -> None:
        """Test case for library filter"""
        manga_info_2: dict[str, Any] = {
            'id': '2',
            'attributes': {
                'title': {'en': 'Another Manga'},
                'description': {'en': 'Another Description'},
                'tags': [{'attributes': {'name': {'en': 'Adventure'}}}],
                'publicationDemographic': 'shounen',
                'lastChapter': '5',
                'lastVolume': '1'
            },
            'relationships': [{'id': 'cover2', 'type': 'cover_art'}]
        }
        manga_2: Manga = Manga.from_res(manga_info_2)
        self.library.add(manga_2)
        self.library.filter('Adventure')
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, 'Another Manga')

    def test_library_search(self) -> None:
        """Test case for library search"""
        manga_info_2: dict[str, Any] = {
            'id': '2',
            'attributes': {
                'title': {'en': 'Another Manga'},
                'description': {'en': 'Another Description'},
                'tags': [{'attributes': {'name': {'en': 'Adventure'}}}],
                'publicationDemographic': 'shounen',
                'lastChapter': '5',
                'lastVolume': '1'
            },
            'relationships': [{'id': 'cover2', 'type': 'cover_art'}]
        }
        manga_2: Manga = Manga.from_res(manga_info_2)
        self.library.add(manga_2)
        self.library.search('Another')
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, 'Another Manga')

class TestUser(unittest.TestCase):
    """Tests for user class"""
    def setUp(self) -> None:
        self.user_info: dict[str, Any] = {
            'username': 'testuser',
            'password': 'password',
            'library': {
                'books': []
            }
        }
        self.user: User = User(self.user_info)

    def test_user_initialization(self) -> None:
        """Test Case for user initialization"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.password, 'password')
        self.assertIsInstance(self.user.library, Library)

if __name__ == '__main__':
    unittest.main()
