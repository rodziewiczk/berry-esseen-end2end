"""Notebook35 generation only; original mathematics is never imported."""
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("n5_remaining_notebook_builder",ROOT/"tools/make_n5_remaining_notebook.py")
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)


class Notebook35(unittest.TestCase):
    def test_full_fixed_batch_scoped_progress_and_cache(self):
        doc=builder.build("a"*40);text="\n".join("".join(c["source"])for c in doc["cells"])
        self.assertEqual(doc["metadata"]["colab"]["name"],"35_n5_complete_remaining.ipynb")
        for word in("all326","all295","all12","all15","1,200","75,178","every20 seconds","every60 seconds",
                     "three separate support-corruption","No full n5","per-process CPU","sampled"):
            self.assertIn(word,text)
        self.assertIn("run_colab(durable_root=DURABLE, backup_interval=60)",text)
        self.assertIn('CODE_COMMIT = "'+"a"*40+'"',text)
        self.assertIn("test_n5_remaining*.py",text)
        for cell in doc["cells"]:
            if cell["cell_type"]=="code":compile("".join(cell["source"]),"notebook35","exec")
    def test_reject_mutable_or_placeholder_pin_and_lf_writer(self):
        for pin in("main","0"*40,"a"*39,"A"*40):
            with self.assertRaises(ValueError):builder.build(pin)
        self.assertIn("path.write_bytes",Path(builder.__file__).read_text())


if __name__=="__main__":unittest.main()
