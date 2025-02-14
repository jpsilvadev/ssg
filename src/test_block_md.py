import unittest
from block_md import BlockType, markdown_to_blocks, block_to_block_type


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


if __name__ == "__main__":
    unittest.main()
