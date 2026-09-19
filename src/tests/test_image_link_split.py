import unittest

from src.textnode import TextType, TextNode
from src.functions import split_nodes_image, split_nodes_link, split_nodes_delimiter

class TestImageLinkSplit(unittest.TestCase):
    def test_image_split(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        nodes = split_nodes_image([node])
        answer = [
            TextNode('This is text with a ', TextType.TEXT),
            TextNode('rick roll', TextType.IMAGE, 'https://i.imgur.com/aKaOqIh.gif'),
            TextNode(' and ', TextType.TEXT),
            TextNode('obi wan', TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg'),
        ]
        self.assertListEqual(nodes, answer)
    
    def test_link_split(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        nodes = split_nodes_link([node])
        answer = [
            TextNode('This is text with a link ', TextType.TEXT),
            TextNode('to boot dev', TextType.LINK, 'https://www.boot.dev'),
            TextNode(' and ', TextType.TEXT),
            TextNode('to youtube', TextType.LINK, 'https://www.youtube.com/@bootdotdev'),
        ]
        self.assertListEqual(nodes, answer)
    
    def test_image_and_link_split(self):
        node = TextNode("This is text with a link to a [predator game](https://www.roblox.com) and an image of the ![predator game logo](https://upload.wikimedia.org/wikipedia/commons/1/1e/Roblox_Logo_2025.png)", TextType.TEXT)
        nodes = split_nodes_image([node])
        nodes = split_nodes_link(nodes)
        answer = [
            TextNode('This is text with a link to a ', TextType.TEXT),
            TextNode('predator game', TextType.LINK, 'https://www.roblox.com'),
            TextNode(' and an image of the ', TextType.TEXT),
            TextNode('predator game logo', TextType.IMAGE, 'https://upload.wikimedia.org/wikipedia/commons/1/1e/Roblox_Logo_2025.png'),
        ]
        self.assertListEqual(nodes, answer)
    
    def test_image_and_delimiters(self):
        node = TextNode("This text has **bold words**, ![one image](https://www.image.png), and `code blocks`", TextType.TEXT)
        nodes = split_nodes_image([node])
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        answer = [
            TextNode('This text has ', TextType.TEXT),
            TextNode('bold words', TextType.BOLD),
            TextNode(', ', TextType.TEXT),
            TextNode('one image', TextType.IMAGE, 'https://www.image.png'),
            TextNode(', and ', TextType.TEXT),
            TextNode('code blocks', TextType.CODE),
        ]
        self.assertListEqual(nodes, answer)
    
    def test_no_plain_text(self):
        node = TextNode("**This text does **_not_** contain **_any_** TextType.TEXT or plain text, only bold, **_italics,_` code blocks, `![an image](https://image.png)**, and **[one link](https://boot.dev)", TextType.TEXT)
        nodes = split_nodes_image([node])
        nodes = split_nodes_link(nodes)
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        answer = [
            TextNode('This text does ', TextType.BOLD),
            TextNode('not', TextType.ITALIC),
            TextNode(' contain ', TextType.BOLD),
            TextNode('any', TextType.ITALIC),
            TextNode(' TextType.TEXT or plain text, only bold, ', TextType.BOLD),
            TextNode('italics,', TextType.ITALIC),
            TextNode(' code blocks, ', TextType.CODE),
            TextNode('an image', TextType.IMAGE, 'https://image.png'),
            TextNode(', and ', TextType.BOLD),
            TextNode('one link', TextType.LINK, 'https://boot.dev'),
        ]
        self.assertListEqual(nodes, answer)
    
    def test_list_of_text(self):
        nodes = [
            TextNode("Not _much_ to see here at _all_.", TextType.TEXT),
            TextNode("I mean really, it's just some **random** filler text.", TextType.TEXT),
            TextNode("`Putting a code block here` along with a random ![image](https://image.gif).", TextType.TEXT),
            TextNode("Maybe a [random link](https://youtube.com) and some **bold text**.", TextType.TEXT),
        ]
        nodes = split_nodes_image(nodes)
        nodes = split_nodes_link(nodes)
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        answer = [
            TextNode('Not ', TextType.TEXT),
            TextNode('much', TextType.ITALIC),
            TextNode(' to see here at ', TextType.TEXT),
            TextNode('all', TextType.ITALIC),
            TextNode('.', TextType.TEXT),
            TextNode('I mean really, it\'s just some ', TextType.TEXT),
            TextNode('random', TextType.BOLD),
            TextNode(' filler text.', TextType.TEXT),
            TextNode('Putting a code block here', TextType.CODE),
            TextNode(' along with a random ', TextType.TEXT),
            TextNode('image', TextType.IMAGE, 'https://image.gif'),
            TextNode('.', TextType.TEXT),
            TextNode('Maybe a ', TextType.TEXT),
            TextNode('random link', TextType.LINK, 'https://youtube.com'),
            TextNode(' and some ', TextType.TEXT),
            TextNode('bold text', TextType.BOLD),
            TextNode('.', TextType.TEXT),
        ]
        self.assertListEqual(nodes, answer)