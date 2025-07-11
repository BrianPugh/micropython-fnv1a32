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

    def test_file_with_custom_bytearray_buffer(self):
        mv = bytearray(4096)
        with TemporaryDirectory() as tmp_dir:
            filename = Path(tmp_dir) / "test_file"
            filename.write_text("foobar")
            with filename.open() as f:
                self.assertEqual(fnv1a32(f, buffer=mv), 0xBF9CF968)
        self.assertEqual(mv[:6], b"foobar")

    def test_file_with_custom_memoryview_buffer(self):
        mv = memoryview(bytearray(4096))
        with TemporaryDirectory() as tmp_dir:
            filename = Path(tmp_dir) / "test_file"
            filename.write_text("foobar")
            with filename.open() as f:
                self.assertEqual(fnv1a32(f, buffer=mv), 0xBF9CF968)
        self.assertEqual(mv[:6], b"foobar")

    def test_file_with_invalid_buffer(self):
        mv = "this is not a writable buffer."
        with TemporaryDirectory() as tmp_dir:
            filename = Path(tmp_dir) / "test_file"
            filename.write_text("foobar")
            with filename.open() as f:
                with self.assertRaises(TypeError):
                    fnv1a32(f, buffer=mv)
