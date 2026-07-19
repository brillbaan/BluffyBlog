import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"'
        )

    def test_props_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode(
            "p",
            "Hello",
            None,
            {"class": "text"}
        )

        expected = (
            "HTMLNode(tag=p, value=Hello, "
            "children=None, props={'class': 'text'})"
        )

        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()