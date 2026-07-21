import unittest

from block_md import (
    BlockType,
    block_to_block_type,
    code_to_html_node,
    heading_to_html_node,
    markdown_to_blocks,
    ordered_list_to_html_node,
    paragraph_to_html_node,
    quote_to_html_node,
    unordered_list_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        self.assertEqual(markdown_to_blocks(""), [])
        self.assertEqual(markdown_to_blocks("   \n\n  \n"), [])

    def test_markdown_to_blocks_single_block(self):
        blocks = markdown_to_blocks("just one paragraph")
        self.assertEqual(blocks, ["just one paragraph"])

    def test_markdown_to_blocks_strips_inner_whitespace(self):
        md = "   some text  \n\nanother block\t\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["some text", "another block"])


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_code(self):
        block = "```\ncode block\nline two\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> line one\n> line two"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- item one\n- item two"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. item one\n2. item two\n3. item three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "Just a regular paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_with_language_tag(self):
        block = "```python\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_single_line_unclosed_is_paragraph(self):
        block = "```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_non_sequential_is_paragraph(self):
        block = "5. item one\n5. item two\n9. item three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_must_start_at_one(self):
        block = "2. item one\n3. item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestParagraphToHTMLNode(unittest.TestCase):
    def test_simple(self):
        node = paragraph_to_html_node("Just some plain text.")
        self.assertEqual(node.to_html(), "<p>Just some plain text.</p>")

    def test_inline_markdown(self):
        node = paragraph_to_html_node("This is **bold** and _italic_ text")
        self.assertEqual(
            node.to_html(),
            "<p>This is <b>bold</b> and <i>italic</i> text</p>",
        )

    def test_multiline_collapses_to_spaces(self):
        node = paragraph_to_html_node("line one\nline two\nline three")
        self.assertEqual(node.to_html(), "<p>line one line two line three</p>")


class TestHeadingToHTMLNode(unittest.TestCase):
    def test_h1(self):
        node = heading_to_html_node("# Heading")
        self.assertEqual(node.to_html(), "<h1>Heading</h1>")

    def test_h6(self):
        node = heading_to_html_node("###### Deep heading")
        self.assertEqual(node.to_html(), "<h6>Deep heading</h6>")

    def test_heading_with_inline_markdown(self):
        node = heading_to_html_node("## A **bold** heading")
        self.assertEqual(node.to_html(), "<h2>A <b>bold</b> heading</h2>")


class TestCodeToHTMLNode(unittest.TestCase):
    def test_simple(self):
        block = "```\ncode line one\ncode line two\n```"
        node = code_to_html_node(block)
        self.assertEqual(
            node.to_html(),
            "<pre><code>code line one\ncode line two\n</code></pre>",
        )

    def test_code_ignores_inline_markdown(self):
        block = "```\nnot **bold** here\n```"
        node = code_to_html_node(block)
        self.assertEqual(
            node.to_html(),
            "<pre><code>not **bold** here\n</code></pre>",
        )


class TestQuoteToHTMLNode(unittest.TestCase):
    def test_single_line(self):
        node = quote_to_html_node("> a wise quote")
        self.assertEqual(node.to_html(), "<blockquote>a wise quote</blockquote>")

    def test_multiline(self):
        node = quote_to_html_node("> line one\n> line two")
        self.assertEqual(node.to_html(), "<blockquote>line one line two</blockquote>")

    def test_quote_with_inline_markdown(self):
        node = quote_to_html_node("> a **bold** quote")
        self.assertEqual(node.to_html(), "<blockquote>a <b>bold</b> quote</blockquote>")

    def test_quote_with_empty_line(self):
        node = quote_to_html_node("> line one\n>\n> line two")
        self.assertEqual(node.to_html(), "<blockquote>line one  line two</blockquote>")


class TestUnorderedListToHTMLNode(unittest.TestCase):
    def test_simple(self):
        node = unordered_list_to_html_node("- item one\n- item two")
        self.assertEqual(node.to_html(), "<ul><li>item one</li><li>item two</li></ul>")

    def test_items_with_inline_markdown(self):
        node = unordered_list_to_html_node("- an _italic_ item\n- a `code` item")
        self.assertEqual(
            node.to_html(),
            "<ul><li>an <i>italic</i> item</li><li>a <code>code</code> item</li></ul>",
        )


class TestOrderedListToHTMLNode(unittest.TestCase):
    def test_simple(self):
        node = ordered_list_to_html_node("1. first\n2. second\n3. third")
        self.assertEqual(
            node.to_html(),
            "<ol><li>first</li><li>second</li><li>third</li></ol>",
        )

    def test_items_with_inline_markdown(self):
        node = ordered_list_to_html_node("1. a **bold** item\n2. plain item")
        self.assertEqual(
            node.to_html(),
            "<ol><li>a <b>bold</b> item</li><li>plain item</li></ol>",
        )


if __name__ == "__main__":
    unittest.main()
