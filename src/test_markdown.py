import unittest

from htmlnode import ParentNode, LeafNode
from markdown import markdown_to_html_node, extract_title

markdown = '''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

```
def foo="bar"
```

1. Foo
1. Bar

> Cinnamonrolls
> are
> amazing
'''

class TestBlock(unittest.TestCase):
    def test_to_blocks(self):
        result = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            LeafNode("h1", "This is a heading"),
            ParentNode("p", [
                LeafNode(None, "This is a paragraph of text. It has some "),
                LeafNode("b", "bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
                LeafNode(None, " words inside of it."),
            ]),
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode(None, "This is the first list item in a list block"),
                ]),
                ParentNode("li", [
                    LeafNode(None, "This is a list item"),
                ]),
                ParentNode("li", [
                    LeafNode(None, "This is another list item"),
                ]),
            ]),
            ParentNode("pre", [
                LeafNode("code", "def foo=\"bar\""),
            ]),
            ParentNode("ol", [
                ParentNode("li", [
                    LeafNode(None, "Foo"),
                ]),
                ParentNode("li", [
                    LeafNode(None, "Bar"),
                ]),
            ]),
            ParentNode("blockquote", [
                LeafNode(None, "Cinnamonrolls\nare\namazing"),
            ]),
        ])
        self.assertEqual(result, expected)

    def test_extract_title(self):
        result = extract_title("# Test Title\nFoo bar")
        expected = "Test Title"
        self.assertEqual(result, expected)

    def test_extract_title_missing(self):
        self.assertRaises(Exception, extract_title, "Foo bar")

if __name__ == "__main__":
    unittest.main()
