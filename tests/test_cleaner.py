
from html_chunker.cleaner import clean_html

def test_clean_html_basic():
    html = "<html><body><script>console.log('hi')</script><p>Hello</p></body></html>"
    cleaned, removed = clean_html(html)
    assert "<script>" not in cleaned
    assert "Hello" in cleaned
