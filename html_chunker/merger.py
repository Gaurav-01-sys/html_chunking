
from bs4 import BeautifulSoup
from html_chunker.utils import count_tokens

def get_common_root_path(soup1, soup2):
    path1 = []
    path2 = []

    while soup1 and soup2 and soup1.name == soup2.name and soup1.attrs == soup2.attrs:
        path1.append(soup1)
        path2.append(soup2)
        if len(soup1.contents) > 0 and len(soup2.contents) > 0:
            soup1 = next((child for child in soup1.contents if child.name), None)
            soup2 = next((child for child in soup2.contents if child.name), None)
        else:
            break

    return path1, path2

def merge_html_chunk(html_1, html_2):
    soup1 = BeautifulSoup(html_1, 'html.parser')
    soup2 = BeautifulSoup(html_2, 'html.parser')

    path1, path2 = get_common_root_path(soup1, soup2)
    common_parent1 = path1[-1] if path1 else soup1
    common_parent2 = path2[-1] if path2 else soup2

    for element in common_parent2.contents:
        if element not in common_parent1.contents:
            common_parent1.append(element)

    return str(soup1)

def merge_html_chunks(html_chunks, k: int):
    merged_chunks = []
    current_chunk = html_chunks[0]

    for i in range(1, len(html_chunks)):
        next_chunk = html_chunks[i]
        merged = merge_html_chunk(current_chunk, next_chunk)

        if count_tokens(merged) <= k:
            current_chunk = merged
        else:
            merged_chunks.append(current_chunk)
            current_chunk = next_chunk

    merged_chunks.append(current_chunk)
    return merged_chunks
