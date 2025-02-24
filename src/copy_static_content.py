import os
import shutil


def copy_static_content(src, dest):
    ROOT_DIR = os.getcwd()
    src = os.path.join(ROOT_DIR, src)
    dest = os.path.join(ROOT_DIR, dest)

    if os.path.exists(dest):
        shutil.rmtree(dest)

    if not os.path.exists(dest):
        os.makedirs(dest)

    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)

        if os.path.isfile(src_item):
            shutil.copy(src_item, dest_item)
        else:
            copy_static_content(src_item, dest_item)
