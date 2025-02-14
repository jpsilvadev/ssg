import unittest
from textnode import TextNode, TextType
from inline_md import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_delim_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_delim_italic(self):
        node = TextNode("This is text with a *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_delim_double_bold(self):
        node = TextNode(
            "This is text with a **bold** word and **another** one", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
                TextNode(" one", TextType.TEXT),
            ],
        )

    def test_delim_double_italic(self):
        node = TextNode(
            "This is text with a *italic* word and *another* one", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.ITALIC),
                TextNode(" one", TextType.TEXT),
            ],
        )

    def test_delim_bold_and_italic(self):
        node = TextNode(
            "This is text with a **bold** word and *italic* word", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        newer_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertEqual(
            newer_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_delim_italic_multiword(self):
        node = TextNode("This is text with a *italic multi word* format", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic multi word", TextType.ITALIC),
                TextNode(" format", TextType.TEXT),
            ],
        )


class TestExtractMarkdownImages(unittest.TestCase):
    def test_image_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_image_extraction2(self):
        text = "This is text with a ![funny image](https://i.imgur.com/testabc.gif) and ![not fun image](https://i.imgur.com/testxyz.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("funny image", "https://i.imgur.com/testabc.gif"),
                ("not fun image", "https://i.imgur.com/testxyz.jpeg"),
            ],
        )

    def test_no_image(self):
        text = "This is text without images"
        self.assertEqual(extract_markdown_images(text), [])


class TestExtractMarkDownLinks(unittest.TestCase):
    def test_link_extraction(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_no_link(self):
        text = "This is text without links"
        self.assertEqual(extract_markdown_links(text), [])


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode(
            "This is text and here is an image ![alt text](https://example.com/image.png) followed by more text.",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("This is text and here is an image ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" followed by more text.", TextType.TEXT),
            ],
        )

    def test_EOL_image(self):
        node = TextNode(
            "This is text and here is an image ![alt text](https://example.com/image.png)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("This is text and here is an image ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
            ],
        )

    def test_multiple_images(self):
        node = TextNode(
            "This is text and here is an image ![alt text](https://example.com/image.png) followed by another ![alt text second image](https://example.com/image2.png).",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("This is text and here is an image ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" followed by another ", TextType.TEXT),
                TextNode(
                    "alt text second image",
                    TextType.IMAGE,
                    "https://example.com/image2.png",
                ),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_no_images(self):
        # return the original TextNode
        node = TextNode("This is text without images", TextType.TEXT)
        self.assertEqual(
            split_nodes_image([node]),
            [TextNode("This is text without images", TextType.TEXT)],
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            "Here is [a link](https://example.com) and some more text after it.",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://example.com"),
                TextNode(" and some more text after it.", TextType.TEXT),
            ],
        )

    def test_EOL_link(self):
        node = TextNode(
            "This is text with a link [to example](https://example.com)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to example", TextType.LINK, "https://example.com"),
            ],
        )

    def test_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube",
                    TextType.LINK,
                    "https://www.youtube.com/@bootdotdev",
                ),
            ],
        )

    def test_no_links(self):
        # return the original TextNode
        node = TextNode("This is text without links", TextType.TEXT)
        self.assertEqual(
            split_nodes_link([node]),
            [TextNode("This is text without links", TextType.TEXT)],
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_all_tokens(self):
        md_sting = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnodes(md_sting),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_no_tokens(self):
        text_string = "This is some text without md tokens"
        self.assertEqual(
            text_to_textnodes(text_string),
            [TextNode("This is some text without md tokens", TextType.TEXT)],
        )


if __name__ == "__main__":
    unittest.main()
