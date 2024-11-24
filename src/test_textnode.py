import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links, text_to_textnodes


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

    def test_split_nodes_simple(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        expected_nodes = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_multiple(self):
        node = TextNode("This is an *italic text* with a **bold** word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is an ", TextType.NORMAL),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" with a ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_unclosed(self):
        node = TextNode("This is *text* with a *broken italic", TextType.NORMAL)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "*", TextType.ITALIC)

    def test_extract_markdown_images(self):
        extracted = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extracted, expected)

    def test_extract_markdown_links(self):
        extracted = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extracted, expected)

    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with an image ![boot dev favicon](https://www.boot.dev/favicon.ico) and ![dev boot favicon](https://www.dev.boot/favicon.ico)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node])
        expected = [
            TextNode("This is text with an image ", TextType.NORMAL),
            TextNode("boot dev favicon", TextType.IMAGE, "https://www.boot.dev/favicon.ico"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("dev boot favicon", TextType.IMAGE, "https://www.dev.boot/favicon.ico"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_links([node])
        expected = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_images_and_links(self):
        node = TextNode(
            "This is text with an image ![boot dev favicon](https://www.boot.dev/favicon.ico) and ![dev boot favicon](https://www.dev.boot/favicon.ico) and [to boot dev](https://www.boot.dev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node])
        new_nodes = split_nodes_links(new_nodes)
        expected = [
            TextNode("This is text with an image ", TextType.NORMAL),
            TextNode("boot dev favicon", TextType.IMAGE, "https://www.boot.dev/favicon.ico"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("dev boot favicon", TextType.IMAGE, "https://www.dev.boot/favicon.ico"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_text_to_textnodes(self):
        input = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(input)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)

if __name__ == "__main__":
    unittest.main()
