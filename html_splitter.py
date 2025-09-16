"""
HTML splitting and merging utilities for creating optimal chunks.
"""

from bs4 import BeautifulSoup
from typing import List, Dict, Any
from .core import traverse_dom, count_tokens, get_common_root_path


def split_html_by_dom(html_string: str, max_tokens: int) -> List[Dict[str, Any]]:
    """
    Split HTML into chunks by DOM structure, respecting token limits.
    
    Args:
        html_string: HTML string to split
        max_tokens: Maximum tokens per chunk
    
    Returns:
        List of chunk dictionaries with metadata
    """
    chunks = []
    soup = BeautifulSoup(html_string, 'html.parser')
    traverse_dom(soup, chunks, max_tokens)
    return chunks


def merge_html_chunk(html_1: str, html_2: str) -> str:
    """
    Merge two HTML chunks by combining their common structure.
    
    Args:
        html_1: First HTML chunk
        html_2: Second HTML chunk
    
    Returns:
        Merged HTML string
    """
    soup1 = BeautifulSoup(html_1, 'html.parser')
    soup2 = BeautifulSoup(html_2, 'html.parser')

    path1, path2 = get_common_root_path(soup1, soup2)
    common_parent1 = path1[-1] if path1 else soup1
    common_parent2 = path2[-1] if path2 else soup2

    # Append unique content from second chunk
    for element in common_parent2.contents:
        if element not in common_parent1.contents:
            common_parent1.append(element)

    return str(soup1)


def merge_html_chunks(html_chunks: List[str], max_tokens: int) -> List[str]:
    """
    Merge HTML chunks to optimize token usage while staying under limits.
    
    Args:
        html_chunks: List of HTML chunk strings
        max_tokens: Maximum tokens per merged chunk
    
    Returns:
        List of optimally merged HTML chunks
    """
    if not html_chunks:
        return []
    
    merged_chunks = []
    current_chunk = html_chunks[0]

    for i in range(1, len(html_chunks)):
        next_chunk = html_chunks[i]
        merged = merge_html_chunk(current_chunk, next_chunk)

        if count_tokens(merged) <= max_tokens:
            current_chunk = merged
        else:
            merged_chunks.append(current_chunk)
            current_chunk = next_chunk

    merged_chunks.append(current_chunk)
    return merged_chunks