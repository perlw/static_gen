import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq_optional(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_eq_tag(self):
        node = HTMLNode("div")
        node2 = HTMLNode("div")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = HTMLNode("div")
        node2 = HTMLNode()
        self.assertNotEqual(node, node2)

    def test_eq_children(self):
        node = HTMLNode(children = [ HTMLNode(), HTMLNode() ])
        node2 = HTMLNode(children = [ HTMLNode(), HTMLNode() ])
        self.assertEqual(node, node2)

    def test_neq_children(self):
        node = HTMLNode(children = [ HTMLNode("div"), HTMLNode() ])
        node2 = HTMLNode(children = [ HTMLNode("a"), HTMLNode() ])
        self.assertNotEqual(node, node2)

    def test_eq_props(self):
        node = HTMLNode(props = { "prop": "value" })
        node2 = HTMLNode(props = { "prop": "value" })
        self.assertEqual(node, node2)

    def test_neq_props(self):
        node = HTMLNode(props = { "propa": "value" })
        node2 = HTMLNode(props = { "propb": "value" })
        self.assertNotEqual(node, node2)

    def test_to_html(self):
        node = HTMLNode()
        self.assertRaises(Exception, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode(props = {
            "propa": "valuea",
            "propb": "valueb",
            "propc": "valuec",
        })
        self.assertEqual(node.props_to_html(), "propa=valuea propb=valueb propc=valuec")


if __name__ == "__main__":
    unittest.main()
