
from enum import Enum

from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


def block_to_block_type(block):
    # Heading
    for i in range(1, 7):
        if block.startswith("#" * i + " "):
            return BlockType.HEADING

    lines = block.split("\n")

    # Code
    if (
        len(lines) >= 2
        and lines[0] == "```"
        and lines[-1] == "```"
    ):
        return BlockType.CODE

    # Quote
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list
    ordered = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            ordered = False
            break

    if ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def paragraph_to_html(block):
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def heading_to_html(block):
    level = 0
    while block[level] == "#":
        level += 1

    text = block[level + 1 :]
    return ParentNode(f"h{level}", text_to_children(text))


def quote_to_html(block):
    lines = []

    for line in block.split("\n"):
        if line.startswith("> "):
            lines.append(line[2:])
        else:
            lines.append(line[1:])

    text = " ".join(lines)
    return ParentNode("blockquote", text_to_children(text))


def unordered_list_to_html(block):
    items = []

    for line in block.split("\n"):
        items.append(
            ParentNode(
                "li",
                text_to_children(line[2:])
            )
        )

    return ParentNode("ul", items)


def ordered_list_to_html(block):
    items = []

    for line in block.split("\n"):
        idx = line.find(".")
        text = line[idx + 2:]

        items.append(
            ParentNode(
                "li",
                text_to_children(text)
            )
        )

    return ParentNode("ol", items)


def code_to_html(block):
    lines = block.split("\n")

    # Remove opening and closing ```
    code_text = "\n".join(lines[1:-1]) + "\n"

    code_node = LeafNode("code", code_text)

    return ParentNode(
        "pre",
        [code_node]
    )


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html(block)

    if block_type == BlockType.HEADING:
        return heading_to_html(block)

    if block_type == BlockType.CODE:
        return code_to_html(block)

    if block_type == BlockType.QUOTE:
        return quote_to_html(block)

    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html(block)

    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html(block)

    raise ValueError("Unknown block type")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    children = []

    for block in blocks:
        children.append(block_to_html_node(block))

    return ParentNode("div", children)

