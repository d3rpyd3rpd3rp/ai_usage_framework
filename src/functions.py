import re
import os
import shutil
from enum import Enum

from src.textnode import TextNode, TextType
from src.htmlnode import LeafNode, ParentNode

class BlockType(Enum):
    PARAGRAPH = 1,
    HEADING = 2,
    CODE = 3,
    QUOTE = 4,
    UNORDERED_LIST = 5,
    ORDERED_LIST = 6,

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise TypeError("Error: TextType does not exist")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            for i in range(len(parts)):
                if parts[i] == '':
                    continue
                if i % 2 == 0:
                    nodes.append(TextNode(parts[i], TextType.TEXT))
                else:
                    nodes.append(TextNode(parts[i], text_type))
    return nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            remaining = node.text
            for image in images:
                before, after = remaining.split(f"![{image[0]}]({image[1]})", 1)
                if before != '':
                    nodes.append(TextNode(before, TextType.TEXT))
                nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                remaining = after
            if remaining != '':
                nodes.append(TextNode(remaining, TextType.TEXT))
    return nodes

def split_nodes_link(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            remaining = node.text
            for link in links:
                before, after = remaining.split(f"[{link[0]}]({link[1]})", 1)
                if before != '':
                    nodes.append(TextNode(before, TextType.TEXT))
                nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                remaining = after
            if remaining != '':
                nodes.append(TextNode(remaining, TextType.TEXT))
    return nodes

def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(node)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    index = 0
    while index < len(blocks):
        blocks[index] = blocks[index].strip()
        if blocks[index] == "":
            blocks.pop(index)
            continue
        index += 1
    return blocks

def block_to_block_type(block):
    for i in range(1, 7):
        if block.startswith("#" * i + " "):
            return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    if all(map(lambda line: line.startswith(">"), lines)):
        return BlockType.QUOTE
    if all(map(lambda line: line.startswith("- "), lines)):
        return BlockType.UNORDERED_LIST
    for i, line in enumerate(lines):
        if not line.startswith(f"{i+1}. "):
            break
    else:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children

def list_to_children(block):
    lines = [line[line.find(" ")+1:] for line in block.split("\n")]
    children = []
    for line in lines:
        parent = ParentNode("li", [])
        text_nodes = text_to_textnodes(line)
        for node in text_nodes:
            parent.children.append(text_node_to_html_node(node))
        children.append(parent)
    return children

def markdown_to_html_node(markdown):
    parent_node = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                num = block.find(" ")
                html_node = ParentNode(f"h{num}", text_to_children(block[num+1:]))
            case BlockType.CODE:
                node = TextNode(block[4:len(block)-3], TextType.CODE)
                html_node = ParentNode("pre", [text_node_to_html_node(node)])
            case BlockType.QUOTE:
                lines = [line[1:].strip() for line in block.split("\n")]
                html_node = ParentNode("blockquote", text_to_children(" ".join(lines)))
            case BlockType.UNORDERED_LIST:
                html_node = ParentNode("ul", list_to_children(block))
            case BlockType.ORDERED_LIST:
                html_node = ParentNode("ol", list_to_children(block))
            case BlockType.PARAGRAPH:
                html_node = ParentNode("p", text_to_children(" ".join(block.split("\n"))))
        parent_node.children.append(html_node)
    return parent_node

def copy_dir_to_dir(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
        
    def helper(src_path, dest_path):
        entries = os.listdir(src_path)
        for entry in entries:
            src_entry = os.path.join(src_path, entry)
            dest_entry = os.path.join(dest_path, entry)
            if os.path.isfile(src_entry):
                shutil.copy(src_entry, dest_path)
            elif os.path.isdir(src_entry):
                os.mkdir(dest_entry)
                helper(src_entry, dest_entry)
        
    helper(source, destination)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()
    raise Exception("title not found") # will change Exception to be more general

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = open(from_path).read()
    template = open(template_path).read()
    html = markdown_to_html_node(md)
    html = html.to_html()
    title = extract_title(md)
    new_html = template.replace("{{ Title }}", title)
    new_html = new_html.replace("{{ Content }}", html)
    dirs = os.path.dirname(dest_path)
    if dirs:
        os.makedirs(dirs, exist_ok=True)
    open(dest_path, "w").write(new_html)

def generate_website(from_path_dir, template_path, dest_path_dir):
    entries = os.listdir(from_path_dir)
    for entry in entries:
        src_entry = os.path.join(from_path_dir, entry)
        dest_entry = os.path.join(dest_path_dir, entry)
        if os.path.isfile(src_entry):
            if src_entry.endswith(".md"):
                dest_entry = dest_entry[:-2] + "html"
                generate_page(src_entry, template_path, dest_entry)
        elif os.path.isdir(src_entry):
            generate_website(src_entry, template_path, dest_entry)
