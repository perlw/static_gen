import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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

    def test_to_html_node_normal(self):
        node = TextNode("Text", TextType.NORMAL)
        html = text_node_to_html_node(node).to_html()
        self.assertEqual(html, "Text")

    def test_to_html_node_bold(self):
        node = TextNode("Text", TextType.BOLD)
        html = text_node_to_html_node(node).to_html()
        self.assertEqual(html, "<b>Text</b>")

    def test_to_html_node_italic(self):
        node = TextNode("Text", TextType.ITALIC)
        html = text_node_to_html_node(node).to_html()
        self.assertEqual(html, "<i>Text</i>")

    def test_to_html_node_code(self):
        node = TextNode("Text", TextType.CODE)
        html = text_node_to_html_node(node).to_html()
        self.assertEqual(html, "<code>Text</code>")

    def test_to_html_node_link(self):
        node = TextNode("Text", TextType.LINK, "https://boot.dev")
        html = text_node_to_html_node(node).to_html()
        self.assertEqual(html, "<a href=\"https://boot.dev\">Text</a>")

    def test_to_html_node_image(self):
        node = TextNode("Text", TextType.IMAGE, "https://boot.dev/favicon.ico")
        html = text_node_to_html_node(node).to_html()
        self.assertEqual(html, "<img src=\"https://boot.dev/favicon.ico\" alt=\"Text\"></img>")


if __name__ == "__main__":
    unittest.main()
