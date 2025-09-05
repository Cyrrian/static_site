import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT_PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.TEXT_BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is a italic text node", TextType.TEXT_ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is a italic text node")

    def test_code(self):
        node = TextNode("This is a code text node", TextType.TEXT_CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a code text node")

    def test_link(self):
        node = TextNode("This is a link text node", TextType.TEXT_LINK, 'https://www.boot.dev')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {'href': 'https://www.boot.dev'})

    def test_img(self):
        node = TextNode("This is a image text node", TextType.TEXT_IMAGE, 'helloworld.png')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'helloworld.png', 'alt': 'This is a image text node'})

    def test_delimeter_code(self):
        node = TextNode('This is text with a `code block` word', TextType.TEXT_PLAIN)
        new_nodes = split_nodes_delimiter([node], '`', TextType.TEXT_CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT_PLAIN),
                                     TextNode("code block", TextType.TEXT_CODE),
                                     TextNode(" word", TextType.TEXT_PLAIN),
                                    ])
        
    def test_delim_bold_multiword(self):
        node = TextNode(
            'This is text with a **bolded word** and **another**', TextType.TEXT_PLAIN
        )
        new_nodes = split_nodes_delimiter([node], '**', TextType.TEXT_BOLD)
        self.assertListEqual(new_nodes, 
            [
                TextNode('This is text with a ', TextType.TEXT_PLAIN),
                TextNode('bolded word', TextType.TEXT_BOLD),
                TextNode(' and ', TextType.TEXT_PLAIN),
                TextNode('another', TextType.TEXT_BOLD),
            ]
        )

    def test_delim_bold_and_italic(self):
        node = TextNode('**bold** and _italic_', TextType.TEXT_PLAIN)
        new_nodes = split_nodes_delimiter([node], '**', TextType.TEXT_BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.TEXT_ITALIC)
        self.assertListEqual(new_nodes, 
            [
                TextNode('bold', TextType.TEXT_BOLD),
                TextNode(' and ', TextType.TEXT_PLAIN),
                TextNode('italic', TextType.TEXT_ITALIC),
            ]
        )
    
    def test_extract_markdown_image(self):
        matches = extract_markdown_images('This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)')
        self.assertListEqual(matches, [('image', 'https://i.imgur.com/zjjcJKZ.png')])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images('This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)')
        self.assertListEqual(matches, [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])

    def test_extract_markdown_links(self):
        matches = extract_markdown_links('This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)')
        self.assertListEqual(matches, [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')])

    def test_split_images(self):
        node = TextNode('This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)', TextType.TEXT_PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes,
            [
                TextNode('This is text with an ', TextType.TEXT_PLAIN),
                TextNode('image', TextType.TEXT_IMAGE, 'https://i.imgur.com/zjjcJKZ.png'),
                TextNode(' and another ', TextType.TEXT_PLAIN),
                TextNode('second image', TextType.TEXT_IMAGE, 'https://i.imgur.com/3elNhQu.png'),
            ]
        )

    def test_split_links(self):
        node = TextNode('This is text with an [Link](https://www.google.com) and another [Second Link](https://www.boot.dev)', TextType.TEXT_PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes,
            [
                TextNode('This is text with an ', TextType.TEXT_PLAIN),
                TextNode('Link', TextType.TEXT_LINK, 'https://www.google.com'),
                TextNode(' and another ', TextType.TEXT_PLAIN),
                TextNode('Second Link', TextType.TEXT_LINK, 'https://www.boot.dev'),
            ]
        )

    def test_text_to_textnodes(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes,
            [
                TextNode('This is ', TextType.TEXT_PLAIN),
                TextNode('text', TextType.TEXT_BOLD),
                TextNode(' with an ', TextType.TEXT_PLAIN),
                TextNode('italic', TextType.TEXT_ITALIC),
                TextNode(' word and a ', TextType.TEXT_PLAIN),
                TextNode('code block', TextType.TEXT_CODE),
                TextNode(' and an ', TextType.TEXT_PLAIN),
                TextNode('obi wan image', TextType.TEXT_IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg'),
                TextNode(' and a ', TextType.TEXT_PLAIN),
                TextNode('link', TextType.TEXT_LINK, 'https://boot.dev'),
            ]
        )

if __name__ == "__main__":
    unittest.main()