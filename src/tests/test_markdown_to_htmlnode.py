import unittest

from src.functions import markdown_to_html_node

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_code_block(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_quote_block(self):
        md = """
> All of this **text** is within a quoteblock
>with a few instances of _funny_ things
>   to check that it actually works.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>All of this <b>text</b> is within a quoteblock with a few instances of <i>funny</i> things to check that it actually works.</blockquote></div>"
        )
    
    def test_heading_block(self):
        h2 = """
## This is an **h2 heading** across
multiple lines because _why not_
"""
        h5 = """
##### This is an **h5 heading** to test
a _lot_ of #s and multiple lines
"""
        h2_node = markdown_to_html_node(h2)
        h5_node = markdown_to_html_node(h5)
        h2_html = h2_node.to_html()
        h5_html = h5_node.to_html()
        self.assertEqual(
            h2_html,
            "<div><h2>This is an <b>h2 heading</b> across\nmultiple lines because <i>why not</i></h2></div>"
        )
        self.assertEqual(
            h5_html,
            "<div><h5>This is an <b>h5 heading</b> to test\na <i>lot</i> of #s and multiple lines</h5></div>"
        )
    
    def test_unordered_list_block(self):
        md = """
- This is an **unordered list**
- There are a _few_ things here, not too much
- `Just enough to test all the features necessary`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an <b>unordered list</b></li><li>There are a <i>few</i> things here, not too much</li><li><code>Just enough to test all the features necessary</code></li></ul></div>"
        )
    
    def test_ordered_list_block(self):
        md = """
1. This is an **ordered list**
2. It increments _automatically_
3. It does this `consistently`
4. And does **not** break the cycle
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an <b>ordered list</b></li><li>It increments <i>automatically</i></li><li>It does this <code>consistently</code></li><li>And does <b>not</b> break the cycle</li></ol></div>"
        )
