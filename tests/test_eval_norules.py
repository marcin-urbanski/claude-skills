import importlib.util
import os
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "eval-norules.py")
spec = importlib.util.spec_from_file_location("eval_norules", SCRIPT)
eval_norules = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eval_norules)

PROMPT = """---
description: A bug fix.
runs: 5
append_system_prompt: |
  The user's rules:

  ## How I work

  1. Think before coding.
allowed_tools: [Read, Edit]
---
Fix split_cents.
"""


class EvalNoRulesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.src = os.path.join(self.tmp.name, "evals")
        self.dst = os.path.join(self.tmp.name, "evals-norules")
        self.write("case-a/prompt.md", PROMPT)
        self.write("case-a/fixture.sh", "#!/usr/bin/env bash\n")
        self.write("_shared/fixture.sh", "echo shared\n")
        self.write("results/old/aggregate-result.json", "{}")

    def write(self, rel, text):
        path = os.path.join(self.src, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def read(self, rel):
        with open(os.path.join(self.dst, rel)) as f:
            return f.read()

    def test_drops_the_rules_and_keeps_the_rest_of_the_prompt(self):
        eval_norules.build(self.src, self.dst)
        self.assertEqual(
            self.read("case-a/prompt.md"),
            "---\ndescription: A bug fix.\nruns: 5\nallowed_tools: [Read, Edit]\n---\nFix split_cents.\n",
        )

    def test_copies_fixtures_and_shared_files(self):
        eval_norules.build(self.src, self.dst)
        self.assertEqual(self.read("case-a/fixture.sh"), "#!/usr/bin/env bash\n")
        self.assertEqual(self.read("_shared/fixture.sh"), "echo shared\n")

    def test_skips_results(self):
        eval_norules.build(self.src, self.dst)
        self.assertFalse(os.path.exists(os.path.join(self.dst, "results")))

    def test_replaces_an_earlier_copy(self):
        os.makedirs(os.path.join(self.dst, "stale-case"))
        eval_norules.build(self.src, self.dst)
        self.assertFalse(os.path.exists(os.path.join(self.dst, "stale-case")))


if __name__ == "__main__":
    unittest.main()
