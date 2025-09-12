import unittest

from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_b2bt_para(self):
        block = 'This is just text'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_b2bt_code(self):
        block = '```This is a code block```'
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_b2bt_heading(self):
        block = '##### This is a heading'
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_b2bt_quote(self):
        block = '> This is a quote'
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_b2bt_unordered(self):
        block = '- Thing one'
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_b2bt_ordered(self):
        block = '1. First thing'
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_markdown_to_blocks(self):
        md = '''
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
'''
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                'This is **bolded** paragraph',
                'This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line',
                '- This is a list\n- with items',
            ],
        )

    def test_markdown_to_blocks2(self):
        md = '''
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
'''
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                'This is **bolded** paragraph',
                'This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line',
                '- This is a list\n- with items',
            ],
        )

    def test_m2h_paragraphs(self):
        md = '''
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

'''

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_m2h_headings(self):
        md = '''
## This is an h2 heading

#### This is an h4 heading

This is a regular paragraph

'''

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is an h2 heading</h2><h4>This is an h4 heading</h4><p>This is a regular paragraph</p></div>",
        )

    def test_m2h_codeblock(self):
        md = '''
```
This is text that _should_ remain
the **same** even with inline stuff
```
'''

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_m2h_quote(self):
        md = '''>This is a quote block.
>With two lines.
'''

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote block. With two lines.</blockquote></div>",
        )

    def test_m2h_ul(self):
        md = '''- Item 1
- Item 2
- Item 3
'''

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_m2h_ul2(self):
        md = '''
- Item 1
- _Item 2_
- Item 3
'''

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li><i>Item 2</i></li><li>Item 3</li></ul></div>",
        )

    def test_m2h_ol(self):
        md = '''1. Item 1
2. Item 2
3. Item 3
'''

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()