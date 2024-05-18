import unittest
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    quote_block_to_html,
    ulist_block_to_html,
    olist_block_to_html,
    code_block_to_html,
    heading_block_to_html,
    paragraph_block_to_html,
    markdown_to_html_node,
    block_type_code,
    block_type_heading,
    block_type_olist,
    block_type_paragraph,
    block_type_quote,
    block_type_ulist
)
from htmlnode import ParentNode, LeafNode

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        self.assertEqual(markdown_to_blocks(markdown),[
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
        ])
        markdown = """# This is a heading

        

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
"""
        self.assertEqual(markdown_to_blocks(markdown), [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item"
        ])

    def test_block_type_heading(self):
        block = "# This is an L1 heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "###### This is an L6 heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)

    def test_block_type_invalid_heading(self):
        block = "####### This is an L1 heading"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_block_type_code(self):
        block = """```this is a 
block of code
```"""
        self.assertEqual(block_to_block_type(block), block_type_code)

    def test_quote_block(self):
        block = """>this is the first line
>of a quote block
>about a cool thing"""
        self.assertEqual(block_to_block_type(block), block_type_quote)

    def test_not_quote_block(self):
        block = """>this is not a real quote
>because the last line
doesn't have the right starting char"""
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_unordered_list_block(self):
        block = """* this is the first line
* of a list block
* of really cool things"""
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = """- this is the first line
- of a list block
- of really cool things"""
        self.assertEqual(block_to_block_type(block), block_type_ulist)

    def test_not_unordered_list_block(self):
        block = """* this is not a real list
because all lines
don't have the right starting char"""
        self.assertEqual(block_to_block_type(block), block_type_paragraph)
        block = """-this is not a real list
because all lines
- don't have the right starting char"""
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_ordered_list_block(self):
        block = """1. this is a list
2. of an ordered list block
3. of really cool things"""
        self.assertEqual(block_to_block_type(block), block_type_olist)

    def test_not_ordered_list_block(self):
        block = """1. this is not a list
3. of an ordered list block
3. because numbers aren't in order"""
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

#     def test_quote_block_to_html(self):
#         block = """>this is the first line
# >of a quote block
# >about a cool thing"""
#         self.assertEqual(quote_block_to_html(block), HTMLNode("blockquote", block, [

#         ]))


    def test_paragraph_block_to_html(self):
        block = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        self.assertEqual(
            repr(paragraph_block_to_html(block)), 
            repr(ParentNode("p", [
                LeafNode(None, "This is a paragraph of text. It has some "),
                LeafNode("b", "bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
                LeafNode(None, " words inside of it.")
            ]))
        )

    def test_paragraph_block_to_html(self):
        block = "# This is a **bold heading**"
        self.assertEqual(
            repr(heading_block_to_html(block)), 
            repr(ParentNode("h1", [
                LeafNode(None, "This is a "),
                LeafNode("b", "bold heading")
            ]))
        )
        block = "## *This is an italic heading*"
        self.assertEqual(
            repr(heading_block_to_html(block)), 
            repr(ParentNode("h2", [
                LeafNode("i", "This is an italic heading")
            ]))
        )
        block = "### This is an h3 heading"
        self.assertEqual(
            repr(heading_block_to_html(block)), 
            repr(ParentNode("h3", [
                LeafNode(None, "This is an h3 heading")
            ]))
        )
        block = "#### This is an h4 heading"
        self.assertEqual(
            repr(heading_block_to_html(block)), 
            repr(ParentNode("h4", [
                LeafNode(None, "This is an h4 heading")
            ]))
        )
        block = "##### This is an h5 heading"
        self.assertEqual(
            repr(heading_block_to_html(block)), 
            repr(ParentNode("h5", [
                LeafNode(None, "This is an h5 heading")
            ]))
        )
        block = "###### This is an h6 heading"
        self.assertEqual(
            repr(heading_block_to_html(block)), 
            repr(ParentNode("h6", [
                LeafNode(None, "This is an h6 heading")
            ]))
        )

    def test_code_block_to_html(self):
        block = """```this is a 
block of code
```"""
        self.assertEqual(
            repr(code_block_to_html(block)),
            repr(ParentNode("code", [
                ParentNode("pre", [
                    LeafNode(None, "this is a \nblock of code\n")
                ])
            ]))
        )

    def test_olist_block_to_html(self):
        block = """1. this is a list
2. of an ordered list block
3. of really **cool things**"""
        self.assertEqual(
            repr(olist_block_to_html(block)),
            repr(ParentNode("ol", [
                ParentNode("li", [LeafNode(None, "this is a list")]),
                ParentNode("li", [LeafNode(None, "of an ordered list block")]),
                ParentNode("li", [
                    LeafNode(None, "of really "),
                    LeafNode("b", "cool things")
                ])
            ]))
        )

    def test_ulist_block_to_html(self):
        block = """* bread
* ice cream
* *cookies and cakes*"""
        self.assertEqual(
            repr(ulist_block_to_html(block)),
            repr(ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "bread")]),
                ParentNode("li", [LeafNode(None, "ice cream")]),
                ParentNode("li", [LeafNode("i", "cookies and cakes")])
            ]))
        )

    def test_quote_block_to_html(self):
        block = """>this is the first line
>of a quote *block*
>about a cool thing"""
        self.assertEqual(
            repr(quote_block_to_html(block)),
            repr(ParentNode("blockquote", [
                LeafNode(None, "this is the first line\nof a quote "),
                LeafNode("i", "block"),
                LeafNode(None, "\nabout a cool thing")
            ]))
        )

    def test_markdown_to_html_node(self):
        markdown = """# This is an entire page of text to test that talks about really cool things.

>We have a quote from me
>because I'm *awesome* and have
>really **cool things** to say

1. And an
2. ordered list

- and an
- unordered list

```and a code block of code doing code things```

And thus concludes my page
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is an entire page of text to test that talks about really cool things.</h1><blockquote>We have a quote from me\nbecause I'm <i>awesome</i> and have\nreally <b>cool things</b> to say</blockquote><ol><li>And an</li><li>ordered list</li></ol><ul><li>and an</li><li>unordered list</li></ul><code><pre>and a code block of code doing code things</pre></code><p>And thus concludes my page</p></div>"
        )



if __name__ == "__main__":
    unittest.main()