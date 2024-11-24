import os
import shutil

from markdown import markdown_to_html_node, extract_title

def copy_static_files(source: str, dest: str):
    if not os.path.exists(dest):
        os.mkdir(dest)
    for path in os.listdir(source):
        fullpath = os.path.join(source, path)
        if os.path.isdir(fullpath):
            copy_static_files(fullpath, os.path.join(dest, path))
        elif os.path.isfile(fullpath):
            shutil.copy(fullpath, os.path.join(dest, path))

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md = ""
    try:
        file = open(from_path, )
        md = file.read()
        file.close()
    except Exception as e:
        print(f"could not open {from_path}: {e}")

    html_nodes = markdown_to_html_node(md)
    print(html_nodes)
    print(html_nodes.to_html())

def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    copy_static_files("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")


if __name__ == "__main__":
    main()
