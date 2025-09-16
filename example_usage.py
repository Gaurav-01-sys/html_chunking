"""
Basic usage examples for HTML Chunking Library
"""

import os
from html_chunking import get_html_chunks, HTMLChunker, count_tokens

def example_basic_chunking():
    """Basic HTML chunking example."""
    print("=== Basic HTML Chunking ===")
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sample Document</title>
        <style>
            .hidden { display: none; }
            body { font-family: Arial; }
        </style>
    </head>
    <body>
        <header>
            <h1>Main Title</h1>
            <nav>
                <ul>
                    <li><a href="#section1">Section 1</a></li>
                    <li><a href="#section2">Section 2</a></li>
                </ul>
            </nav>
        </header>
        
        <main>
            <section id="section1">
                <h2>First Section</h2>
                <p>This is a longer paragraph with substantial content that demonstrates how the chunking algorithm works with real HTML content.</p>
                <div class="content-block">
                    <h3>Subsection</h3>
                    <p>More content here with additional information that adds to the token count.</p>
                    <ul>
                        <li>List item 1</li>
                        <li>List item 2</li>
                        <li>List item 3</li>
                    </ul>
                </div>
            </section>
            
            <section id="section2">
                <h2>Second Section</h2>
                <p>Another section with different content structure.</p>
                <table>
                    <tr>
                        <th>Column 1</th>
                        <th>Column 2</th>
                    </tr>
                    <tr>
                        <td>Data 1</td>
                        <td>Data 2</td>
                    </tr>
                </table>
            </section>
        </main>
        
        <div class="hidden">This should be removed during cleaning</div>
        
        <script>
            console.log("This script will be removed");
        </script>
    </body>
    </html>
    """
    
    # Basic chunking
    chunks = get_html_chunks(html_content, max_tokens=500)
    
    print(f"Original HTML: {count_tokens(html_content)} tokens")
    print(f"Generated {len(chunks)} chunks:")
    
    for i, chunk in enumerate(chunks):
        token_count = count_tokens(chunk)
        print(f"  Chunk {i+1}: {token_count} tokens")


def example_class_based_api():
    """Example using class-based API with metadata."""
    print("\n=== Class-based API with Metadata ===")
    
    html_content = """
    <html>
    <head>
        <title>Test Page</title>
        <style>
            .ads { display: none; }
            .sidebar { visibility: hidden; }
        </style>
        <script src="analytics.js"></script>
    </head>
    <body>
        <article>
            <h1>Article Title</h1>
            <p>Main article content goes here with important information.</p>
        </article>
        <div class="ads">Advertisement content</div>
        <div class="sidebar">Hidden sidebar content</div>
    </body>
    </html>
    """
    
    # Create chunker with custom settings
    chunker = HTMLChunker(
        max_tokens=300,
        clean_html=True,
        attr_cutoff_len=30
    )
    
    # Process with metadata
    chunks, removed_content = chunker.chunk_with_metadata(html_content)
    
    print(f"Processed into {len(chunks)} chunks")
    
    if removed_content:
        print(f"Removed content ({len(removed_content)} chars):")
        print(f"  Preview: {removed_content[:100]}...")


def example_file_processing():
    """Example of processing HTML files and saving chunks."""
    print("\n=== File Processing Example ===")
    
    # Create sample HTML file
    sample_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Large Document</title>
    </head>
    <body>
        <h1>Chapter 1: Introduction</h1>
        <p>This is the beginning of a large document that needs to be split into smaller chunks for processing.</p>
        
        <h2>Section 1.1: Overview</h2>
        <p>Detailed overview content with multiple paragraphs and extensive information about the topic.</p>
        <p>Additional paragraph with more content to increase the token count significantly.</p>
        
        <h2>Section 1.2: Background</h2>
        <p>Background information that provides context for the rest of the document.</p>
        <ul>
            <li>Point one with detailed explanation</li>
            <li>Point two with additional context</li>
            <li>Point three with supporting information</li>
        </ul>
        
        <h1>Chapter 2: Methodology</h1>
        <p>This chapter describes the methodology used in this work.</p>
        <p>Multiple paragraphs of detailed methodology explanation.</p>
    </body>
    </html>
    """
    
    # Save sample file
    os.makedirs('temp', exist_ok=True)
    with open('temp/sample_document.html', 'w', encoding='utf-8') as f:
        f.write(sample_html)
    
    # Process file
    with open('temp/sample_document.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    chunker = HTMLChunker(max_tokens=800)
    chunks = chunker.chunk(html_content)
    
    # Save chunks
    os.makedirs('temp/chunks', exist_ok=True)
    for i, chunk in enumerate(chunks):
        chunk_file = f'temp/chunks/chunk_{i:03d}.html'
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(chunk)
        
        token_count = count_tokens(chunk)
        print(f"Saved {chunk_file}: {token_count} tokens")
    
    print(f"All chunks saved to temp/chunks/ directory")


def example_advanced_configuration():
    """Advanced configuration examples."""
    print("\n=== Advanced Configuration ===")
    
    html_content = """
    <html>
    <body>
        <div data-very-long-attribute="https://example.com/very/long/url/that/exceeds/normal/length/limits/and/should/be/truncated">
            <h1>Content with Long Attributes</h1>
            <img src="https://example.com/images/very/long/path/to/image.jpg" alt="Description">
        </div>
    </body>
    </html>
    """
    
    # Different configurations
    configs = [
        {"name": "Default", "chunker": HTMLChunker()},
        {"name": "No Cleaning", "chunker": HTMLChunker(clean_html=False)},
        {"name": "Long Attributes", "chunker": HTMLChunker(attr_cutoff_len=0)},
        {"name": "Small Chunks", "chunker": HTMLChunker(max_tokens=200)},
        {"name": "GPT-4 Tokens", "chunker": HTMLChunker(model="gpt-4")},
    ]
    
    for config in configs:
        chunks = config["chunker"].chunk(html_content)
        total_tokens = sum(count_tokens(chunk) for chunk in chunks)
        print(f"{config['name']}: {len(chunks)} chunks, {total_tokens} total tokens")


if __name__ == "__main__":
    example_basic_chunking()
    example_class_based_api()
    example_file_processing()
    example_advanced_configuration()
    
    print("\n✅ All examples completed successfully!")
    print("Check the temp/ directory for generated files.")