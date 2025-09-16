"""
HTML cleaning utilities for removing unwanted content and optimizing for chunking.
"""

import cssutils
from bs4 import BeautifulSoup
from typing import Tuple, List


def clean_html(html: str, attr_max_len: int = 0) -> Tuple[str, str]:
    """
    Clean HTML by removing scripts, styles, hidden elements, and long attributes.
    
    Args:
        html: Raw HTML string to clean
        attr_max_len: Maximum length for attributes (0 = no limit)
    
    Returns:
        Tuple of (cleaned_html, removed_content_text)
    """
    soup = BeautifulSoup(html, "lxml")
    removed_content = []

    # Remove CSS-hidden elements
    css_texts = [style.get_text() for style in soup.find_all('style')]
    for css_text in css_texts:
        try:
            sheet = cssutils.parseString(css_text)
            for rule in sheet:
                if rule.type == rule.STYLE_RULE:
                    selector = rule.selectorText
                    # Skip pseudo-elements
                    if '::' in selector or ':after' in selector or ':before' in selector:
                        continue
                    
                    # Remove elements with display:none or visibility:hidden
                    if 'display' in rule.style and 'none' in rule.style['display']:
                        for element in soup.select(selector):
                            removed_content.append(element.get_text())
                            element.decompose()
                    elif 'visibility' in rule.style and 'hidden' in rule.style['visibility']:
                        for element in soup.select(selector):
                            removed_content.append(element.get_text())
                            element.decompose()
        except Exception:
            # Skip malformed CSS
            continue

    # Remove script and style tags
    for tag in ['script', 'style']:
        for element in soup.find_all(tag):
            removed_content.append(element.get_text())
            element.decompose()

    # Remove elements with inline hidden styles
    for elem in soup.find_all(style=lambda value: value and (
        'display:none' in value or 'display: none' in value or 
        'visibility:hidden' in value or 'visibility: hidden' in value
    )):
        elem.decompose()

    # Truncate long attributes
    attr_to_truncate = ['href', 'src', 'd', 'url', 'data-url', 'data-src', 'data-src-hq']
    for attr in attr_to_truncate:
        for tag in soup.find_all(attrs={attr: True}):
            if attr_max_len and len(tag[attr]) > attr_max_len:
                tag[attr] = tag[attr][:attr_max_len] + "..."

    # Remove aria-hidden and non-focusable elements
    for element in soup.find_all(attrs={"aria-hidden": "true"}):
        removed_content.append(element.get_text())
        element.decompose()

    for element in soup.find_all(attrs={"tabindex": "-1"}):
        removed_content.append(element.get_text())
        element.decompose()

    cleaned_html = str(soup)
    removed_content_text = "\n".join(removed_content)
    
    return cleaned_html, removed_content_text