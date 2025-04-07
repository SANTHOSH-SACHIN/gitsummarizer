# GitSummarizer

## Release Notes (v0.5.0 - April 2025)

🚀 **Major Updates**:
- Added comprehensive project configuration via pyproject.toml
- Created USAGE.md with detailed documentation and examples
- Implemented automated testing with pytest and GitHub Actions
- Enhanced CLI configuration management
- Improved error handling and user feedback

🔧 **Technical Improvements**:
- Modernized Python packaging configuration
- Added test coverage reporting
- Standardized development tooling (black, isort, pytest)
- Updated dependencies and requirements

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

GitSummarizer provides human-readable summaries of git changes and commits, making complex repository activities easier to understand. It leverages various language models to transform technical git data into plain language explanations.

## Features

- 📅 **Summarize by Time Range**: Get summaries of commits between specific dates (YYYY-MM-DD format)
- 🔍 **Summarize Recent Commits**: Get a human-friendly overview of your recent commit activity
- 🔎 **Analyze Specific Commits**: Deep dive into a particular commit with natural language descriptions
- 🔀 **Compare Branches**: Understand the differences between branches in plain English
- 🔌 **Multiple LLM Providers**: Support for Groq, OpenAI, Google Gemini, Anthropic Claude, and local Ollama models
- ⚙️ **Customizable Defaults**: Configure default number of commits, comparison branch, and output format
- 💻 **Command-line Interface**: Easy-to-use CLI with rich, colorful output

## Installation
I haven't published this on PyPI yet, so fetch it from Github ;)

```bash
pip install git+https://github.com/SANTHOSH-SACHIN/gitsummarizer.git
```

## Setup and Configuration

Before using GitSummarizer, you need to configure an LLM provider:

```bash
gitsumm setup
```

This interactive setup will:
1. Let you select from available providers (Groq, OpenAI, Google Gemini, Anthropic Claude, or local Ollama)
2. Securely store your API keys (except for Ollama)
3. Set default model preferences

Recommended defaults:
- **Provider**: Groq (fastest response time)
- **Model**: llama-3.2-1b-preview (lightweight but effective)

### Configuration File

GitSummarizer stores configuration in `~/.config/gitsumm/config.json`. You can:
- Edit this file directly (not recommended)
- Use the CLI commands to modify settings
- Set environment variables for API keys (takes precedence over config file)

## Usage Examples

### Basic Usage

```bash
# Summarize last 5 commits (default)
gitsumm recent

# Summarize last 10 commits from feature branch
gitsumm recent -n 10 -b feature-branch

# Get detailed analysis of a specific commit
gitsumm commit abc1234
```

### Advanced Usage

```bash
# Compare branches with custom output format
gitsumm compare main feature-branch --format markdown > comparison.md

# Summarize commits from last quarter (2025 Q1)
gitsumm time 2025-01-01 2025-03-31

# Get JSON output for programmatic processing
gitsumm recent --format json | jq .
```

### Configuration Management

```bash
# List available LLM providers
gitsumm provider -l

# Switch to OpenAI provider
gitsumm provider openai

# Set multiple defaults at once
gitsumm defaults --recent 10 --branch develop --format markdown

# Verify current configuration
cat ~/.config/gitsumm/config.json
```

### Integration Examples

```bash
# Use in CI/CD pipeline (GitHub Actions example)
- name: Summarize changes
  run: |
    pip install gitsummarizer
    gitsumm compare ${{ github.base_ref }} ${{ github.head_ref }} --format markdown >> summary.md

# Daily summary cron job
0 18 * * * cd /path/to/repo && gitsumm time $(date -d "yesterday" +%F) $(date +%F) >> ~/git-summaries.log
```

## Output Formats

GitSummarizer supports multiple output formats:

1. **Text** (default): Human-readable plain text with colors
2. **Markdown**: Formatted for documentation
3. **JSON**: Structured data for programmatic use

Example JSON output:
```json
{
  "summary": "Added new authentication module",
  "details": [
    {
      "file": "src/auth.py",
      "changes": "+120 -0",
      "description": "Implemented JWT token generation"
    }
  ]
}
```

## Supported LLM Providers

- **Groq**: Fast performance with various Llama models
- **OpenAI**: High-quality summaries with GPT models
- **Google Gemini**: Google's latest language models
- **Anthropic Claude**: Advanced AI models from Anthropic
- **Ollama**: Run LLMs locally on your machine for privacy

## Requirements

- Python 3.8+
- Git
- For Ollama provider: [Ollama](https://ollama.ai/) installed and running

## Contributing

Contributions are welcome! Check out the [Contributing Guide](CONTRIBUTING.md) to get started.

P.S: I need help to setup the tests and worflow. Would be happy if someone can help me out ;)

## Documentation

For detailed usage instructions and configuration options, see:
- [USAGE.md](USAGE.md) - Advanced usage examples and configuration details
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development and contribution guidelines

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
