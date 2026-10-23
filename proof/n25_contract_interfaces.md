# Seven n25 resource-to-count contract interfaces

`be_replay/n25_contract_interfaces.py` checks an exact rational parameter edge. It imports only Python's standard library and does not import, replay or accept a numerical proof kernel. A successful report is conditional. It does not acquire a resource, validate a native execution, establish the physical same-law premises, discharge attained contact, or establish the full n25 union.

## Public interface and evidence boundary

```python
validate(target, *, resource_proof, contract, original_v12_contract=None)
target_spec(target)
canonical_sha256(json_object)
```

The seven targets have the same identifiers as `count_task.TARGETS`. `target_spec` exports the literal branch, original resource panel, closed count interval, rho interval, optional quarter, and original V12 reference filename/member/SHA-256. `validate` returns schema `N25_RESOURCE_COUNT_INTERFACE_V1` only after all checks succeed. Malformed, missing, unknown, incompatible or inexact inputs raise `ValueError`.

The caller must first revalidate the completed 09/10 parent and 01–07 count evidence, its source closure, actual captures, execution controls, full arithmetic census and dependencies. It must bind the actual original file-byte SHA-256 values. The mapper receives already parsed dictionaries, cannot detect duplicate keys discarded by an unsafe JSON loader, and cannot certify execution or original serialization. The caller must use its duplicate-rejecting bounded loader.

Reports additionally bind the parsed objects by SHA-256 of ASCII JSON with sorted keys and compact separators. Floats and non-JSON objects are rejected. This canonical binding is explicitly distinct from an original file-byte hash. The mapper does not mutate any input. Historical `source_inputs_sha256` maps remain copied provenance; their old timing-bearing resource-acceptance hashes are not required to equal fresh acceptance bytes.

## Selected domains

| Target | Parent row | Closed count p interval | Literal rho interval |
|---|---:|---|---|
| `b4-q0` | B4 p29 | `[29/100,117/400]` | `[7/5,3/2]` |
| `b4-q1` | B4 p29 | `[117/400,59/200]` | `[7/5,3/2]` |
| `b4-q2` | B4 p29 | `[59/200,119/400]` | `[7/5,3/2]` |
| `b4-q3` | B4 p29 | `[119/400,3/10]` | `[7/5,3/2]` |
| `b3-p33` | B3 p33 | `[33/100,17/50]` | `[13/10,7/5]` |
| `b3-p31-v14-new` | B3 p31 | `[31/100,8/25]` | `[13/10,7/5]` |
| `b3-p32-v14-new` | B3 p32 | `[8/25,33/100]` | `[13/10,7/5]` |

The four B4 intervals cover the original closed `[29/100,3/10]` panel, including their shared endpoints. Their contract metadata binds the original parent contract SHA-256 `e7274cc690ea04ae3b9ce837986e006b9c538dd42d70c42cca5ecd87b23a1934`. Every scalar and acquired-moment bound remains the one constructed for that whole original resource panel. Narrowing p does not authorize recomputing or strengthening its contract fields.

## Exact reconstructed mappings

The independently transcribed mapping source is archive member `cutoff25_20261011/new_root/prepare_global_theta_count_v2.py`, SHA-256 `57977808d95691aec623ccde4c209a8e0e15c711c70281a72d0419f2b1b7dcd0`, especially lines 24–49. It was read as source; no original imports or top-level execution were used. The closed-quarter source is `new_root/prepare_stoploss2_quarters_v11.py`, SHA-256 `07efb2d7e05c00eeaed26747d8ad0c682f282419f1aef9ca7bd58ebad16f999a`; later selected ports preserve those parameters.

For a rational x, the source uses `upper(x)=(ceil(10^6 x)+1)/10^6` and `lower(x)=(floor(10^6 x)-1)/10^6`. The extra unit is intentional even when x is already on the grid. The mapper reconstructs exact reduced fraction strings and requires complete dictionary equality for the resulting row, rather than accepting approximate equality or an unrelated scalar maximum.

It requires the matching whole resource schema, zero barrier and branch rho profile; all 100 ordered resource rows; one surviving selected row; and the same original panel in the exported resource result, raw row and INITIAL seed. It checks these simultaneous mappings:

* D, d0, Lambda, both H caps, both support radii and both outer caps are rounded upward. D is not rescaled, and the joint Lambda intercept is not replaced by another quantity.
* Binary, gap and noise prices are rounded downward; the binary price is clamped below at zero. Positive divisors and the positive gap/noise prices are checked.
* All six simultaneous quadratic planes retain their order. A, Fplus and Fminus round upward; Qbudget rounds downward and must remain strictly positive. All 24 coefficients are checked. The original complete signed-envelope implication is also checked independently for both signs and every source plane: the minimum of the quadratic difference on the full closed `[0,Hplus]` or `[0,Hminus]` interval must be nonnegative for at least one target plane. Endpoints and an interior convex vertex are included. The report contains all twelve mappings and rational margins.
* The exact `ACTUAL_SIGN_CONDITIONED_MARGINAL_V1` dictionary, its conditional zero-mean boolean and its declared conditional resource status are required. Each positive endpoint floor is `lower(max(raw endpoint, INITIAL endpoint))` and must remain strictly positive. This verifies the dictionary and rational implications; it does not prove their physical-law theorem.
* Signed beta uses `[max(raw beta_lo, seed beta_lo), min(raw beta_hi_signed, seed beta)]`, with outward rounding and clipping to `[-1,1]`.
* The mean floor is the downward `10^-12` grid square root of `(1-raw theta)*min(pl*(1-pl),pu*(1-pu))`, using the original whole resource panel. Integer-square-root construction is checked by both `floor^2 <= square` and `square < (floor+10^-12)^2`. The mean interval intersects this floor with the raw/seed mean bounds, then rounds outward and clips to `[0,1/2]`.
* Raw theta lies in `[0,1)`, its upper-rounded contract cap remains below one, and signed beta/mean intersections are nonempty.
* The original exported rho upper bound is intersected with the literal independent branch ceiling. The intersection must be nonempty and dominated by the unchanged literal count rho interval.

There are 43 individually recorded rounded-field checks, twelve signed quadratic checks, and a separate complete domain/premise dictionary record. Complete reconstructed-row equality rejects unexpected fields, wrong types, changed scalar constants and altered sign-premise metadata.

## Two new V14 contracts

For p31/p32, the caller must provide the source-bound `ORIGINAL_V12_CONTRACT.json` reference. Its original archive members are `new_root/global_alpha_stoploss2_b3_p31_v12/contract.json` and `new_root/global_alpha_stoploss2_b3_p32_v12/contract.json`, with SHA-256 values:

* p31: `8efeda84e286785b13016738d88bf229d1386f3ce8194dfee868e319fe53862c`
* p32: `69a5b51120045874f3a02514aac3d258a7842f33502c05157e08486c9895fe16`

Those original file-byte pins are exported by `target_spec`; the collector must verify them against the supplied bytes. The mapper requires the **entire** current contract to equal that original dictionary with exactly two fields inserted into its one row: `local_contact_allowance="5/16"` and the precise `ATTAINED_POSITIVE_CLOSED_CONTACT_V1` dictionary with sample size 25 and all three booleans true (`same_unrestricted_attained_witness`, `positive_closed_threshold`, `score_at_least_CE`). All original resource fields, provenance and scope must be unchanged.

That syntactic identity and the rational parameter implication do not establish the additional same-witness attained-contact hypothesis. A matching global auxiliary `C24 < CE+1/80` supplies the predecessor allowance `q25 <= 5/16` only through the retained same-law analytic argument. The report leaves `analytic_attained_contact_premise_acquired`, `physical_same_law_premises_acquired`, both fresh-execution validation flags, native arithmetic acceptance, full n25 and all-index conclusions false.

## Validation actually performed here

Fourteen small synthetic test methods pass, including all seven successful target shapes, every rounded scalar and every quadratic coefficient, outward-grid edge cases, both signed envelopes, the convex interior vertex, positive endpoints, closed quarter seams, whole-panel mean-floor use, exact square-root neighbors, incompatible rho/panel selectors, missing/reordered global rows, complete V14 dictionary preservation, changed provenance hashes, nonmutation and rejection of floats/booleans/unknown fields. No real proof resource mapping or mathematical kernel was evaluated locally.

A separate read-only static audit compared the archived five original contract shapes and the two already prepared portable V14 contract shapes with the mapper's expected field sets, six-plane counts and literal p intervals. The two portable dictionaries were compared with their pinned V12 references plus exactly the two fields above. This is compatibility inspection, not fresh arithmetic acceptance. The observed contract file hashes were:

| Target | Contract file SHA-256 |
|---|---|
| b4-q0 | `6da0412a35fa160d9eef1e88e1ace38eb3b8425ecfd5a4fce0f3eaf3ce5b2535` |
| b4-q1 | `15e13d70c655faf449825b355c8b22dffcf5efef4fb704f9d65e1425aae00c35` |
| b4-q2 | `0576748a8e4deb2450fea8fc7b1b06898dd8bd3ae2d5fc3465163a123d9425c3` |
| b4-q3 | `07cabb29930701f591d9822eac130afd1bdfc81cbb5e69b73f569b70f6151f75` |
| b3-p33 | `fe106d1ffe295de3fa68ccf44a625323fe0e68ce1c4462730729b5b2e0e3963a` |
| b3-p31-v14-new | `9b71a135188234ba200ae145860659f4def488aec9feec278748f8e31eafd142` |
| b3-p32-v14-new | `0019e13d3857849762eed1518ad63c3f6aa6133dde0fd84a9ea88674f6e34627` |

The next collector can call this mapper on the actually revalidated exported objects. Those fresh comparisons and the remainder of the n25 regional union are pending.
