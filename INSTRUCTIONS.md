# How to use this ZIP — simple instructions

**Goal:** Put mixed files in one folder, run a command, and sort them into `Images`, `Documents`, `Videos`, etc.

1. **Unzip** `python-file-organizer.zip`.
2. **Open** the extracted `python-file-organizer` folder in VS Code.
3. **Open Terminal** inside VS Code.
4. **Check Python:** `python --version`.
5. **Preview the example files:** `python file_organizer.py sample_files`.
6. **Actually sort the example files:** `python file_organizer.py sample_files --apply`.
7. Check the `sample_files` folder. Files have moved into category folders.

## Sort a real folder on Windows

Preview (makes no changes):

```powershell
python file_organizer.py "C:\Users\YOUR_NAME\Downloads"
```

Move files after inspecting preview:

```powershell
python file_organizer.py "C:\Users\YOUR_NAME\Downloads" --apply
```

Use your real Windows username or a different folder path. Quotation marks are important for paths with spaces.

**Remember:** No `--apply` = preview only. With `--apply` = actual file movement. Files are not deleted, but there is no undo button. Try the included samples first. It does not touch nested folders.

## If a command fails

- If `python` isn't recognized on Windows, replace `python` with `py`.
- If it says **Not an existing folder**, check the folder path.
- If it says **Permission denied**, test in a normal personal test folder, not a system folder.

## Read the full details

See [README.md](README.md) for categories, safety notes, tests, project layout, and further ideas.
