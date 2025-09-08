import unittest

from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks

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

if __name__ == "__main__":
    unittest.main()