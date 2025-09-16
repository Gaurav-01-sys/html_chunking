
import tiktoken

def count_tokens(text: str) -> int:
    encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoder.encode(text))

def format_attrs(attrs):
    return {k: ' '.join(v) if isinstance(v, list) else v for k, v in attrs.items()}
