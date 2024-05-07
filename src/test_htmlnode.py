import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="p", value="link", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_no_props(self):
        node2 = HTMLNode(tag="p", value="this is some test text")
        self.assertEqual(node2.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode(tag="a", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual("HTMLNode(a, None, None, {'href': 'https://www.google.com', 'target': '_blank'})", repr(node))

class TestLeafNode(unittest.TestCase):
    def test_no_props(self):
        leaf = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(leaf.to_html(), "<p>This is a paragraph of text.</p>")

    def test_no_tag(self):
        leaf = LeafNode(value="hello world")
        self.assertEqual(leaf.to_html(), "hello world")

    def test_no_val(self):
        leaf = LeafNode(tag="p", props={"href": "https://www.google.com"})
        self.assertRaises(ValueError,leaf.to_html)

    def test_html_w_props(self):
        leaf2 = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(leaf2.to_html(), '<a href="https://www.google.com">Click me!</a>')

    


if __name__ == "__main__":
    unittest.main()