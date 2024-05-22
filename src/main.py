import shutil
from copy_files import copy_directory
from generate_pages import generate_pages_recursive


def main():
    content = "content/"
    static_content = "static/"
    dest = "public/"
    shutil.rmtree(dest)
    copy_directory(static_content, dest)
    generate_pages_recursive(content, "template.html", dest)

main()