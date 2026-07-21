import os
from pathlib import Path

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
    basepath: str | os.PathLike[str] = "/",  # tweak to allow github pages hosting
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

    # tweaks to allow github pages hosting
    html_to_write = html_to_write.replace('href="/', f'href="{basepath}')
    html_to_write = html_to_write.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html_to_write)


def generate_page_recursive(
    dir_path_content: str | os.PathLike[str],
    template_path: str | os.PathLike[str],
    dest_dir_path: str | os.PathLike[str],
    basepath: str | os.PathLike[str] = "/",
) -> None:
    dir_path_content = os.path.join(os.getcwd(), os.fspath(dir_path_content))
    template_path = os.path.join(os.getcwd(), os.fspath(template_path))
    dest_dir_path = os.path.join(os.getcwd(), os.fspath(dest_dir_path))

    # base case -> markdown file found
    if os.path.isfile(dir_path_content):
        path = Path(dest_dir_path)
        updated_dest_path = path.with_suffix(".html")
        generate_page(dir_path_content, template_path, updated_dest_path, basepath)
        return

    # handle dirs
    for item in os.listdir(dir_path_content):
        deeper_src_path = os.path.join(dir_path_content, item)
        deeper_dest_path = os.path.join(dest_dir_path, item)
        generate_page_recursive(
            deeper_src_path, template_path, deeper_dest_path, basepath
        )
