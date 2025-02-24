import os
from block_md import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line.lstrip("# ").strip()
            return title

    raise ValueError("Title not found")


def generate_page(src_path, template_path, dest_path):
    print(f"Generating page from {src_path} to {dest_path} using {template_path}")

    with open(src_path, "r", encoding="utf-8") as file:
        markdown = file.read()

    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()

    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)

    # swap extension to html
    root, _ = os.path.splitext(dest_path)

    # ensure path exists
    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    dest_path = root + ".html"
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(html)


def generate_pages_recursive(src_path, template_path, dest_path):
    if os.path.isfile(src_path):
        generate_page(src_path, template_path, dest_path)
    else:
        for item in os.listdir(src_path):
            src_item = os.path.join(src_path, item)
            dest_item = os.path.join(dest_path, item)

            if os.path.isfile(src_item):
                generate_page(src_item, template_path, dest_item)
            else:
                generate_pages_recursive(src_item, template_path, dest_item)
