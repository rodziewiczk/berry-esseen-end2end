# Seven count caches: independent handoff inventory

Reviewed on 2026-10-23 after the last original session ended. This is a source, transport and JSON topology audit. No mathematical kernel was imported, no search or leaf acceptance was replayed, and no Drive file was changed. The seven original sessions ended naturally; this review did not stop them.

## Preserved final candidates

All seven final exported ZIPs are available locally. Every row below was checked against the actual ZIP bytes, rather than inferred solely from a progress message or Drive listing. All candidates have 26 roots in the exact order `k=0,...,25` and retain pending nodes.

| Target | Run stamp | Final state | Nodes | Leaves | Splits | Pending | Maximum saved depth |
|---|---|---|---:|---:|---:|---:|---:|
| `b3-p33` | `20261023T104452Z-27bcc48d` | Search time budget exhausted | 9,004 | 4,500 | 4,489 | 15 | 22 |
| `b4-q0` | `20261023T102119Z-6c7d4fc5` | Search time budget exhausted | 5,736 | 2,865 | 2,855 | 16 | 24 |
| `b4-q1` | `20261023T102126Z-6b60dd82` | Search time budget exhausted | 5,858 | 2,920 | 2,916 | 22 | 23 |
| `b4-q2` | `20261023T102233Z-af459eba` | Original 10,000-node budget exhausted | 10,000 | 4,996 | 4,987 | 17 | 20 |
| `b4-q3` | `20261023T102325Z-b23b6768` | Search time budget exhausted | 6,828 | 3,404 | 3,401 | 23 | 20 |
| `b3-p31-v14-new` | `20261023T104235Z-241928db` | Search time budget exhausted | 2,656 | 1,322 | 1,315 | 19 | 22 |
| `b3-p32-v14-new` | `20261023T104633Z-40db3a7f` | Search time budget exhausted | 2,948 | 1,469 | 1,461 | 18 | 19 |

These are topology counts, not a completion percentage or an estimate of remaining runtime. The maximum saved depth is the observed tree depth, not an exhausted depth allowance. For the specific q2 stop and the independently reconstructed closed split geometry, see [the q2 review](b4_q2_node_limit_review.md).

## Checks actually performed

For each actual local export:

- Recomputed the whole ZIP SHA-256 and the final main checkpoint SHA-256 and byte count.
- Checked that the main and backup checkpoint bytes are identical and that their digest and size match the final saved execution receipt.
- Recomputed every hash in the saved `FROZEN_DESIGN.json`: 76 frozen files for each of the five V12 targets and 178 frozen files for each of the two portable V14 targets. No frozen input was missing or mismatched. The V12 capsules contain exactly those files plus the design. The V14 capsules additionally contain the preparation report `SOURCE_PREPARATION_REPORT.json`; it is descriptive preparation output, not a frozen mathematical input or an acceptance receipt.
- Checked the actual design digest against `TASK.json` and checkpoint bindings. Checked the actual checker and contract digests against the checkpoint header, and all 71 V12 or 175 V14 kernel/input digests in that header against actual capsule files.
- Parsed all saved trees, checked their 26 ordered root labels, and counted `leaf`, `split` and `pending` records; every split had exactly two node children.

All seven tasks record source commit `75a94708872e2bc053f42a279559b23ed91e4402`. For the two V14 targets, this is the input source provenance; their portable conditional source epochs are explicitly new and do not recover historical V14 identity. The saved V14 capsules contain historical parent material as bound conditional inputs. Preserving those bytes does not acquire the parent facts afresh.

All seven checkpoints retain `arithmetic_accepted=false`. Session native acceptance, parent acquisition and all-index conclusion flags remain false. This audit does not verify mathematical leaf predicates, a complete forest, native acceptance, fresh auxiliary premises or a theorem-level join.

## Immutable backup identifiers

Each ZIP filename is the run stamp from the table followed by `-results.zip`.

| Target | ZIP bytes | Actual ZIP SHA-256 |
|---|---:|---|
| `b3-p33` | 2,710,250 | `a7477a3d78dec87bc29138c822f756000265881d342911df034889a9eba6c1a8` |
| `b4-q0` | 1,438,916 | `fa5a1daf1df3a20be753be8eac569642daef930cd92c0b6506a0661598f0fd51` |
| `b4-q1` | 1,290,334 | `1f753d70ace9629c1c6b6e2f61327346bbdd1a42d607c86a57403d7f01c568cc` |
| `b4-q2` | 1,913,858 | `84a5272daa9858e66c369f18365bf5f17568dd912e9901cfc0c5c1859a9972f0` |
| `b4-q3` | 1,461,950 | `fb596733440941f19de99359703db686cdca5a940bef5400eecd5b7a0641a785` |
| `b3-p31-v14-new` | 38,739,799 | `a16459f5ea03a9b3561ee8bdf53dffccffb265dc03d5f1a386a48fca8629135d` |
| `b3-p32-v14-new` | 45,297,235 | `35b7bf6a65122a0f335dea0363f9809726e5592e78a7492c27da8da6dea8cc7c` |

| Target | Final checkpoint bytes | Actual final checkpoint SHA-256 |
|---|---:|---|
| `b3-p33` | 1,633,316 | `172d0df2de17899af7f0a71b74db99af15f805a2584dd60a62a03b31eb7a3d1b` |
| `b4-q0` | 1,010,067 | `0c327ca9d37fd524b7f26ea3237a970ed8f855a54e0aa95874c2ee71451cfa7e` |
| `b4-q1` | 927,520 | `be78adf26a67657278efd77ba73ebba056f629ed613cde2babb8720c22bb269e` |
| `b4-q2` | 1,733,980 | `c08d59310fad35069c8d368629cdb0e2a902c39fff0deab9696f4b22bdc609e1` |
| `b4-q3` | 1,232,300 | `2991a74b36f0bbe35dd951398ce7d7c835f31bca714a1d588fabe777ad0f4009` |
| `b3-p31-v14-new` | 12,053,533 | `16259cd78342f92486a4b1fee5d04cc028d02ae63a52d5d9c7ae63e68cce26da` |
| `b3-p32-v14-new` | 13,577,039 | `5917cb637e17b0435be5f218a623fb013a37ab62ef383804a745cd5cfd477e8a` |

## Connected Drive evidence and its boundary

The connected Drive root, seven target folders, latest run folders and their `live/task/capsule` folders were listed read-only. The small `SESSION_RESULT.json`, `LIVE_SNAPSHOT.json`, task records and available final search receipts were read as JSON. Every read backup marker reported an empty `skipped` list. The final checkpoint and backup files were independently visible in folder metadata for all seven targets. Their observed sizes agreed with the local exports at the corresponding snapshot; the p32 files advanced during this inspection and its final local export supersedes the earlier metadata snapshot.

Drive folder existence and a reported checkpoint digest do not independently prove remote file bytes. The connector metadata response did not expose the requested provider checksum fields. The two larger V14 capsule folder listings were partial at 100 files. No remote ZIP was downloaded or decoded. Consequently the complete byte and source-closure checks in this report are established by the actual local exported ZIPs, not by an unverified assertion that the current remote tree is byte-identical. Drive IDs, account paths and raw private logs are intentionally omitted.

## Compatibility with the new resource epochs

Independently read `be_replay/count_limit_epoch.py` at SHA-256 `5b3c2d17f1f566353e767c114628ac1940d6ca9f4d095771df2176589e5dfbe6`. Applied only its source/AST derivation to the actual original design and checker bytes from each of the seven exports; no mathematical source module was imported. All seven externally pinned original design, original checker and contract digests matched. All seven deterministically derived design and checker digests matched their declared profiles. Every original non-checker input digest, including V14 source-epoch and parent input records, was preserved.

The checked transformation changes only the top-level `LIMIT=10000` assignment to `LIMIT=100000`; both uses remain the original `visited<=LIMIT` resource guards. The entire source AST otherwise agrees, and all function ASTs agree. The q2 public aliases preserve its previously published profile bytes. Each derived capsule seals the original design, original checker and explicit resource-policy metadata. Verification rejects extra helpers and directories and permits only the explicit native forest/acceptance JSON outputs beyond the sealed inventory.

The available bytes therefore support a cache-preserving handoff for all seven jobs. The replacement runner must still perform its own full original checkpoint validation, geometry checks, explicit migration to the newly sealed resource identity and fresh native acceptance after search completion. A checkpoint is untrusted search state throughout migration. This inventory neither promises that 100,000 nodes will suffice nor promotes a resource-extended result into original-profile or global proof acceptance.
