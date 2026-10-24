"""Original CAPS list/terminal schema and exact old execution reader boundary."""
import copy,unittest
from be_replay import finite69_caps_evidence as e

class CapsControls(unittest.TestCase):
    def setUp(self):
        self.names=['original control '+str(i)for i in range(17)]
        self.packet=dict(status='PASS_EXACT_TIGHTER_LITERAL7_9_OWNCAPS',negative_controls=self.names.copy())
        self.stdout=self.packet['status']+' 17\n'
    def test_original_list_schema_and_exact_terminal_pass(self):
        e.validate_caps_controls(self.packet,self.stdout,self.names)
    def test_count_boolean_short_duplicate_reordered_or_wrong_terminal_fail(self):
        for bad in(17,True,self.names[:-1],self.names[:-1]+[self.names[0]],list(reversed(self.names))):
            p=dict(self.packet,negative_controls=bad)
            with self.assertRaises(ValueError):e.validate_caps_controls(p,self.stdout,self.names)
        for output in(self.packet['status']+' 16',self.stdout+'unbound extra line'):
            with self.assertRaises(ValueError):e.validate_caps_controls(self.packet,output,self.names)
    def test_only_exact_old_reader_with_every_other_pin_unchanged_is_admitted(self):
        current=e.implementation();old=dict(current,**{'finite69_caps_evidence.py':e.LEGACY_CAPS_READER_SHA256})
        self.assertTrue(e.compatible_observed_implementation(current));self.assertTrue(e.compatible_observed_implementation(old))
        for key in('finite69_caps.py','finite69_caps_sources.py','finite69_cap_epoch.py','catalog_sha256'):
            changed=dict(old);changed[key]='0'*64;self.assertFalse(e.compatible_observed_implementation(changed))
        self.assertFalse(e.compatible_observed_implementation(dict(old,**{'finite69_caps_evidence.py':'0'*64})))
if __name__=='__main__':unittest.main()
