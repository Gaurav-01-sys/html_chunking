
import argparse
from html_chunker.cleaner import clean_html
from html_chunker.chunker import split_html_by_dom
from html_chunker.merger import merge_html_chunks
import os

def main():
    parser = argparse.ArgumentParser(description="HTML Chunker CLI")
    parser.add_argument("html_file", type=str, help="Path to HTML file")
    parser.add_argument("--max_tokens", type=int, default=1000)
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--attr_cutoff", type=int, default=40)
    args = parser.parse_args()

    with open(args.html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    html, _ = clean_html(html, args.attr_cutoff) if args.clean else (html, "")
    chunks = split_html_by_dom(html, args.max_tokens)
    merged = merge_html_chunks([chunk['content'] for chunk in chunks], args.max_tokens)

    if not os.path.exists("chunks"):
        os.makedirs("chunks")

    for i, chunk in enumerate(merged):
        with open(f"chunks/chunk_{i}.html", "w", encoding="utf-8") as f:
            f.write(chunk)

if __name__ == "__main__":
    main()
