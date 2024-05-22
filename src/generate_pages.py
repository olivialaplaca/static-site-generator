import os.path
from pathlib import Path
from block_markdown import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("Title not found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with (
        open(from_path) as s,
        open(template_path) as t
    ):
        source = s.read()
        template = t.read()
    contents = markdown_to_html_node(source).to_html()
    title = extract_title(source)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", contents)
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as d:
        d.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        old_path = os.path.join(dir_path_content, filename)
        new_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(old_path):
            new_path = Path(new_path).with_suffix(".html")
            generate_page(old_path, template_path, new_path)
        else:
            generate_pages_recursive(old_path, template_path, new_path)
