import os
from textnode import TextNode, TextType
from copy_static_content import copy_static_content
from site_generator import generate_page

ROOT_DIR = os.getcwd()
STATIC_PATH = os.path.join(ROOT_DIR, "static")
PUBLIC_PATH = os.path.join(ROOT_DIR, "public")
TEMPLATE_PATH = os.path.join(ROOT_DIR, "template.html")
CONTENT_PATH = os.path.join(ROOT_DIR, "content")


def main():
    copy_static_content(STATIC_PATH, PUBLIC_PATH)

    MD_INDEX_PATH = os.path.join(CONTENT_PATH, "index.md")
    HTML_INDEX_PATH = os.path.join(PUBLIC_PATH, "index.html")
    generate_page(MD_INDEX_PATH, TEMPLATE_PATH, HTML_INDEX_PATH)


if __name__ == "__main__":
    main()
