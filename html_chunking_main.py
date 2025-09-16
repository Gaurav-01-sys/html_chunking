"""
Main HTML chunking interface and class-based API.
"""

from typing import List, Optional, Tuple
from html_chunking.html_cleaner import clean_html
from html_chunking.html_splitter import split_html_by_dom, merge_html_chunks


def get_html_chunks(
    html: str, 
    max_tokens: int, 
    is_clean_html: bool = True, 
    attr_cutoff_len: int = 40
) -> List[str]:
    """
    Main function to split HTML into chunks with token limits.
    
    Args:
        html: Raw HTML string to process
        max_tokens: Maximum tokens per chunk
        is_clean_html: Whether to clean the HTML first
        attr_cutoff_len: Maximum length for HTML attributes (0 for no limit)
    
    Returns:
        List of HTML chunk strings
    """
    # Clean HTML if requested
    if is_clean_html:
        html, _ = clean_html(html, attr_cutoff_len)
    
    # Split into initial chunks
    chunks = split_html_by_dom(html, max_tokens)
    chunk_contents = [chunk['content'] for chunk in chunks]
    
    # Merge chunks optimally
    merged_chunks = merge_html_chunks(chunk_contents, max_tokens)
    
    return merged_chunks


class HTMLChunker:
    """
    Class-based interface for HTML chunking with configuration options.
    """
    
    def __init__(
        self,
        max_tokens: int = 1000,
        clean_html: bool = True,
        attr_cutoff_len: int = 40,
        model: str = "gpt-3.5-turbo"
    ):
        """
        Initialize HTMLChunker with configuration.
        
        Args:
            max_tokens: Maximum tokens per chunk
            clean_html: Whether to clean HTML before chunking
            attr_cutoff_len: Maximum attribute length
            model: Tokenizer model to use
        """
        self.max_tokens = max_tokens
        self.clean_html = clean_html
        self.attr_cutoff_len = attr_cutoff_len
        self.model = model
        self._last_removed_content = None
    
    def chunk(self, html: str) -> List[str]:
        """
        Split HTML into chunks using instance configuration.
        
        Args:
            html: HTML string to chunk
        
        Returns:
            List of HTML chunk strings
        """
        return get_html_chunks(
            html=html,
            max_tokens=self.max_tokens,
            is_clean_html=self.clean_html,
            attr_cutoff_len=self.attr_cutoff_len
        )
    
    def chunk_with_metadata(self, html: str) -> Tuple[List[str], Optional[str]]:
        """
        Split HTML into chunks and return removed content metadata.
        
        Args:
            html: HTML string to chunk
        
        Returns:
            Tuple of (chunks, removed_content)
        """
        from .cleaner import clean_html as clean_html_func
        
        if self.clean_html:
            cleaned_html, removed_content = clean_html_func(html, self.attr_cutoff_len)
            self._last_removed_content = removed_content
        else:
            cleaned_html = html
            removed_content = None
        
        chunks = split_html_by_dom(cleaned_html, self.max_tokens)
        chunk_contents = [chunk['content'] for chunk in chunks]
        merged_chunks = merge_html_chunks(chunk_contents, self.max_tokens)
        
        return merged_chunks, removed_content
    
    def get_last_removed_content(self) -> Optional[str]:
        """
        Get content that was removed during the last cleaning operation.
        
        Returns:
            Removed content text or None
        """
        return self._last_removed_content