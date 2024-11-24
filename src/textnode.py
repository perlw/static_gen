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

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        i = 0
        while i < len(node.text):
            start = node.text.find(delimiter, i)
            if start == -1:
                new_nodes.append(TextNode(node.text[i:], TextType.NORMAL))
                break
            elif start - i > 1:
                new_nodes.append(TextNode(node.text[i:start], TextType.NORMAL))
            stop = node.text.find(delimiter, start + len(delimiter))
            if stop == -1:
                raise Exception("no closing delimiter")
            new_nodes.append(TextNode(node.text[start + len(delimiter):stop], text_type))
            i = stop + len(delimiter)

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        tuples = extract_markdown_images(node.text)
        if len(tuples) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        for t in tuples:
            sections = text.split(f"![{t[0]}]({t[1]})", 1)
            new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(t[0], TextType.IMAGE, t[1]))
            text = sections[1]

        if text != "":
            new_nodes.append(TextNode(text, TextType.NORMAL))

    return new_nodes

def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        tuples = extract_markdown_links(node.text)
        if len(tuples) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        for t in tuples:
            sections = text.split(f"[{t[0]}]({t[1]})", 1)
            new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(t[0], TextType.LINK, t[1]))
            text = sections[1]

        if text != "":
            new_nodes.append(TextNode(text, TextType.NORMAL))

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    result = split_nodes_delimiter([TextNode(text, TextType.NORMAL)], "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "*", TextType.ITALIC)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    result = split_nodes_images(result)
    result = split_nodes_links(result)
    return result

