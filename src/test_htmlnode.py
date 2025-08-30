import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
        
    def test_to_html_without_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError)

if __name__ == "__main__":
    unittest.main()