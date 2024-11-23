from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    result = []
    blocks = re.split(r"\n\n", markdown)
    for b in blocks:
        stripped = b.strip()
        if stripped == "":
            continue
        result.append(stripped)
    return result

def block_to_block_type(block: str) -> BlockType:
    if re.match(r"#+ ", block) != None:
        return BlockType.HEADING
    elif block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE

    lines = block.splitlines()
    is_quote = True
    is_unordered = True
    is_ordered = True
    for line in lines:
        if line[:2] != "> ":
            is_quote = False
        if line[:2] != "* " and line[:1] != "- ":
            is_unordered = False
        if not line[0].isdigit() and line[1] != '.':
            is_ordered = False
    if is_quote:
        return BlockType.QUOTE
    if is_unordered:
        return BlockType.UNORDERED_LIST
    if is_ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
