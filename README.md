# Python File Organizer 📁

A beginner-friendly **Python file organizer** for Windows, macOS, and Linux. Sort loose files by their extensions into category folders such as `Images`, `Documents`, `Videos`, `Audio`, and more.

**Safe by default:** the script shows a preview first and does not move files unless you add `--apply`.

## Requirements

- Python 3.9 or newer (recommended)
- No additional packages or `pip install` needed; uses the Python standard library.

## Quick start (VS Code terminal)

1. Extract the ZIP. Open the extracted `python-file-organizer` folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Check Python is installed:

   ```powershell
   python --version
   ```

4. Try it with the included sample files **without moving anything**:

   ```powershell
   python file_organizer.py sample_files
   ```

5. Actually organize the sample files:

   ```powershell
   python file_organizer.py sample_files --apply
   ```

6. Open `sample_files/` in the VS Code Explorer. You will see category folders.

If `python` doesn't work on Windows, try `py` instead (for example, `py file_organizer.py sample_files`).

## Organize your own folder

**PREVIEW first:**

```powershell
python file_organizer.py "C:\Users\YOUR_NAME\Downloads"
```

**MOVE files only when preview looks right:**

```powershell
python file_organizer.py "C:\Users\YOUR_NAME\Downloads" --apply
```

Replace `YOUR_NAME` with your Windows username. Or use any folder you have permission to access. Put paths containing spaces in double quotes.

## Categories

| Destination folder | Examples |
| --- | --- |
| Images | jpg, jpeg, png, gif, webp, heic |
| Documents | pdf, docx, txt, md |
| Spreadsheets | xlsx, csv, ods |
| Presentations | pptx, ppt |
| Videos | mp4, mov, mkv, webm |
| Audio | mp3, wav, m4a, flac |
| Archives | zip, rar, 7z, tar, gz |
| Code | py, js, html, css, sql, json |
| Installers | exe, msi, apk, dmg |
| Others | Unknown extensions, or files without extensions |

Add more extensions by editing the `CATEGORIES` dictionary at the top of `file_organizer.py`.

## How it behaves (important)

- **Preview is default:** no changes without `--apply`.
- **Moves, not copies:** with `--apply`, original files are moved into new subfolders.
- **Does not delete files.** There is no automatic undo, so test on copies of important files first.
- **Does not inspect subfolders:** only files directly inside the folder you specify are processed. Existing folders are left alone.
- **Name conflicts:** if `Images/photo.jpg` exists, another `photo.jpg` will become `photo (1).jpg` (or next available number).
- **Symbolic links are skipped.**
- **No internet required** and nothing is uploaded.
- **Do not point it at** operating-system, application, or active project directories. Start with the included samples or a separate test folder.
- **Note:** categorized files already in subfolders stay there; rerunning the command only checks the selected folder's top-level files.

## Example output

```text
Folder: C:\Users\YOUR_NAME\Downloads
Mode: PREVIEW ONLY (nothing will change)
photo.jpg  ->  Images/photo.jpg
report.pdf  ->  Documents/report.pdf
movie.mp4  ->  Videos/movie.mp4

Summary: Documents: 1, Images: 1, Videos: 1
Preview complete. Add --apply to move files.
```

## Project structure

```text
python-file-organizer/
├── file_organizer.py     # Main application
├── README.md             # Guide and usage instructions
├── INSTRUCTIONS.md       # Extra beginner-friendly how-to
├── .gitignore            # Files Git should ignore
├── tests/
│   └── test_file_organizer.py
└── sample_files/         # Tiny test files; safe to reorganize
    ├── example.txt
    ├── notes.csv
    └── picture.jpg
```

## Run automated tests

```powershell
python -m unittest discover -s tests -v
```

Tests use temporary folders and won't move your personal files.

## GitHub

Your project is ready to push to GitHub. `.gitignore` excludes Python cache, virtual environments, and locally generated categorized sample folders. Commit source, documentation, tests, and the original sample files; avoid committing real personal files.

## Next features to learn

Try adding a GUI using Tkinter, a log file, a `--copy` option, sorting by dates, and an undo feature.

MIT-style learning use: adapt for your own projects. No external libraries needed.
