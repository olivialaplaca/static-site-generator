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
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)


class TestTextNode(unittest.TestCase):
    def test_split_end(self):
        node = TextNode("This is a node with **bold text**", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(new_nodes, [
            TextNode("This is a node with ", text_type_text),
            TextNode("bold text", text_type_bold)
        ])

    def test_split_start(self):
        node = TextNode("**Bold text** is in this node", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(new_nodes, [
            TextNode("Bold text", text_type_bold),
            TextNode(" is in this node", text_type_text)
        ])
    
    def test_split_many(self):
        node = TextNode("This **node** has **lots of** bolded **words.**", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(new_nodes, [
            TextNode("This ", text_type_text),
            TextNode("node", text_type_bold),
            TextNode(" has ", text_type_text),
            TextNode("lots of", text_type_bold),
            TextNode(" bolded ", text_type_text),
            TextNode("words.", text_type_bold)
        ])

    def test_split_code(self):
        node = TextNode("This node `has a code block` in it", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(new_nodes, [
            TextNode("This node ", text_type_text),
            TextNode("has a code block", text_type_code),
            TextNode(" in it", text_type_text)
        ])

    def test_split_italic(self):
        node = TextNode("This node has *italic* text", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(new_nodes, [
            TextNode("This node has ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" text", text_type_text)
        ])

    def test_split_node_list(self):
        nodes = [
            TextNode("this *is* a list", text_type_text),
            TextNode("*of* text nodes.", text_type_text)
        ]
        new_nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
        self.assertEqual(new_nodes, [
            TextNode("this ", text_type_text),
            TextNode("is", text_type_italic),
            TextNode(" a list", text_type_text),
            TextNode("of", text_type_italic),
            TextNode(" text nodes.", text_type_text)
        ])
    
    def test_image(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(extract_markdown_images(text),[("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])

    def test_link(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(extract_markdown_links(text), [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        self.assertEqual(split_nodes_image([node]),[
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode("second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png")
        ])

    def test_split_single_image_start(self):
        node = TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) with some text!",
            text_type_text,
        )
        self.assertEqual(split_nodes_image([node]),[
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" with some text!", text_type_text)
        ])

    def test_split_without_image(self):
        node = TextNode(
            "![image] with some text!",
            text_type_text,
        )
        self.assertEqual(split_nodes_image([node]),[
            TextNode("![image] with some text!", text_type_text)
        ])

    def test_split_nodes_link(self):
        node = TextNode("This is a node with a [link](https://www.linkedin.com/in/olivialaplaca/)", text_type_text)
        self.assertEqual(split_nodes_link([node]),[
            TextNode("This is a node with a ", text_type_text),
            TextNode("link", text_type_link, "https://www.linkedin.com/in/olivialaplaca/")
        ])

    def test_split_nodes_multi_link(self):
        node = TextNode("[links and links](https://www.google.com) with more links to [LinkedIn](https://www.linkedin.com/in/olivialaplaca/).", text_type_text)
        self.assertEqual(split_nodes_link([node]),[
            TextNode("links and links", text_type_link, "https://www.google.com"),
            TextNode(" with more links to ", text_type_text),
            TextNode("LinkedIn", text_type_link, "https://www.linkedin.com/in/olivialaplaca/"),
            TextNode(".", text_type_text)
        ])

    def test_split_without_link(self):
        node = TextNode(
            "[empty link] with some text",
            text_type_text,
        )
        self.assertEqual(split_nodes_image([node]),[
            TextNode("[empty link] with some text", text_type_text)
        ])

    def test_text_to_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text),[
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev")
        ])
    def test_text_to_nodes_no_images(self):
        text = "This is **text** with an *italic* word and a `code block` and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text),[
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev")
        ])

    def test_text_to_nodes_link_before_image(self):
        text = "This is **text** with an *italic* word and a `code block` and a [link](https://boot.dev) and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"
        self.assertEqual(text_to_textnodes(text),[
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")
        ])

    def test_text_to_nodes_italic_before_bold(self):
        text = "This is *italic text* with a **bold** word and a `code block` and a [link](https://boot.dev) and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"
        self.assertEqual(text_to_textnodes(text),[
            TextNode("This is ", text_type_text),
            TextNode("italic text", text_type_italic),
            TextNode(" with a ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")
        ])


if __name__ == "__main__":
    unittest.main()