from enum import Enum
from textnode import text_node_to_html_node
from htmlnode import ParentNode
from inline_md import text_to_textnodes


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


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children, None)


def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]


def block_to_html_node(block):
    block_t = block_to_block_type(block)

    if block_t == BlockType.HEADING:
        return heading_to_html_node(block)

    if block_t == BlockType.CODE:
        return code_to_html_node(block)

    if block_t == BlockType.QUOTE:
        return quote_to_html_node(block)

    if block_t == BlockType.UL:
        return ul_to_html_node(block)

    if block_t == BlockType.OL:
        return ol_to_html_node(block)

    if block_t == BlockType.PARAGRAPH:
        return paragraph_to_html_bode(block)

    raise ValueError(f"Invalid BlockType: {block_t}")


def heading_to_html_node(block):
    heading_lvl = 0
    for char in block:
        if char == "#":
            heading_lvl += 1
        else:
            break
    if heading_lvl + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {heading_lvl}")

    text = block[heading_lvl + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{heading_lvl}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")

    text = block[4:-3]
    children = text_to_children(text)
    return ParentNode("pre", [ParentNode("code", children)])


def quote_to_html_node(block):
    lines = block.split("\n")
    quotes = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")

        quotes.append(line.lstrip(">").strip())

    content = " ".join(quotes)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def ul_to_html_node(block):
    lines = block.split("\n")
    ul = []
    for line in lines:
        if not (line.startswith("* ") or line.startswith("- ")):
            raise ValueError("Invalid unordered list block")

        text = line[2:]
        children = text_to_children(text)
        ul.append(ParentNode("li", children))
    return ParentNode("ul", ul)


def ol_to_html_node(block):
    lines = block.split("\n")
    ol = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        ol.append(ParentNode("li", children))
    return ParentNode("ol", ol)


def paragraph_to_html_bode(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)
