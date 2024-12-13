import unittest
from your_app import get_user_language  # Replace with your app's filename

class TestLanguageSelection(unittest.TestCase):

    def test_valid_language_choices(self):
        # Test valid language choices (1, 2, 3)
        for choice in ['1', '2', '3']:
            language = get_user_language()
            self.assertIn(language, ['en', 'pt_PT', 'de'])  # Expected language codes

    def test_invalid_language_choice(self):
        # Test invalid language choice (4)
        with self.assertRaises(SystemExit):
            get_user_language()  # Should raise SystemExit on invalid input

if __name__ == '__main__':
    unittest.main()
