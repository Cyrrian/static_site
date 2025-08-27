from enum import Enum

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