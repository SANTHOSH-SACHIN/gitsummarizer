"""
Command-line interface for GitSummarizer.
"""

import argparse
import sys
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm

from . import config
from . import git_utils
from .summarizer import Summarizer
from .models import PROVIDERS

# Console for rich output
console = Console()


def setup_command():
    """Set up GitSummarizer configuration."""
    console.print("[bold green]GitSummarizer Setup[/bold green]")

    # Get provider
    providers = list(PROVIDERS.keys())
    provider_choices = ", ".join(providers[:-1]) + f", or {providers[-1]}"
    console.print(f"[yellow]Available LLM providers: {provider_choices}[/yellow]")

    provider = Prompt.ask(
        "Select LLM provider",
        choices=providers,
        default=config.get_current_provider()
    )

    # Set as current provider
    config.set_current_provider(provider)

    # Handle API key for non-Ollama providers
    if provider != "ollama":
        console.print(f"[yellow]Please provide your {provider.capitalize()} API key:[/yellow]")
        console.print("[dim](API key will be stored locally in ~/.config/gitsumm/config.json)[/dim]")

        # Check if we already have an API key
        existing_key = config.get_provider_api_key(provider)
        if existing_key:
            if not Confirm.ask("API key already exists. Update it?", default=False):
                console.print("[green]Keeping existing API key.[/green]")
            else:
                api_key = Prompt.ask("API Key", password=True)
                config.set_provider_api_key(provider, api_key)
                console.print("[green]API key updated.[/green]")
        else:
            api_key = Prompt.ask("API Key", password=True)
            config.set_provider_api_key(provider, api_key)
            console.print("[green]API key saved.[/green]")
    else:
        console.print("[yellow]Using local Ollama instance (make sure Ollama is installed and running)[/yellow]")

    # Set model for provider
    current_model = config.get_model_for_provider(provider)
    model = Prompt.ask(
        f"Model for {provider}",
        default=current_model
    )
    config.set_model_for_provider(provider, model)

    console.print("[bold green]✓ Setup complete![/bold green]")
    console.print(f"Using {provider} with model {model}")


def recent_command(args):
    """Summarize recent commits."""
    with console.status("[bold green]Analyzing recent commits...[/bold green]"):
        summarizer = Summarizer()
        result = summarizer.summarize_recent_commits(args.num, args.branch)

    console.print(Panel(Markdown(result), title="Git Summary", border_style="green"))


def commit_command(args):
    """Summarize a specific commit."""
    with console.status(f"[bold green]Analyzing commit {args.commit_hash}...[/bold green]"):
        summarizer = Summarizer()
        result = summarizer.summarize_commit(args.commit_hash)

    console.print(Panel(Markdown(result), title=f"Commit {args.commit_hash} Summary", border_style="green"))


def compare_command(args):
    """Compare and summarize branches."""
    with console.status(f"[bold green]Comparing {args.base_branch} and {args.compare_branch}...[/bold green]"):
        summarizer = Summarizer()
        result = summarizer.compare_branches(args.base_branch, args.compare_branch)

    console.print(Panel(
        Markdown(result),
        title=f"Comparison: {args.base_branch} → {args.compare_branch}",
        border_style="green"
    ))


def time_range_command(args):
    """Summarize commits in a time range."""
    with console.status(f"[bold green]Analyzing commits between {args.start_date} and {args.end_date}...[/bold green]"):
        summarizer = Summarizer()
        result = summarizer.summarize_time_range(args.start_date, args.end_date, args.branch)

    console.print(Panel(
        Markdown(result),
        title=f"Summary: {args.start_date} to {args.end_date}",
        border_style="green"
    ))


def template_command(args):
    """Manage prompt templates."""
    if args.list:
        # List available templates
        config_data = config.load_config()
        templates = config_data.get("prompt_templates", {})
        active = config.get_active_template_name()

        console.print("[bold green]Available Templates:[/bold green]")
        console.print(f"→ [bold]default[/bold] {'(active)' if active == 'default' else ''}")
        for name in templates:
            if name != "default":
                console.print(f"  {name} {'(active)' if name == active else ''}")
        return

    if args.set:
        # Set active template
        config.set_active_template(args.set)
        console.print(f"[bold green]✓ Active template set to {args.set}[/bold green]")
        return

    if args.name and args.content:
        # Add new template
        config.set_prompt_template(args.name, args.content)
        console.print(f"[bold green]✓ Added template: {args.name}[/bold green]")
        return

def provider_command(args):
    """Change LLM provider."""
    if args.list:
        # List available providers
        providers = list(PROVIDERS.keys())
        current = config.get_current_provider()

        console.print("[bold green]Available LLM Providers:[/bold green]")
        for provider in providers:
            if provider == current:
                console.print(f"→ [bold]{provider}[/bold] (current)")
            else:
                console.print(f"  {provider}")

        return

    if args.provider:
        # Check if provider is valid
        if args.provider not in PROVIDERS:
            console.print(f"[bold red]Error:[/bold red] Unknown provider: {args.provider}")
            console.print(f"Available providers: {', '.join(PROVIDERS.keys())}")
            return

        # Set provider
        config.set_current_provider(args.provider)
        console.print(f"[bold green]✓ Provider set to {args.provider}[/bold green]")

        # Check if we have an API key
        if args.provider != "ollama" and not config.get_provider_api_key(args.provider):
            console.print("[yellow]No API key found for this provider. Run 'gitsumm setup' to configure.[/yellow]")


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="GitSummarizer: Human-readable summaries of git changes"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Setup command
    subparsers.add_parser("setup", help="Configure GitSummarizer")

    # Recent commits command
    recent_parser = subparsers.add_parser("recent", help="Summarize recent commits")
    recent_parser.add_argument("-n", "--num", type=int,
                              default=config.get_default_recent_commits(),
                              help=f"Number of commits to summarize (default: {config.get_default_recent_commits()})")
    recent_parser.add_argument("-b", "--branch", type=str, help="Branch to summarize commits from")

    # Commit command
    commit_parser = subparsers.add_parser("commit", help="Summarize a specific commit")
    commit_parser.add_argument("commit_hash", type=str, help="Commit hash to summarize")

    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare and summarize two branches")
    compare_parser.add_argument("base_branch", type=str,
                              default=config.get_default_compare_branch(),
                              help=f"Base branch (default: {config.get_default_compare_branch()})")
    compare_parser.add_argument("compare_branch", type=str, help="Branch to compare against base")

    # Defaults command
    defaults_parser = subparsers.add_parser("defaults", help="Configure default settings")
    defaults_parser.add_argument("--recent", type=int,
                               help=f"Set default number of recent commits (current: {config.get_default_recent_commits()})")
    defaults_parser.add_argument("--branch", type=str,
                               help=f"Set default comparison branch (current: {config.get_default_compare_branch()})")
    defaults_parser.add_argument("--format", type=str, choices=["text", "json", "markdown"],
                               help=f"Set default output format (current: {config.get_default_output_format()})")

    # Time range command
    time_parser = subparsers.add_parser("time", help="Summarize commits in a date range")
    time_parser.add_argument("start_date", type=str, help="Start date (YYYY-MM-DD)")
    time_parser.add_argument("end_date", type=str, help="End date (YYYY-MM-DD)")
    time_parser.add_argument("-b", "--branch", type=str, help="Branch to summarize commits from")
    time_parser.set_defaults(func=time_range_command)

    # Template command
    template_parser = subparsers.add_parser("template", help="Manage prompt templates")
    template_parser.add_argument("-l", "--list", action="store_true", help="List available templates")
    template_parser.add_argument("-s", "--set", type=str, help="Set active template")
    template_parser.add_argument("-n", "--name", type=str, help="Name for new template")
    template_parser.add_argument("-c", "--content", type=str, help="Content for new template")

    # Provider command
    provider_parser = subparsers.add_parser("provider", help="List or set LLM provider")
    provider_parser.add_argument("-l", "--list", action="store_true", help="List available providers")
    provider_parser.add_argument("provider", nargs="?", help="Provider to use")

    args = parser.parse_args()

    # Check if running in a git repository for commands that need it
    if args.command in ["recent", "commit", "compare", "time"]:
        try:
            git_utils.get_repo()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
            sys.exit(1)

    # Execute command
    if args.command == "setup":
        setup_command()
    elif args.command == "recent":
        recent_command(args)
    elif args.command == "commit":
        commit_command(args)
    elif args.command == "compare":
        compare_command(args)
    elif args.command == "time":
        time_range_command(args)
    elif args.command == "provider":
        provider_command(args)
    elif args.command == "template":
        template_command(args)
    elif args.command == "defaults":
        if args.recent:
            config.set_default_recent_commits(args.recent)
            console.print(f"[green]Default recent commits set to {args.recent}[/green]")
        if args.branch:
            config.set_default_compare_branch(args.branch)
            console.print(f"[green]Default comparison branch set to {args.branch}[/green]")
        if args.format:
            config.set_default_output_format(args.format)
            console.print(f"[green]Default output format set to {args.format}[/green]")

        if not any([args.recent, args.branch, args.format]):
            console.print("[yellow]No defaults specified. Use --recent, --branch or --format to set defaults.[/yellow]")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
