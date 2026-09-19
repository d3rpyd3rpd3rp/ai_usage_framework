import unittest

from src.functions import BlockType, block_to_block_type

class TestHTMLNode(unittest.TestCase):
    def test_heading(self):
        valid = [
            "# 1 char",
            "## 2 char",
            "### 3 char",
            "#### 4 char",
            "##### 5 char",
            "###### 6 char",
            "## multiline\nheading"
        ]
        invalid = [
            "#no space",
            " #space first",
            "####### too many char",
            "char in # middle"
        ]
        for md in valid:
            self.assertTrue(block_to_block_type(md) == BlockType.HEADING)
        for md in invalid:
            self.assertFalse(block_to_block_type(md) == BlockType.HEADING)
    
    def test_code(self):
        valid = [
            "```\n```",
            "```\n\n\n```",
            "```\nsome text as well```",
            "```\nmultiple\nlines\nin one\ncode block```"
        ]
        invalid = [
            "``````",
            "`\ncode block?`",
            "``` ```",
            "```no closer",
            "no opener```"
        ]
        for md in valid:
            self.assertTrue(block_to_block_type(md) == BlockType.CODE)
        for md in invalid:
            self.assertFalse(block_to_block_type(md) == BlockType.CODE)
    
    def test_quote(self):
        valid = [
            ">no space",
            "> with space",
            ">> multiple",
            ">   multiple spaces",
            "> multiple\n>lines\n>with\n> mix of\n>spaces",
            ">",
        ]
        invalid = [
            " >space first",
            "<wrong char",
            "> right char\nno char",
            "\">quotation marks around\"",
            ">>>\nusing quotes like code block>>>"
        ]
        for md in valid:
            self.assertTrue(block_to_block_type(md) == BlockType.QUOTE)
        for md in invalid:
            self.assertFalse(block_to_block_type(md) == BlockType.QUOTE)
    
    def test_unordered_list(self):
        valid = [
            "- one thing",
            "- two\n- things",
            "- a\n- few\n- things",
            "- many\n- more\n- things\n- here",
        ]
        invalid = [
            "-no space",
            " -space first",
            "- space\n-no space\n- space",
            "-",
            "-\n-\n-"
        ]
        for md in valid:
            self.assertTrue(block_to_block_type(md) == BlockType.UNORDERED_LIST)
        for md in invalid:
            self.assertFalse(block_to_block_type(md) == BlockType.UNORDERED_LIST)
    
    def test_ordered_list(self):
        valid = [
            "1. a thing",
            "1. a thing\n2. another thing",
            "1. a thing\n2. another thing\n3. yet another thing\n4. yet another nother thing\n5. yet another nother NOTHER thing"
        ]
        invalid = [
            "1) wrong opener",
            "1. a thing\n3. wrong order",
            "2. wrong start"
        ]
        for md in valid:
            self.assertTrue(block_to_block_type(md) == BlockType.ORDERED_LIST)
        for md in invalid:
            self.assertFalse(block_to_block_type(md) == BlockType.ORDERED_LIST)
    
    def test_paragraph(self):
        valid = [
            "just a sentence",
            "couple of\nlines here",
            "insert\nbee\nmovie\nscript\nhere"
        ]
        invalid = [
            "# header",
            "```\ncode block```",
            "> quote\n> block",
            "- unordered\n- list",
            "1. ordered\n2. list"
        ]
        for md in valid:
            self.assertTrue(block_to_block_type(md) == BlockType.PARAGRAPH)
        for md in invalid:
            self.assertFalse(block_to_block_type(md) == BlockType.PARAGRAPH)
