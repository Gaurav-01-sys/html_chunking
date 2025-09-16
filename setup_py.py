"""
Setup script for HTML Chunking Library
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="html-chunking",
    version="1.0.0",
    author="HTML Chunking Team",
    author_email="contact@htmlchunking.dev",
    description="Intelligent HTML document chunking for LLM processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/html-chunking",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/html-chunking/issues",
        "Source": "https://github.com/yourusername/html-chunking",
        "Documentation": "https://github.com/yourusername/html-chunking/wiki",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
            "mypy>=1.0",
        ],
        "web": [
            "gradio>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "html-chunker=html_chunking.cli:main",
        ],
    },
    keywords="html chunking tokenization llm nlp dom parsing",
    include_package_data=True,
    zip_safe=False,
)