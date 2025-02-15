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

    markdown = ""
    template = ""
    try:
        file = open(from_path)
        markdown = file.read()
        file.close()
    except Exception as e:
        print(f"could not open {from_path}: {e}")

    try:
        file = open(template_path)
        template = file.read()
        file.close()
    except Exception as e:
        print(f"could not open {template_path}: {e}")

    title = extract_title(markdown)
    content_html = markdown_to_html_node(markdown).to_html()
    out_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

    os.makedirs(os.path.dirname(dest_path), exist_ok = True)
    try:
        file = open(dest_path, 'w')
        file.write(out_html)
        file.close()
    except Exception as e:
        print(f"could not open {dest_path}: {e}")

def generate_page_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    for path in os.listdir(dir_path_content):
        full_content_path = os.path.join(dir_path_content, path)
        full_dest_path = os.path.join(dest_dir_path, path)
        if os.path.isdir(full_content_path):
            generate_page_recursive(full_content_path, template_path, full_dest_path)
        elif os.path.isfile(full_content_path):
            generate_page(full_content_path, "./template.html", full_dest_path[:-2] + "html")

def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    copy_static_files("./static", "./public")
    generate_page_recursive("./content", "./template.html", "./public")


if __name__ == "__main__":
    main()
