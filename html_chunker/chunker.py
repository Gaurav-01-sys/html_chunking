
from bs4 import BeautifulSoup
from html_chunker.utils import count_tokens, format_attrs

def build_full_content(path, node):
    opening_tags = ''.join(
        ["<" + p['tag'] + ''.join([' {}="{}"'.format(k, v) for k, v in p['attrs'].items()]) + ">" for p in path]
    )
    node_content = str(node)
    closing_tags = ''.join(["</" + p['tag'] + ">" for p in reversed(path)])
    return opening_tags + node_content + closing_tags

def traverse_dom(node, chunks, k, path=[]):
    if not node.name:
        return

    node_length = count_tokens(str(node))
    if node_length < k:
        full_content = build_full_content(path, node)
        chunks.append({'tag': node.name, 'attrs': node.attrs, 'content': full_content, 'path': path.copy()})
        return

    for child in node.children:
        if child.name:
            path.append({'tag': node.name, 'attrs': format_attrs(node.attrs)})
            traverse_dom(child, chunks, k, path)
            path.pop()

def split_html_by_dom(html_string: str, max_token: int):
    chunks = []
    soup = BeautifulSoup(html_string, 'html.parser')
    traverse_dom(soup, chunks, k=max_token)
    return chunks
