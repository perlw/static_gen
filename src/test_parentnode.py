import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node2 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node, node2)

    def test_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        html = node.to_html()
        self.assertEqual(html, "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_no_tag(self):
        node = LeafNode(None, None)
        self.assertRaises(Exception, node.to_html)

    def test_no_children(self):
        node = LeafNode("div", None)
        self.assertRaises(Exception, node.to_html)

    def test_parent_props(self):
        node = ParentNode(
            "p", [ LeafNode("b", "Bold text"), ],
            {
                "class": "test"
            }
        )
        html = node.to_html()
        self.assertEqual(html, "<p class=\"test\"><b>Bold text</b></p>")

    def test_child_props(self):
        node = ParentNode(
            "p", [ LeafNode("b", "Bold text", { "class": "test" }), ],
        )
        html = node.to_html()
        self.assertEqual(html, "<p><b class=\"test\">Bold text</b></p>")

    def test_all_props(self):
        node = ParentNode(
            "p", [ LeafNode("b", "Bold text", { "class": "test" }), ],
            {
                "class": "test"
            }
        )
        html = node.to_html()
        self.assertEqual(html, "<p class=\"test\"><b class=\"test\">Bold text</b></p>")

    def test_nested(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode("p",
                           [
                               LeafNode("i", "italic text"),
                               LeafNode(None, "Normal text"),
                           ]
                           ),
            ],
        )
        html = node.to_html()
        self.assertEqual(html, "<p><b>Bold text</b>Normal text<p><i>italic text</i>Normal text</p></p>")


if __name__ == "__main__":
    unittest.main()
