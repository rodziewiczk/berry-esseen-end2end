"""Collect fresh parent/count exports and verify seven conditional n25 interfaces.

This is an evidence/contract join, not the complete n25 finite cover. Numerical
leaf kernels are never imported or rerun; the retained analytic premises remain
explicit. Existing notebook source pins and evidence bytes are unchanged.
"""
from __future__ import annotations

from datetime import datetime, timezone
from fractions import Fraction as F
import json
from pathlib import Path, PurePosixPath
import traceback
import uuid

from . import aux24_join as transport, count_task as common, n25_parents

COUNTS = tuple(common.TARGETS)
PARENTS = ("n25-parents-b3", "n25-parents-b4")
JOBS = PARENTS + COUNTS
FALSE_FLAGS = dict(stronger24_acquisition_verified=False,
                   analytic_attained_contact_premise_acquired=False,
                   full_n25_verified=False, all_index_conclusion_verified=False,
                   native_arithmetic_accepted=False)
PREMISES = [
    "The matching global auxiliary statement C24 < CE+1/80, not acquired here",
    "Retained unrestricted attainment and positive closed contact for the same actual-n25 witness",
    "Same-law support, INITIAL/resource/count and V14 contact implications",
    "Remaining n25 branches, probability panels, Fourier/high/middle domains and final seams",
]


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def contained(root, relative):
    need(type(relative) is str and relative and "\\" not in relative and ":" not in relative,
         "Portable relative imported artifact path")
    parts = relative.split("/")
    need(all(p and p not in (".", "..") for p in parts)
         and not PurePosixPath(relative).is_absolute(), "Contained literal imported artifact path")
    literal = Path(root)
    for part in parts:
        literal = literal / part
        need(not literal.is_symlink(), "No symlinks in imported artifact ancestry")
    result = literal.resolve()
    need(result.is_relative_to(Path(root).resolve()),
         "Imported artifact stays inside its extracted task")
    return result


def validators():
    from . import n25_count_evidence, n25_parent_evidence, n25_contract_interfaces
    return n25_count_evidence, n25_parent_evidence, n25_contract_interfaces


def recovery_validator():
    from . import count_recovery_evidence
    return count_recovery_evidence


def validate_count_export(task, key, ordinary):
    """Dispatch seven fixed resource profiles; original validators stay intact."""
    task_record = Path(task) / "TASK.json"
    # The selected ordinary validator itself rejects a missing TASK. Keeping
    # that dispatch fallback also preserves its existing injectable test seam.
    record = common.read(task_record, 4 * common.MIB) if task_record.exists() else {}
    if record.get("schema") == "COUNT_LIMIT_RECOVERY_TASK_V1":
        need(key in COUNTS and record.get("target") == key,
             "Only the matching logical target's reviewed resource profile")
        validator = recovery_validator()
    else:
        validator = ordinary
    return validator.validate_completed(task, expected_target=key), validator


def validate_scope(key, packet):
    need(key in JOBS and type(packet) is dict, "One exact selected fresh n25 export")
    need(packet["native_arithmetic_accepted"] is True
         and packet["all_index_conclusion_verified"] is False
         and type(packet["n"]) is int and packet["n"] == 25,
         "Complete scoped n25 native arithmetic without a global claim")
    if key in COUNTS:
        branch = "b4" if key.startswith("b4-") else "b3"
        expected_design = common.TARGETS[key][2]
        if packet.get("resource_epoch") is not None:
            recovery = recovery_validator()
            profile = recovery.limit.profile(key)
            recovery.memory_policy(packet, key)
            need(recovery.same(packet["resource_epoch"], recovery.resource_epoch(
                    key, native_memory_bytes=packet["native_memory_bytes"]))
                 and packet["original_design_sha256"] == common.TARGETS[key][2]
                 and packet["new_design_sha256"] == profile["new_design_sha256"],
                 "Exact fixed resource-only profile with unchanged original mathematical inputs")
            expected_design = profile["new_design_sha256"]
        need(packet["schema"] == "REVALIDATED_N25_COUNT_V1" and packet["target"] == key
             and packet["branch"] == branch and type(packet["index"]) is int
             and packet["index"] == common.TARGETS[key][1]
             and packet["design_sha256"] == expected_design
             and packet["parent_acquisitions_verified"] is False
             and type(packet["census"]["roots"]) is int and packet["census"]["roots"] == 26,
             "Exact complete selected count design, branch and original roots")
    else:
        branch = key[len("n25-parents-"):]
        need(packet["schema"] == "REVALIDATED_N25_PARENT_V1" and packet["branch"] == branch
             and packet["contact_allowance"] == "5/16"
             and packet["stronger24_acquisition_verified"] is False
             and packet["count_interface_join_verified"] is False,
             "Exact complete conditional B3/B4 parent and predecessor allowance")
    return packet


def collect(durable_root, work, *, progress):
    """Restore latest compatible complete evidence, retaining rejected diagnostics."""
    counts, parents, _ = validators()
    imports, missing = {}, []
    for key in JOBS:
        progress("n25_searching_completed_export", job=key)
        candidates = []
        for path in (Path(durable_root) / key).rglob("*-results.zip"):
            try:
                candidates.append((path.stat().st_mtime_ns, path))
            except FileNotFoundError:
                continue
        failures = []
        for _, candidate in sorted(candidates, key=lambda row: (row[0], str(row[1])), reverse=True):
            try:
                destination = Path(work) / "imports" / key / uuid.uuid4().hex[:12]
                task, zip_sha = transport.extract(candidate, destination, progress=progress)
                if key in COUNTS:
                    packet, validator = validate_count_export(task, key, counts)
                else:
                    packet = parents.validate_completed(task, expected_branch=key[len("n25-parents-"):])
                    validator = parents
                validate_scope(key, packet)
                if key in COUNTS:
                    actual = contained(task, packet["accepted_report_relative"])
                    need(common.digest(actual) == packet["accepted_report_sha256"],
                         "Validated count report binds actual preserved acceptance bytes")
                report = destination / "REVALIDATED_REPORT.json"
                report.write_text(json.dumps(packet, sort_keys=True, indent=2)+"\n", encoding="utf-8")
                imports[key] = dict(zip_path=str(candidate.resolve()), zip_sha256=zip_sha,
                    task_relative=task.relative_to(work).as_posix(),
                    validated_report_relative=report.relative_to(work).as_posix(),
                    validated_report_sha256=common.digest(report),
                    validator_sha256=common.digest(validator.__file__), report=packet)
                progress("n25_completed_export_revalidated", job=key, zip_sha256=zip_sha)
                break
            except Exception as error:
                reason = type(error).__name__+": "+str(error)
                failures.append(dict(zip_path=str(candidate), reason=reason[:1200]))
                progress("n25_export_not_complete", job=key, reason=reason[:1200])
        if key not in imports:
            missing.append(dict(job=key, candidates_checked=len(candidates), reasons=failures[:20]))
    return imports, missing


def interfaces(imports, work, *, progress):
    """Read only fresh revalidated capsules; verify actual simultaneous guards."""
    _, _, mapper = validators()
    packets, pending = {}, []
    for target in COUNTS:
        branch = "b4" if target.startswith("b4-") else "b3"
        parent_key = "n25-parents-"+branch
        if target not in imports or parent_key not in imports:
            pending.append(target)
            continue
        count_import, parent_import = imports[target], imports[parent_key]
        count_task = contained(work, count_import["task_relative"])
        parent_task = contained(work, parent_import["task_relative"])
        count = count_import["report"]
        parent = parent_import["report"]
        count_root = contained(count_task, count["accepted_capsule_relative"])
        parent_root = contained(parent_task, parent["resource_capsule_relative"])
        contract_path = count_root / "contract.json"
        names = n25_parents.names(branch)
        resource_path = parent_root / names["resource_dir"] / names["resource_proof"]
        need(common.digest(contract_path) == count["contract_sha256"]
             and common.digest(resource_path) == parent["resource_proof_sha256"],
             "Exact imported fresh resource and accepted count contract bytes")
        contract = common.read(contract_path)
        resource = common.read(resource_path)
        original = None
        original_path = None
        if common.TARGETS[target][0] == "new-conditional-v14":
            reference = mapper.target_spec(target)
            need(reference["original_v12_reference_filename"] == "ORIGINAL_V12_CONTRACT.json",
                 "One literal original V12 reference filename")
            original_path = count_root / reference["original_v12_reference_filename"]
            need(common.digest(original_path) == reference["original_v12_reference_file_sha256"],
                 "Externally pinned original V12 contract file bytes")
            original = common.read(original_path)
        progress("n25_resource_count_interface_started", target=target, branch=branch)
        packet = mapper.validate(target, resource_proof=resource, contract=contract,
                                 original_v12_contract=original)
        need(packet["schema"] == "N25_RESOURCE_COUNT_INTERFACE_V1" and packet["target"] == target
             and packet["branch"] == branch and packet["numeric_interface_verified"] is True
             and packet["analytic_attained_contact_premise_acquired"] is False,
             "Complete simultaneous conditional resource-to-count interface")
        packets[target] = dict(interface=packet,
            mapper_sha256=common.digest(mapper.__file__),
            count_zip_sha256=count_import["zip_sha256"], parent_zip_sha256=parent_import["zip_sha256"],
            count_report_sha256=count_import["validated_report_sha256"],
            parent_report_sha256=parent_import["validated_report_sha256"],
            actual_contract_sha256=common.digest(contract_path),
            actual_resource_proof_sha256=common.digest(resource_path),
            actual_resource_receipt_sha256=parent["resource_receipt_sha256"],
            original_v12_contract_sha256=common.digest(original_path) if original_path else None)
        progress("n25_resource_count_interface_verified", target=target, full_n25_verified=False)
    return packets, pending


def cover(packets):
    """Check closed seams of exactly the seven selected replacement regions."""
    order = ("b4-q0", "b4-q1", "b4-q2", "b4-q3")
    expected = ["29/100", "117/400", "59/200", "119/400", "3/10"]
    for i, key in enumerate(order):
        need(packets[key]["interface"]["expected_p_interval"] == expected[i:i+2],
             "Four literal closed p quarters cover original B4 p29")
    order3 = ("b3-p31-v14-new", "b3-p32-v14-new", "b3-p33")
    endpoints = ["31/100", "8/25", "33/100", "17/50"]
    for i, key in enumerate(order3):
        need(packets[key]["interface"]["expected_p_interval"] == endpoints[i:i+2],
             "Three literal closed B3 panels preserve both seam endpoints")
    need(all(F(x) < F(y) for x,y in zip(expected, expected[1:]))
         and all(F(x) < F(y) for x,y in zip(endpoints, endpoints[1:])), "Ordered nondegenerate exact closed intervals")
    return dict(b4_p29_closed_quarter_endpoints=expected, b3_closed_panel_endpoints=endpoints,
                same_witness_analytic_implication_acquired=False, full_n25_verified=False)


def run(durable_root, work):
    from . import colab_batch
    work = Path(work).resolve()
    progress = lambda name, **fields: colab_batch.event(work, name, **fields)
    imported, missing = collect(durable_root, work, progress=progress)
    edges, pending = interfaces(imported, work, progress=progress)
    result = dict(schema="FRESH_CONDITIONAL_SEVEN_N25_INTERFACES_V1", status="WAITING_FOR_N25_EVIDENCE",
                  selected_interfaces_verified=False, imports=imported, interfaces=edges,
                  missing_jobs=missing, pending_interfaces=pending, conditional_premises=PREMISES,
                  driver_sha256=common.digest(__file__), **FALSE_FLAGS)
    if missing or pending:
        progress("n25_interface_join_waiting", missing=[p["job"] for p in missing], pending=pending)
        return result
    need(set(edges) == set(COUNTS), "All seven selected conditional interfaces")
    result.update(status="CONDITIONAL_SEVEN_N25_COUNT_INTERFACES_VERIFIED",
                  selected_interfaces_verified=True, selected_closed_cover=cover(edges),
                  total_selected_count_leaves=sum(imported[k]["report"]["census"]["leaves"] for k in COUNTS))
    progress("n25_seven_conditional_interfaces_verified", count_targets=7, full_n25_verified=False,
             all_index_conclusion_verified=False)
    return result


def run_colab(*, durable_root, work_root="/content/berry-esseen-runs", backup_interval=60):
    """Restore/inspect finished ZIPs; no search or numerical leaf replay."""
    from . import colab_batch
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:8]
    root = Path(work_root) / "n25-seven-interfaces" / stamp
    root.mkdir(parents=True)
    durable = Path(durable_root) / "n25-seven-interfaces" / stamp
    status = dict(state="started", selected_interfaces_verified=False, **FALSE_FLAGS)
    colab_batch.atomic_json(root / "SESSION_RESULT.json", status)
    monitor = colab_batch.Backups(root, durable, interval=backup_interval)
    monitor.start()
    try:
        colab_batch.event(root, "n25_seven_interface_join_started", jobs=list(JOBS), **FALSE_FLAGS)
        result = run(durable_root, root)
        colab_batch.atomic_json(root / "CONDITIONAL_N25_INTERFACES.json", result)
        status.update(state=result["status"], selected_interfaces_verified=result["selected_interfaces_verified"], result=result)
    except BaseException as error:
        status.update(state="PARTIAL_ERROR_NOT_ACCEPTED", error=type(error).__name__+": "+str(error))
        (root / "ERROR.txt").write_text(traceback.format_exc(), encoding="utf-8")
        colab_batch.event(root, "n25_interface_join_incomplete", error=status["error"])
    finally:
        colab_batch.atomic_json(root / "SESSION_RESULT.json", status)
        try:
            monitor.close()
        except Exception as error:
            colab_batch.event(root, "final_backup_failed", error=str(error))
        output = colab_batch.bundle(root, durable)
        colab_batch.event(root, "n25_interface_bundle_saved", path=str(output), state=status["state"], **FALSE_FLAGS)
    print("\nRESULT:", status["state"], "\nZIP:", output, flush=True)
    return dict(status=status, bundle=str(output), work=str(root))
