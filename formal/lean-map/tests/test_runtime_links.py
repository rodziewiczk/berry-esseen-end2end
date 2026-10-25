"""The Unix runtime inventory pins real link chains, not just their names."""
import os
from pathlib import Path
import tempfile
import unittest

from be import count_native as native


@unittest.skipUnless(os.name == "posix", "Native Unix link operations are tested on the Linux pilot")
class RuntimeLinkTests(unittest.TestCase):
    def test_relative_chain_and_target_mutation_change_profile_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root / "target.py"
            target.write_bytes(b"original\n")
            (root / "middle.py").symlink_to("target.py")
            link = root / "entry.py"
            link.symlink_to("middle.py")
            files, links = {}, {}
            native._runtime_file(link, "test/entry.py", files, links)
            self.assertEqual(files["test/entry.py"], native.sha(b"original\n"))
            self.assertEqual([r["literal_target"] for r in links["test/entry.py"]["chain"]],
                             ["middle.py", "target.py"])
            self.assertEqual(links["test/entry.py"]["resolved_path"], str(target.resolve()))
            target.write_bytes(b"changed\n")
            changed_files, changed_links = {}, {}
            native._runtime_file(link, "test/entry.py", changed_files, changed_links)
            self.assertNotEqual(files, changed_files)
            self.assertNotEqual(links, changed_links)

    def test_broken_cycle_and_directory_targets_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "broken.py").symlink_to("missing.py")
            (root / "a.py").symlink_to("b.py")
            (root / "b.py").symlink_to("a.py")
            (root / "directory.py").symlink_to(root, target_is_directory=True)
            for name in ("broken.py", "a.py", "directory.py"):
                with self.subTest(name=name), self.assertRaises(native.CountError):
                    native._runtime_file(root / name, name, {}, {})

    def test_directory_alias_in_input_or_link_target_is_not_silently_followed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            real = root / "real"
            real.mkdir()
            (real / "value.py").write_bytes(b"value\n")
            alias = root / "alias"
            alias.symlink_to(real, target_is_directory=True)
            (root / "entry.py").symlink_to("alias/value.py")
            for path in (alias / "value.py", root / "entry.py"):
                with self.subTest(path=path), self.assertRaises(native.CountError) as caught:
                    native._runtime_file(path, "entry", {}, {})
                self.assertEqual(caught.exception.code, "runtime_directory_link")


if __name__ == "__main__":
    unittest.main()
