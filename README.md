# GitSummarizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

GitSummarizer provides human-readable summaries of git changes and commits, making complex repository activities easier to understand. It leverages various language models to transform technical git data into plain language explanations.

## Features

- 📅 **Summarize by Time Range**: Get summaries of commits between specific dates (YYYY-MM-DD format)
- 🔍 **Summarize Recent Commits**: Get a human-friendly overview of your recent commit activity
- 🔎 **Analyze Specific Commits**: Deep dive into a particular commit with natural language descriptions
- 🔀 **Compare Branches**: Understand the differences between branches in plain English
- 🔌 **Multiple LLM Providers**: Support for Groq, OpenAI, Google Gemini, and local Ollama models
- ⚙️ **Customizable Defaults**: Configure default number of commits, comparison branch, and output format
- 💻 **Command-line Interface**: Easy-to-use CLI with rich, colorful output

## Installation
I haven't published this on PyPI yet, so fetch it from Github ;)
```bash
pip install git+https://github.com/SANTHOSH-SACHIN/gitsummarizer.git
```

## Setup

Before using GitSummarizer, you need to configure an LLM provider:

```bash
gitsumm setup
```

This will guide you through selecting a provider and setting up any API keys. Reccommended default is Groq (Use the most lightweight Llama 1B Model for instant results)

## Usage

### Summarize Recent Commits

```bash
# Summarize the last 5 commits
gitsumm recent

# Summarize the last 10 commits
gitsumm recent -n 10

# Summarize commits from a specific branch
gitsumm recent -b feature-branch
```

### Analyze a Specific Commit

```bash
gitsumm commit abc1234
```

### Compare Branches

```bash
gitsumm compare main feature-branch
```

### Summarize Commits by Time Range

```bash
# Summarize commits between two dates (YYYY-MM-DD format)
gitsumm time 2025-01-01 2025-03-25

# Summarize commits from a specific branch within a date range
gitsumm time 2025-01-01 2025-03-25 -b feature-branch
```

### Change LLM Provider

```bash
# List available providers
gitsumm provider -l

# Switch to a different provider
gitsumm provider openai
```

### Configure Default Settings

```bash
# Set default number of recent commits to 10
gitsumm defaults --recent 10

# Set default comparison branch to 'develop'
gitsumm defaults --branch develop

# Set default output format to markdown
gitsumm defaults --format markdown
```

## Supported LLM Providers

- **Groq**: Fast performance with various Llama models
- **OpenAI**: High-quality summaries with GPT models
- **Google Gemini**: Google's latest language models
- **Ollama**: Run LLMs locally on your machine for privacy

## Requirements

- Python 3.8+
- Git
- For Ollama provider: [Ollama](https://ollama.ai/) installed and running

## Contributing

Contributions are welcome! Check out the [Contributing Guide](CONTRIBUTING.md) to get started.

P.S: I need help to setup the tests and worflow. Would be happy if someone can help me out ;)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
