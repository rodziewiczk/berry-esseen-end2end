"""Portable V14 producer fixtures; no archive, mathematical oracle or native run."""
import ast
from copy import deepcopy
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from be_replay import prepare_v14_portable as portable


class PortableV14Tests(unittest.TestCase):
    def test_frozen_source_is_unchanged_and_transform_is_one_checked_edit(self):
        original = portable.FROZEN_SOURCE.read_bytes()
        self.assertEqual(hashlib.sha256(original).hexdigest(), portable.FROZEN_SHA256)
        expected = original.decode("utf-8").replace(portable.OLD_DESTINATION, portable.NEW_DESTINATION, 1)
        self.assertEqual(portable.transformed_source(), expected)
        self.assertEqual(portable.FROZEN_SOURCE.read_bytes(), original)

    def test_entire_producer_ast_changes_only_the_reference_output_destination(self):
        original = ast.parse(portable.FROZEN_SOURCE.read_text(encoding="utf-8"))
        revised = ast.parse(portable.transformed_source())
        normalized = deepcopy(revised)
        changed = []
        for node in ast.walk(normalized):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "add"
                    and node.args and isinstance(node.args[0], ast.BinOp)
                    and isinstance(node.args[0].left, ast.Constant)
                    and node.args[0].left.value == "ORIGINAL_V12_"
                    and isinstance(node.args[0].right, ast.IfExp)):
                conditional = node.args[0].right
                destination = ast.Expression(body=deepcopy(node.args[0]))
                ast.fix_missing_locations(destination)
                for name, expected in (("contract.json", "ORIGINAL_V12_CONTRACT.json"),
                                       ("count_protocol.py", "ORIGINAL_V12_count_protocol.py"),
                                       ("KERNEL_COPY_MANIFEST.json", "ORIGINAL_V12_KERNEL_COPY_MANIFEST.json")):
                    self.assertEqual(eval(compile(destination, "filename-fixture", "eval"), {"name": name}), expected)
                self.assertIsInstance(conditional.orelse, ast.Name)
                self.assertEqual(conditional.orelse.id, "name")
                node.args[0].right = ast.Name(id="name", ctx=ast.Load())
                changed.append(node)
        self.assertEqual(len(changed), 1)
        self.assertEqual(ast.dump(normalized), ast.dump(original))

    def test_native_protocol_derivation_and_all_other_functions_are_identical(self):
        original = ast.parse(portable.FROZEN_SOURCE.read_text(encoding="utf-8"))
        revised = ast.parse(portable.transformed_source())
        before = {node.name: node for node in original.body if isinstance(node, ast.FunctionDef)}
        after = {node.name: node for node in revised.body if isinstance(node, ast.FunctionDef)}
        self.assertEqual(before.keys(), after.keys())
        for name in before:
            if name != "main":
                self.assertEqual(ast.dump(before[name]), ast.dump(after[name]), name)
        self.assertEqual(ast.dump(before["derive_protocol"]), ast.dump(after["derive_protocol"]))
        self.assertIn("original=json.loads((HERE/'ORIGINAL_V12_CONTRACT.json').read_text()",
                      portable.transformed_source())

    def test_preparer_self_hash_binds_the_adapter_instead_of_the_legacy_vendor(self):
        with patch("builtins.exec") as execute:
            portable.main()
        execute.assert_called_once()
        code, namespace = execute.call_args.args
        self.assertEqual(namespace["__name__"], "__main__")
        self.assertEqual(namespace["__file__"], str(Path(portable.__file__).resolve()))
        self.assertEqual(code.co_filename, namespace["__file__"])
        self.assertNotEqual(Path(namespace["__file__"]), portable.FROZEN_SOURCE)

    def test_corrupted_vendor_source_is_rejected_before_execution(self):
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / "modified.py"
            path.write_bytes(portable.FROZEN_SOURCE.read_bytes() + b"\n# modified\n")
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                portable.transformed_source(path)


if __name__ == "__main__":
    unittest.main()
