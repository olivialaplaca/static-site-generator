import re
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = re.split(r"(?:\n){2,}", markdown.strip())
    blocks = list(filter(lambda block: block.strip() != "", blocks))
    return blocks

def block_to_block_type(block):
    def check_lines(block, prefix):
        valid_lines = []
        lines = block.splitlines()
        if prefix == "1. ":
            num = 1
            for line in lines:
                prefix = f"{num}. "
                if line.startswith(prefix):
                    valid_lines.append(line)
                    num += 1
        else:
            for line in lines:
                if line.startswith(prefix):
                    valid_lines.append(line)
        return valid_lines == lines

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    elif block.startswith("```") and block.endswith("```"):
        return block_type_code
    elif check_lines(block, ">"):
        return block_type_quote
    elif check_lines(block, "* ") or check_lines(block, "- "):
        return block_type_ulist
    elif check_lines(block, "1. "):
        return block_type_olist
    else:
        return block_type_paragraph
    
def text_to_children(text):
    children = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        children.append(text_node_to_html_node(textnode))
    return children
    
def quote_block_to_html(block):
    lines = block.splitlines(True)
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">"))
    chlidren = text_to_children("".join(new_lines))
    return ParentNode("blockquote", chlidren)

def ulist_block_to_html(block):
    children = []
    lines = block.splitlines()
    for line in lines:
        children.append(ParentNode("li", text_to_children(line[2:])))
    return ParentNode("ul", children)

def olist_block_to_html(block):
    children = []
    lines = block.splitlines()
    for line in lines:
        children.append(ParentNode("li", text_to_children(line.lstrip("1234567890. "))))
    return ParentNode("ol", children)

def code_block_to_html(block):
    children = text_to_children(block.strip("```"))
    return ParentNode("code", [
        ParentNode("pre", children)
    ])

def heading_block_to_html(block):
    if block.startswith("# "):
        tag = "h1"
    elif block.startswith("## "):
        tag = "h2"
    elif block.startswith("### "):
        tag = "h3"
    elif block.startswith("#### "):
        tag = "h4"
    elif block.startswith("##### "):
        tag = "h5"
    elif block.startswith("###### "):
        tag = "h6"
    children = text_to_children(block.lstrip("# "))
    return ParentNode(tag, children)


def paragraph_block_to_html(block):
    children = text_to_children(block)
    return ParentNode("p", children)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_code:
            children.append(code_block_to_html(block))
        elif block_type == block_type_quote:
            children.append(quote_block_to_html(block))
        elif block_type == block_type_heading:
            children.append(heading_block_to_html(block))
        elif block_type == block_type_olist:
            children.append(olist_block_to_html(block))
        elif block_type == block_type_ulist:
            children.append(ulist_block_to_html(block))
        else:
            children.append(paragraph_block_to_html(block))
    return ParentNode("div", children)
