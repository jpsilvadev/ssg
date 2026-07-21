import os
import shutil
import sys
import tomllib

from generate_content import generate_page_recursive

CONFIG_PATH = "./config.toml"


def main() -> None:
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    paths = load_config()

    clear_dir(paths["output"])
    copy_recursive(paths["static"], paths["output"])

    generate_page_recursive(
        paths["content"], paths["template"], paths["output"], basepath
    )


def load_config(path: str | os.PathLike[str] = CONFIG_PATH) -> dict[str, str]:
    with open(path, "rb") as f:
        return tomllib.load(f)["paths"]


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
