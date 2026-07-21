import os
import shutil

from generate_content import generate_page_recursive


def main() -> None:
    src = "./static/"
    dest = "./public/"

    clear_dir(dest)
    copy_recursive(src, dest)

    from_path = "content/"
    template_path = "template.html"
    dest_path = "public/"
    generate_page_recursive(from_path, template_path, dest_path)


def copy_recursive(
    src: str | os.PathLike[str] = "static/", dest: str | os.PathLike[str] = "public/"
) -> None:
    src_path = os.path.join(os.getcwd(), os.fspath(src))
    dest_path = os.path.join(os.getcwd(), os.fspath(dest))

    # base case -> src is file
    if os.path.isfile(src_path):
        print(f"{src_path} -> {dest_path}")
        shutil.copy(src_path, dest_path)
        return

    # if not file -> src is a directory
    if not os.path.exists(dest_path):
        print(f"mkdir {dest_path}")
        os.mkdir(dest_path)

    for item in os.listdir(src_path):
        source_item = os.path.join(src_path, item)
        dest_item = os.path.join(dest_path, item)
        copy_recursive(source_item, dest_item)


def clear_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


if __name__ == "__main__":
    main()
