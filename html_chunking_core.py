"""
Core HTML chunking functionality for splitting large HTML documents into smaller, manageable chunks.
"""

import tiktoken
from typing import List, Dict, Any, Tuple


def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Count the number of tokens in a text string using the specified model's tokenizer.
    
    Args:
        text: The text to count tokens for
        model: The model name to use for tokenization (default: gpt-3.5-turbo)
    
    Returns:
        Number of tokens in the text
    """
    encoder = tiktoken.encoding_for_model(model)
    tokens = encoder.encode(text)
    return len(tokens)


def format_attrs(attrs: Dict[str, Any]) -> Dict[str, str]:
    """
    Format HTML attributes, converting lists to space-separated strings.
    
    Args:
        attrs: Dictionary of HTML attributes
    
    Returns:
        Formatted attributes dictionary
    """
    formatted_attrs = {}
    for key, value in attrs.items():
        if isinstance(value, list):
            value = ' '.join(value) if value else ''
        formatted_attrs[key] = value
    return formatted_attrs


def build_full_content(path: List[Dict[str, Any]], node) -> str:
    """
    Build full HTML content by wrapping node with its parent tags from the path.
    
    Args:
        path: List of parent elements with their tags and attributes
        node: The current node to wrap
    
    Returns:
        Complete HTML string with proper nesting
    """
    opening_tags = ''.join([
        "<" + p['tag'] + ''.join([' {}="{}"'.format(key, value) for key, value in p['attrs'].items()]) + ">"
        for p in path
    ])
    node_content = str(node)
    closing_tags = ''.join(["</" + p['tag'] + ">" for p in reversed(path)])
    
    full_content = opening_tags + node_content + closing_tags
    
    # Clean up document markers
    if full_content.startswith('<[document]>'):
        full_content = full_content[len('<[document]>'):].strip()
    if full_content.endswith('</[document]>'):
        full_content = full_content[:-len('</[document]>')].strip()
    
    return full_content


def traverse_dom(node, chunks: List[Dict[str, Any]], max_tokens: int, path: List[Dict[str, Any]] = None) -> None:
    """
    Recursively traverse DOM and create chunks that fit within token limits.
    
    Args:
        node: BeautifulSoup node to traverse
        chunks: List to store the generated chunks
        max_tokens: Maximum tokens per chunk
        path: Current path of parent elements
    """
    if path is None:
        path = []
    
    if not node.name:
        return

    node_length = count_tokens(str(node))
    if node_length < max_tokens:
        full_content = build_full_content(path, node)
        chunks.append({
            'tag': node.name, 
            'attrs': node.attrs, 
            'content': full_content, 
            'path': path.copy()
        })
        return

    for child in node.children:
        if child.name:
            path.append({'tag': node.name, 'attrs': format_attrs(node.attrs)})
            traverse_dom(child, chunks, max_tokens, path)
            path.pop()


def get_common_root_path(soup1, soup2) -> Tuple[List, List]:
    """
    Find the common root path between two BeautifulSoup objects.
    
    Args:
        soup1: First BeautifulSoup object
        soup2: Second BeautifulSoup object
    
    Returns:
        Tuple of common paths for both soups
    """
    path1 = []
    path2 = []

    while (soup1 and soup2 and 
           soup1.name == soup2.name and 
           soup1.attrs == soup2.attrs):
        path1.append(soup1)
        path2.append(soup2)
        
        if len(soup1.contents) > 0 and len(soup2.contents) > 0:
            soup1 = next((child for child in soup1.contents if child.name), None)
            soup2 = next((child for child in soup2.contents if child.name), None)
        else:
            break

    return path1, path2