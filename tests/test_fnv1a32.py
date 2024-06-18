from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from fnv1a32 import fnv1a32


class TestFnv(unittest.TestCase):
    def test_bytes(self):
        self.assertEqual(fnv1a32("foobar"), 0xBF9CF968)

    def test_file(self):
        with TemporaryDirectory() as tmp_dir:
            filename = Path(tmp_dir) / "test_file"
            filename.write_text("foobar")
            with filename.open() as f:
                self.assertEqual(fnv1a32(f), 0xBF9CF968)
