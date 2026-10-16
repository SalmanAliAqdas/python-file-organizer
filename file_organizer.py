"""Safely organize files in a folder by file type. Standard library only."""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import shutil

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".heic", ".tiff"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"},
    "Spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
    "Presentations": {".ppt", ".pptx", ".odp"},
    "Videos": {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".webm", ".m4v"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".json", ".java", ".cpp", ".c", ".sql"},
    "Installers": {".exe", ".msi", ".apk", ".dmg", ".deb"},
}


def category_for(file: Path) -> str:
    for category, extensions in CATEGORIES.items():
        if file.suffix.lower() in extensions:
            return category
    return "Others"


def unique_destination(folder: Path, filename: str, reserved: set[Path]) -> Path:
    original = Path(filename)
    candidate = folder / filename
    number = 1
    while candidate.exists() or candidate in reserved:
        candidate = folder / f"{original.stem} ({number}){original.suffix}"
        number += 1
    reserved.add(candidate)
    return candidate


def organize(folder: Path, apply: bool = False) -> None:
    """Show planned moves without changing files, unless apply is True."""
    folder = folder.expanduser().resolve()
    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"Not an existing folder: {folder}")
    # Only organize files directly inside target folder, not subfolders.
    files = sorted((p for p in folder.iterdir() if p.is_file() and not p.is_symlink()), key=lambda p: p.name.lower())
    reserved: set[Path] = set()
    counts: Counter[str] = Counter()
    print(f"Folder: {folder}")
    print("Mode:", "MOVE FILES" if apply else "PREVIEW ONLY (nothing will change)")
    if not files:
        print("No files found at the top level of this folder.")
        return
    for source in files:
        category = category_for(source)
        destination = unique_destination(folder / category, source.name, reserved)
        print(f"{source.name}  ->  {category}/{destination.name}")
        if apply:
            destination.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.move(str(source), str(destination))
            except OSError as exc:
                print(f"  ERROR: Could not move {source.name}: {exc}")
                continue
        counts[category] += 1
    print("\nSummary:", ", ".join(f"{category}: {count}" for category, count in sorted(counts.items())))
    print("Completed." if apply else "Preview complete. Add --apply to move files.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sort files into folders by type. Previews by default.")
    parser.add_argument("folder", type=Path, help="Folder containing files to organize; put paths with spaces in quotes")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--preview", action="store_true", help="Preview destinations without changing files (default)")
    mode.add_argument("--apply", action="store_true", help="Actually move files (otherwise previews only)")
    args = parser.parse_args()
    try:
        organize(args.folder, args.apply)
    except (ValueError, PermissionError, OSError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
