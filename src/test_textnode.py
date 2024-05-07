import unittest

from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)
        self.assertEqual(node.url, None)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", text_type_code)
        node2 = TextNode("this is a test text node", text_type_link, "https://www.linkedin.com/in/olivialaplaca/")
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node1 = TextNode("this is a test text node", text_type_link, "https://www.linkedin.com/in/olivialaplaca/")
        node2 = TextNode("this is a test text node", text_type_link, "https://www.linkedin.com/in/olivialaplaca/")
        self.assertEqual(node1, node2)

    def test_repr(self):
        node = TextNode("this is a test node", text_type_italic, "https://www.linkedin.com/in/olivialaplaca/")
        self.assertEqual("TextNode(this is a test node, italic, https://www.linkedin.com/in/olivialaplaca/)", repr(node))
        


if __name__ == "__main__":
    unittest.main()