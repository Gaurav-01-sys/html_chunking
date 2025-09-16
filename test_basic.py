"""
Basic tests for HTML Chunking Library
"""

import pytest
from html_chunking import get_html_chunks, HTMLChunker, count_tokens


def test_count_tokens():
    """Test token counting functionality."""
    text = "This is a simple test sentence."
    tokens = count_tokens(text)
    assert tokens > 0
    assert isinstance(tokens, int)


def test_basic_chunking():
    """Test basic HTML chunking."""
    html = """
    <html>
    <body>
        <h1>Title</h1>
        <p>This is a paragraph with some content.</p>
        <div>
            <h2>Subtitle</h2>
            <p>More content here.</p>
        </div>
    </body>
    </html>
    """
    
    chunks = get_html_chunks(html, max_tokens=100)
    
    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)
    assert all(count_tokens(chunk) <= 100 for chunk in chunks)


def test_html_chunker_class():
    """Test HTMLChunker class."""
    html = "<html><body><h1>Test</h1><p>Content</p></body></html>"
    
    chunker = HTMLChunker(max_tokens=50)
    chunks = chunker.chunk(html)
    
    assert len(chunks) > 0
    assert all(count_tokens(chunk) <= 50 for chunk in chunks)


def test_chunker_with_metadata():
    """Test chunking with metadata."""
    html = """
    <html>
    <head>
        <script>console.log('test');</script>
        <style>body { font-size: 14px; }</style>
    </head>
    <body>
        <h1>Header</h1>
        <p>Some content in the body.</p>
    </body>
    </html>
    """
    chunker = HTMLChunker(max_tokens=60, include_metadata=False)
    chunks = chunker.chunk(html)

    assert len(chunks) > 0
    assert all("<script>" not in chunk and "<style>" not in chunk for chunk in chunks)
    assert all(count_tokens(chunk) <= 60 for chunk in chunks)


def test_empty_html():
    """Test chunking with empty HTML."""
    html = ""
    chunks = get_html_chunks(html, max_tokens=50)
    assert chunks == []


def test_large_html_chunking():
    """Test chunking with a large HTML input."""
    html = "<html><body>" + "".join(f"<p>Paragraph {i}</p>" for i in range(100)) + "</body></html>"
    chunks = get_html_chunks(html, max_tokens=100)

    assert len(chunks) > 1
    assert all(count_tokens(chunk) <= 100 for chunk in chunks)
