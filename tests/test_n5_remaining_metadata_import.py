"""Notebook-parent metadata imports and exact prior-cache compatibility only."""
from pathlib import Path
import importlib,sys,tempfile,unittest
from unittest.mock import patch
from be_replay import n5_remaining_sources as src,n5_remaining_evidence as ev

class MetadataImport(unittest.TestCase):
    def test_non_B_notebook_parent_never_creates_vendor_bytecode_and_restores_flag(self):
        names=('c5_counts','c5_inputs','c5_high_one','c5_acquisition_plan','c5_initial_one',
               'c5_resources_arithmetic','c5_resource_accept_port','stable_guard','supervised')
        saved={name:sys.modules.get(name)for name in names}
        try:
            for name in names:sys.modules.pop(name,None)
            with tempfile.TemporaryDirectory(dir=src.ROOT.parent)as tmp:
                directory=Path(tmp)/'reproduction/all_indices';directory.mkdir(parents=True)
                (directory/'c5_counts.py').write_text('import sys\nassert sys.dont_write_bytecode is True\nVALUE=7\n')
                (directory/'c5_acquisition_plan.py').write_text('import sys\nassert sys.dont_write_bytecode is True\nfrom c5_counts import VALUE\n')
                with patch.object(src,'VENDOR',Path(tmp)),patch.object(sys,'dont_write_bytecode',False):
                    module=ev.metadata_module('c5_acquisition_plan');self.assertEqual(module.VALUE,7)
                    self.assertIs(sys.dont_write_bytecode,False)
                    self.assertFalse(list(Path(tmp).rglob('*.pyc')))
                    self.assertFalse(list(Path(tmp).rglob('__pycache__')))
        finally:
            for name,old in saved.items():
                if old is None:sys.modules.pop(name,None)
                else:sys.modules[name]=old

    def test_failed_adapter_import_restores_parent_flag_and_path(self):
        name='c5_acquisition_plan';old=sys.modules.pop(name,None);before=sys.path[:]
        try:
            with tempfile.TemporaryDirectory(dir=src.ROOT.parent)as tmp:
                directory=Path(tmp)/'reproduction/all_indices';directory.mkdir(parents=True)
                (directory/(name+'.py')).write_text('raise ValueError("synthetic metadata import failure")\n')
                with patch.object(src,'VENDOR',Path(tmp)),patch.object(sys,'dont_write_bytecode',False):
                    with self.assertRaisesRegex(ValueError,'synthetic metadata'):ev.metadata_module(name)
                    self.assertIs(sys.dont_write_bytecode,False);self.assertEqual(sys.path,before)
                    self.assertFalse(list(Path(tmp).rglob('*.pyc')))
        finally:
            if old is None:sys.modules.pop(name,None)
            else:sys.modules[name]=old

    def test_only_exact_prior_metadata_reader_is_compatible(self):
        current=ev.implementation();self.assertTrue(ev.compatible_implementation(current))
        old=dict(current,**{'n5_remaining_evidence.py':ev.LEGACY_METADATA_READER_SHA256})
        self.assertTrue(ev.compatible_implementation(old))
        self.assertTrue(ev.compatible_implementation(dict(current,**{
            'n5_remaining_evidence.py':ev.PRIOR_METADATA_IMPORT_READER_SHA256})))
        for key in ('n5_remaining.py','n5_remaining_sources.py','n5_remaining_bridge.py','resource_policy','catalog'):
            altered=dict(old);altered[key]='changed';self.assertFalse(ev.compatible_implementation(altered))
        self.assertFalse(ev.compatible_implementation(dict(old,**{'n5_remaining_evidence.py':'0'*64})))

    def test_resource_metadata_port_ordinary_kernel_leaves_snapshot_unchanged(self):
        name='c5_resource_accept_port';old=sys.modules.pop(name,None)
        try:
            with tempfile.TemporaryDirectory(dir=src.ROOT.parent)as tmp:
                directory=Path(tmp)/'reproduction/all_indices';directory.mkdir(parents=True)
                adapter=directory/(name+'.py')
                adapter.write_text('import sys\nassert sys.dont_write_bytecode is True\nVALUE=17\n')
                before=adapter.read_bytes()
                with patch.object(src,'VENDOR',Path(tmp)),patch.object(sys,'dont_write_bytecode',False):
                    module=ev.metadata_module(name)
                    self.assertEqual(module.VALUE,17)
                    self.assertIs(sys.dont_write_bytecode,False)
                    self.assertEqual(adapter.read_bytes(),before)
                    self.assertEqual([p.name for p in directory.iterdir()],[name+'.py'])
        finally:
            if old is None:sys.modules.pop(name,None)
            else:sys.modules[name]=old

    def test_resource_metadata_port_failure_restores_parent_flag(self):
        name='c5_resource_accept_port';old=sys.modules.pop(name,None);before=sys.path[:]
        try:
            with tempfile.TemporaryDirectory(dir=src.ROOT.parent)as tmp:
                directory=Path(tmp)/'reproduction/all_indices';directory.mkdir(parents=True)
                (directory/(name+'.py')).write_text('raise ValueError("synthetic resource metadata failure")\n')
                with patch.object(src,'VENDOR',Path(tmp)),patch.object(sys,'dont_write_bytecode',False):
                    with self.assertRaisesRegex(ValueError,'synthetic resource'):ev.metadata_module(name)
                    self.assertIs(sys.dont_write_bytecode,False)
                    self.assertEqual(sys.path,before)
                    self.assertFalse(list(Path(tmp).rglob('*.pyc')))
        finally:
            if old is None:sys.modules.pop(name,None)
            else:sys.modules[name]=old

if __name__=='__main__':unittest.main()
