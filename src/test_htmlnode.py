import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self) -> None:
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty(self) -> None:
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self) -> None:
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple(self) -> None:
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_repr_default(self) -> None:
        node = HTMLNode()
        self.assertEqual("HTMLNode(None, None, children: None, None)", repr(node))

    def test_repr_values(self) -> None:
        node = HTMLNode(
            "a",
            "Click me",
            None,
            {"href": "https://www.google.com"},
        )
        self.assertEqual(
            "HTMLNode(a, Click me, children: None, {'href': 'https://www.google.com'})",
            repr(node),
        )

    def test_repr_with_children(self) -> None:
        child = HTMLNode("span", "child text")
        node = HTMLNode("div", None, [child], None)
        self.assertEqual(
            f"HTMLNode(div, None, children: [{repr(child)}], None)",
            repr(node),
        )


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self) -> None:
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self) -> None:
        node = LeafNode("a", "Click me", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me</a>'
        )

    def test_leaf_to_html_no_tag(self) -> None:
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


if __name__ == "__main__":
    unittest.main()
