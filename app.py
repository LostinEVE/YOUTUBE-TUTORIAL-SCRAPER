"""Main application for YouTube Tutorial Scraper"""

import sys
import webbrowser
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import print as rprint

from youtube_scraper import YouTubeScraper
from database import TutorialDatabase
from config import PROGRAMMING_LANGUAGES, PROGRAMMING_SUBJECTS, MIN_VIDEO_DURATION_SECONDS


console = Console()


class TutorialApp:
    def __init__(self):
        self.db = TutorialDatabase()
        self.scraper = None

    def _init_scraper(self):
        """Initialize the YouTube scraper"""
        if self.scraper is None:
            try:
                self.scraper = YouTubeScraper()
            except ValueError as e:
                console.print(f"[red]Error: {e}[/red]")
                console.print(
                    "\n[yellow]Please create a .env file with your "
                    "YOUTUBE_API_KEY[/yellow]"
                )
                console.print(
                    "Get your API key from: "
                    "https://console.cloud.google.com/apis/credentials"
                )
                return False
        return True

    def display_menu(self):
        """Display the main menu"""
        console.print("\n")
        console.print(Panel.fit(
            "[bold cyan]YouTube Programming Tutorial Scraper[/bold cyan]",
            border_style="cyan"
        ))
        console.print()
        console.print("[1] 🔍 Scrape new tutorials")
        console.print("[2] 📚 Browse by programming language")
        console.print("[3] 📂 Browse by subject")
        console.print("[4] 📊 View statistics")
        console.print("[5] 🔎 Search tutorials")
        console.print("[6] ⭐ View favorites")
        console.print("[7] 📋 View all tutorials")
        console.print("[8] ⚙️  Settings")
        console.print("[0] 🚪 Exit")
        console.print()

    def scrape_tutorials(self):
        """Scrape new tutorials from YouTube"""
        if not self._init_scraper():
            return

        console.print("\n[bold]Scraping Options:[/bold]")
        console.print("[1] Scrape all categories")
        console.print("[2] Scrape specific language")
        console.print("[3] Scrape specific subject")
        console.print("[0] Back")

        choice = Prompt.ask("Select option", choices=["0", "1", "2", "3"])

        if choice == "0":
            return

        tutorials = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:

            if choice == "1":
                task = progress.add_task("Scraping...", total=100)

                def update_progress(current, total, message):
                    progress.update(
                        task,
                        completed=(current / total) * 100,
                        description=message
                    )

                if self.scraper:
                    tutorials = self.scraper.scrape_all_categories(
                        progress_callback=update_progress
                    )

            elif choice == "2":
                console.print("\n[bold]Available languages:[/bold]")
                for i, lang in enumerate(PROGRAMMING_LANGUAGES, 1):
                    console.print(f"  [{i}] {lang}")

                idx = Prompt.ask(
                    "Select language number",
                    default="1"
                )
                try:
                    language = PROGRAMMING_LANGUAGES[int(idx) - 1]
                    task = progress.add_task(
                        f"Searching {language}...",
                        total=100
                    )
                    if self.scraper:
                        tutorials = self.scraper.search_tutorials(
                            language=language)
                        progress.update(task, completed=100)
                except (ValueError, IndexError):
                    console.print("[red]Invalid selection[/red]")
                    return

            elif choice == "3":
                console.print("\n[bold]Available subjects:[/bold]")
                for i, subj in enumerate(PROGRAMMING_SUBJECTS, 1):
                    console.print(f"  [{i}] {subj}")

                idx = Prompt.ask(
                    "Select subject number",
                    default="1"
                )
                try:
                    subject = PROGRAMMING_SUBJECTS[int(idx) - 1]
                    task = progress.add_task(
                        f"Searching {subject}...",
                        total=100
                    )
                    if self.scraper:
                        tutorials = self.scraper.search_tutorials(subject=subject)
                        progress.update(task, completed=100)
                except (ValueError, IndexError):
                    console.print("[red]Invalid selection[/red]")
                    return

        # Save to database
        added = 0
        duplicates = 0
        for tutorial in tutorials:
            if self.db.add_tutorial(tutorial):
                added += 1
            else:
                duplicates += 1

        console.print(f"\n[green]✓ Added {added} new tutorials[/green]")
        if duplicates > 0:
            console.print(
                f"[yellow]  ({duplicates} duplicates skipped)[/yellow]")

    def browse_by_language(self):
        """Browse tutorials by programming language"""
        summary = self.db.get_categories_summary()

        if not summary['by_language']:
            console.print(
                "\n[yellow]No tutorials found. "
                "Try scraping some first![/yellow]"
            )
            return

        console.print("\n[bold]Tutorials by Language:[/bold]\n")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Language", style="cyan")
        table.add_column("Count", justify="right")

        languages = list(summary['by_language'].items())
        for i, (lang, count) in enumerate(languages, 1):
            table.add_row(str(i), lang, str(count))

        console.print(table)

        idx = Prompt.ask(
            "\nSelect language number to view (0 to go back)",
            default="0"
        )

        if idx == "0":
            return

        try:
            language = languages[int(idx) - 1][0]
            self._display_tutorials(
                self.db.get_tutorials_by_language(language),
                f"Tutorials for {language}"
            )
        except (ValueError, IndexError):
            console.print("[red]Invalid selection[/red]")

    def browse_by_subject(self):
        """Browse tutorials by subject"""
        summary = self.db.get_categories_summary()

        if not summary['by_subject']:
            console.print(
                "\n[yellow]No tutorials found. "
                "Try scraping some first![/yellow]"
            )
            return

        console.print("\n[bold]Tutorials by Subject:[/bold]\n")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Subject", style="cyan")
        table.add_column("Count", justify="right")

        subjects = list(summary['by_subject'].items())
        for i, (subj, count) in enumerate(subjects, 1):
            table.add_row(str(i), subj, str(count))

        console.print(table)

        idx = Prompt.ask(
            "\nSelect subject number to view (0 to go back)",
            default="0"
        )

        if idx == "0":
            return

        try:
            subject = subjects[int(idx) - 1][0]
            self._display_tutorials(
                self.db.get_tutorials_by_subject(subject),
                f"Tutorials for {subject}"
            )
        except (ValueError, IndexError):
            console.print("[red]Invalid selection[/red]")

    def view_statistics(self):
        """View tutorial statistics"""
        summary = self.db.get_categories_summary()

        console.print("\n")
        console.print(Panel.fit(
            f"[bold]📊 Tutorial Statistics[/bold]\n\n"
            f"Total Tutorials: [cyan]{summary['total']}[/cyan]\n"
            f"Languages: [cyan]{len(summary['by_language'])}[/cyan]\n"
            f"Subjects: [cyan]{len(summary['by_subject'])}[/cyan]",
            border_style="green"
        ))

        if summary['by_language']:
            console.print("\n[bold]Top Languages:[/bold]")
            for lang, count in list(summary['by_language'].items())[:5]:
                bar = "█" * min(count, 20)
                console.print(f"  {lang:15} {bar} {count}")

        if summary['by_subject']:
            console.print("\n[bold]Top Subjects:[/bold]")
            for subj, count in list(summary['by_subject'].items())[:5]:
                bar = "█" * min(count, 20)
                console.print(f"  {subj:20} {bar} {count}")

    def search_tutorials(self):
        """Search tutorials by keyword"""
        query = Prompt.ask("\nEnter search query")

        if not query:
            return

        tutorials = self.db.search_tutorials(query)
        self._display_tutorials(tutorials, f"Search results for '{query}'")

    def view_favorites(self):
        """View favorite tutorials"""
        tutorials = [
            t for t in self.db.get_all_tutorials()
            if t.get('is_favorite')
        ]
        self._display_tutorials(tutorials, "Favorite Tutorials")

    def view_all_tutorials(self):
        """View all tutorials"""
        tutorials = self.db.get_all_tutorials()
        self._display_tutorials(tutorials, "All Tutorials")

    def _display_tutorials(self, tutorials: list, title: str):
        """Display a list of tutorials in a table"""
        if not tutorials:
            console.print(
                f"\n[yellow]No tutorials found for: {title}[/yellow]")
            return

        console.print(f"\n[bold]{title}[/bold] ({len(tutorials)} videos)\n")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Title", max_width=50)
        table.add_column("Channel", style="cyan", max_width=20)
        table.add_column("Views", justify="right")
        table.add_column("Duration", justify="right")
        table.add_column("Lang/Subject", style="green")

        for i, t in enumerate(tutorials[:25], 1):  # Show max 25
            duration_mins = t.get('duration_seconds', 0) // 60
            views = t.get('view_count', 0)
            views_str = f"{views:,}" if views < 1000000 else f"{views/1000000:.1f}M"

            lang_subj = t.get('programming_language') or t.get(
                'subject') or '-'

            fav = "⭐ " if t.get('is_favorite') else ""
            watched = "✓ " if t.get('is_watched') else ""

            table.add_row(
                str(i),
                f"{fav}{watched}{t.get('title', 'Unknown')[:47]}",
                t.get('channel_name', 'Unknown')[:18],
                views_str,
                f"{duration_mins}m",
                lang_subj[:15]
            )

        console.print(table)

        if len(tutorials) > 25:
            console.print(
                f"\n[dim](Showing 25 of {len(tutorials)} tutorials)[/dim]"
            )

        # Video actions
        console.print("\n[dim]Enter video # to open, 'f#' to favorite, "
                      "'w#' to mark watched, or 0 to go back[/dim]")

        action = Prompt.ask("Action", default="0")

        if action == "0":
            return

        try:
            if action.startswith('f'):
                idx = int(action[1:]) - 1
                video_id = tutorials[idx]['video_id']
                self.db.mark_favorite(video_id)
                console.print("[green]✓ Added to favorites[/green]")
            elif action.startswith('w'):
                idx = int(action[1:]) - 1
                video_id = tutorials[idx]['video_id']
                self.db.mark_watched(video_id)
                console.print("[green]✓ Marked as watched[/green]")
            else:
                idx = int(action) - 1
                url = tutorials[idx]['video_url']
                console.print(f"\n[cyan]Opening: {url}[/cyan]")
                webbrowser.open(url)
        except (ValueError, IndexError):
            console.print("[red]Invalid selection[/red]")

    def show_settings(self):
        """Show and modify settings"""
        console.print("\n[bold]Current Settings:[/bold]\n")
        console.print(f"  Languages configured: {len(PROGRAMMING_LANGUAGES)}")
        console.print(f"  Subjects configured: {len(PROGRAMMING_SUBJECTS)}")
        console.print(f"  Min video duration: {MIN_VIDEO_DURATION_SECONDS}s")
        console.print(
            f"\n[dim]Edit config.py to modify these settings[/dim]"
        )

    def run(self):
        """Run the main application loop"""
        console.print(
            "\n[bold green]Welcome to YouTube Tutorial Scraper![/bold green]"
        )

        while True:
            self.display_menu()
            choice = Prompt.ask(
                "Select option",
                choices=["0", "1", "2", "3", "4", "5", "6", "7", "8"],
                default="0"
            )

            if choice == "0":
                console.print("\n[cyan]Goodbye! Happy learning! 📚[/cyan]\n")
                break
            elif choice == "1":
                self.scrape_tutorials()
            elif choice == "2":
                self.browse_by_language()
            elif choice == "3":
                self.browse_by_subject()
            elif choice == "4":
                self.view_statistics()
            elif choice == "5":
                self.search_tutorials()
            elif choice == "6":
                self.view_favorites()
            elif choice == "7":
                self.view_all_tutorials()
            elif choice == "8":
                self.show_settings()


def main():
    try:
        app = TutorialApp()
        app.run()
    except KeyboardInterrupt:
        console.print("\n\n[cyan]Goodbye![/cyan]\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
