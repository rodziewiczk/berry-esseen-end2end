import hashlib
import unittest
from fractions import Fraction

from be import codec
from be.errors import ProtocolError


class CodecContractTests(unittest.TestCase):
    def test_golden_bytes_and_hash_domains(self):
        value = {"z": [True, False, None, 'a/b"\\'], "a": "0"}
        expected = b'{"a":"0","z":[true,false,null,"a/b\\\"\\\\"]}'
        self.assertEqual(codec.canonical_bytes(value), expected)
        self.assertEqual(codec.loads(expected), value)
        expected_hash = "sha256:" + hashlib.sha256(b"BELOCALPILOT/1\ncontext\n" + expected).hexdigest()
        self.assertEqual(codec.digest("context", value), expected_hash)
        self.assertNotEqual(codec.digest("context", value), codec.domain_digest("context", value))
        self.assertNotEqual(codec.digest("context", value), codec.digest("statement", value))

    def test_hostile_and_noncanonical_inputs(self):
        controls = [b'{"x":"1","x":"2"}', b'{"n":1}', b'{"x":NaN}',
                    b'{"x":Infinity}', b'"\\u03bb"', b'"\\n"', b'\xef\xbb\xbf{}',
                    b'{}{}', b'{}\n', b'{"a": "1"}', b'{"z":"1","a":"2"}', b'"\\/"']
        for raw in controls:
            with self.subTest(raw=raw), self.assertRaises(ProtocolError):
                codec.loads(raw)

    def test_canonical_rationals_and_closed_limits(self):
        self.assertEqual(codec.parse_rational({"num": "-3", "den": "2"}), Fraction(-3, 2))
        for value in ({"num": "0", "den": "2"}, {"num": "2", "den": "4"},
                      {"num": "1", "den": "0"}, {"num": "-0", "den": "1"},
                      {"num": "+1", "den": "1"}, {"num": "01", "den": "1"},
                      {"num": "1", "den": "1", "extra": True}):
            with self.subTest(value=value), self.assertRaises(ProtocolError):
                codec.parse_rational(value)
        with self.assertRaises(ProtocolError):
            codec.parse_integer("9" * (codec.MAX_INTEGER_DIGITS + 1))
        with self.assertRaises(ProtocolError):
            codec.rational(0.5)

    def test_bounded_decoder_and_encoder(self):
        with self.assertRaises(ProtocolError):
            codec.loads(b" " * (codec.MAX_BYTES + 1))
        with self.assertRaises(ProtocolError):
            codec.loads(b"[" * (codec.MAX_DEPTH + 1) + b'"x"' + b"]" * (codec.MAX_DEPTH + 1))
        with self.assertRaises(ProtocolError):
            codec.canonical_bytes({"x": "a" * (codec.MAX_STRING_BYTES + 1)})


if __name__ == "__main__":
    unittest.main()
