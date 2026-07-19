import unittest
import re

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestSplitNodes(unittest.TestCase):

    def test_text_to_textnodes(self):
        text = (
            "This is **text** with an _italic_ word and a "
            "`code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
            " and a "
            "[link](https://boot.dev)"
        )

        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://boot.dev",
                ),
            ],
        )

    def test_plain_text(self):
        self.assertEqual(
            text_to_textnodes("Hello World"),
            [TextNode("Hello World", TextType.TEXT)],
        )

    def test_only_bold(self):
        self.assertEqual(
            text_to_textnodes("**Hello**"),
            [TextNode("Hello", TextType.BOLD)],
        )

    def test_only_link(self):
        self.assertEqual(
            text_to_textnodes("[Google](google.com)"),
            [
                TextNode(
                    "Google",
                    TextType.LINK,
                    "google.com",
                )
            ],
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_single_image(self):
        node = TextNode(
            "Hello ![cat](cat.png)",
            TextType.TEXT,
        )

        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "cat.png"),
            ],
        )

    def test_split_no_image(self):
        node = TextNode(
            "Hello world",
            TextType.TEXT,
        )

        self.assertEqual(
            split_nodes_image([node]),
            [node],
        )

    def test_split_links(self):
        node = TextNode(
            "Go to [Google](google.com) and [GitHub](github.com)",
            TextType.TEXT,
        )

        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("GitHub", TextType.LINK, "github.com"),
            ],
        )

    def test_split_single_link(self):
        node = TextNode(
            "Visit [Boot.dev](boot.dev)",
            TextType.TEXT,
        )

        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "boot.dev"),
            ],
        )

    def test_split_no_link(self):
        node = TextNode(
            "Nothing here",
            TextType.TEXT,
        )

        self.assertEqual(
            split_nodes_link([node]),
            [node],
        )