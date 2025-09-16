"""
HTML Chunking Library

A Python library for intelligently splitting large HTML documents into smaller,
semantically coherent chunks while preserving DOM structure and staying within
token limits for LLM processing.
"""

from html_chunking.html_chunking_main import get_html_chunks, HTMLChunker
from html_chunking.html_chunking_core import count_tokens
from html_chunking.html_cleaner import clean_html
from html_chunking.html_splitter import split_html_by_dom, merge_html_chunks

__version__ = "1.0.0"
__author__ = "HTML Chunking Team"
__email__ = "contact@htmlchunking.dev"

__all__ = [
    "get_html_chunks",
    "HTMLChunker",
    "count_tokens",
    "clean_html",
    "split_html_by_dom",
    "merge_html_chunks"
]