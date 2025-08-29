import unittest

from htmlnode import HTMLNode, LeafNode

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
    def test_leaf_to_html_p(self):
        node = LeafNode('p', 'Hello, world!')
        self.assertEqual(node.to_html(), '<p>Hello, world!</p>')
    def test_leaf_to_html_a(self):
        node = LeafNode(
            'a',
            'Google Link',
            {'href': 'https://www.google.com', 'target': '_blank'}
        )
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Google Link</a>')
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, 'Hello, world!')
        self.assertEqual(node.to_html(), 'Hello, world!')

if __name__ == "__main__":
    unittest.main()