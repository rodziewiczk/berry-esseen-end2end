import copy
from pathlib import Path
import tempfile
import unittest

from be.authority import LocalAuthority
from be.errors import ProtocolError


class LocalAuthorityTests(unittest.TestCase):
    def test_resume_retains_authority_and_payload_cannot_be_changed(self):
        with tempfile.TemporaryDirectory() as directory:
            first = LocalAuthority(directory)
            payload = {"campaign": "one", "scope": "all-seven-roots", "accepted": True}
            seal = first.sign(payload)
            resumed = LocalAuthority(directory)
            resumed.verify(payload, seal)
            self.assertEqual(first.authority_id, resumed.authority_id)
            for field, value in (("campaign", "another"), ("scope", "one-root"), ("accepted", False)):
                altered = dict(payload, **{field: value})
                with self.subTest(field=field), self.assertRaises(ProtocolError):
                    resumed.verify(altered, seal)
            bad_seal = copy.deepcopy(seal)
            bad_seal["signature"] = "0" * 64
            with self.assertRaises(ProtocolError):
                resumed.verify(payload, bad_seal)

    def test_another_local_authority_does_not_authorize_prior_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            a = LocalAuthority(Path(directory) / "a")
            b = LocalAuthority(Path(directory) / "b")
            payload = {"claim": "conditional"}
            with self.assertRaises(ProtocolError):
                b.verify(payload, a.sign(payload))

    def test_partial_key_does_not_mint_replacement_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "authority.key"
            path.write_bytes(b"partial")
            with self.assertRaises(ProtocolError):
                LocalAuthority(directory)
            self.assertEqual(path.read_bytes(), b"partial")


if __name__ == "__main__":
    unittest.main()
