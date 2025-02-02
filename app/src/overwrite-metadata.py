"""Metadata Problem"""

from pathlib import Path

import streamlit as st

index = Path(st.__file__).parent / "static" / "index.html"
html = index.read_text()

html = html.replace(
    "<head>",
    """<head>
<meta name="description" content="Foo">
<meta property="og:image" content="https://example.com/bar.jpg">
""".replace(
        "\n", ""
    ),
)

index.write_text(html)
