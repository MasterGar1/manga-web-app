"""Unittests for utility module"""
import unittest
from src.utility import encrypt, decrypt, split_words

class TestsUtility(unittest.TestCase):
    def test_encrypt_decrypt(self):
        """Tests Case for encryption/decryption"""
        original_text = "HelloWorld"
        key = 69
        encrypted_text = encrypt(original_text, key)
        decrypted_text = decrypt(encrypted_text, key)
        self.assertEqual(original_text, decrypted_text)

    def test_split_words_pascal(self):
        """Test case for split with PascalCase"""
        self.assertEqual(split_words("HelloWorld"), "Hello world")

    def test_split_words_camel(self):
        """Test case for split with camelCase"""
        self.assertEqual(split_words("splitWordsFunction"), "Split words function")

    def test_split_words_snake(self):
        """Test case for split with snake_case"""
        self.assertEqual(split_words("another_test_case"), "Another test case")

if __name__ == '__main__':
    unittest.main()