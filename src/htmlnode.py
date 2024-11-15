from typing import Self


class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list[Self] = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = None
        self.props = None

        if children != None:
            self.children = children.copy()
        if props != None:
            self.props = props.copy()

    def __eq__(self, other: Self):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplemented

    def props_to_html(self):
        if self.props == None:
            return ""
        pairs = []
        for k, v in self.props.items():
            pairs.append(f"{k}=\"{v}\"")
        return ' '.join(pairs)


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[Self], props: dict[str, str] = None):
        super().__init__(tag = tag, children = children, props = props)

    def to_html(self) -> str:
        if self.tag == None:
            raise ValueError("Parent nodes must have a tag")
        if self.children == None or len(self.children) == 0:
            raise ValueError("Parent nodes must children")
        props = self.props_to_html()
        if props != "":
            props = " " + props
        result = f"<{self.tag}{props}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"
        return result


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] = None):
        super().__init__(tag = tag, value = value, props = props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("Leaf nodes must have a value")
        if self.tag == None or self.tag == "":
            return self.value
        props = self.props_to_html()
        if props != "":
            props = " " + props
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
