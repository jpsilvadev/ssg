import re
from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_md import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip() != ""]


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    # HEADING
    if re.match(r"^#{1,6}\s+.+$", block):
        return BlockType.HEADING

    # CODE
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    # QUOTE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # UNORDERED_LIST
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # ORDERED_LIST
    if all(re.match(rf"^{i}\.\s+", line) for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)

    children: list[HTMLNode] = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children


def paragraph_to_html_node(block: str) -> HTMLNode:
    children = text_to_children(block.replace("\n", " "))
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> HTMLNode:
    parts = block.split(" ", maxsplit=1)
    heading_count = len(parts[0])

    children = text_to_children(parts[1].lstrip())
    return ParentNode(f"h{heading_count}", children)


def code_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    code_text = "\n".join(lines[1:-1]) + "\n"
    code_wrapped = LeafNode("code", code_text)
    return ParentNode("pre", [code_wrapped])


def quote_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    quote_text = " ".join(
        line.lstrip(">").strip() for line in lines
    )  # strip '>' or '> '
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")

    li_items: list[HTMLNode] = []
    for line in lines:
        item_text = line[2:]  # strip '- '
        item_children = text_to_children(item_text)
        item_node = ParentNode("li", item_children)
        li_items.append(item_node)
    return ParentNode("ul", li_items)


def ordered_list_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")

    li_items: list[HTMLNode] = []
    for line in lines:
        # strip '1. '
        # cant use slicing (i.e [2:]) because might be '10. ' or '100. '
        _, item_text = line.split(". ", 1)
        item_children = text_to_children(item_text)
        item_node = ParentNode("li", item_children)
        li_items.append(item_node)
    return ParentNode("ol", li_items)


def block_to_html_node(block: str, block_type: BlockType) -> HTMLNode:
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    else:
        raise ValueError(f"invalid block type: {block_type}")


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        children.append(html_node)

    return ParentNode("div", children)
