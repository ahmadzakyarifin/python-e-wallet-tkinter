import unittest
import sys
import os

# Add parent dir to path so we can import backend
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from backend.utils import validator

class TestValidator(unittest.TestCase):

    def test_email_validation(self):
        self.assertTrue(validator.is_valid_email("test@example.com"))
        self.assertTrue(validator.is_valid_email("user.name@domain.co.id"))
        self.assertFalse(validator.is_valid_email("invalid-email"))
        self.assertFalse(validator.is_valid_email("user@domain"))
        self.assertFalse(validator.is_valid_email("@domain.com"))

    def test_phone_validation(self):
        self.assertTrue(validator.is_valid_phone("08123456789"))
        self.assertTrue(validator.is_valid_phone("089876543210")) # 12 digits
        self.assertFalse(validator.is_valid_phone("0812345")) # too short
        self.assertFalse(validator.is_valid_phone("081234567890123")) # too long
        self.assertFalse(validator.is_valid_phone("18123456789")) # doesn't start with 08
        self.assertFalse(validator.is_valid_phone("abcdefghijk")) # non-numeric

    def test_password_validation(self):
        self.assertTrue(validator.is_valid_password("Password123"))
        self.assertFalse(validator.is_valid_password("weak")) # too short
        self.assertFalse(validator.is_valid_password("nodigits")) # no numbers
        self.assertFalse(validator.is_valid_password("12345678")) # no letters

    def test_username_validation(self):
        self.assertTrue(validator.is_valid_username("user123"))
        self.assertTrue(validator.is_valid_username("us")) # Now allowed
        self.assertTrue(validator.is_valid_username("user!@#")) # Now allowed
        self.assertFalse(validator.is_valid_username("")) # Empty should fail

    def test_pln_validation(self):
        self.assertTrue(validator.is_valid_pln_number("12345678901")) # 11 digits
        self.assertTrue(validator.is_valid_pln_number("123456789012")) # 12 digits
        self.assertFalse(validator.is_valid_pln_number("12345")) # Too short
        self.assertFalse(validator.is_valid_pln_number("123456789012345")) # Too long
        self.assertFalse(validator.is_valid_pln_number("123abc78901")) # Non-numeric

if __name__ == "__main__":
    unittest.main()
