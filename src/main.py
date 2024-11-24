import os
import shutil

def copy_static_files(dest, source):
    if not os.path.exists(dest):
        os.mkdir(dest)
    for path in os.listdir(source):
        fullpath = os.path.join(source, path)
        if os.path.isdir(fullpath):
            copy_static_files(os.path.join(dest, path), fullpath)
        elif os.path.isfile(fullpath):
            shutil.copy(fullpath, os.path.join(dest, path))

def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    copy_static_files("./public", "./static")


if __name__ == "__main__":
    main()
