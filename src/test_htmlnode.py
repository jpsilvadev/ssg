import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("p", "some text")
        self.assertEqual(
            repr(node),
            "HTMLNode(p, some text, None, None)",
        )

    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_not_eq_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertNotEqual(
            node.props_to_html(), ' href="https://www.somesite.com" target="_blank"'
        )


class TestLeafNode(unittest.TestCase):
    def test_repr(self):
        node = LeafNode("p", "some text here", None)
        self.assertEqual(
            repr(node),
            "LeafNode(p, some text here, None)",
        )

    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.", None)
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )
