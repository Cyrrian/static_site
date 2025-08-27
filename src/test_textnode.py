import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT_BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT_BOLD)
        self.assertEqual(node, node2)
    def test_textdiff(self):
        node = TextNode("This is a text node", TextType.TEXT_BOLD)
        node2 = TextNode("This is a test text node", TextType.TEXT_BOLD)
        self.assertNotEqual(node, node2)
    def test_texttypediff(self):
        node = TextNode("This is a text node", TextType.TEXT_BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT_ITALIC)
        self.assertNotEqual(node, node2)
    def test_texturldiff(self):
        node = TextNode("This is a text node", TextType.TEXT_LINK, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.TEXT_LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()