import os

from block_md import markdown_to_html_node


def extract_title(markdown: str) -> str:

    has_h1 = False
    heading = ""
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            heading = line
            has_h1 = True
            break
    if not has_h1:
        raise RuntimeError("did not find an h1 heading in content")

    return heading.lstrip("#").strip()


def generate_page(
    from_path: str | os.PathLike[str],
    template_path: str | os.PathLike[str],
    dest_path: str | os.PathLike[str],
) -> None:
    from_path = os.path.join(os.getcwd(), os.fspath(from_path))
    template_path = os.path.join(os.getcwd(), os.fspath(template_path))
    dest_path = os.path.join(os.getcwd(), os.fspath(dest_path))
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()

    html_string = markdown_to_html_node(md_content).to_html()
    page_title = extract_title(md_content)

    html_to_write = html_template.replace("{{ Title }}", page_title)
    html_to_write = html_to_write.replace("{{ Content }}", html_string)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html_to_write)
