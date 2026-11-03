import importlib.util
import json
import os
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "study-table.py")
spec = importlib.util.spec_from_file_location("study_table", SCRIPT)
study_table = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study_table)


def run(*passes, error=None):
    return {"error": error, "graders": [{"name": n, "passed": p} for n, p in passes]}


def result(case, eval_dir, with_runs, without_runs):
    return {
        "cases": [
            {
                "name": case,
                "dir": f"{eval_dir}/{case}",
                "arms": {"with": with_runs, "without": without_runs},
            }
        ]
    }


class WilsonTest(unittest.TestCase):
    def test_matches_the_published_interval_for_7_of_10(self):
        low, high = study_table.wilson(7, 10)
        self.assertAlmostEqual(low, 0.397, places=3)
        self.assertAlmostEqual(high, 0.892, places=3)

    def test_all_passed_still_has_a_lower_bound_below_one(self):
        low, high = study_table.wilson(10, 10)
        self.assertAlmostEqual(low, 0.722, places=3)
        self.assertEqual(high, 1.0)


class TableTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def write(self, name, data):
        path = os.path.join(self.tmp.name, name)
        with open(path, "w") as f:
            json.dump(data, f)
        return path

    def test_maps_eval_dirs_and_arms_to_the_four_study_arms(self):
        rules = self.write("a.json", result("c", "evals", [run(("g", True))], [run(("g", False))]))
        norules = self.write("b.json", result("c", "evals-norules", [run(("g", True))], [run(("g", False))]))
        out = study_table.table([rules, norules])
        self.assertIn("| case | grader | bare | skills | rules | rules + skills |", out)
        self.assertIn("| c | g | 0/1 (0–79%) | 1/1 (21–100%) | 0/1 (0–79%) | 1/1 (21–100%) |", out)

    def test_leaves_errored_runs_out_and_counts_them(self):
        path = self.write(
            "a.json",
            result("c", "evals", [run(("g", True)), run(("g", False), error="timeout")], [run(("g", True))]),
        )
        out = study_table.table([path])
        self.assertIn("| c | g | – | – | 1/1 (21–100%) | 1/1 (21–100%) |", out)
        self.assertIn("Errored runs left out: c rules + skills 1", out)


if __name__ == "__main__":
    unittest.main()
