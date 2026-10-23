"""Collect nine fresh auxiliary jobs into a conditional finite numerical chain.

Only the small exact scalar comparison runs here. Numerical kernels are never
imported. Original ZIP/receipt bytes and original execution contexts survive
relocation. Universal C20 and the retained analytic framework remain premises.
"""
from __future__ import annotations
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import time
import traceback
import uuid
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MIB = 1024**2
JOBS = tuple("auxiliary" + n for n in ("21", "22", "23")) + tuple("stronger24-b" + str(n) for n in range(6))
RHO = ["1", "11/10", "6/5", "13/10", "7/5", "3/2", "712569/449000"]
BRANCHES = {
    "b0": (list(range(37, 49)), 1929), "b1": (list(range(32, 41)), 9803),
    "b2": (list(range(28, 37)), 26625), "b3": (list(range(25, 33)), 12484),
    "b4": (list(range(23, 31)), 4168), "b5": (list(range(21, 28)), 2444),
}
PREDECESSOR_SHA = "8871835341669078aa1a25b62e95ad7e8342dffae794c8d0cd7faf8032d4d563"
PREMISES = ["Published universal C20 <= 469/1000 (external, not acquired by these jobs)",
            "Retained fixed-index attainment, unrestricted positive closed contact, same-law support, Fourier/INITIAL/resource/count implications",
            "Published universal rho envelopes used for the high-rho tail", "Exact optimized-arithmetic identities in the selected frozen sources"]
FALSE_FLAGS = dict(analytic_framework_verified=False, universal_C20_acquisition_verified=False,
                   full_auxiliary_bound_verified=False, stronger24_acquisition_verified=False,
                   all_index_conclusion_verified=False, native_arithmetic_accepted=False)


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(MIB), b""):
            h.update(block)
    return h.hexdigest()


def scalar_certificate():
    """Exact rational Machin/square comparisons; called on Colab, not in fixtures."""
    def atan(q, count):
        need(count % 2 == 0, "Even alternating arctangent truncation")
        lower = sum((F((-1)**k, (2*k+1)*q**(2*k+1)) for k in range(count)), F(0))
        return lower, lower + F(1, (2*count+1)*q**(2*count+1))
    a, au = atan(5, 12)
    b, bu = atan(239, 4)
    pi_lower, pi_upper = 16*a-4*bu, 16*au-4*b
    r, s, floor = F(3162277660168, 10**12), F(2506628274632, 10**12), F(40973218, 10**8)
    need(0 < r and r*r < 10 and s > 0 and s*s > 2*pi_upper and pi_lower > 3,
         "Exact sqrt10 lower and sqrt(2*pi) upper square comparisons")
    ce_lower = (3+r)/(6*s)
    need(ce_lower > floor, "Certified strict CE lower bound")
    rho = F(712569, 449000)
    envelopes = [F(469, 1000), F(1661, 5000)*(1+F(429, 1000)/rho), F(3031, 10000)*(1+F(646, 1000)/rho)]
    tail = min(envelopes)
    need(tail == F(211, 500) and tail < floor + F(1, 80), "Full monotone high-rho tail below CE+1/80")
    allowances = [22*F(11, 210)-F(9, 10), 23*F(9, 220)-F(3, 5), 24*F(3, 115)-F(3, 10), 25*F(1, 80)]
    need(allowances == [F(53, 210), F(15, 44), F(15, 46), F(5, 16)], "Exact contact allowance chain")
    return dict(schema="FRESH_AUX24_SCALAR_COMPARISON_V1", rho_tail_start=str(rho), envelope_values=list(map(str, envelopes)),
                tail_upper=str(tail), CE_strict_floor=str(floor), CE_lower_rational=str(ce_lower),
                pi_interval=list(map(str, (pi_lower, pi_upper))), sqrt10_lower=str(r), sqrt2pi_upper=str(s),
                atan_terms={"5": 12, "239": 4}, allowance_chain=list(map(str, allowances)),
                strict_tail_comparison=True, external_envelope_theorems_acquired=False,
                calculation_source_sha256=digest(__file__), **FALSE_FLAGS)


def verified_zip(path):
    path = Path(path)
    need(path.is_file() and not path.is_symlink() and 0 < path.stat().st_size <= 512*MIB, "Bounded ordinary completed evidence ZIP")
    sidecar = path.with_suffix(".zip.sha256")
    need(sidecar.is_file() and not sidecar.is_symlink() and sidecar.stat().st_size <= 1024, "Actual ZIP SHA-256 sidecar")
    fields = sidecar.read_text("ascii").strip().split()
    need(len(fields) == 2 and re.fullmatch(r"[0-9a-f]{64}", fields[0]) and fields[1] == path.name,
         "Exact sidecar digest and ZIP basename")
    need(digest(path) == fields[0], "Actual completed ZIP bytes match sidecar")
    return fields[0]


def extract(path, output, *, progress=None):
    """Bounded, path-safe extraction; receipt and source bytes are never rewritten."""
    path, output = Path(path), Path(output)
    need(not output.exists(), "New private evidence extraction")
    before = verified_zip(path)
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        need(0 < len(entries) <= 20000 and sum(i.file_size for i in entries) <= 1024*MIB, "Bounded complete ZIP expansion")
        seen, roots, total = set(), set(), 0
        for info in entries:
            name = info.filename.rstrip("/")
            pure = PurePosixPath(name)
            parts = name.split("/")
            need(name and "\\" not in name and ":" not in name and not pure.is_absolute()
                 and all(p and p not in (".", "..") and p == p.rstrip(" .")
                         and not any(ord(c) < 32 for c in p) for p in parts), "Safe literal evidence ZIP path")
            need(name.casefold() not in seen, "Unique portable ZIP member")
            seen.add(name.casefold())
            roots.add(parts[0])
            mode = stat.S_IFMT(info.external_attr >> 16)
            need(mode in ((0, stat.S_IFDIR) if info.is_dir() else (0, stat.S_IFREG))
                 and not info.flag_bits & 1 and 0 <= info.file_size <= 128*MIB, "Ordinary bounded unencrypted ZIP member")
        need(len(roots) == 1, "One original evidence root")
        output.mkdir(parents=True)
        last = time.monotonic()
        for number, info in enumerate(entries, 1):
            destination = output.joinpath(*PurePosixPath(info.filename).parts)
            need(destination.resolve().is_relative_to(output.resolve()), "Contained evidence extraction")
            if info.is_dir():
                destination.mkdir(parents=True, exist_ok=True)
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            copied = 0
            with archive.open(info) as source, destination.open("xb") as target:
                while block := source.read(MIB):
                    copied += len(block)
                    total += len(block)
                    need(copied <= info.file_size and total <= 1024*MIB, "Exact bounded member expansion")
                    target.write(block)
            need(copied == info.file_size, "Complete unchanged extracted member bytes")
            if progress and time.monotonic()-last >= 20:
                progress("join_evidence_extraction_progress", files=number, total_files=len(entries), bytes=total)
                last = time.monotonic()
    need(verified_zip(path) == before, "ZIP unchanged during complete extraction")
    task = output / next(iter(roots)) / "task"
    need(task.is_dir() and not task.is_symlink(), "Original completed task folder in evidence bundle")
    return task, before


def validators():
    from . import aux21_23, strong24_branches
    return aux21_23, strong24_branches


def validate_scope(key, packet):
    aux, branches = validators()
    if key.startswith("auxiliary"):
        value = key[len("auxiliary"):]
        spec = aux.SPECS[value]
        need(packet["schema"] == "FRESH_AUX21_23_JOB_RESULT_V1" and packet["target"] == value
             and type(packet["n"]) is int and packet["n"] == spec["n"] and packet["K"] == spec["K"]
             and packet["allowance"] == spec["allowance"] and packet["conditional_arithmetic_replayed"] is True
             and packet["semantics_verified"] is True and packet["source_manifest_sha256"] == aux.EPOCH_PINS[value]
             and packet["driver_sha256"] == digest(aux.__file__), "Exact freshly revalidated auxiliary target and source epoch")
        edges = packet["semantic_edges"]
        if value == "21":
            need(edges["signed_rectangles"] == 92160 and edges["allowance"] == "299/2000", "Complete five-cover auxiliary21 evidence")
        else:
            need(edges["initial_signed_rectangles"] == spec["rectangles"] and edges["probability_panels"] == 100
                 and edges["count_indices"] == spec["indices"] and edges["count_leaves"] == spec["leaves"],
                 "Complete auxiliary INITIAL/resource/count census")
        need(all(packet[field] is False for field in ("predecessor_acquisition_verified", "full_auxiliary_bound_verified",
                                                      "stronger24_acquisition_verified", "all_index_conclusion_verified")), "Conditional auxiliary scope preserved")
    else:
        branch = key[len("stronger24-"):]
        position = int(branch[1:])
        indices, leaves = BRANCHES[branch]
        need(packet["schema"] == "REVALIDATED_CONDITIONAL_STRONG24_BRANCH_V1" and packet["branch"] == branch
             and type(packet["n"]) is int and packet["n"] == 24 and packet["K"] == "3/10"
             and packet["rho_interval"] == RHO[position:position+2] and packet["contact_allowance"] == "15/46"
             and packet["effective_contact_allowance"] == branches.EFFECTIVE_Q[branch]
             and 0 <= F(packet["effective_contact_allowance"]) <= F(15, 46)
             and packet["predecessor_statement_sha256"] == PREDECESSOR_SHA
             and packet["driver_sha256"] == digest(branches.__file__)
             and packet["source_manifest_sha256"] == branches.SELECTION_SHA[branch], "Exact original branch, predecessor statement and source epoch")
        need(packet["probability_panels"] == 100 and packet["count_indices"] == indices
             and packet["count_forests"] == len(indices) and packet["count_leaves"] == leaves
             and packet["numeric_resource_to_count_interfaces_verified"] is True and packet["arithmetic_computed"] is True,
             "Every branch resource interface, count forest and closed panel")
        need(all(packet[field] is False for field in ("native_arithmetic_accepted", "branch_theorem_acquired",
                                                      "stronger24_acquisition_verified", "all_index_conclusion_verified")), "Conditional BASIC branch scope preserved")
    return packet


def collect(durable_root, work, *, progress):
    """Choose the latest fully validated ZIP per job, skipping incomplete evidence."""
    from . import aux24_evidence
    aux, branches = validators()
    imports, missing = {}, []
    for key in JOBS:
        progress("join_searching_completed_job", job=key)
        candidates = sorted((Path(durable_root) / key).rglob("*-results.zip"), key=lambda p: p.stat().st_mtime_ns, reverse=True)
        failures = []
        for candidate in candidates:
            try:
                output = Path(work) / "imports" / key / uuid.uuid4().hex[:12]
                task, zip_sha = extract(candidate, output, progress=progress)
                packet = aux.validate_completed(task) if key.startswith("auxiliary") else branches.validate_completed(task)
                validate_scope(key, packet)
                transport = aux24_evidence.validate_task_transport(task, key)
                need(transport["execution_transport_revalidated"] is True and transport["job"] == key,
                     "Separate strict actual launch, supervisor and kernel-guard evidence")
                transport_path = output / "TRANSPORT_REPORT.json"
                transport_path.write_text(json.dumps(transport, sort_keys=True, indent=2)+"\n", encoding="utf-8")
                report = output / "REVALIDATED_REPORT.json"
                report.write_text(json.dumps(packet, sort_keys=True, indent=2)+"\n", encoding="utf-8")
                original_result = task / ("JOB_RESULT.json" if key.startswith("auxiliary") else "RESULT.json")
                if not key.startswith("auxiliary"):
                    need(packet["result_sha256"] == digest(original_result), "Validated branch result binds actual unchanged imported bytes")
                imports[key] = dict(zip_path=str(candidate.resolve()), zip_sha256=zip_sha,
                    task_relative=task.relative_to(work).as_posix(), validated_report_relative=report.relative_to(work).as_posix(),
                    validated_report_sha256=digest(report), actual_job_result_sha256=digest(original_result),
                    source_manifest_sha256=packet["source_manifest_sha256"], driver_sha256=packet["driver_sha256"], report=packet,
                    transport_report_relative=transport_path.relative_to(work).as_posix(),
                    transport_report_sha256=digest(transport_path), transport_validator_sha256=digest(aux24_evidence.__file__))
                progress("join_completed_job_revalidated", job=key, zip_sha256=zip_sha)
                break
            except Exception as error:
                reason = type(error).__name__ + ": " + str(error)
                failures.append(dict(zip_path=str(candidate), reason=reason[:1200]))
                progress("join_candidate_not_complete", job=key, reason=reason[:1200])
        if key not in imports:
            missing.append(dict(job=key, candidates_checked=len(candidates), reasons=failures[:20]))
    return imports, missing


def run(durable_root, work):
    from . import colab_batch
    work = Path(work).resolve()
    progress = lambda name, **fields: colab_batch.event(work, name, **fields)
    imports, missing = collect(durable_root, work, progress=progress)
    result = dict(schema="FRESH_CONDITIONAL_AUX24_NUMERIC_CHAIN_V1", status="WAITING_FOR_COMPLETED_JOBS",
                  conditional_fresh_numeric_chain_verified=False, premises=PREMISES, imports=imports,
                  missing_jobs=missing, driver_sha256=digest(__file__), **FALSE_FLAGS)
    if missing:
        progress("join_waiting_for_jobs", missing=[r["job"] for r in missing])
        return result
    scalar = scalar_certificate()
    need(scalar["rho_tail_start"] == RHO[-1] and scalar["tail_upper"] == "211/500"
         and scalar["strict_tail_comparison"] is True, "Fresh exact full tail comparison")
    forests = 9+21+sum(p["report"]["count_forests"] for k, p in imports.items() if k.startswith("stronger24-"))
    leaves = 258+18377+sum(p["report"]["count_leaves"] for k, p in imports.items() if k.startswith("stronger24-"))
    need(forests == 83 and leaves == 76088, "Whole selected nine-job count census")
    result.update(status="CONDITIONAL_FRESH_NUMERIC_CHAIN_VERIFIED", conditional_fresh_numeric_chain_verified=True,
                  scalar_certificate=scalar, count_forests=forests, count_leaves=leaves, rho_closed_cover=RHO,
                  conditional_chain=["C20 <= 469/1000 (external)", "C21 < CE+11/210", "C22 < CE+9/220",
                                     "C23 < CE+3/115", "C24 < CE+1/80", "n25 contact allowance <= 5/16"],
                  n25_contact_allowance="5/16")
    progress("join_conditional_fresh_numeric_chain_verified", count_forests=forests, count_leaves=leaves,
             stronger24_acquisition_verified=False, all_index_conclusion_verified=False)
    return result


def run_colab(*, durable_root, work_root="/content/berry-esseen-runs", backup_interval=60):
    """Discover/validate available finished bundles; missing jobs produce WAITING."""
    from . import colab_batch
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:8]
    root = Path(work_root) / "auxiliary24-join" / stamp
    root.mkdir(parents=True)
    durable = Path(durable_root) / "auxiliary24-join" / stamp
    status = dict(state="started", conditional_fresh_numeric_chain_verified=False, **FALSE_FLAGS)
    colab_batch.atomic_json(root / "SESSION_RESULT.json", status)
    monitor = colab_batch.Backups(root, durable, interval=backup_interval)
    monitor.start()
    try:
        colab_batch.event(root, "conditional_auxiliary24_join_started", jobs=list(JOBS), **FALSE_FLAGS)
        result = run(durable_root, root)
        colab_batch.atomic_json(root / "CONDITIONAL_NUMERIC_CHAIN.json", result)
        status.update(state=result["status"], conditional_fresh_numeric_chain_verified=result["conditional_fresh_numeric_chain_verified"], result=result)
    except BaseException as error:
        status.update(state="PARTIAL_ERROR_NOT_ACCEPTED", error=type(error).__name__+": "+str(error))
        (root / "ERROR.txt").write_text(traceback.format_exc(), encoding="utf-8")
        colab_batch.event(root, "conditional_join_incomplete", error=status["error"])
    finally:
        colab_batch.atomic_json(root / "SESSION_RESULT.json", status)
        try:
            monitor.close()
        except Exception as error:
            colab_batch.event(root, "final_backup_failed", error=str(error))
        output = colab_batch.bundle(root, durable)
        colab_batch.event(root, "conditional_join_bundle_saved", path=str(output), state=status["state"], **FALSE_FLAGS)
    print("\nRESULT:", status["state"], "\nZIP:", output, flush=True)
    return dict(status=status, bundle=str(output), work=str(root))
