
from html_chunker.chunker import split_html_by_dom

def test_split_html_by_dom():
    html = "<html><body><p>Hello</p><div>World</div></body></html>"
    chunks = split_html_by_dom(html, max_token=1000)
    assert len(chunks) > 0
