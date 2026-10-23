import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from be_replay import colab_batch as batch

class BackupAndBatchTests(unittest.TestCase):
    def test_unfinished_json_is_not_promoted_and_prior_backup_survives(self):
        with tempfile.TemporaryDirectory() as name:
            root, dest = Path(name)/"work", Path(name)/"drive"
            root.mkdir()
            source = root/"CHECKPOINT.json"
            source.write_text('{"schema":"UNTRUSTED_COUNT_SEARCH_CHECKPOINT_V1","n":1}')
            batch.live_backup(root, dest)
            old = (dest/source.name).read_bytes()
            source.write_text('{"schema":')
            batch.live_backup(root, dest)
            self.assertEqual((dest/source.name).read_bytes(), old)
            self.assertFalse(json.loads((dest/"LIVE_SNAPSHOT.json").read_text())["all_index_conclusion_verified"])

    def test_backup_preserves_original_order_and_results_are_self_contained(self):
        import os
        with tempfile.TemporaryDirectory() as name:
            root, dest = Path(name)/"run", Path(name)/"drive"
            root.mkdir()
            for index in (1, 2):
                directory = root/str(index)
                directory.mkdir()
                path = directory/"CHECKPOINT.json"
                path.write_text('{"schema":"UNTRUSTED_COUNT_SEARCH_CHECKPOINT_V1"}')
                os.utime(path, ns=(index*10**9, index*10**9))
            batch.live_backup(root, dest/"live")
            self.assertEqual(batch.latest_checkpoint(dest).parent.name, "2")
            bundle = batch.bundle(root, dest)
            with zipfile.ZipFile(bundle) as archive:
                self.assertEqual(set(archive.namelist()), {"run/1/CHECKPOINT.json", "run/2/CHECKPOINT.json"})
            self.assertTrue(bundle.with_suffix(".zip.sha256").is_file())

    def test_failed_native_replay_remains_incomplete_and_still_bundles(self):
        from be_replay import count_task
        with tempfile.TemporaryDirectory() as name:
            base = Path(name)
            def prepare(target, archives, output, **kwargs):
                output.mkdir()
            def search(task, **kwargs):
                candidate = task/"CANDIDATE_FOREST.json"
                candidate.write_text("{}")
                return dict(epoch=str(task), observed={"status":"completed"},
                            search_result={"status":"CANDIDATE_COMPLETE_NOT_ACCEPTED"},
                            candidate=str(candidate), checkpoint=str(task/"missing"))
            with patch.object(count_task, "prepare", side_effect=prepare), \
                 patch.object(count_task, "search", side_effect=search), \
                 patch.object(count_task, "accept", side_effect=ValueError("native guard unavailable")):
                result = batch.run_count("b3-p33", durable_root=base/"drive", work_root=base/"work",
                                         archives=base/"archives", total_seconds=1)
            self.assertEqual(result["status"]["state"], "incomplete_error")
            self.assertFalse(result["status"]["native_arithmetic_accepted"])
            self.assertFalse(result["status"]["all_index_conclusion_verified"])
            self.assertTrue(Path(result["bundle"]).is_file())

    def test_partial_search_never_invokes_native_acceptor(self):
        from be_replay import count_task
        with tempfile.TemporaryDirectory() as name:
            base = Path(name)
            def prepare(target, archives, output, **kwargs):
                output.mkdir()
            def search(task, **kwargs):
                return dict(epoch=str(task), observed={"status":"completed"},
                            search_result={"status":"SEARCH_CHECKPOINTED_INCOMPLETE"},
                            candidate=str(task/"absent"), checkpoint=str(task/"absent"))
            with patch.object(count_task, "prepare", side_effect=prepare), \
                 patch.object(count_task, "search", side_effect=search), \
                 patch.object(count_task, "accept") as accept:
                result = batch.run_count("b3-p33", durable_root=base/"drive", work_root=base/"work",
                                         archives=base/"archives", total_seconds=1)
            accept.assert_not_called()
            self.assertEqual(result["status"]["state"], "candidate_incomplete_budget_exhausted")
            self.assertFalse(result["status"]["native_arithmetic_accepted"])

if __name__ == "__main__":
    unittest.main()
