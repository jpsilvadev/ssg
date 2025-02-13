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
