"""Bounded, canonical RJSON-BE/1 and explicitly separated pilot identities.

The mathematical codec is the restricted ASCII/no-number encoding in the
architecture contract. Python bools are allowed; Python numeric values are not.
"""
from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from math import gcd
from pathlib import Path

from .errors import ProtocolError

MAX_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 64
MAX_NODES = 100_000
MAX_STRING_BYTES = 65_536
MAX_INTEGER_DIGITS = 2048
_INT = re.compile(r"(?:0|-?[1-9][0-9]*)\Z", re.ASCII)
_KIND = re.compile(r"[a-z][a-z0-9_./-]{0,127}\Z", re.ASCII)


def _number(_: str):
    raise ProtocolError("json_number_forbidden", "JSON numeric tokens are forbidden")


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ProtocolError("duplicate_json_key", "Duplicate JSON object key")
        result[key] = value
    return result


def _check(value) -> None:
    remaining = MAX_NODES
    stack = [(value, 0)]
    while stack:
        item, depth = stack.pop()
        remaining -= 1
        if remaining < 0 or depth > MAX_DEPTH:
            raise ProtocolError("json_resource_limit", "JSON depth or node limit exceeded")
        if isinstance(item, str):
            if len(item) > MAX_STRING_BYTES:
                raise ProtocolError("json_resource_limit", "JSON string limit exceeded")
            if any(ord(c) < 32 or ord(c) > 126 for c in item):
                raise ProtocolError("non_ascii_json", "Only printable ASCII strings are allowed")
        elif isinstance(item, dict):
            for key, child in item.items():
                if not isinstance(key, str):
                    raise ProtocolError("invalid_json_key", "Object keys must be strings")
                stack.append((key, depth + 1))
                stack.append((child, depth + 1))
        elif isinstance(item, list):
            stack.extend((child, depth + 1) for child in item)
        elif item is not None and not isinstance(item, bool):
            raise ProtocolError("json_number_forbidden", "Only strings, objects, arrays, booleans and null are allowed")


def canonical_bytes(value) -> bytes:
    _check(value)
    try:
        raw = json.dumps(value, sort_keys=True, ensure_ascii=True,
                         separators=(",", ":"), allow_nan=False).encode("ascii")
    except (ValueError, TypeError, RecursionError) as exc:
        raise ProtocolError("invalid_json", "Cannot encode bounded RJSON") from exc
    if len(raw) > MAX_BYTES:
        raise ProtocolError("json_resource_limit", "JSON byte limit exceeded")
    return raw


def loads(raw: bytes, *, require_canonical: bool = True):
    if not isinstance(raw, bytes):
        raise ProtocolError("invalid_json_input", "Decoder requires bytes")
    if len(raw) > MAX_BYTES:
        raise ProtocolError("json_resource_limit", "JSON byte limit exceeded")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ProtocolError("json_bom_forbidden", "UTF-8 BOM is forbidden")
    try:
        value = json.loads(raw.decode("utf-8", errors="strict"),
                           object_pairs_hook=_pairs, parse_int=_number,
                           parse_float=_number, parse_constant=_number)
    except ProtocolError:
        raise
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ProtocolError("invalid_json", "Invalid bounded UTF-8 JSON") from exc
    encoded = canonical_bytes(value)
    if require_canonical and encoded != raw:
        raise ProtocolError("noncanonical_json", "Sealed JSON bytes are not canonical RJSON-BE/1")
    return value


def load_json(path: str | Path, *, require_canonical: bool = True):
    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    return loads(raw, require_canonical=require_canonical)


def bytes_digest(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def domain_digest(kind: str, value, *, domain: str = "BEARCH/1") -> str:
    if not _KIND.fullmatch(kind) or domain not in ("BEARCH/1", "BELOCALPILOT/1"):
        raise ProtocolError("invalid_hash_domain", "Unknown hash domain or invalid kind")
    return bytes_digest((domain + "\n" + kind + "\n").encode("ascii") + canonical_bytes(value))


def digest(kind: str, value) -> str:
    """Identity in the separate, versioned BELOCALPILOT/1 namespace."""
    return domain_digest(kind, value, domain="BELOCALPILOT/1")


def parse_integer(value: str, *, nonnegative: bool = False) -> int:
    if not isinstance(value, str) or len(value.removeprefix("-")) > MAX_INTEGER_DIGITS \
            or not _INT.fullmatch(value):
        raise ProtocolError("invalid_integer", "Expected a bounded canonical integer string")
    number = int(value)
    if nonnegative and number < 0:
        raise ProtocolError("invalid_integer", "Expected a nonnegative integer")
    return number


def parse_rational(value) -> Fraction:
    if not isinstance(value, dict) or set(value) != {"num", "den"}:
        raise ProtocolError("invalid_rational", "Rational requires exactly num and den")
    num = parse_integer(value["num"])
    den = parse_integer(value["den"], nonnegative=True)
    if den == 0 or gcd(abs(num), den) != 1:
        raise ProtocolError("noncanonical_rational", "Rational must be reduced with positive denominator")
    return Fraction(num, den)


def rational(value: Fraction | int) -> dict[str, str]:
    if isinstance(value, bool) or not isinstance(value, (Fraction, int)):
        raise ProtocolError("invalid_rational", "Exact rational input required")
    value = Fraction(value)
    result = {"num": str(value.numerator), "den": str(value.denominator)}
    parse_rational(result)
    return result


dumps = canonical_bytes
sha256_bytes = bytes_digest
