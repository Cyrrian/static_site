import re
from enum import Enum

from textnode import TextNode, TextType, text_to_textnodes, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(markdown):
    lines = markdown.split('\n')

    if len(re.findall(r'#{1,6} .*', markdown)) != 0:
        return BlockType.HEADING
    elif len(re.findall(r'```[\S\s]*```', markdown)) != 0:
        return BlockType.CODE
    elif len(re.findall(r'>.*', markdown)) != 0:
        for line in lines:
            if not line.startswith('>'):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif len(re.findall(r'- .*', markdown)) != 0:
        for line in lines:
            if not line.startswith('-'):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif len(re.findall(r'1\. .*', markdown)) != 0:
        i = 1
        for line in lines:
            if not line.startswith(f'{i}. '):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    new_html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.CODE:
            code_text = re.findall(r'```\n*([\S\s]*)```', block)[0]
            code_text_node = TextNode(code_text, TextType.TEXT_CODE)
            code_html_node = text_node_to_html_node(code_text_node)
            new_html_nodes.append(ParentNode('pre', [code_html_node]))
        else:
            text_nodes = text_to_textnodes(block)
            html_nodes_to_add = []
            for text_node in text_nodes:
                text_node.text = text_node.text.replace('\n', ' ')
                if block_type == BlockType.HEADING:
                    text_node.text = re.findall(r'#{1,6} (.*)', text_node.text)[0]
                    html_nodes_to_add.append(text_node_to_html_node(text_node))
                elif block_type == BlockType.QUOTE:
                    text_node.text = re.findall(r'>(.*)', text_node.text)[0]
                    html_nodes_to_add.append(text_node_to_html_node(text_node))
                elif block_type == BlockType.UNORDERED_LIST:
                    split_nodes = split_lists_node(text_node, block_type)
                    for node in split_nodes:
                        html_nodes_to_add.append(ParentNode('li', [text_node_to_html_node(node)]))
                elif block_type == BlockType.ORDERED_LIST:
                    split_nodes = split_lists_node(block, block_type)
                    for node in split_nodes:
                        html_nodes_to_add.append(ParentNode('li', [text_node_to_html_node(node)]))
                else:
                    html_nodes_to_add.append(text_node_to_html_node(text_node))
            if block_type == BlockType.PARAGRAPH:
                new_html_nodes.append(ParentNode('p', html_nodes_to_add))
            elif block_type == BlockType.HEADING:
                h_count = len(re.findall(r'(#{1,6}) .*', block)[0])
                new_html_nodes.append(ParentNode(f'h{h_count}', html_nodes_to_add))
            elif block_type == BlockType.QUOTE:
                new_html_nodes.append(ParentNode('blockquote', html_nodes_to_add))
            elif block_type == BlockType.UNORDERED_LIST:
                new_html_nodes.append(ParentNode('ul', html_nodes_to_add))
            elif block_type ==BlockType.ORDERED_LIST:
                new_html_nodes.append(ParentNode('ol', html_nodes_to_add))
    return ParentNode('div', new_html_nodes)

def split_lists_node(original_node, type):
    new_nodes = []
    if type == BlockType.UNORDERED_LIST:
        for item in original_node.text.split('-'):
            new_nodes.extend(text_to_textnodes(item.strip()))
    elif type == BlockType.ORDERED_LIST:
            split_items = original_node.split('\n')
            for item in split_items:
                item = re.findall(r'\d+\. (.*)', item)[0]
                new_nodes.extend(text_to_textnodes(item.strip()))
    return new_nodes