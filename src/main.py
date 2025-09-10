import os, shutil

from textnode import TextNode, TextType


def main():
    public_dir = 'public'
    static_dir = 'static'

    clear_public(public_dir)
    copy_files(static_dir, public_dir)


def clear_public(dir):
    
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)

def copy_files(dir, target):
    dir_content = os.listdir(dir)
    for item in dir_content:
        item_path = os.path.join(dir, item)
        target_path = os.path.join(target, item)
        if os.path.isdir(item_path):
            print(f'DIR {item_path}')
            os.mkdir(target_path)
            copy_files(item_path, target_path)
        else:
            print(f'FILE {item_path}')
            shutil.copy(item_path, target_path)

if __name__ == "__main__":
    main()