
from bs4 import BeautifulSoup
import cssutils

def clean_html(html: str, attr_max_len: int = 0) -> tuple[str, str]:
    soup = BeautifulSoup(html, "lxml")
    removed_content = []

    css_texts = [style.get_text() for style in soup.find_all('style')]
    for css_text in css_texts:
        sheet = cssutils.parseString(css_text)
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                selector = rule.selectorText
                if '::' in selector or ':after' in selector or ':before' in selector:
                    continue
                if 'display' in rule.style and 'none' in rule.style['display']:
                    for element in soup.select(selector):
                        removed_content.append(element.get_text())
                        element.decompose()
                elif 'visibility' in rule.style and 'hidden' in rule.style['visibility']:
                    for element in soup.select(selector):
                        removed_content.append(element.get_text())
                        element.decompose()

    for tag in ['script', 'style']:
        for element in soup.find_all(tag):
            removed_content.append(element.get_text())
            element.decompose()

    for elem in soup.find_all(style=lambda value: value and (
        'display:none' in value or 'visibility:hidden' in value)):
        elem.decompose()

    attr_to_truncate = ['href', 'src', 'd', 'url', 'data-url', 'data-src', 'data-src-hq']
    for attr in attr_to_truncate:
        for tag in soup.find_all(attrs={attr: True}):
            if attr_max_len and len(tag[attr]) > attr_max_len:
                tag[attr] = tag[attr][:attr_max_len] + "..."

    for element in soup.find_all(attrs={"aria-hidden": "true"}):
        removed_content.append(element.get_text())
        element.decompose()
    for element in soup.find_all(attrs={"tabindex": "-1"}):
        removed_content.append(element.get_text())
        element.decompose()

    return str(soup), "\n".join(removed_content)
