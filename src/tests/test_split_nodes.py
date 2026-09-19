import unittest

from src.textnode import TextNode, TextType
from src.functions import split_nodes_delimiter

class TestSplitNodes(unittest.TestCase):
    def test_one_delimiter(self):
        nodes = [TextNode("This is text with a `code block` word", TextType.TEXT)]
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        answer = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(nodes, answer)
    
    def test_two_delimiters(self):
        nodes = [TextNode("This text has **bold** delimiters and _italic_ delimiters. Oh my!", TextType.TEXT)]
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        answer = [
            TextNode("This text has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" delimiters and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" delimiters. Oh my!", TextType.TEXT),
        ]
        self.assertEqual(nodes, answer)
    
    def test_three_delimiters(self):
        nodes = [TextNode("Use **bold** and _italic_ and `code`", TextType.TEXT)]
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        answer = [
            TextNode("Use ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ]
        self.assertEqual(nodes, answer)
