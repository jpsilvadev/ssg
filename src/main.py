from textnode import TextNode, TextType
from copy_static_content import copy_static_content

STATIC_PATH = "static"
PUBLIC_PATH = "public"


def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")

    copy_static_content(STATIC_PATH, PUBLIC_PATH)


if __name__ == "__main__":
    main()
