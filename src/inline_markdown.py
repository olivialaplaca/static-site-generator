import re
from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        split_nodes = node.text.split(delimiter)
        if len(split_nodes) % 2 == 0:
            raise ValueError("Cannot split node: Missing closing tag")
        for i in range(len(split_nodes)):
            if i % 2 == 0:
                new_nodes.append(TextNode(split_nodes[i], text_type_text))
            else:
                new_nodes.append(TextNode(split_nodes[i], text_type))
    for node in new_nodes.copy():
        if node.text_type == text_type_text and node.text == "":
            new_nodes.remove(node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
        elif len(images) == 1:
            plain_text = node.text.split(f"![{images[0][0]}]({images[0][1]})", 1)
            new_nodes.extend([
                TextNode(plain_text[0], text_type_text),
                TextNode(images[0][0], text_type_image, images[0][1]),
                TextNode(plain_text[1], text_type_text)
            ])
        else:
            plain_text = node.text.split(f"![{images[0][0]}]({images[0][1]})", 1)
            new_nodes.extend([
                TextNode(plain_text[0], text_type_text),
                TextNode(images[0][0], text_type_image, images[0][1])])
            for node in split_nodes_image([TextNode(plain_text[1], text_type_text)]):
                new_nodes.append(node)
    for node in new_nodes.copy():
        if node.text_type == text_type_text and node.text == "":
            new_nodes.remove(node)
    return new_nodes 

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
        elif len(links) == 1:
            plain_text = node.text.split(f"[{links[0][0]}]({links[0][1]})", 1)
            new_nodes.extend([
                TextNode(plain_text[0], text_type_text),
                TextNode(links[0][0], text_type_link, links[0][1]),
                TextNode(plain_text[1], text_type_text)
            ])
        else:
            plain_text = node.text.split(f"[{links[0][0]}]({links[0][1]})", 1)
            new_nodes.extend([
                TextNode(plain_text[0], text_type_text),
                TextNode(links[0][0], text_type_link, links[0][1])
            ])
            for node in split_nodes_link([TextNode(plain_text[1], text_type_text)]):
                new_nodes.append(node)
    for node in new_nodes.copy():
        if node.text_type == text_type_text and node.text == "":
            new_nodes.remove(node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    #search for bold before italic
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    #search for images before links
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
