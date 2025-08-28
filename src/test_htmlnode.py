import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(
            'a',
            'some text',
            None,
            {'href': 'https://www.google.com', 'target': '_blank'}
        )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    def test_values(self):
        node = HTMLNode(
            'p',
            'some text',
        )
        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, 'some text')
    def test_repr(self):
        node = HTMLNode(
            'p',
            'Hello world',
            None,
            {'class': 'primary'}
       )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, Hello world, children: None, {'class': 'primary'})",
        )

if __name__ == "__main__":
    unittest.main()