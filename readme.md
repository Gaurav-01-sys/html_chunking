# HTML Chunking Library 🔧

A powerful Python library for intelligently splitting large HTML documents into smaller, semantically coherent chunks while preserving DOM structure and staying within token limits for LLM processing.

## 🌟 Features

- **Smart DOM-aware splitting** - Preserves HTML structure and semantic meaning
- **Token counting** - Uses tiktoken for accurate token counting with various LLM models
- **Content cleaning** - Automatically removes scripts, styles, and hidden elements
- **Intelligent merging** - Optimizes chunk sizes while respecting token limits
- **Gradio web interface** - Easy-to-use web app for interactive HTML chunking
- **Modular design** - Clean, extensible codebase with separate concerns

## 🚀 Use Cases

### 1. **LLM Document Processing**
- Prepare large HTML documents for processing with ChatGPT, Claude, or other LLMs
- Stay within token limits while maintaining document structure
- Perfect for RAG (Retrieval Augmented Generation) systems

### 2. **Web Scraping Analysis**
- Split scraped web pages into manageable sections
- Analyze website structure and content systematically
- Process large e-commerce catalogs or news websites

### 3. **Content Management Systems**
- Break down large CMS pages for better organization
- Create content previews and summaries
- Optimize content for search and indexing

### 4. **Document Processing Pipelines**
- Preprocess HTML for machine learning models
- Create training data from web content
- Build content analysis and classification systems

### 5. **API and Data Processing**
- Batch process multiple HTML documents
- Create microservices for HTML content processing
- Build scalable document processing workflows

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/html-chunking.git
cd html-chunking

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

## 🔧 Quick Start

### Basic Usage

```python
from html_chunking import get_html_chunks

# Simple chunking
html_content = """
<html>
    <body>
        <h1>Large Document</h1>
        <p>Your HTML content here...</p>
    </body>
</html>
"""

chunks = get_html_chunks(
    html=html_content,
    max_tokens=1000,
    is_clean_html=True,
    attr_cutoff_len=40
)

print(f"Created {len(chunks)} chunks")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {len(chunk)} characters")
```

### Class-based API

```python
from html_chunking import HTMLChunker

# Create chunker with custom settings
chunker = HTMLChunker(
    max_tokens=1500,
    clean_html=True,
    attr_cutoff_len=50,
    model="gpt-4"
)

# Process HTML with metadata
chunks, removed_content = chunker.chunk_with_metadata(html_content)

# Access removed content
if removed_content:
    print(f"Removed: {len(removed_content)} characters of scripts/styles")
```

### Advanced Usage

```python
from html_chunking import HTMLChunker, count_tokens

# Custom processing pipeline
chunker = HTMLChunker(max_tokens=2000, clean_html=False)

# Read from file
with open('large_document.html', 'r') as f:
    html = f.read()

# Process and analyze
chunks = chunker.chunk(html)

for i, chunk in enumerate(chunks):
    token_count = count_tokens(chunk)
    print(f"Chunk {i+1}: {token_count} tokens")
    
    # Save individual chunks
    with open(f'output/chunk_{i:03d}.html', 'w') as f:
        f.write(chunk)
```

## 🌐 Web Interface

Launch the Gradio web interface for interactive HTML chunking:

```bash
python app.py
```

Features:
- **Text Input**: Paste HTML directly
- **File Upload**: Upload .html files
- **Real-time Processing**: See results instantly
- **Download Chunks**: Get ZIP file with all chunks
- **Statistics**: Token counts and processing metrics

## 📁 Project Structure

```
html-chunking/
├── html_chunking/          # Main package
│   ├── __init__.py        # Package initialization
│   ├── main.py           # Main API functions
│   ├── core.py           # Core chunking logic
│   ├── cleaner.py        # HTML cleaning utilities
│   └── splitter.py       # DOM splitting and merging
├── app.py                # Gradio web interface
├── requirements.txt      # Dependencies
├── setup.py             # Package setup
├── README.md            # Documentation
├── examples/            # Usage examples
└── tests/              # Unit tests
```

## 🎯 API Reference

### `get_html_chunks(html, max_tokens, is_clean_html=True, attr_cutoff_len=40)`

Main function for HTML chunking.

**Parameters:**
- `html` (str): Raw HTML string to process
- `max_tokens` (int): Maximum tokens per chunk
- `is_clean_html` (bool): Whether to clean HTML first
- `attr_cutoff_len` (int): Maximum attribute length (0 for no limit)

**Returns:** List of HTML chunk strings

### `HTMLChunker` Class

Class-based interface with configuration options.

**Methods:**
- `chunk(html)`: Split HTML into chunks
- `chunk_with_metadata(html)`: Split with removed content info
- `get_last_removed_content()`: Get last removed content

### Utility Functions

- `count_tokens(text, model="gpt-3.5-turbo")`: Count tokens in text
- `clean_html(html, attr_max_len=0)`: Clean HTML content
- `split_html_by_dom(html, max_tokens)`: Split HTML by DOM structure

## ⚙️ Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_tokens` | 1000 | Maximum tokens per chunk |
| `clean_html` | True | Remove scripts, styles, hidden elements |
| `attr_cutoff_len` | 40 | Truncate long attributes |
| `model` | "gpt-3.5-turbo" | Tokenizer model |

## 📊 Performance

- **Processing Speed**: ~1MB HTML/second on average hardware
- **Memory Usage**: Efficient DOM processing with minimal memory overhead
- **Token Accuracy**: Uses tiktoken for precise token counting
- **Chunk Quality**: Preserves semantic structure and readability

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=html_chunking
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- Built with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- Uses [tiktoken](https://github.com/openai/tiktoken) for accurate token counting
- Web interface powered by [Gradio](https://gradio.app/)
- CSS parsing with [cssutils](https://github.com/jaraco/cssutils)

## 📞 Support

- 🐛 [Report Issues](https://github.com/yourusername/html-chunking/issues)
- 💡 [Feature Requests](https://github.com/yourusername/html-chunking/discussions)
- 📖 [Documentation](https://github.com/yourusername/html-chunking/wiki)

---

Made with ❤️ for the developer community