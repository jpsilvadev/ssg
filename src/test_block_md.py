import unittest
from block_md import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_md_blocks(self):
        md_document = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        self.assertEqual(
            markdown_to_blocks(md_document),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
        )

    def test_md_blocks_multiple_blank_lines(self):
        md_document = """
# This is a heading



This is a paragraph of text. It has some **bold** and *italic* words inside of it.
"""
        self.assertEqual(
            markdown_to_blocks(md_document),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_headings(self):
        self.assertEqual(block_to_block_type("# Valid heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#Invalid heading"), BlockType.PARAGRAPH)
        self.assertEqual(
            block_to_block_type("####### Too many headings"), BlockType.PARAGRAPH
        )

    def test_codeblocks(self):
        self.assertEqual(block_to_block_type("```\nsome code\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```no closing"), BlockType.PARAGRAPH)

    def test_quotes(self):
        self.assertEqual(block_to_block_type(">line1\n>line2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">line1\nline2"), BlockType.PARAGRAPH)

    def test_unordered_lists(self):
        self.assertEqual(block_to_block_type("* item1\n* item2"), BlockType.UL)
        self.assertEqual(block_to_block_type("- item1\n- item2"), BlockType.UL)
        self.assertEqual(block_to_block_type("*no space"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("no token"), BlockType.PARAGRAPH)

    def test_ordered_lists(self):
        self.assertEqual(block_to_block_type("1. first\n2. second"), BlockType.OL)
        # handle multiple digits
        self.assertEqual(
            block_to_block_type(
                "1. one\n2. two\n3. three\n4. four\n5. five\n6. six\n7. seven\n8. eight\n9. nine\n10. ten\n11. eleven"
            ),
            BlockType.OL,
        )
        self.assertEqual(block_to_block_type("1. first\n3. third"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("2. wrong start"), BlockType.PARAGRAPH)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_heading(self):
        md = """
# This is a title heading

Some p text here

## This is a subtitle heading
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a title heading</h1><p>Some p text here</p><h2>This is a subtitle heading</h2></div>",
        )

    def test_code(self):
        md = """
This is some text with `inline code`
and some more text and

```
code block
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is some text with <code>inline code</code> and some more text and</p><pre><code>code block\n</code></pre></div>",
        )

    def test_quote(self):
        md = """
> This is a quote block
> with multiple lines

and some text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote block with multiple lines</blockquote><p>and some text</p></div>",
        )

    def test_ul(self):
        md = """
- This is a list
- with another item
- and *important* items
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with another item</li><li>and <i>important</i> items</li></ul></div>",
        )

    def test_ol(self):
        md = """
1. This is a list
2. with another item
3. and even more items     
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is a list</li><li>with another item</li><li>and even more items</li></ol></div>",
        )

    def test_paragraph(self):
        md = """
This is a paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a paragraph</p></div>")


if __name__ == "__main__":
    unittest.main()
