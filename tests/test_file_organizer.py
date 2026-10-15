import tempfile
import unittest
from pathlib import Path
from file_organizer import organize


class FileOrganizerTests(unittest.TestCase):
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
