from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"


def markdown_to_blocks(markdown):
    # blocks are separated by blank lines
    # if block ensures that we don't get empty strings
    # when blocks are separated by more than 1 blank line
    blocks = [block.strip() for block in markdown.split("\n\n") if block]
    return blocks


def block_to_block_type(md_block):

    # detect heading block
    if md_block.startswith("#"):
        heading_count = 0
        for char in md_block:
            if char == "#":
                heading_count += 1
            else:
                break

        if heading_count > 6:
            return BlockType.PARAGRAPH

        if len(md_block) > heading_count + 2:
            if md_block[heading_count] == " " and md_block[heading_count + 1] != " ":
                return BlockType.HEADING

    # detect code block
    if md_block.startswith("```") and md_block.endswith("```"):
        return BlockType.CODE

    # detect quote block
    is_quote = True
    for line in md_block.splitlines():
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE

    # detect unordered lists
    is_ul = True
    for item in md_block.splitlines():
        if not (item.startswith("* ") or item.startswith("- ")):
            is_ul = False
            break
    if is_ul:
        return BlockType.UL

    # detect ordered lists
    is_ol = True
    ol_int = 1
    for item in md_block.splitlines():
        if "." not in item:
            is_ol = False
            break
        current_num, text = item.split(".", 1)
        if current_num.isdigit():
            current_num = int(current_num)
        if current_num == ol_int and text.startswith(" "):
            ol_int += 1
        else:
            is_ol = False
            break
    if is_ol:
        return BlockType.OL

    return BlockType.PARAGRAPH
