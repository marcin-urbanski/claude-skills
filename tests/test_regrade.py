import importlib.util
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "regrade.py")
spec = importlib.util.spec_from_file_location("regrade", SCRIPT)
regrade = importlib.util.module_from_spec(spec)
spec.loader.exec_module(regrade)

REGEX_GRADER = """---
type: regex
target: trace
pattern: '"command":"make it''s green"'
---
The run says make it's green.
"""
LLM_GRADER = """---
type: llm
focus: { source: file, path: money.py }
---
PASS if it is right.
"""


def grader(name, passed):
    return {"name": name, "passed": passed, "weight": 1, "explanation": "old", "withOnly": False, "scored": True}


def run(run_id, regex_passed, llm_passed=True):
    graders = [grader("green", regex_passed), grader("right", llm_passed)]
    score = sum(g["passed"] for g in graders) / 2
    return {
        "score": score,
        "passed": score >= 1,
        "error": None,
        "tracePath": f"/private/tmp/{run_id}/out/trace.jsonl",
        "graders": graders,
    }


class RegradeTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = tmp.name
        self.evals = os.path.join(self.root, "evals")
        self.traces = os.path.join(self.root, "traces")
        os.makedirs(os.path.join(self.evals, "c", "graders"))
        os.makedirs(self.traces)
        self.write(os.path.join(self.evals, "c", "graders", "green.md"), REGEX_GRADER)
        self.write(os.path.join(self.evals, "c", "graders", "right.md"), LLM_GRADER)

    def write(self, path, text):
        with open(path, "w") as f:
            f.write(text)
        return path

    def trace(self, name, run_id, command, first=()):
        lines = list(first) + [
            {"type": "system", "subtype": "init", "cwd": f"/private/tmp/{run_id}/home/cwd"},
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash", "input": {"command": command}}]}},
        ]
        text = "".join(json.dumps(line, separators=(",", ":"), ensure_ascii=False) + "\n" for line in lines)
        return self.write(os.path.join(self.traces, name), text)

    def result(self, eval_dir, with_runs, without_runs):
        return {
            "cases": [
                {
                    "name": "c",
                    "dir": f"{eval_dir}/c",
                    "graders": [
                        {"name": "green", "type": "regex", "config": {"pattern": "old"}},
                        {"name": "right", "type": "llm", "config": {}},
                    ],
                    "arms": {"with": with_runs, "without": without_runs},
                    "aggregates": {"score": 0, "passRate": 0, "scoreWithout": 0, "passRateWithout": 0, "delta": 0},
                }
            ],
            "aggregates": {"overallScore": 0},
        }

    def test_reads_a_single_quoted_yaml_pattern(self):
        graders = regrade.load_regex_graders(os.path.join(self.evals, "c"))
        self.assertEqual(graders, {"green": '"command":"make it\'s green"'})

    def test_finds_a_transcript_by_the_run_folder_in_its_cwd_whatever_its_name(self):
        path = self.trace("anything.jsonl", "e-Ab12Cd", "ls")
        self.assertEqual(regrade.index_traces(self.traces), {"e-Ab12Cd": path})

    def test_finds_the_cwd_after_hook_lines_that_come_before_init(self):
        hook = {"type": "system", "subtype": "hook_started", "hook_name": "SessionStart:startup"}
        path = self.trace("plugin.jsonl", "e-Ab12Cd", "ls", first=[hook])
        self.assertEqual(regrade.index_traces(self.traces), {"e-Ab12Cd": path})

    def test_matches_the_run_folder_name_used_on_linux(self):
        self.trace("linux.jsonl", "eval-tmp/claude-eval-2QvQHL", "make it's green")
        linux_run = run("eval-tmp/claude-eval-2QvQHL", False)
        linux_run["tracePath"] = linux_run["tracePath"].replace("/private/tmp/", "/home/user/")
        data = self.result("evals", [linux_run], [])
        flips = regrade.regrade(data, regrade.index_traces(self.traces), self.evals)
        self.assertEqual(flips, [("c", "evals", "with", 0, "green", False, True)])

    def test_ignores_files_that_are_not_transcripts(self):
        self.write(os.path.join(self.traces, ".DS_Store"), "\x00\x01")
        path = self.trace("run.jsonl", "e-Ab12Cd", "ls")
        self.assertEqual(regrade.index_traces(self.traces), {"e-Ab12Cd": path})

    def test_flips_a_regex_grader_and_rescores_the_run(self):
        self.trace("one.jsonl", "e-aaaaaa", "make it's green")
        self.trace("two.jsonl", "e-bbbbbb", "make it red")
        data = self.result("evals-norules", [run("e-aaaaaa", False)], [run("e-bbbbbb", True)])

        flips = regrade.regrade(data, regrade.index_traces(self.traces), self.evals)

        case = data["cases"][0]
        with_run, without_run = case["arms"]["with"][0], case["arms"]["without"][0]
        self.assertEqual(flips, [("c", "evals-norules", "with", 0, "green", False, True),
                                 ("c", "evals-norules", "without", 0, "green", True, False)])
        self.assertTrue(with_run["graders"][0]["passed"])
        self.assertIn("matched", with_run["graders"][0]["explanation"])
        self.assertEqual((with_run["score"], with_run["passed"]), (1, True))
        self.assertEqual(without_run["graders"][0]["explanation"], "pattern not found in trace")
        self.assertEqual((without_run["score"], without_run["passed"]), (0.5, False))

    def test_records_the_pattern_it_applied(self):
        self.trace("one.jsonl", "e-aaaaaa", "make it's green")
        data = self.result("evals", [run("e-aaaaaa", True)], [])
        regrade.regrade(data, regrade.index_traces(self.traces), self.evals)
        self.assertEqual(data["cases"][0]["graders"][0]["config"]["pattern"], '"command":"make it\'s green"')
        self.assertEqual(data["cases"][0]["graders"][1]["config"], {})

    def test_leaves_llm_graders_as_they_were(self):
        self.trace("one.jsonl", "e-aaaaaa", "make it's green")
        data = self.result("evals", [run("e-aaaaaa", True, llm_passed=False)], [])
        regrade.regrade(data, regrade.index_traces(self.traces), self.evals)
        self.assertEqual(data["cases"][0]["arms"]["with"][0]["graders"][1],
                         grader("right", False))

    def test_drops_the_aggregates_rather_than_leave_them_stale(self):
        self.trace("one.jsonl", "e-aaaaaa", "make it's green")
        data = self.result("evals", [run("e-aaaaaa", True)], [])
        regrade.regrade(data, regrade.index_traces(self.traces), self.evals)
        self.assertNotIn("aggregates", data)
        self.assertNotIn("aggregates", data["cases"][0])

    def test_skips_errored_runs(self):
        errored = run("e-gone00", False)
        errored["error"] = "timeout"
        data = self.result("evals", [errored], [])
        self.assertEqual(regrade.regrade(data, {}, self.evals), [])

    def test_skips_runs_that_ended_without_grading(self):
        aborted = run("e-gone00", False)
        aborted["graders"] = []
        data = self.result("evals", [aborted], [])
        self.assertEqual(regrade.regrade(data, {}, self.evals), [])

    def test_refuses_a_run_whose_transcript_is_missing(self):
        data = self.result("evals", [run("e-gone00", False)], [])
        with self.assertRaisesRegex(SystemExit, "e-gone00"):
            regrade.regrade(data, {}, self.evals)

    def test_cli_writes_regraded_results_and_prints_the_flips(self):
        self.trace("one.jsonl", "e-aaaaaa", "make it's green")
        path = self.write(os.path.join(self.root, "opus-c.json"),
                          json.dumps(self.result("evals", [run("e-aaaaaa", False)], [])))
        out = os.path.join(self.root, "out")
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            regrade.main(["--traces", self.traces, "--out", out, "--evals", self.evals, path])
        with open(os.path.join(out, "opus-c.json")) as f:
            self.assertTrue(json.load(f)["cases"][0]["arms"]["with"][0]["graders"][0]["passed"])
        self.assertIn("c evals with 0 green: FAIL -> PASS", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
