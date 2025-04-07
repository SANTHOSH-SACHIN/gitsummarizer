# GitSummarizer Usage Guide

## Configuration File Details

GitSummarizer stores configuration in `~/.config/gitsumm/config.json`. The file structure is:

```json
{
  "provider": "groq",
  "api_keys": {
    "openai": "sk-...",
    "groq": "gsk-..."
  },
  "model_preferences": {
    "groq": "llama-3.2-1b-preview",
    "openai": "gpt-4o"
  },
  "defaults": {
    "recent_commits": 5,
    "compare_branch": "main",
    "output_format": "text"
  }
}
```

### Managing Configuration

1. **View current config**:
   ```bash
   cat ~/.config/gitsumm/config.json
   ```

2. **Override with environment variables**:
   ```bash
   export OPENAI_API_KEY='sk-...'
   export GROQ_API_KEY='gsk-...'
   ```

## Advanced Usage Examples

### Integration with Git Hooks

Add to `.git/hooks/post-commit`:
```bash
#!/bin/sh
gitsumm recent -n 1 >> .git/commit_summaries.log
```

### Team Workflow Integration

1. **Daily standup report**:
   ```bash
   gitsumm time $(date -d "yesterday" +%F) $(date +%F) --format markdown > daily_standup.md
   ```

2. **PR description helper**:
   ```bash
   gitsumm compare main feature-branch --format markdown > pr_description.md
   ```

## Configuration Management

### Multiple Profiles

Create separate config files and switch between them:
```bash
# Use work profile
cp ~/.config/gitsumm/work_config.json ~/.config/gitsumm/config.json

# Use personal profile
cp ~/.config/gitsumm/personal_config.json ~/.config/gitsumm/config.json
```

### Secure API Key Storage

For production environments, we recommend:
1. Using environment variables
2. Using secret management services
3. Restricting file permissions:
   ```bash
   chmod 600 ~/.config/gitsumm/config.json
   ```

## Troubleshooting

### Common Issues

1. **Missing API Key**:
   ```bash
   gitsumm setup
   ```

2. **Invalid Date Format**:
   ```bash
   # Correct format:
   gitsumm time 2025-01-01 2025-01-31
   ```

3. **No Git Repository**:
   ```bash
   cd /path/to/your/repo
