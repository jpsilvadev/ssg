import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
    def test_leaf_to_html_no_value(self) -> None:
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

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

    def test_leaf_to_html_no_tag_ignores_props(self) -> None:
        node = LeafNode(None, "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "Hello, world!")


class TestParentNode(unittest.TestCase):
    def test_to_html_no_children(self) -> None:
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_empty_children(self) -> None:
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_tag(self) -> None:
        parent_node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_children(self) -> None:
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self) -> None:
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self) -> None:
        parent_node = ParentNode(
            "p",
            [
                LeafNode(None, "Bold text soon: "),
                LeafNode("b", "bold"),
                LeafNode(None, "!"),
            ],
        )
        self.assertEqual(parent_node.to_html(), "<p>Bold text soon: <b>bold</b>!</p>")

    def test_to_html_with_props(self) -> None:
        parent_node = ParentNode(
            "p",
            [LeafNode(None, "Hello")],
            props={"class": "greeting"},
        )
        self.assertEqual(parent_node.to_html(), '<p class="greeting">Hello</p>')

    def test_repr(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "bold"),
            ],
            props={"class": "greeting"},
        )
        self.assertEqual(node.to_html(), '<p class="greeting"><b>bold</b></p>')


if __name__ == "__main__":
    unittest.main()
