import tempfile
import unittest
import io
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path
from file_organizer import organize


class FileOrganizerTests(unittest.TestCase):
    @staticmethod
    def snapshot(folder):
        """Record every relative path and file's contents to detect changes."""
        return {
            path.relative_to(folder).as_posix(): path.read_bytes() if path.is_file() else None
            for path in folder.rglob("*")
        }

    def test_preview_lists_destinations_and_preserves_entire_folder(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            for name in ("photo.JPG", "report.pdf", "data.csv", "unknown.xyz", "no_extension"):
                (folder / name).write_bytes(b"sample content")
            (folder / "nested").mkdir()
            (folder / "nested" / "private.txt").write_bytes(b"nested content")
            before = self.snapshot(folder)
            output = io.StringIO()
            with redirect_stdout(output):
                organize(folder)
            self.assertEqual(self.snapshot(folder), before)
            for line in (
                "photo.JPG  ->  Images/photo.JPG",
                "report.pdf  ->  Documents/report.pdf",
                "data.csv  ->  Spreadsheets/data.csv",
                "unknown.xyz  ->  Others/unknown.xyz",
                "no_extension  ->  Others/no_extension",
            ):
                self.assertIn(line, output.getvalue())
            self.assertIn("PREVIEW ONLY", output.getvalue())
            self.assertNotIn("private.txt", output.getvalue())

    def test_preview_predicts_duplicate_names_without_renaming(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "Images").mkdir()
            (folder / "Images" / "same.jpg").write_bytes(b"original")
            (folder / "same.jpg").write_bytes(b"new")
            (folder / "same (1).jpg").write_bytes(b"another")
            before = self.snapshot(folder)
            preview = io.StringIO()
            with redirect_stdout(preview):
                organize(folder)
            self.assertEqual(self.snapshot(folder), before)
            self.assertIn("same.jpg  ->  Images/same (2).jpg", preview.getvalue())
            applied = io.StringIO()
            with redirect_stdout(applied):
                organize(folder, apply=True)
            preview_moves = [line for line in preview.getvalue().splitlines() if "  ->  " in line]
            applied_moves = [line for line in applied.getvalue().splitlines() if "  ->  " in line]
            self.assertEqual(preview_moves, applied_moves)

    def test_command_line_preview_modes_leave_files_unchanged(self):
        script = Path(__file__).resolve().parents[1] / "file_organizer.py"
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "photo.jpg").write_bytes(b"sample")
            before = self.snapshot(folder)
            for flags in ([], ["--preview"]):
                with self.subTest(flags=flags):
                    result = subprocess.run(
                        [sys.executable, "-B", str(script), str(folder), *flags],
                        capture_output=True, text=True, check=False,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("photo.jpg  ->  Images/photo.jpg", result.stdout)
                    self.assertIn("PREVIEW ONLY", result.stdout)
                    self.assertEqual(self.snapshot(folder), before)
            result = subprocess.run(
                [sys.executable, "-B", str(script), str(folder), "--preview", "--apply"],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertEqual(self.snapshot(folder), before)

    def test_preview_empty_folder_creates_nothing(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            output = io.StringIO()
            with redirect_stdout(output):
                organize(folder)
            self.assertIn("No files found", output.getvalue())
            self.assertEqual(self.snapshot(folder), {})

    def test_preview_does_not_move(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "a.jpg").write_bytes(b"fake image")
            organize(folder, apply=False)
            self.assertTrue((folder / "a.jpg").exists())
            self.assertFalse((folder / "Images").exists())

    def test_apply_moves_files_and_skips_subfolders(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "a.jpg").write_bytes(b"fake image")
            (folder / "b.PDF").write_bytes(b"fake pdf")
            (folder / "nested").mkdir()
            (folder / "nested" / "c.mp4").write_bytes(b"fake video")
            organize(folder, apply=True)
            self.assertTrue((folder / "Images" / "a.jpg").exists())
            self.assertTrue((folder / "Documents" / "b.PDF").exists())
            self.assertTrue((folder / "nested" / "c.mp4").exists())

    def test_existing_filename_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "Images").mkdir()
            (folder / "Images" / "same.jpg").write_bytes(b"original")
            (folder / "same.jpg").write_bytes(b"new")
            organize(folder, apply=True)
            self.assertEqual((folder / "Images" / "same.jpg").read_bytes(), b"original")
            self.assertEqual((folder / "Images" / "same (1).jpg").read_bytes(), b"new")


if __name__ == "__main__":
    unittest.main()
