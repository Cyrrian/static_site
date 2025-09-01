from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    TEXT_PLAIN = 'plain'
    TEXT_BOLD = 'bold'
    TEXT_ITALIC = 'italic'
    TEXT_CODE = 'code'
    TEXT_LINK = 'link'
    TEXT_IMAGE = 'image'

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT_PLAIN:
            return LeafNode(None, text_node.text, None)
        case TextType.TEXT_BOLD:
            return LeafNode('b', text_node.text, None)
        case TextType.TEXT_ITALIC:
            return LeafNode('i', text_node.text, None)
        case TextType.TEXT_CODE:
            return LeafNode('code', text_node.text, None)
        case TextType.TEXT_LINK:
            return LeafNode('a', text_node.text, {'href': text_node.url})
        case TextType.TEXT_IMAGE:
            return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})
        case _:
            raise Exception('unknown TextType')

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT_PLAIN:
            new_nodes.append(node)
            continue
        nodes_to_add = []
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise Exception('Wrong number of delimeters')
        for i in range(len(split_node)):
            if split_node[i] == '':
                continue
            if i % 2 == 0:
                nodes_to_add.append(TextNode(split_node[i], TextType.TEXT_PLAIN))
            else:
                nodes_to_add.append(TextNode(split_node[i], text_type))
        new_nodes.extend(nodes_to_add)
    return new_nodes