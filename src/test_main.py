import unittest

from main import extract_title

class TestHTMLNode(unittest.TestCase):
    def test_extract_title(self):
        markdown = '''
# This is the title
This is some extra text
Another line of text
'''
        self.assertEqual(extract_title(markdown), 'This is the title')

    def test_extract_title2(self):
        markdown = '''
## This is the title
This is some extra text
Another line of text
'''
        with self.assertRaises(Exception) as result:
            extract_title(markdown)
        self.assertEqual(str(result.exception), 'No title found')

if __name__ == "__main__":
    unittest.main()