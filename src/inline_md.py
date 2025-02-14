import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []

    for old_node in old_nodes:
        # if not text type, don't need to split
        if old_node.text_type != TextType.TEXT:
            nodes.append(old_node)
            continue

        split_nodes = []
        segments = old_node.text.split(delimiter)

        # if the count of indices is not even
        # it means we're missing a matching/closing token
        if len(segments) % 2 == 0:
            raise ValueError("invalid markdown, missing closing token")

        for i in range(len(segments)):  # pylint: disable=consider-using-enumerate
            # prevent appending empty strings of TextType when the string contains
            # multiple token types -> for example splitting bold and italic
            # need true index, enumerate idx gets incremented when checking for empty strings
            if segments[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(segments[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(segments[i], text_type))

        nodes.extend(split_nodes)
    return nodes


def extract_markdown_images(text):
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    image_matches = re.findall(image_pattern, text)
    return image_matches


def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    link_matches = re.findall(link_pattern, text)
    return link_matches


def split_nodes_image(old_nodes):
    for old_node in old_nodes:
        image_nodes = extract_markdown_images(old_node.text)

        nodes = []

        # needs to be sliced off each iteration
        text_to_process = old_node.text
        for image_node in image_nodes:
            before, after = text_to_process.split(
                f"![{image_node[0]}]({image_node[1]})", 1
            )

            # can use TextNode here to avoid processing downstream
            nodes.append(TextNode(before, TextType.TEXT))

            # handle the link itself
            nodes.append(TextNode(image_node[0], TextType.IMAGE, image_node[1]))

            text_to_process = after

        # handle remaining text or return original object if no images were provided
        if text_to_process:
            nodes.append(TextNode(text_to_process, TextType.TEXT))

    return nodes


def split_nodes_link(old_nodes):
    for old_node in old_nodes:
        link_nodes = extract_markdown_links(old_node.text)

        nodes = []

        # needs to be sliced off each iteration
        text_to_process = old_node.text
        for link_node in link_nodes:
            before, after = text_to_process.split(
                f"[{link_node[0]}]({link_node[1]})", 1
            )

            # can use TextNode here to avoid processing downstream
            nodes.append(TextNode(before, TextType.TEXT))

            # handle the link itself
            nodes.append(TextNode(link_node[0], TextType.LINK, link_node[1]))

            text_to_process = after

        # handle remaining text or return original object if no links were provided
        if text_to_process:
            nodes.append(TextNode(text_to_process, TextType.TEXT))

    return nodes
