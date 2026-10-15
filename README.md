# Python File Organizer

A lightweight command-line utility that organizes files into folders based on their extensions. Built with Python's standard library, it previews proposed changes by default and moves files only when explicitly requested.

## Features

- Organizes files into nine predefined categories, with an `Others` category for unmatched extensions.
- Runs in preview mode by default; no files are moved without `--apply`.
- Prevents filename collisions by adding a numeric suffix instead of overwriting an existing file.
- Processes only files directly inside the selected folder; existing subfolders are not traversed.
- Skips symbolic links.
- Works offline, without third-party dependencies.
- Includes automated tests and sample files.

## Requirements

- Python 3.9 or later
- Windows, macOS, or Linux

No additional packages are required.

## Project Structure

```text
python-file-organizer/
├── file_organizer.py
├── README.md
├── INSTRUCTIONS.md
├── .gitignore
├── sample_files/
│   ├── example.txt
│   ├── notes.csv
│   └── picture.jpg
└── tests/
    └── test_file_organizer.py
```

After a sample run with `--apply`, the sample files are moved into category subfolders.

## Usage

Run all commands from the project root directory.

### Preview sample files

```bash
python file_organizer.py sample_files
```

This displays the proposed destinations without changing any files.

### Organize sample files

```bash
python file_organizer.py sample_files --apply
```

### Preview another folder

**Windows PowerShell:**

```powershell
python file_organizer.py "$HOME\Downloads"
```

**macOS / Linux:**

```bash
python file_organizer.py "$HOME/Downloads"
```

### Apply changes to another folder

Add `--apply` after reviewing the preview:

```powershell
python file_organizer.py "$HOME\Downloads" --apply
```

Paths containing spaces should be enclosed in quotation marks.

### Command-line options

```text
usage: file_organizer.py [-h] [--apply] folder

positional arguments:
  folder     Directory containing the files to organize

options:
  -h, --help  Show help and exit
  --apply     Move files into their destination folders
```

## File Categories

| Destination | Supported extensions |
| --- | --- |
| Images | `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.bmp`, `.svg`, `.heic`, `.tiff` |
| Documents | `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`, `.md` |
| Spreadsheets | `.xls`, `.xlsx`, `.csv`, `.ods` |
| Presentations | `.ppt`, `.pptx`, `.odp` |
| Videos | `.mp4`, `.mov`, `.avi`, `.mkv`, `.wmv`, `.webm`, `.m4v` |
| Audio | `.mp3`, `.wav`, `.aac`, `.flac`, `.ogg`, `.m4a` |
| Archives | `.zip`, `.rar`, `.7z`, `.tar`, `.gz` |
| Code | `.py`, `.js`, `.ts`, `.html`, `.css`, `.json`, `.java`, `.cpp`, `.c`, `.sql` |
| Installers | `.exe`, `.msi`, `.apk`, `.dmg`, `.deb` |
| Others | Unrecognized extensions and files without an extension |

Extension matching is case-insensitive. Categories can be customized by editing the `CATEGORIES` dictionary in `file_organizer.py`.

## Example

Given a folder containing:

```text
MyFiles/
├── photo.jpg
├── report.pdf
├── movie.mp4
└── data.csv
```

After running the organizer with `--apply`:

```text
MyFiles/
├── Images/
│   └── photo.jpg
├── Documents/
│   └── report.pdf
├── Videos/
│   └── movie.mp4
└── Spreadsheets/
    └── data.csv
```

If the destination already contains a file with the same name, the organizer uses a new name such as `photo (1).jpg` rather than overwriting the existing file.

## Safety and Limitations

- Preview mode is the default. Files are only moved when `--apply` is specified.
- The organizer moves files; it does not copy or delete them.
- Only top-level regular files are processed. Subdirectories and symbolic links are skipped.
- There is currently no automatic undo or rollback mechanism.
- Moving files can break applications, shortcuts, or workflows that depend on their original paths.
- Avoid running the organizer on operating-system folders, application installations, active development projects, or other directories where file locations are important.
- Back up important files and inspect the preview before applying changes.
- The tool processes local files and does not transmit data over the internet.

## Testing

The project uses Python's built-in `unittest` framework. Tests use temporary directories rather than personal files.

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

The test suite covers preview mode, file moving and subfolder preservation, and duplicate-name handling.

## Development

The application uses the following Python standard-library modules:

- `argparse` for command-line arguments
- `pathlib` for filesystem paths
- `shutil` for moving files
- `collections.Counter` for category totals

No package installation or external API is required.

## Roadmap

Possible future enhancements include:

- Desktop graphical interface using Tkinter
- Organization history and log files
- Copy mode as an alternative to moving files
- Sorting by date or file size
- Undo support
- Duplicate-content detection

## License

No open-source license file is included in this project. Reuse and distribution terms should be defined in a separate `LICENSE` file before publishing the project under a specific license.
