"""
Gradio web interface for HTML Chunking Library
"""

import gradio as gr
import tempfile
import os
from typing import List, Tuple
from html_chunking import get_html_chunks, HTMLChunker, count_tokens


def process_html_text(
    html_text: str,
    max_tokens: int,
    clean_html: bool,
    attr_cutoff_len: int
) -> Tuple[str, str, str]:
    """Process HTML text input and return chunks with statistics."""
    if not html_text.strip():
        return "", "Please enter some HTML content.", ""
    
    try:
        # Create chunker instance
        chunker = HTMLChunker(
            max_tokens=max_tokens,
            clean_html=clean_html,
            attr_cutoff_len=attr_cutoff_len if attr_cutoff_len > 0 else 40
        )
        
        # Process chunks with metadata
        chunks, removed_content = chunker.chunk_with_metadata(html_text)
        
        # Calculate statistics
        original_tokens = count_tokens(html_text)
        total_chunk_tokens = sum(count_tokens(chunk) for chunk in chunks)
        
        # Format output
        chunk_output = ""
        for i, chunk in enumerate(chunks):
            chunk_tokens = count_tokens(chunk)
            chunk_output += f"=== CHUNK {i+1} ({chunk_tokens} tokens) ===\n"
            chunk_output += chunk
            chunk_output += "\n\n"
        
        # Statistics
        stats = f"""
📊 **Chunking Statistics:**
- Original document: {original_tokens:,} tokens
- Number of chunks: {len(chunks)}
- Total tokens after processing: {total_chunk_tokens:,}
- Average tokens per chunk: {total_chunk_tokens//len(chunks) if chunks else 0}
- Max tokens per chunk: {max(count_tokens(chunk) for chunk in chunks) if chunks else 0}
- Min tokens per chunk: {min(count_tokens(chunk) for chunk in chunks) if chunks else 0}
"""
        
        # Removed content info
        removed_info = ""
        if removed_content:
            removed_info = f"""
🗑️ **Removed Content Summary:**
- {len(removed_content.split())} words removed from scripts, styles, and hidden elements
- First 200 characters: {removed_content[:200]}{"..." if len(removed_content) > 200 else ""}
"""
        
        return chunk_output, stats, removed_info
        
    except Exception as e:
        return "", f"❌ Error processing HTML: {str(e)}", ""


def process_html_file(
    file,
    max_tokens: int,
    clean_html: bool,
    attr_cutoff_len: int
) -> Tuple[str, str, str]:
    """Process uploaded HTML file."""
    if file is None:
        return "", "Please upload an HTML file.", ""
    
    try:
        # Read file content
        with open(file.name, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        return process_html_text(html_content, max_tokens, clean_html, attr_cutoff_len)
        
    except Exception as e:
        return "", f"❌ Error reading file: {str(e)}", ""


def download_chunks(
    html_text: str,
    max_tokens: int,
    clean_html: bool,
    attr_cutoff_len: int
) -> str:
    """Generate downloadable ZIP file with chunks."""
    if not html_text.strip():
        return None
    
    try:
        chunks = get_html_chunks(
            html=html_text,
            max_tokens=max_tokens,
            is_clean_html=clean_html,
            attr_cutoff_len=attr_cutoff_len if attr_cutoff_len > 0 else 40
        )
        
        # Create temporary directory for chunks
        temp_dir = tempfile.mkdtemp()
        
        for i, chunk in enumerate(chunks):
            chunk_file = os.path.join(temp_dir, f'chunk_{i:03d}.html')
            with open(chunk_file, 'w', encoding='utf-8') as f:
                f.write(chunk)
        
        # Create ZIP file
        import zipfile
        zip_path = os.path.join(temp_dir, 'html_chunks.zip')
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for i in range(len(chunks)):
                chunk_file = os.path.join(temp_dir, f'chunk_{i:03d}.html')
                zipf.write(chunk_file, f'chunk_{i:03d}.html')
        
        return zip_path
        
    except Exception as e:
        print(f"Error creating download: {e}")
        return None


# Create Gradio interface
with gr.Blocks(title="HTML Chunker", theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # 🔧 HTML Chunking Tool
    
    Split large HTML documents into smaller, semantically coherent chunks while preserving DOM structure.
    Perfect for preparing HTML content for LLM processing, web scraping analysis, or document processing pipelines.
    
    ## Features:
    - **Smart DOM-aware splitting** - Preserves HTML structure
    - **Token counting** - Uses tiktoken for accurate token limits
    - **Content cleaning** - Removes scripts, styles, and hidden elements
    - **Intelligent merging** - Optimizes chunk sizes
    """)
    
    with gr.Tabs():
        # Text input tab
        with gr.TabItem("📝 Text Input"):
            with gr.Row():
                with gr.Column(scale=2):
                    html_input = gr.Textbox(
                        label="HTML Content",
                        placeholder="Paste your HTML content here...",
                        lines=10,
                        max_lines=20
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("### ⚙️ Settings")
                    max_tokens_text = gr.Slider(
                        label="Max Tokens per Chunk",
                        minimum=100,
                        maximum=8000,
                        value=1000,
                        step=100
                    )
                    clean_html_text = gr.Checkbox(
                        label="Clean HTML (remove scripts, styles, hidden elements)",
                        value=True
                    )
                    attr_cutoff_text = gr.Slider(
                        label="Attribute Length Cutoff (0 = no limit)",
                        minimum=0,
                        maximum=200,
                        value=40,
                        step=10
                    )
                    
                    process_btn_text = gr.Button("🚀 Process HTML", variant="primary")
                    download_btn_text = gr.Button("💾 Download Chunks (ZIP)", variant="secondary")
            
            with gr.Row():
                with gr.Column():
                    chunks_output_text = gr.Textbox(
                        label="Generated Chunks",
                        lines=15,
                        max_lines=30
                    )
                
                with gr.Column(scale=1):
                    stats_output_text = gr.Markdown(label="Statistics")
                    removed_output_text = gr.Markdown(label="Removed Content")
        
        # File upload tab
        with gr.TabItem("📁 File Upload"):
            with gr.Row():
                with gr.Column(scale=2):
                    file_input = gr.File(
                        label="Upload HTML File",
                        file_types=[".html", ".htm"],
                        file_count="single"
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("### ⚙️ Settings")
                    max_tokens_file = gr.Slider(
                        label="Max Tokens per Chunk",
                        minimum=100,
                        maximum=8000,
                        value=1000,
                        step=100
                    )
                    clean_html_file = gr.Checkbox(
                        label="Clean HTML",
                        value=True
                    )
                    attr_cutoff_file = gr.Slider(
                        label="Attribute Length Cutoff",
                        minimum=0,
                        maximum=200,
                        value=40,
                        step=10
                    )
                    
                    process_btn_file = gr.Button("🚀 Process File", variant="primary")
            
            with gr.Row():
                with gr.Column():
                    chunks_output_file = gr.Textbox(
                        label="Generated Chunks",
                        lines=15,
                        max_lines=30
                    )
                
                with gr.Column(scale=1):
                    stats_output_file = gr.Markdown(label="Statistics")
                    removed_output_file = gr.Markdown(label="Removed Content")
    
    # Example section
    with gr.Accordion("📚 Example HTML", open=False):
        example_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sample Page</title>
    <style>
        .hidden { display: none; }
        body { font-family: Arial, sans-serif; }
    </style>
</head>
<body>
    <header>
        <h1>Welcome to My Website</h1>
        <nav>
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <section id="home">
            <h2>Home Section</h2>
            <p>This is the main content area with lots of important information that users need to see.</p>
            <div class="content-block">
                <h3>Subsection</h3>
                <p>More detailed content goes here with multiple paragraphs and rich information.</p>
            </div>
        </section>
        
        <section id="about">
            <h2>About Us</h2>
            <p>Learn more about our company and mission.</p>
        </section>
    </main>
    
    <div class="hidden">This content should be removed during cleaning</div>
    
    <script>
        console.log("This script will be removed");
    </script>
</body>
</html>'''
        
        gr.Code(example_html, language="html")
        
        load_example_btn = gr.Button("📋 Load Example")
        load_example_btn.click(
            lambda: example_html,
            outputs=[html_input]
        )
    
    # Event handlers
    process_btn_text.click(
        process_html_text,
        inputs=[html_input, max_tokens_text, clean_html_text, attr_cutoff_text],
        outputs=[chunks_output_text, stats_output_text, removed_output_text]
    )
    
    process_btn_file.click(
        process_html_file,
        inputs=[file_input, max_tokens_file, clean_html_file, attr_cutoff_file],
        outputs=[chunks_output_file, stats_output_file, removed_output_file]
    )
    
    download_btn_text.click(
        download_chunks,
        inputs=[html_input, max_tokens_text, clean_html_text, attr_cutoff_text],
        outputs=[gr.File()]
    )


if __name__ == "__main__":
    app.launch(share=True, debug=True)