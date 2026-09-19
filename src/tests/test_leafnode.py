import unittest

from src.htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("a", "Link", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://example.com\">Link</a>")
    
    def test_props_none(self):
        node = LeafNode("p", "rAnDoM tExT", None)
        self.assertEqual(node.to_html(), "<p>rAnDoM tExT</p>")
