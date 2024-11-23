import unittest

from block import BlockType, markdown_to_blocks, block_to_block_type

markdown = '''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

```
def foo="bar"
```

1. Foo
1. Bar

> Cinnamonrolls
> are
> amazing
'''

class TestBlock(unittest.TestCase):
    def test_to_blocks(self):
        result = markdown_to_blocks(markdown)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            '''* This is the first list item in a list block
* This is a list item
* This is another list item''',
            '''```
def foo="bar"
```''',
            '''1. Foo
1. Bar''',
            '''> Cinnamonrolls
> are
> amazing''',
        ]
        self.assertEqual(result, expected)

    def test_block_type(self):
        blocks = markdown_to_blocks(markdown)
        expected = [
            BlockType.HEADING,
            BlockType.PARAGRAPH,
            BlockType.UNORDERED_LIST,
            BlockType.CODE,
            BlockType.ORDERED_LIST,
            BlockType.QUOTE,
        ]
        for i in range(0, len(expected)):
            result = block_to_block_type(blocks[i])
            self.assertEqual(result, expected[i])


if __name__ == "__main__":
    unittest.main()
