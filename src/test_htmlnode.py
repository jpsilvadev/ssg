import unittest

from htmlnode import HTMLNode


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
        self.assertEqual("HTMLNode(None, None, None, None)", repr(node))

    def test_repr_values(self) -> None:
        node = HTMLNode(
            "a",
            "Click me",
            None,
            {"href": "https://www.google.com"},
        )
        self.assertEqual(
            "HTMLNode(a, Click me, None, {'href': 'https://www.google.com'})",
            repr(node),
        )

    def test_repr_with_children(self) -> None:
        child = HTMLNode("span", "child text")
        node = HTMLNode("div", None, [child], None)
        self.assertEqual(
            f"HTMLNode(div, None, [{repr(child)}], None)",
            repr(node),
        )


if __name__ == "__main__":
    unittest.main()
