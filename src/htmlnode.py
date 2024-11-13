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
        pairs = []
        for k, v in self.props.items():
            pairs.append(f"{k}={v}")
        return ' '.join(pairs)
