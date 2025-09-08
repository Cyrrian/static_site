import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip()
        if blocks[i] == "":
            del blocks[i]
            i = i - 1
    return blocks

def block_to_block_type(markdown):
    if len(re.findall(r'#{1,6} .*', markdown)) != 0:
        return BlockType.HEADING
    elif len(re.findall(r'```.*```', markdown)) != 0:
        return BlockType.CODE
    elif len(re.findall(r'>.*', markdown)) != 0:
        return BlockType.QUOTE
    elif len(re.findall(r'- .*', markdown)) != 0:
        return BlockType.UNORDERED_LIST
    elif len(re.findall(r'1\. .*', markdown)) != 0:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH