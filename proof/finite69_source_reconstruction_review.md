# Finite7–9 source reconstruction and fresh-parent metadata boundary

Date: 23 October 2026. This is a fallible internal source/metadata review by the same AI system, not external independent mathematical verification. Only supplied ZIP bytes, JSON, hashes, source text and ASTs were inspected. No original mathematical module, construction, evaluator or acceptor was imported or executed.

## Result

All nine missing INITIAL `INPUT.json` copies can be restored byte for byte, and all nine missing `PREPARED.json` files can be reconstructed with exactly the external original SHA-256 commitments. The original batch candidates are physically supplied in the combined archive and independently duplicate the later resource-capsule candidates. The historical timed INITIAL acceptance receipts remain absent in the bounded two-archive search; they must be freshly computed and explicitly rebound, never fabricated.

## Exact source inputs

| Archive | Bytes | SHA-256 checked in this readback |
|---|---:|---|
| `cutoff6_20261020.zip` | 69,459,175 | `d45b1f99ca01ea4d1cfad445fdab3c48a508adf9fdcda17b6cded5236d77b8d6` |
| `cutoff5_10_15.zip` | 224,483,065 | `268f71662171764d7ebe116910b5df82dfd58cadb2de2a7ef82db7da98b66dae` |
| `cutoff20_20261016.zip` | 31,681,776 | `b1dd7e730187f62142faa1e82eff5a9fd13a879e933a2fafbd22af8a4709ef83` |
| `cutoff25_continue_20261015.zip` | 37,200,633 | `2b848227a5f5e2f54f210a347829c6b3f1c56bd656ef0cf01482a7898e11d63a` |
| `cutoff25_rethink_20261015.zip` | 6,398,244 | `47503aa52408b24243e554a080730f3d546c7ad425a5480af16e40678310f43b` |

The primary selector is `work/cutoff6_20261020/root/final_composition_v2/CUTOFF6_COMPLETE.json`, SHA-256 `c73ca47d7a4c8ccffd6c84be4d2805db4c43e86693989dd478b1ecc327517579`. Canonical `work/` paths in these tables are archive/runtime identities, not personal absolute paths. For the two primary archives, remove `work/` to obtain the archive member.

Common INITIAL preparation sources:

| Canonical suffix under `work/cutoff6_20261018/analytic/initial7_9_accept_v1/` | SHA-256 |
|---|---|
| `prepare.py` | `cf90569d44013cfa4360baf52880db53d4634bbd7e6679888aea8f3c281a346a` |
| `replay.py` | `dfd8d2b820f1e221eaed0e6b515649a9b15dc71e66af78f947330bb8129ad5ab` |
| `PROOF.txt` | `24f909ab438ed8d4a39e588198ea60fe7a2248b2983adeb7c09a65f4ebbc1900` |
| `SOURCE_PREPARED.json` | `5976edb922dcfc7d3b992534a2dbf23f7b0a369daa87b82bee571e96f62e9b97` |

The complete `SOURCE_PREPARED.files_sha256` inventory has 97 rows; all 97 physical files were read and matched their pins across the two primary archives. Its `original_source_graph` has 54 rows and equals each supplied candidate's source graph.

## Exact nine-case aliases and reconstruction

For each case `nN_BAND`, the following three paths have the same candidate bytes:

- Combined member `cutoff6_20261018/analytic/initial7_9_batch_v1/INITIALN_BAND.json`.
- Primary cutoff6 member `cutoff6_20261020/entry/resource7_9_accept_v2/nN_BAND/INITIAL.json`.
- Restored canonical `work/cutoff6_20261018/analytic/initial7_9_accept_v1/nN_BAND/INPUT.json`.

In the next table the candidate pin matches both the origin and INPUT pins in the final graph. The PREPARED pin is the independently reconstructed output. The last column is the missing historical timed acceptance commitment, not a newly available receipt.

| Case | Candidate/origin/INPUT SHA-256 | Reconstructed PREPARED SHA-256 | Historical missing REPLAY_CHECKED SHA-256 |
|---|---|---|---|
| `n7_B0` | `d626302d683539042ae69af61b3006c0269efa50cfe29b20f29e75067a0135a3` | `d40735c4a7c8ad6e8177b8e0c5c40f490d68b7fe0fbce82ca96080db40ee176e` | `0ac2c56b36e27d99acc94af3d7c2652302c7b4bd2c988ff0720e861fcdc4c19e` |
| `n7_BN` | `e873a42ee6fb3a27406857c97fabc97a18d3b805fba40543f74efbd47fcde6ab` | `e6add083b789257bb130e5fb12bd90cf7aa22021c9add6b26ee60ea59492bfeb` | `66a7feb37f7f7250ab6b4d32fcda526a0d1cf31059d507ccd405cf1a760e4e11` |
| `n7_B2` | `9e936898c34d3fc538ef90f10b95e8c8e153671edb55a3b5e7f81f94374847bb` | `54cd1db99f0a08e3b4e395216053d8212745dccdae88865121da07b1cf7c05ca` | `7ffbb2ec90fb87d616471b9cb5c38382c4d901584fd44af2a5f61ddc4a68f0f3` |
| `n8_B0` | `54d9aa1d9d61d3ff3dee0ee5466a7e43cdf8a3f171b3be8687bb181bba3a9721` | `4504c64f3195e39f7dce052c437f0d12422926dcec3d4102ec7fea9893ae5a3d` | `53af260b119d2fbda91d853ef62b67a4533b7314b45f9681bf0f5b278e6ffa72` |
| `n8_BN` | `1d771f14279725f6377447c44b3e6e9a090acfe3ddf07765f1be4fd8e704d938` | `207bc34f9c933e553e47aed27514ea24222ec7948009b368d9b580059e15ff49` | `56ad9d5334cbf3d112f1d252c54a314fe1e07c8b1f04882e802cb921f7c79fd5` |
| `n8_B2` | `3d924ca0e2e184e61ba1ead2932fa9023924fef6a3dc7a4f442d87fa02274278` | `b95827f09bdea2f68c11dbac56210a600d50e7c8038fab509c2d60750e6414cd` | `c5af0ee0f14e95c4e0bdb0a80f4413fe532a3909153542e219e6ab69ff219a78` |
| `n9_B0` | `2a13772abaf84f516fa67c4463feb9040db0b180f7e05b5fe498ae0b2591bc83` | `dc4c3e14dc0d2c0ec91e2d2974e1090af159910a2e904dc036a7c29075df20ee` | `9a87f19d295f59fddedc4a84bcdb24560705dbbb0f8921623ff891d902d87fef` |
| `n9_BN` | `fd4476ca0469df954ead50b168872a8f61aab84a2822fa7311d69cb512f3a923` | `63918e21f7bb3ab5c822409b06666c2d4fc5b01e0dc2523e577e29b06eea3226` | `b0a653181f6ebf93b1088b25bfab6a4b41a8bb50c1f22ed1a346cd7b922c2e0f` |
| `n9_B2` | `e46b13e20aa8ae883556bb49546a81f53b9bfc9b682b233f60c726b774b1e294` | `3ef82cb2e8641f9b7c3efa21bacf36262b3d38aa54e6bf772d750c112a09b85e` | `3ff22b3af8ef509f1a8d99b66bb59998f63a579912695f577904a26471aabac6` |

The exact original `prepare.py` metadata algorithm (lines 11–17) starts with the ordered 97-row source dictionary, then inserts the origin, INPUT, SOURCE_PREPARED, prepare.py, replay.py and PROOF.txt paths in that order. It serializes the resulting job with `json.dumps(indent=2)` and a final newline. The job contains `n`, `band`, `input_path`, `input_sha256`, `original_source_graph`, `files_sha256` in that order. POSIX slash path spelling reproduces every external PREPARED pin; Windows backslash spelling does not. This is deterministic metadata reconstruction, not nine-stage numerical replay.

`be_replay/finite69_metadata.py::reconstruct_prepared` implements this byte-only operation and requires all external source/candidate/output pins. It rejects a missing or changed external PREPARED pin, duplicate JSON keys, malformed inputs, wrong cases and source inconsistencies.

## Fresh INITIAL to resource epoch

The original INITIAL replay writes `seconds=time.monotonic()-began` into its acceptance receipt (`initial7_9_accept_v1/replay.py:100–101`). That old acceptance byte stream cannot be inferred from a successful candidate or reconstructed preparation. A fresh completed INITIAL run must supply its own receipt and actual execution evidence.

The selected resource replay is `work/cutoff6_20261020/entry/resource7_9_accept_v2/replay.py`, SHA-256 `6bcff8b60eb00c3422a0aec0d9382157669617fcfa526e466ad1618bd88b3470`. Each original resource PREPARED has eight fields and 357 graph rows; SOURCE_RESULT has thirteen fields and 331 graph rows. All nine source packets contain ordered indices 0–99, 100 complete row candidates, the original old INITIAL cap, the tighter same-index resource cap and the historical INITIAL receipt hash.

The metadata-only helper `derive_resource_epoch` returns `replay_bytes`, `fresh_prepared_bytes`, `fresh_source_result_bytes`, `report`. Its explicit new identity preserves the original script and both original candidate files separately. The derived PORT_REPLAY changes exactly two PREPARED filename literals and three SOURCE_RESULT filename literals to their FRESH names. Its fixed SHA-256 is `ad817754825d81d1ca7a560a6f029fc3cd8aeef4d366d869113be1ff7d6ce637`; reverse normalization gives identical original bytes and AST.

The FRESH source packet changes only the top-level INITIAL receipt hash and that same parent path's graph hash. The FRESH preparation changes only its source-file hash, the same parent graph entry, and adds the actual FRESH_SOURCE_RESULT file commitment. The original SOURCE_RESULT/provenance hashes remain preserved. Full JSON reverse-difference checks preserve every row, numeric result, profile, cap, status and duration. The helper requires the same literal n/band, exact INPUT hash, sharp-predecessor/contact-zero premise and original INITIAL owncap. The calling controller must independently validate the actual complete fresh INITIAL execution before invoking it; the helper's report explicitly leaves that evidence verification false.

The unchanged resource arithmetic then recomputes every ordered row through the original `core.resource` call and compares its whole result, including its retained support plan (`replay.py:59–70`). The helper itself performs none of these calls and cannot accept a resource stage.

## Separate CAPS ancestry boundary

The resource replay also imports `work/cutoff6_20261020/entry/resource7_9_v2/CAPS_CHECKED.json`, SHA-256 `616bb25496af353963f74f9165342cd5fe85ba387bc5cb49e161199955b5ac08`. Its status/cap lookup is checked at replay lines 37–38 and every one of its 182 ancestry hashes at line 39. This boundary is separate from the fresh INITIAL timestamp binding.

Exactly 96 of those 182 referenced files were found with their required hashes in the two primary assets. The other 86 are inventoried below. Additional supplied cutoff20/25 archives resolve 74 exactly; an existing source-only n5 cache resolves 50, with overlap. Their union leaves nine owncap run files unavailable in this bounded lookup. Those nine are not claimed globally absent from every possible user package.

Additional archive matches by asset: `cutoff20_20261016.zip`: 49, `cutoff25_continue_20261015.zip`: 11, `cutoff25_rethink_20261015.zip`: 14. The 2026-10-11 and 2026-10-13 cutoff25 baseline ZIPs and final cutoff20 continuation were also queried at exact/suffix member paths; they supplied none of the remaining nine owncap run files in this pass.

For each extra-archive work path below, its verified member is the canonical path with `work/` removed. “n5 source cache” means only that the corresponding previously prepared local source bytes were read and hash-matched here; it is not a new durable public asset mapping or fresh arithmetic acceptance.

| CAPS referenced canonical path | Expected SHA-256 | Exact located bytes in bounded lookup |
|---|---|---|
| `runs/cutoff25_rethink_20261015/scale_analytic/kappa_62_625_01/metadata.json` | `9bc09745362c8caa1e24de97e3a442c1fcca8406c118852b7295976adcc7c93e` | n5 source cache |
| `runs/cutoff25_rethink_20261015/scale_analytic/kappa_62_625_01/stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | n5 source cache |
| `runs/cutoff25_rethink_20261015/scale_analytic/kappa_62_625_01/stdout.txt` | `163bf7eff250f62806ee308eab31d71fc1f35da49fdf625675071387b08b0031` | n5 source cache |
| `work/cutoff20_20261016/fourier/PORT.diff` | `bcb067893a80fa5d294db02600b6bb7a139201e897abb9adff56304ce33772da` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/PROOF.txt` | `e31638ee8444ef66e6b752a392823e34781a602894799393c1f4047ecf0c71e9` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/batch.py` | `6afbd94977681730b63a406087c948622155c50720a18a36f3868d4f87f2f164` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/controls.py` | `9f298e23550e9366048c64570a996000912d47004a1ff5cb1575e5fe20d35a63` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/discovery.py` | `0f484fc8d7ef8eeca811cb0678af32be937180a3241e35cbd938e8e517862bc7` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/integrate.py` | `e4bda2d00d905bf0963ca6f48d62c7d52a831e14cc695a2bae18183239bb64fc` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/jet.py` | `8decccac51b92cf58b3275e291b83e775da85cd9032f81501e9592d11d591329` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/kernel.py` | `a0c2c5f0aaa1c216ae2c9c796a1e17c88217049e4b30f844e9bb7979c0cb944e` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/pilot.py` | `107c6d85a6ba8b530ededa8868276433418b68298098ad39c4b5a52f10f7e301` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/run.py` | `df6d99c397ddf1b5eed0e589dc849755f76ed5e25891e568ac5acc1e2e7ab3fb` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff25_continue_20261015/analytic/universal_zeta_v1/CHECKED.json` | `04a8c2110951e551a7e46711e57ef8384a1b9b47e31cba75a01702db260a6400` | `cutoff25_continue_20261015.zip`; n5 source cache |
| `work/cutoff25_continue_20261015/analytic/universal_zeta_v1/PROOF.txt` | `6f68c67bab4f198b20388e108a0d5564593bcb1f36f047fa6aff1454ebc4c66c` | `cutoff25_continue_20261015.zip`; n5 source cache |
| `work/cutoff25_continue_20261015/analytic/universal_zeta_v1/check.py` | `60816afdefba8b65c673a22f7edf39f8a594d5dae53ff9a8577ebed0635fecc3` | `cutoff25_continue_20261015.zip`; n5 source cache |
| `work/cutoff25_continue_20261015/root/taylor_circle_v1/PROOF.txt` | `cc0545ed99ff8c247bcf64f05753e42c883432cfc4276c0a34e6c6d8b52f973c` | `cutoff25_continue_20261015.zip`; n5 source cache |
| `work/cutoff25_continue_20261015/root/taylor_circle_v1/integrate.py` | `cfac1967b1ff7a0dfb5e77f9bd1ee96edac7f9ba8a185df7aae64d09bc0f86d0` | `cutoff25_continue_20261015.zip`; n5 source cache |
| `work/cutoff25_continue_20261015/root/taylor_circle_v1/jet.py` | `8d4ecba05181cb71c9d122bc355e5a124d356662f5b30c0be82dc30c4fda5dc1` | `cutoff25_continue_20261015.zip`; n5 source cache |
| `work/cutoff25_rethink_20261015/repo_iid/source/paper/upper-0423.tex` | `a80bc131732539fd4d9a1a125501b7a6e122ce65381e6b26f2fde764c36f9220` | `cutoff25_rethink_20261015.zip`; n5 source cache |
| `work/cutoff25_rethink_20261015/repo_iid_low_v1/ZETA_CIRCLE_PROOF.txt` | `79ccb6400d557744e015ffa90a00ee9262b92a558b361e2dfcc6fcd03b2de3dd` | `cutoff25_rethink_20261015.zip`; n5 source cache |
| `work/cutoff25_rethink_20261015/repo_independent/FOURIER_AUDIT.txt` | `40acdf27ea60aa7a792927009e39e7f33c6609c90461e65134818247f619227b` | `cutoff25_rethink_20261015.zip`; n5 source cache |
| `work/cutoff25_rethink_20261015/root/FOURIER_REDUCTION_V2.txt` | `7389d85b02adbef18d598d57d97bdf93b9fe76502b826ed405fd54b95d5d40c6` | `cutoff25_rethink_20261015.zip`; n5 source cache |
| `work/cutoff25_rethink_20261015/scale_analytic/fourier_absmean_v1/PROOF.txt` | `df92603993c8b3ef4bab8767d3db7c21e694fc7d78661845b306dfd0e68dc0fc` | `cutoff25_rethink_20261015.zip`; n5 source cache |
| `work/cutoff25_rethink_20261015/scale_analytic/fourier_absmean_v1/batch.py` | `04045148b9e86dc4d92357d09642c04218ed2ea6f8ed27b5e7796a159f85b39e` | `cutoff25_rethink_20261015.zip`; n5 source cache |
| `work/cutoff25_rethink_20261015/scale_analytic/fourier_interval/PROOF.txt` | `e88f28253b08150ea49443c25888cfabe0e432492534b4f354a27b4d84fdbb9b` | `cutoff25_rethink_20261015.zip`; n5 source cache |
| `work/cutoff25_rethink_20261015/scale_analytic/fourier_interval/kernel.py` | `a0c2c5f0aaa1c216ae2c9c796a1e17c88217049e4b30f844e9bb7979c0cb944e` | `cutoff25_rethink_20261015.zip`; n5 source cache |
| `work/cutoff25_rethink_20261015/scale_analytic/kappa_62_625_v1/CERTIFICATE.json` | `02dc46c334ec9c9cbf0e7bb4c982869c6e3e0649a915169d3542b8820b51aac7` | `cutoff25_rethink_20261015.zip`; n5 source cache |
| `work/cutoff25_rethink_20261015/scale_analytic/kappa_62_625_v1/CHECKED.json` | `163bf7eff250f62806ee308eab31d71fc1f35da49fdf625675071387b08b0031` | `cutoff25_rethink_20261015.zip`; n5 source cache |
| `work/cutoff25_rethink_20261015/scale_analytic/kappa_62_625_v1/PROOF.txt` | `6645891bc75553f1a35faba00dd2a09e6b47c5fd374e637d83d62ec82069c162` | `cutoff25_rethink_20261015.zip`; n5 source cache |
| `work/cutoff25_rethink_20261015/scale_analytic/kappa_62_625_v1/controls.py` | `331ee713e7950c9013d969b70de5809d4eb7e37ac34cd22a6184e0f8872fe4b5` | `cutoff25_rethink_20261015.zip`; n5 source cache |
| `work/cutoff25_rethink_20261015/scale_analytic/kappa_62_625_v1/kernel.py` | `16170505dece7571725e4e601f1546989d546ed64685616f9d13283c59702b0a` | `cutoff25_rethink_20261015.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/MANIFEST.json` | `1e4f2d719b84fb065b8184b8b924b57e2ce40608ce436da60c002dd09daf49da` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/coupled_v1/floating.py` | `81b9ab30b41be9068631a4d2e08a93a17bdb3d11f0278345f267802d2d8e8197` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/coupled_v1/discovery.py` | `ade826727fcf4c28b324ef35f8da316cd5b81c4830246164eb41dfd7590c02db` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/coupled_v1/PROOF.txt` | `946a84b93fd337cb2a7d7a4e40f58919f5baf3658fe6a726f5f974e1430c193f` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/coupled_v1/FLOATING.diff` | `d66c81004069e15f18233eaa63601d64e906e93a1b7f8adfb13fe930ad83bdc2` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/coupled_v1/run.py` | `7e4e12c8dcb0d4e1ad9bb2ca6cd48dc7bca77c8041cfe6b36fdc2eedd7089dce` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff25_rethink_20261015/repo_independent/FINAL_RHO130_REVIEW.txt` | `1082d42b360d65ba2b27ad4f7cf4913bc8e6d40e60517e36c578870d14f9695b` | `cutoff25_rethink_20261015.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/auxiliary19_24_v1/planner.py` | `d924912c85f41b32e1eb8aeccfc8da082039ee43e59a20f68ad56f0c701fff9d` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/auxiliary19_24_v1/run.py` | `4b4b4c277882d838a9c2ae127f05c28c377d78fd60689e9c5766cca43b6b8028` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/auxiliary19_24_v1/kernel.py` | `a0c2c5f0aaa1c216ae2c9c796a1e17c88217049e4b30f844e9bb7979c0cb944e` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/auxiliary19_24_v1/protocol.py` | `744723d19f14061c6f69b52890f15109277e978d9fc1e6dbb3500bf72612120e` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/auxiliary19_24_v1/batch.py` | `461cd479f042e85e2b181002910e8414205bce1590908d04abcea2f5769b30bb` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/auxiliary19_24_v1/PORT.diff` | `a502a7d9df6dddbf921f2e1715dca53c6bb38d5f7c4606b5e9ee58b7751e05e6` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/auxiliary19_24_v1/integrate.py` | `e4bda2d00d905bf0963ca6f48d62c7d52a831e14cc695a2bae18183239bb64fc` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/auxiliary19_24_v1/jet.py` | `8decccac51b92cf58b3275e291b83e775da85cd9032f81501e9592d11d591329` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/auxiliary19_24_v1/PROOF.txt` | `0f44deb2f5484c52b2f6b8dac790d57dc53c27f7500892a365a7bc0615baef97` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/auxiliary19_24_v1/MANIFEST.json` | `a4eb496264a920652fedec4c63474a2cceb23adb4a212b844c5a036369697e0c` | `cutoff20_20261016.zip`; n5 source cache |
| `work/cutoff20_20261016/fourier/supported1125_v1/PROOF.txt` | `e27ace1ff17f50ff996bfeb0cf05c7fce67b657eacb1da0ffabd1485516354f2` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/BOUNDED_ETA_SECOND_REVIEW.txt` | `0b882d823e3fe2288a73054c995af5c188cefa20a3a9f6eb54d5736b9703245d` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/analytic/BOUNDED_SUPPORT_ETA.txt` | `766a38a999f86285e695591a7f414c24b0492304d81fecc402e3cac4f980d084` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/analytic/same_law_predecessor_v1/PROOF.txt` | `194b0d4c1003be333874a250e5cb2a589e84bc3b2f8d22e20199f7f5ac1d1642` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law19_discovery_v1/DISCOVERY.json` | `a8430643485533f4dc3890906514c094e0024d5b97282beca4e63d10e744ef36` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law19_discovery_v1/MANIFEST.json` | `391a33392383520d971870a8055b0f14097ac3616321351e5d06967fe0de4b85` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law1920_pilot_v1/pilot.py` | `e55efc08e08879c6908c89c2bcef56339bfcdccb67e17c82779a05772ed407d4` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law1920_pilot_v1/run.py` | `e8b21d62b42063fc1b581acaaab69b967745622e33a4b3cdbaf23c8a56263fe8` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law1920_pilot_v1/kernel.py` | `a0c2c5f0aaa1c216ae2c9c796a1e17c88217049e4b30f844e9bb7979c0cb944e` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law1920_pilot_v1/batch.py` | `b9af09e148a329d29a1210db2b6a746eaa4c8db7ab9eb40075404914a30f919c` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law1920_pilot_v1/PORT.diff` | `0db1e8fe99a2e065bd9dd38ef8c147ca75c5efeeee5982c8b1693591a8cc0c13` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law1920_pilot_v1/integrate.py` | `e4bda2d00d905bf0963ca6f48d62c7d52a831e14cc695a2bae18183239bb64fc` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law1920_pilot_v1/jet.py` | `8decccac51b92cf58b3275e291b83e775da85cd9032f81501e9592d11d591329` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law1920_pilot_v1/PROOF.txt` | `1185382810b244941d0d4ed17b11e23208a25eb47fed5a143335ec17fca584fa` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law1920_pilot_v1/MANIFEST.json` | `40265a9409deda2aaa5cf2eb595c7dfe762142d9ab3b7278b4578bad2b921277` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/analytic/same_law_predecessor_v1/OWN_CAP_COROLLARY.txt` | `1b25c34d40fc18151256843ca556b95a2bb0cb68a6efbed85aff5aa909624de9` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/analytic/same_law_predecessor_v1/PILOT_SOURCE_REVIEW.txt` | `8631a36fa0719815cc42502eb2c742950947eda7232223267dd3dd2c517d5cd7` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law19_discovery_v1/floating.py` | `bdb2ee4af2804d57317e42c5c887fbe5b2536460780ff9109c118e5a3f42cbb9` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law1920_cover_v1/planner.py` | `c3483477761d4e8602e156a82c9191b57423aa25c643c389fe023e546444dd9c` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law1920_cover_v1/run.py` | `d819a81c842eea8a6590d5da211ee3d6d8bc8843ccb3178b3968f8f31857c7d1` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law1920_cover_v1/protocol.py` | `71f132a3de7278183b2fdb886a1100390abf90642616ae9d8838bb2c378e48a7` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law1920_cover_v1/PROOF.txt` | `1b03a14a940f6b73997a7ab674bac75f6813c5a1b8ba6e459c4650a29c755c7d` | `cutoff20_20261016.zip` |
| `work/cutoff20_20261016/fourier/same_law1920_cover_v1/MANIFEST.json` | `aace6821f2a265fbddc6e3764e3bc1e22e5895a9ce23d78fd276cbdf5d4f4939` | `cutoff20_20261016.zip` |
| `work/cutoff25_continue_20261015/root/taylor_sine_v3/scalar.py` | `94981b3eaab98cad5131a9d2af147601e45bcc9f1c1e7b656b45baa745244385` | `cutoff25_continue_20261015.zip` |
| `work/cutoff25_continue_20261015/root/taylor_sine_v3/PROOF.txt` | `5929cc4d1f91ee1e27e85ba0fc7b9685bd5f5f07d9fa9a953615295173b7d959` | `cutoff25_continue_20261015.zip` |
| `work/cutoff25_continue_20261015/root/taylor_sine_v1/PROOF.txt` | `3cc16ea60f17e439d9899d25f48e7c847d73f95beb7024a2d389fb2746920a73` | `cutoff25_continue_20261015.zip` |
| `work/cutoff25_continue_20261015/root/taylor_sine_v2/PROOF.txt` | `c023de89056305a8097f0cec7c19692130f6cd47c5998b36a0591c25e6a189d0` | `cutoff25_continue_20261015.zip` |
| `work/cutoff25_continue_20261015/phase_rectangle_v1/PROOF.txt` | `39b1b674a806e1267fe5b008713e3b41c4b67c15bf8ae9765aa4518069753d77` | `cutoff25_continue_20261015.zip`; n5 source cache |
| `runs/cutoff6_20261018/fourier/owncaps6_9_v1/plan01/PLAN.json` | `538a0a2c524ca4b925e0e4244c5b5bee1de32d552972eecbb5af246658eee990` | NOT LOCATED in this bounded lookup |
| `runs/cutoff6_20261018/fourier/owncaps6_9_v1/construct01/metadata.json` | `934e79a7b18bb320622475f279847d1abfd0177c4419b2acda0938cd0555e956` | NOT LOCATED in this bounded lookup |
| `runs/cutoff6_20261018/fourier/owncaps6_9_v1/construct01/RESULT.json` | `385b5f9512baa22e265feca3275fbd780942893d1179ebb3edef9d8d2921f5e6` | NOT LOCATED in this bounded lookup |
| `runs/cutoff6_20261018/fourier/owncaps6_9_v1/construct01/stdout.txt` | `73ac33279a7b8489436a2954381a69c75dd9af6ce6f91e364718cfe3e32a12ea` | NOT LOCATED in this bounded lookup |
| `runs/cutoff6_20261018/fourier/owncaps6_9_v1/construct01/stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | NOT LOCATED in this bounded lookup |
| `runs/cutoff6_20261018/fourier/owncaps6_9_v1/replay01/metadata.json` | `a0d0e78b9b8b15d6035217d3dc4e8b9231fffdd08f91802c30753f8e4a8f1fbf` | NOT LOCATED in this bounded lookup |
| `runs/cutoff6_20261018/fourier/owncaps6_9_v1/replay01/RESULT.json` | `78a421b2fd946094ae98f5dafdd42064b327ea7e1a17619f6c05007875bfe6f8` | NOT LOCATED in this bounded lookup |
| `runs/cutoff6_20261018/fourier/owncaps6_9_v1/replay01/stdout.txt` | `ab804be920bfb3c0c5930ef8c469b464d5afa28d39ece983cf99f00c8f9e004f` | NOT LOCATED in this bounded lookup |
| `runs/cutoff6_20261018/fourier/owncaps6_9_v1/replay01/stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | NOT LOCATED in this bounded lookup |

The remaining nine paths are the original owncaps `plan01/PLAN.json`, and `construct01`/`replay01` metadata, RESULT, stdout and stderr under `runs/cutoff6_20261018/fourier/owncaps6_9_v1/`. Their expected pins above remain binding provenance requirements. Empty stderr cannot be promoted to a fresh capture by writing new zero bytes under the old path. The constructor/replayer mathematical sources are supplied in the combined archive; absent old run captures are distinct from absent numerical source.

The separately supplied `resource7_9_v2/check_caps.py` checks the accepted supported Fourier owncap readback and the equality of complete construct/replay rows, including all 344 ordered rows, 86 closed strips and all four literal indices 6–9. It then derives the nine tighter caps for n7–9. This readback was not executed. Missing historical captures require either exact additional transport or a separately specified, reviewed conditional-parent boundary/fresh Fourier acquisition. The INITIAL filename/timestamp metadata port alone does not remove that requirement and must not silently bypass it.

## Verification and remaining obligations

Nine synthetic infrastructure tests passed in 0.058 seconds, with no numerical module imported. All nine actual archival candidates passed the implemented PREPARED reconstruction against the external old output hashes. A separate real-source schema exercise derived all nine resource ports using explicitly synthetic, unattested fresh-parent JSON: each preserved all 100 candidate rows and produced the fixed derived replay hash. Those temporary in-memory parent packets were not mathematical receipts or completed runs.

The new helper preserves false arithmetic/acquisition/global flags. Actual full INITIAL and resource execution, the tighter-cap/support/Fourier premises, real process/capture evidence, same-law resource-to-count joins, the sequential global predecessors and final composition remain separate obligations. The bounded source recovery does not establish any new finite-index inequality.
