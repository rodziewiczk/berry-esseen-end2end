"""Exact, source-conditional moment-feasibility pilot; never full COUNT.

The verifier derives its own rectangle and strip from the frozen context.
It accepts no producer-supplied planes, square roots or truth flags.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from pathlib import Path, PurePosixPath

from .codec import canonical_bytes, bytes_digest, digest, parse_integer, parse_rational, rational
from .errors import ProtocolError
from .schema import validate_document

PROTOCOL = "be.local-pilot/1"
RULE_ID = "count-joint-cubics-zero-variance-v1"
BACKEND = "python-fraction-independent-checker-v1"
PROOF_SCOPE = "zero-conditional-variance-moment-feasibility-only"
PREMISES = ["standardized-binary-decomposition",
            "zero-conditional-second-moment-forces-zero-cubic",
            "same-law-absolute-third-moment-identity"]
REPO_ROOT = Path(__file__).resolve().parents[2]
MIN_SQRT_BITS, MAX_SQRT_BITS, MAX_PARAMETER_DIGITS = 8, 512, 128
MAX_SOURCE_BYTES = 1024 * 1024


@dataclass(frozen=True)
class Context:
    p: Fraction
    rho_lower: Fraction
    rho_upper: Fraction
    sqrt_bits: int
    context_digest: str


def _q(value, *, parameter: bool = False) -> Fraction:
    out = parse_rational(value)
    if parameter and max(len(str(abs(out.numerator))), len(str(out.denominator))) > MAX_PARAMETER_DIGITS:
        raise ProtocolError("parameter_resource_limit", "Pilot parameter exceeds its declared digit limit")
    return out


def validate_source_files(manifest: dict, source_root: str | Path = REPO_ROOT) -> None:
    """Validate provenance bytes, not the truth of accepted analytic premises."""
    validate_document(manifest, "source-manifest.schema.json")
    if manifest["analytic_premises"] != PREMISES:
        raise ProtocolError("unsupported_analytic_premises", "Pilot accepts one explicit analytic premise list")
    names = [entry["path"] for entry in manifest["source_files"]]
    if names != sorted(set(names)) or "docs/contracts/COUNT-RULES.md" not in names:
        raise ProtocolError("invalid_source_manifest", "Required ordered source file inventory is missing")
    root = Path(source_root).resolve()
    for entry in manifest["source_files"]:
        rel = PurePosixPath(entry["path"])
        if rel.is_absolute() or ".." in rel.parts or "\\" in entry["path"] or ":" in entry["path"]:
            raise ProtocolError("invalid_source_path", "Source paths must remain inside the source root")
        path = root.joinpath(*rel.parts).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ProtocolError("missing_source_file", "A pinned public source file is missing")
        with path.open("rb") as stream:
            raw = stream.read(MAX_SOURCE_BYTES + 1)
        if len(raw) > MAX_SOURCE_BYTES:
            raise ProtocolError("source_resource_limit", "Pinned pilot source exceeds the source byte limit")
        if bytes_digest(raw) != entry["bytes_digest"] or str(len(raw)) != entry["size_bytes"]:
            raise ProtocolError("source_digest_mismatch", "Pinned source bytes differ from the source inventory")


def parse_request(request: dict) -> Context:
    validate_document(request, "request.schema.json")
    core = request["core"]
    if request["request_id"] != digest("request", core):
        raise ProtocolError("request_digest_mismatch", "Request identity does not bind its exact contents")
    problem = core["problem"]
    validate_document(problem, "problem.schema.json")
    source = core["source_manifest"]
    validate_source_files(source)
    trust = core["trust_profile"]
    validate_document(trust, "trust-profile.schema.json")
    if trust["source_manifest_digest"] != digest("source-manifest", source):
        raise ProtocolError("trust_source_mismatch", "Trust profile names a different source manifest")
    data = problem["context"]
    p = _q(data["p"], parameter=True)
    lo = _q(data["rho"]["lower"], parameter=True)
    hi = _q(data["rho"]["upper"], parameter=True)
    if not 0 < p <= Fraction(1, 2):
        raise ProtocolError("unsupported_probability", "Pilot requires a point probability 0 < p <= 1/2")
    if not 1 <= lo <= hi:
        raise ProtocolError("invalid_rho_interval", "Source rule requires 1 <= rho lower <= rho upper")
    if _q(data["conditional_variance0"]) != 0 or _q(data["conditional_variance1"]) != 0:
        raise ProtocolError("unsupported_conditional_variance", "Pilot only supports two exact zero variances")
    bits = parse_integer(problem["numeric_policy"]["sqrt_bits"], nonnegative=True)
    if not MIN_SQRT_BITS <= bits <= MAX_SQRT_BITS:
        raise ProtocolError("unsupported_precision", "Pilot sqrt precision must be between 8 and 512 bits")
    return Context(p, lo, hi, bits, digest("context", data))


def freeze_request(problem: dict, source_manifest: dict, trust_profile: dict) -> dict:
    core = {"problem": problem, "source_manifest": source_manifest, "trust_profile": trust_profile}
    request = {"schema_version": PROTOCOL, "artifact_kind": "request",
               "request_id": digest("request", core), "core": core}
    parse_request(request)
    return request


def sqrt_enclosure(value: Fraction, bits: int) -> tuple[Fraction, Fraction]:
    """isqrt bounds, followed by exact rational square checks; no float path."""
    if not isinstance(value, Fraction) or type(bits) is not int or value < 0 or not MIN_SQRT_BITS <= bits <= MAX_SQRT_BITS:
        raise ProtocolError("invalid_sqrt_input", "Invalid square-root domain or precision")
    a, b = isqrt(value.numerator), isqrt(value.denominator)
    if a * a == value.numerator and b * b == value.denominator:
        lower = upper = Fraction(a, b)
    else:
        scale = 1 << bits
        k = isqrt((value.numerator * scale * scale) // value.denominator)
        lower, upper = Fraction(k, scale), Fraction(k + 1, scale)
    if not 0 <= lower <= upper or lower * lower > value or upper * upper < value:
        raise ProtocolError("sqrt_enclosure_failed", "Exact square checks rejected a root enclosure")
    return lower, upper


def derive_problem(request: dict) -> dict:
    ctx = parse_request(request)
    p, q = ctx.p, 1 - ctx.p
    v = p * q
    root_lo, root_hi = sqrt_enclosure(v, ctx.sqrt_bits)
    h3_lo, h3_hi = v * root_lo, v * root_hi
    base = v * (1 - 2 * v)
    t_lo, t_hi = ctx.rho_lower * h3_lo - base, ctx.rho_upper * h3_hi - base
    # Source order: four support-rectangle planes, upper strip, lower strip.
    rows = [([1, 0], 0), ([-1, 0], 0), ([0, 1], 0), ([0, -1], 0),
            ([-q, p], t_hi), ([q, -p], -t_lo)]
    return {"schema_version": PROTOCOL, "artifact_kind": "derived_problem",
            "request_id": request["request_id"], "context_digest": ctx.context_digest,
            "rule_id": RULE_ID, "variables": ["conditional_third0", "conditional_third1"],
            "root_enclosure": {"sqrt_v_lower": rational(root_lo), "sqrt_v_upper": rational(root_hi),
                               "h3_lower": rational(h3_lo), "h3_upper": rational(h3_hi)},
            "rows": [{"coefficients": [rational(Fraction(a)) for a in normal],
                      "rhs": rational(Fraction(rhs))} for normal, rhs in rows]}


def _receipt(request: dict, candidate: dict, problem: dict, outcome: str, reason: str,
             totals: dict | None = None) -> dict:
    core = {"request_id": request["request_id"],
            "candidate_digest": bytes_digest(canonical_bytes(candidate)),
            "context_digest": problem["context_digest"],
            "expected_problem_digest": digest("derived-problem", problem),
            "source_manifest_digest": digest("source-manifest", request["core"]["source_manifest"]),
            "trust_profile_digest": digest("trust-profile", request["core"]["trust_profile"]),
            "outcome": outcome, "reason_code": reason, "farkas_totals": totals,
            "numeric_backend": BACKEND, "proof_scope": PROOF_SCOPE,
            "conditional": True, "full_proof_pass": False}
    return {"schema_version": PROTOCOL, "artifact_kind": "verification_receipt",
            "receipt_id": digest("verification-receipt", core), "core": core}


def verify_request(request: dict, candidate: dict) -> dict:
    """Reconstruct the expected planes, bind the witness, then check exact arithmetic."""
    problem = derive_problem(request)
    try:
        validate_document(candidate, "candidate.schema.json")
    except ProtocolError:
        return _receipt(request, candidate, problem, "rejected", "candidate_schema_invalid")
    if candidate["request_id"] != request["request_id"]:
        return _receipt(request, candidate, problem, "rejected", "request_binding_mismatch")
    if candidate["context_digest"] != problem["context_digest"]:
        return _receipt(request, candidate, problem, "rejected", "context_binding_mismatch")
    if candidate["problem_digest"] != digest("derived-problem", problem):
        return _receipt(request, candidate, problem, "rejected", "problem_binding_mismatch")
    witness = candidate["witness"]
    rows = [([_q(a) for a in row["coefficients"]], _q(row["rhs"])) for row in problem["rows"]]
    if witness["kind"] == "farkas":
        try:
            weights = [_q(v, parameter=True) for v in witness["multipliers"]]
        except ProtocolError:
            return _receipt(request, candidate, problem, "rejected", "invalid_multiplier")
        if len(weights) != len(rows) or any(w < 0 for w in weights):
            return _receipt(request, candidate, problem, "rejected", "invalid_multiplier")
        normals = [sum((weight * row[0][axis] for weight, row in zip(weights, rows)), Fraction(0))
                   for axis in range(2)]
        rhs = sum((weight * row[1] for weight, row in zip(weights, rows)), Fraction(0))
        totals = {"normal": [rational(v) for v in normals], "rhs": rational(rhs)}
        if normals != [0, 0] or rhs >= 0:
            return _receipt(request, candidate, problem, "rejected", "farkas_not_contradictory", totals)
        return _receipt(request, candidate, problem, "infeasible", "farkas_contradiction_verified", totals)
    try:
        point = [_q(v) for v in witness["point"]]
    except ProtocolError:
        return _receipt(request, candidate, problem, "rejected", "invalid_relaxed_point")
    if len(point) != 2 or any(sum((a*x for a, x in zip(row[0], point)), Fraction(0)) > row[1] for row in rows):
        return _receipt(request, candidate, problem, "rejected", "invalid_relaxed_point")
    return _receipt(request, candidate, problem, "no_contradiction", "necessary_system_not_excluded")


def authorized_readback(request: dict, candidate: dict, receipt: dict) -> dict:
    """Local pilot authority rechecks math; it never trusts a stored outcome string."""
    validate_document(receipt, "verification-receipt.schema.json")
    expected = verify_request(request, candidate)
    if canonical_bytes(receipt) != canonical_bytes(expected):
        raise ProtocolError("receipt_readback_mismatch", "Receipt differs from independent exact readback")
    return expected
