# Untrusted historical parser fixture

`n6_B0_p61.untrusted-original-forest.json` is the exact original candidate with SHA256 `70255b82689972d911bcc2e94061a7e19b7e58f0b22866b2f4a880619b829b5b`. It is used only for topology/parser mutations and cache-key binding tests. It is not a production input, historical acceptance, cache hit or mathematical proof.

The real end-to-end test calls the native producer from an empty source-only directory, then verifies that newly discovered forest in a separate directory. The runtime vendor capsule contains no original forest and no acceptance receipt. Parent ZIP provenance and MIT license are in `vendor/count_native_n6_b0_p61`.
