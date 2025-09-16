"""
Command-line interface for HTML Chunking Library
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List

from html_chunking.html_chunking_main import HTMLChunker
from html_chunking.html_chunking_core import count_tokens


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Split HTML documents into smaller chunks for LLM processing"
    )
    
    parser.add_argument(
        "input",
        help="Input HTML file or directory"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="./chunks",
        help="Output directory for chunks (default: ./chunks)"
    )
    
    parser.add_argument(
        "-t", "--max-tokens",
        type=int,
        default=1000,
        help="Maximum tokens per chunk (default: 1000)"
    )
    
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Skip HTML cleaning (keep scripts, styles, etc.)"
    )
    
    parser.add_argument(
        "--attr-cutoff",
        type=int,
        default=40,
        help="Maximum attribute length (0 for no limit, default: 40)"
    )
    
    parser.add_argument(
        "--model",
        default="gpt-3.5-turbo",
        help="Tokenizer model to use (default: gpt-3.5-turbo)"
    )
    
    parser.add_argument(
        "--prefix",
        default="chunk_",
        help="Prefix for chunk filenames (default: chunk_)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show detailed statistics"
    )
    
    args = parser.parse_args()
    
    # Validate input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path '{args.input}' does not exist")
        sys.exit(1)
    
    # Create output directory
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize chunker
    chunker = HTMLChunker(
        max_tokens=args.max_tokens,
        clean_html=not args.no_clean,
        attr_cutoff_len=args.attr_cutoff,
        model=args.model
    )
    
    # Process files
    html_files = []
    if input_path.is_file():
        if input_path.suffix.lower() in ['.html', '.htm']:
            html_files = [input_path]
        else:
            print(f"Error: '{args.input}' is not an HTML file")
            sys.exit(1)
    elif input_path.is_dir():
        html_files = list(input_path.glob('**/*.html')) + list(input_path.glob('**/*.htm'))
        if not html_files:
            print(f"No HTML files found in '{args.input}'")
            sys.exit(1)
    
    if args.verbose:
        print(f"Found {len(html_files)} HTML file(s)")
        print(f"Output directory: {output_path}")
        print(f"Max tokens per chunk: {args.max_tokens}")
        print(f"Clean HTML: {not args.no_clean}")
        print()
    
    total_chunks = 0
    total_input_tokens = 0
    total_output_tokens = 0
    
    for html_file in html_files:
        if args.verbose:
            print(f"Processing: {html_file}")
        
        try:
            # Read HTML content
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Count original tokens
            input_tokens = count_tokens(html_content, args.model)
            total_input_tokens += input_tokens
            
            # Process chunks
            chunks, removed_content = chunker.chunk_with_metadata(html_content)
            
            # Create output subdirectory for this file
            file_output_dir = output_path / html_file.stem
            file_output_dir.mkdir(exist_ok=True)
            
            # Save chunks
            chunk_tokens = []
            for i, chunk in enumerate(chunks):
                chunk_filename = f"{args.prefix}{i:03d}.html"
                chunk_path = file_output_dir / chunk_filename
                
                with open(chunk_path, 'w', encoding='utf-8') as f:
                    f.write(chunk)
                
                tokens = count_tokens(chunk, args.model)
                chunk_tokens.append(tokens)
                total_output_tokens += tokens
            
            total_chunks += len(chunks)
            
            if args.verbose:
                print(f"  Created {len(chunks)} chunks in {file_output_dir}")
                if removed_content:
                    print(f"  Removed {len(removed_content)} chars of scripts/styles")
            
            if args.stats:
                print(f"  Input tokens: {input_tokens:,}")
                print(f"  Output tokens: {sum(chunk_tokens):,}")
                print(f"  Avg tokens per chunk: {sum(chunk_tokens)//len(chunk_tokens)}")
                print(f"  Token range: {min(chunk_tokens)} - {max(chunk_tokens)}")
                print()
        
        except Exception as e:
            print(f"Error processing {html_file}: {e}")
            continue
    
    # Final statistics
    print(f"✅ Processing complete!")
    print(f"Processed {len(html_files)} file(s)")
    print(f"Created {total_chunks} chunk(s)")
    print(f"Total input tokens: {total_input_tokens:,}")
    print(f"Total output tokens: {total_output_tokens:,}")
    
    if total_chunks > 0:
        print(f"Average tokens per chunk: {total_output_tokens//total_chunks}")
    
    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    main()