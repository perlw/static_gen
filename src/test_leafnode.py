import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("div", "content")
        node2 = LeafNode("div", "content")
        self.assertEqual(node, node2)

    def test_no_value(self):
        node = LeafNode("div", None)
        self.assertRaises(Exception, node.to_html)

    def test_no_tag(self):
        node = LeafNode("", "content")
        html = node.to_html()
        self.assertEqual(html, "content")

    def test_render_tag(self):
        node = LeafNode("div", "content")
        html = node.to_html()
        self.assertEqual(html, "<div>content</div>")

    def test_render_tag_with_props(self):
        node = LeafNode("div", "content", { "class": "test_class" })
        html = node.to_html()
        self.assertEqual(html, "<div class=\"test_class\">content</div>")

if __name__ == "__main__":
    unittest.main()
