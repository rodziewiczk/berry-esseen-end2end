# n25 B3/B4: fresh INITIAL and resource acquisition

Notebooks 09 and 10 run separate B3 and B4 tasks. They can run concurrently with the missing count searches in notebooks 01–07. No historical INITIAL proof, resource proof or accepted parent result is imported as fresh evidence.

Each task performs the original four actions in order:

1. Construct the full INITIAL proof.
2. Replay it through the unchanged INITIAL acceptor, including all 12 corruption controls.
3. Construct all 100 probability resource panels using that newly accepted INITIAL proof.
4. Replay the complete resource proof through its unchanged acceptor, including all 12 corruption controls.

INITIAL covers all 12 feedback covers and their export, comprising 239,616 signed rectangles over 100 probability panels. The selected exact source closures contain 30 INITIAL files and 32 resource files per branch, bound to externally pinned complete manifests. Archive bytes, source inventory, parent proof hashes, panel census, actual return codes, capture hashes and actual Linux execution capability are checked separately.

Each action receives its own two-hour CPU ceiling, 512 MiB total address-space allowance split between controller and worker, and a 7,260-second external wall ceiling. These are ceilings rather than runtime estimates. The native single-process supervisor must establish its actual Linux capability; an unavailable capability leaves the action incomplete.

Progress is shown during execution and saved to logs. Drive backups run every minute; a final ZIP is saved on success, failure or interruption while the kernel remains alive. An action has no internal resume checkpoint. The programmatic `run(existing_task)` interface can revalidate completed local stages; the default notebook starts a new uniquely named task and does not automatically restore stages from another Drive session.

A successful four-stage result is a **conditional parent-chain acceptance**, not the unrestricted n25 theorem. In particular:

- The stronger24 auxiliary bound is an imported premise whose acquisition is not replayed here.
- The same-law analytic resource/count implications require their separate review.
- Every required count forest and its exact interface to these fresh resources must still be joined.
- The final all-index conclusion remains unverified.

The local infrastructure tests use synthetic small fixtures and source inspection only. They do not constitute a run of the INITIAL or resource mathematics. Actual mathematical computation belongs in the user's Colab sessions.
