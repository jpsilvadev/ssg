import os
from copy_static_content import copy_static_content
from site_generator import generate_pages_recursive

ROOT_DIR = os.getcwd()
STATIC_PATH = os.path.join(ROOT_DIR, "static")
PUBLIC_PATH = os.path.join(ROOT_DIR, "public")
TEMPLATE_PATH = os.path.join(ROOT_DIR, "template.html")
CONTENT_PATH = os.path.join(ROOT_DIR, "content")


def main():
    copy_static_content(STATIC_PATH, PUBLIC_PATH)
    generate_pages_recursive(CONTENT_PATH, TEMPLATE_PATH, PUBLIC_PATH)


if __name__ == "__main__":
    main()
