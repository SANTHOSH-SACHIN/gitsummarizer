#!/usr/bin/env python3

from setuptools import setup, find_packages

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gitsummarizer",
    version="0.5.0",
    author="",
    author_email="",
    description="Human-readable summaries of git changes and commits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SANTHOSH-SACHIN/gitsummarizer",
    project_urls={
        "Bug Tracker": "https://github.com/SANTHOSH-SACHIN/gitsummarizer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    package_dir={"": "."},
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "gitpython>=3.1.0",
        "requests>=2.25.0",
        "rich>=10.0.0",
        "anthropic>=0.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gitsumm=gitsummarizer.cli:main",
        ],
    },
)
