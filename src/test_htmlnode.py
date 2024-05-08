import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="p", value="link", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_no_props(self):
        node = HTMLNode(tag="p", value="this is some test text")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode(tag="a", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual("HTMLNode(a, None, None, {'href': 'https://www.google.com', 'target': '_blank'})", repr(node))

    def test_leaf_no_props(self):
        leaf = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(leaf.to_html(), "<p>This is a paragraph of text.</p>")

    def test_no_tag(self):
        leaf = LeafNode(tag=None,value="hello world")
        self.assertEqual(leaf.to_html(), "hello world")

    def test_no_val(self):
        leaf = LeafNode(tag="p", value=None, props={"href": "https://www.google.com"})
        self.assertRaises(ValueError,leaf.to_html)

    def test_html_w_props(self):
        leaf = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(leaf.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_parent_no_tag(self):
        leaf = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        parent = ParentNode(tag=None,children=[leaf])
        self.assertRaises(ValueError,parent.to_html)

    def test_no_children(self):
        parent = ParentNode(tag="div", children=None)
        self.assertRaises(ValueError, parent.to_html)

    def test_child_leaf(self):
        parent = ParentNode("p",[LeafNode("b", "Bold text")])
        self.assertEqual(parent.to_html(),'<p><b>Bold text</b></p>')
    
    def test_multi_leaf(self):
        node = ParentNode(
            "p",[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text")
                ]
            )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text</p>')

    def test_nested_parent(self):
        node = ParentNode(
            "p",[
                ParentNode("p",[LeafNode("b", "Bold text")]),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text")
                ]
            )
        self.assertEqual(node.to_html(), '<p><p><b>Bold text</b></p><i>Italic text</i>Normal text</p>')

    def test_multi_nested_parent(self):
        node = ParentNode(
            "p",[
                ParentNode("p",[LeafNode("b", "Bold text")]),
                ParentNode("p",[LeafNode(None, "Normal text"),LeafNode("i", "Italic text")]),
                LeafNode("i", "Italic text")
                ]
            )
        self.assertEqual(node.to_html(), '<p><p><b>Bold text</b></p><p>Normal text<i>Italic text</i></p><i>Italic text</i></p>')

    


if __name__ == "__main__":
    unittest.main()