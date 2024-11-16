from typing import Self
from enum import Enum
from htmlnode import LeafNode
import re


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: Self):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match(text_node.text_type):
        case TextType.NORMAL:
            return LeafNode(tag = None, value = text_node.text)
        case TextType.BOLD:
            return LeafNode(tag = "b", value = text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag = "i", value = text_node.text)
        case TextType.CODE:
            return LeafNode(tag = "code", value = text_node.text)
        case TextType.LINK:
            return LeafNode(tag = "a", value = text_node.text, props = { "href": text_node.url })
        case TextType.IMAGE:
            return LeafNode(tag = "img", value = "", props = { "src": text_node.url, "alt": text_node.text })
        case _:
            raise Exception("unknown text type")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        separated = re.split(f"({delimiter})", node.text)
        i = 0
        while i < len(separated):
            if separated[i] != delimiter:
                new_nodes.append(TextNode(separated[i], TextType.NORMAL))
                i += 1
                continue

            if i + 2 > len(separated):
                raise Exception("no closing delimited")
            new_nodes.append(TextNode(separated[i + 1], text_type))
            i += 3

    return new_nodes
