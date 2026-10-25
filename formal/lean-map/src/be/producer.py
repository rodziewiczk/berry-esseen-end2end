"""Small witness search. Its output remains untrusted until verifier readback."""
from fractions import Fraction

from .codec import digest, rational
from .semantic import PROTOCOL, RULE_ID, parse_request, sqrt_enclosure


def produce_request(request: dict) -> dict:
    ctx = parse_request(request)
    p, q = ctx.p, 1 - ctx.p
    v = p*q
    lo, hi = sqrt_enclosure(v, ctx.sqrt_bits)
    t_lo = ctx.rho_lower*v*lo - v*(1-2*v)
    t_hi = ctx.rho_upper*v*hi - v*(1-2*v)
    # Independently materialize the fixed source rows for the claimed binding.
    normals = [(1, 0), (-1, 0), (0, 1), (0, -1), (-q, p), (q, -p)]
    right = [0, 0, 0, 0, t_hi, -t_lo]
    proposed_problem = {"schema_version": PROTOCOL, "artifact_kind": "derived_problem",
        "request_id": request["request_id"], "context_digest": ctx.context_digest,
        "rule_id": RULE_ID, "variables": ["conditional_third0", "conditional_third1"],
        "root_enclosure": {"sqrt_v_lower": rational(lo), "sqrt_v_upper": rational(hi),
                           "h3_lower": rational(v*lo), "h3_upper": rational(v*hi)},
        "rows": [{"coefficients": [rational(Fraction(a)), rational(Fraction(b))],
                  "rhs": rational(Fraction(rhs))} for (a, b), rhs in zip(normals, right)]}
    if t_hi < 0:
        witness = {"kind": "farkas", "multipliers": [rational(a) for a in [q, 0, 0, p, 1, 0]]}
    elif t_lo > 0:
        witness = {"kind": "farkas", "multipliers": [rational(a) for a in [0, q, p, 0, 0, 1]]}
    else:
        witness = {"kind": "relaxed_feasible_point", "point": [rational(0), rational(0)]}
    return {"schema_version": PROTOCOL, "artifact_kind": "candidate",
            "request_id": request["request_id"], "context_digest": ctx.context_digest,
            "problem_digest": digest("derived-problem", proposed_problem), "witness": witness}
