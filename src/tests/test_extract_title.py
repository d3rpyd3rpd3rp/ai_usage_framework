import unittest

from src.functions import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_eq(self):
        md = "# Hello"
        title = extract_title(md)
        self.assertEqual(
            title,
            "Hello"
        )
    
    def test_blocks(self):
        md = """
Paragraph here
just to take up space

```
Code block here
to do code block things
```

# Actual title

- List
- of
- stuff
"""
        title = extract_title(md)
        self.assertEqual(
            title,
            "Actual title"
        )
