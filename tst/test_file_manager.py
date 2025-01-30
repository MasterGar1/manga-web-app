"""Unittests for the File Manager module"""
import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
from src.file_manager import get_name_pass, load_users, save_user, get_user, delete_user, update_user, update_user_simple
from src.classes import User, Manga

class TestFileManager(unittest.TestCase):
    @patch('src.file_manager.os.listdir')
    @patch('src.file_manager.open', new_callable=mock_open)
    @patch('src.file_manager.json.load')
    @patch('src.file_manager.User', side_effect=lambda x: User(x))
    def test_load_users(self, mock_user, mock_json_load, mock_open, mock_listdir):
        """Test case for Load Users"""
        mock_listdir.return_value = ['user1.json']
        mock_json_load.return_value = {'username': 'user1', 'password': 'pass1', 'library': {'books': []}}
        result = load_users()
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], User)

    @patch('src.file_manager.open', new_callable=mock_open)
    @patch('src.file_manager.encrypt')
    @patch('src.file_manager.json.dumps')
    def test_save_user(self, mock_json_dumps, mock_encrypt, mock_open):
        """Test case for Save User"""
        mock_encrypt.return_value = 'encrypted_user'
        mock_user = MagicMock(username='user1')
        mock_json_dumps.return_value = '{"username": "user1"}'
        save_user(mock_user)
        mock_open.assert_called_once_with(os.path.join('users', 'encrypted_user.json'), 'x', encoding='utf-8')
        mock_open().write.assert_called_once_with('{"username": "user1"}')

    @patch('src.file_manager.os.listdir')
    @patch('src.file_manager.open', new_callable=mock_open)
    @patch('src.file_manager.encrypt')
    @patch('src.file_manager.json.load')
    @patch('src.file_manager.User', side_effect=lambda x: User(x))
    def test_get_user(self, mock_user, mock_json_load, mock_encrypt, mock_open, mock_listdir):
        """Test case for Get User"""
        mock_encrypt.return_value = 'encrypted_user'
        mock_listdir.return_value = ['encrypted_user.json']
        mock_json_load.return_value = {'username': 'user1', 'password': 'pass1', 'library': {'books': []}}
        result = get_user('user1')
        self.assertIsInstance(result, User)

    @patch('src.file_manager.os.remove')
    @patch('src.file_manager.os.path.exists')
    @patch('src.file_manager.encrypt')
    def test_delete_user(self, mock_encrypt, mock_path_exists, mock_remove):
        """Test case for Delete User"""
        mock_encrypt.return_value = 'encrypted_user'
        mock_path_exists.return_value = True
        delete_user('user1')
        mock_remove.assert_called_once_with(os.path.join('users', 'encrypted_user.json'))

    @patch('src.file_manager.get_user')
    @patch('src.file_manager.delete_user')
    @patch('src.file_manager.save_user')
    def test_update_user(self, mock_save_user, mock_delete_user, mock_get_user):
        """Test case for Update User with chapter"""
        mock_user = MagicMock()
        mock_get_user.return_value = mock_user
        mock_manga = MagicMock()
        update_user('user1', mock_manga, {'current_chapter': 5})
        mock_get_user.assert_called_once_with('user1')
        mock_delete_user.assert_called_once_with('user1')
        mock_save_user.assert_called_once_with(mock_user)

    @patch('src.file_manager.delete_user')
    @patch('src.file_manager.save_user')
    def test_update_user_simple(self, mock_save_user, mock_delete_user):
        """Test case for Update User with override"""
        mock_user = MagicMock(username='user1')
        update_user_simple(mock_user)
        mock_delete_user.assert_called_once_with('user1')
        mock_save_user.assert_called_once_with(mock_user)

if __name__ == '__main__':
    unittest.main()