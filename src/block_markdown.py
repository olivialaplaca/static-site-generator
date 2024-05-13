import re

def markdown_to_blocks(markdown):
    blocks = re.split(r"(?:\n){2,}", markdown.strip())
    blocks = list(filter(lambda block: block.strip() != "", blocks))
    return blocks