
import streamlit as st
from html_chunker.cleaner import clean_html
from html_chunker.chunker import split_html_by_dom
from html_chunker.merger import merge_html_chunks

st.title("HTML Chunker App")

uploaded_file = st.file_uploader("Upload HTML file", type="html")
max_tokens = st.slider("Max tokens per chunk", 100, 4000, 1000)
clean = st.checkbox("Clean HTML", value=True)

if uploaded_file:
    html = uploaded_file.read().decode("utf-8")
    html, _ = clean_html(html) if clean else (html, "")
    chunks = split_html_by_dom(html, max_tokens)
    merged = merge_html_chunks([chunk['content'] for chunk in chunks], max_tokens)

    st.write(f"Generated {len(merged)} chunks:")
    for i, chunk in enumerate(merged):
        st.markdown(f"### Chunk {i+1}")
        st.code(chunk, language='html')
