import unittest

from src.functions import markdown_to_blocks

class TestMarkdownBlocks(unittest.TestCase):
    def test_eq(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_neq(self):
        md = """
This is a sentence with just text

This is another sentence with some **bold text** and a
`code block` on a new line

Here we have a [link](https://www.youtube.com) and an ![image](https://image.jpeg)
"""
        blocks = markdown_to_blocks(md)
        self.assertNotEqual(
            blocks,
            [
                "This is a sentence with just text\n",
                "This is another sentence with some **bold text** and a `code block` on a new line",
                "Here we have a [link]\n(https://www.youtube.com) and an ![image]\n(https://image.jpeg)",
            ],
        )
    
    def test_no_blocks(self):
        md = """
This is just a sentence.
In fact, there should be no blocks detected.
If any do, there is a bug in the code and should be fixed.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is just a sentence.\nIn fact, there should be no blocks detected.\nIf any do, there is a bug in the code and should be fixed.",
            ],
        )
