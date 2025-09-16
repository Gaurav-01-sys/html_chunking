
from html_chunker.merger import merge_html_chunks

def test_merge_html_chunks():
    chunks = ["<div>Chunk1</div>", "<div>Chunk2</div>"]
    merged = merge_html_chunks(chunks, k=1000)
    assert len(merged) > 0
