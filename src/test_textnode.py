import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ineq_text(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_ineq_type(self) -> None:
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_ineq_links(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD, "https://www.google.com/")
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertNotEqual(node, node2)

    def test_eq_links(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD, "https://www.google.com/")
        node2 = TextNode(
            "This is a text node", TextType.BOLD, "https://www.google.com/"
        )
        self.assertEqual(node, node2)

    def test_eq_none_links(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_repr(self) -> None:
        node = TextNode("This is a text node", TextType.TEXT, "https://www.google.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.google.dev)", repr(node)
        )


if __name__ == "__main__":
    unittest.main()
