import sys, os, shutil

from textnode import TextNode, TextType
from markdown_blocks import markdown_to_html_node
from htmlnode import HTMLNode

def main():
    if sys.argv[0] is not None:
        basepath = sys.argv[1]
    else:
        basepath = '/'

    public_dir = 'docs'
    static_dir = 'static'
    content_dir = 'content'

    clear_public(public_dir)
    copy_files(static_dir, public_dir)

    generate_pages_recursive(content_dir, 'template.html', public_dir, basepath)


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
    
def extract_title(markdown):
    split_md = markdown.split('\n')
    for line in split_md:
        if line.startswith('# '):
            return line[2:]
    raise Exception('No title found')

def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    
    with open(from_path) as file:
        markdown = file.read()
        file.close()
    with open(template_path) as file:
        template = file.read()
        file.close
    
    title = extract_title(markdown)
    html_nodes = markdown_to_html_node(markdown)
    html = html_nodes.to_html()

    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    path = os.path.dirname(dest_path)
    if os.path.exists(path) != True:
        os.makedirs(path)

    with open(dest_path, 'w') as file:
        file.write(template)
        file.close

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    path_contents = os.listdir(dir_path_content)
    for path in path_contents:
        full_content_path = os.path.join(dir_path_content, path)
        full_target_path = os.path.join(dest_dir_path, path)
        if os.path.isfile(full_content_path):
            if full_content_path.endswith('.md'):
               full_target_path = full_target_path[:-3] + '.html'
               generate_page(full_content_path, template_path, full_target_path, basepath)
        else:
            if os.path.exists(full_target_path) != True:
                os.makedirs(full_target_path)
            generate_pages_recursive(full_content_path, template_path, full_target_path, basepath)

if __name__ == "__main__":
    main()