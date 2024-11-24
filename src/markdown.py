from block import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import ParentNode, LeafNode
from textnode import text_to_textnodes, text_node_to_html_node

def text_to_children(markdown: str) -> list[LeafNode]:
    children = []
    text_nodes = text_to_textnodes(markdown)
    for t in text_nodes:
        node = text_node_to_html_node(t)
        children.append(node)
    return children

def markdown_to_html_node(markdown: str) -> ParentNode:
    top_nodes = []

    blocks = markdown_to_blocks(markdown)
    for b in blocks:
        block_type = block_to_block_type(b)

        match block_type:
            case BlockType.HEADING:
                heading_depth = b.count('#')
                if heading_depth > 6:
                    heading_depth = 6

                node = LeafNode(f"h{heading_depth}", b[heading_depth + 1:])
                top_nodes.append(node)

            case BlockType.PARAGRAPH:
                children = text_to_children(b)
                node = ParentNode("p", children)
                top_nodes.append(node)

            case BlockType.CODE:
                node = ParentNode("pre", [
                    LeafNode("code", b[4:-4])
                ])
                top_nodes.append(node)

            case BlockType.QUOTE:
                text = '\n'.join(map(lambda x: x[2:], b.splitlines()))
                children = text_to_children(text)
                node = ParentNode("blockquote", children)
                top_nodes.append(node)

            case BlockType.UNORDERED_LIST:
                items = list(map(lambda x: x[2:], b.splitlines()))
                children = list(map(lambda x: ParentNode("li", text_to_children(x)), items))
                node = ParentNode("ul", children)
                top_nodes.append(node)

            case BlockType.ORDERED_LIST:
                items = list(map(lambda x: x[3:], b.splitlines()))
                children = list(map(lambda x: ParentNode("li", text_to_children(x)), items))
                node = ParentNode("ol", children)
                top_nodes.append(node)

    root = ParentNode("div", top_nodes)
    return root

def extract_title(markdown: str) -> str:
    line = markdown.splitlines()[0]
    if line[0] != '#':
        raise Exception("missing title")
    return line[2:].strip()
