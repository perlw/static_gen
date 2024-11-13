import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_with_url(self):
        node = TextNode("This is a text node", TextType.NORMAL, "https://boot.dev")
        self.assertEqual(node.url, "https://boot.dev")

    def test_without_url(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(node.url, None)

if __name__ == "__main__":
    unittest.main()
