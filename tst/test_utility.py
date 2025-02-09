"""Unittests for utility module"""
import unittest
from src.utility import encrypt, decrypt, split_words, fix_hyphon

class TestsUtility(unittest.TestCase):
    """Tests for utility functions"""
    def test_encrypt_decrypt(self) -> None:
        """Tests Case for encryption/decryption"""
        original_text = "HelloWorld"
        key = 69
        encrypted_text = encrypt(original_text, key)
        decrypted_text = decrypt(encrypted_text, key)
        self.assertEqual(original_text, decrypted_text)

    def test_split_words_pascal(self) -> None:
        """Test case for split with PascalCase"""
        self.assertEqual(split_words("HelloWorld"), "Hello world")

    def test_split_words_camel(self) -> None:
        """Test case for split with camelCase"""
        self.assertEqual(split_words("splitWordsFunction"), "Split words function")

    def test_split_words_snake(self) -> None:
        """Test case for split with snake_case"""
        self.assertEqual(split_words("another_test_case"), "Another test case")

    def test_fix_hyphon(self) -> None:
        """Test case for fix_hyphon function"""
        self.assertEqual(fix_hyphon("Girls' Love"), "Yuri")
        self.assertEqual(fix_hyphon("Boys' Love"), "Yaoi")
        self.assertEqual(fix_hyphon("Yuri"), "Girls' Love")
        self.assertEqual(fix_hyphon("Yaoi"), "Boys' Love")
        self.assertEqual(fix_hyphon("Action"), "Action")

if __name__ == '__main__':
    unittest.main()
