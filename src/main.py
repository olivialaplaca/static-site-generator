from textnode import TextNode
from htmlnode import HTMLNode, LeafNode

def main():
    node1 = TextNode('this is the first text node', 'bold', 'https://www.linkedin.com/in/olivialaplaca/')
    node2 = TextNode('this is the second text node', 'italic')
    print(f'this is my text node', node1)
    print(node2)
    print(node1 == node2)

    leaf2 = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
    print(leaf2.to_html)

main()