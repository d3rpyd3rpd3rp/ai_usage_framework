import unittest

from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", None, None, {"class": "my-class", "id": "my-id"})
        self.assertEqual(node.props_to_html(), ' class="my-class" id="my-id"')
    
    def test_props_none(self):
        node = HTMLNode("p", None, None, None)
        self.assertEqual(node.props_to_html(), '')
    
    def test_neq(self):
        node = HTMLNode("p", None, None, {"class": "my-class", "id": "my-id"})
        self.assertNotEqual(node.props_to_html(), 'class="my-class" id="my-id"')
