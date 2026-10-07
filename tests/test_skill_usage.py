import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import time
import unittest
from unittest import mock

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "skill-usage.py")
spec = importlib.util.spec_from_file_location("skill_usage", SCRIPT)
skill_usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(skill_usage)


def bash(command):
    return {"type": "tool_use", "name": "Bash", "input": {"command": command}}


def write_transcript(path, blocks, timestamp="2026-10-05T07:00:00.000Z"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        for block in blocks:
            f.write(json.dumps({"timestamp": timestamp, "message": {"role": "assistant", "content": [block]}}) + "\n")


class BashWritesCodeTest(unittest.TestCase):
    def test_counts_writes_to_code_files(self):
        for command in [
            "cat > app/A.swift <<'EOF'\nstruct A {}\nEOF",
            "echo x >> lib/a.py",
            "printf x | tee src/x.ts",
            "printf x | tee -a src/x.ts",
            "sed -i '' 's/a/b/' app/Foo.php",
            "sed -i.bak 's/a/b/' x.rb",
            "python3 -c \"open('m.py','w').write('x')\"",
            "python3 -c \"from pathlib import Path; Path('app/x.py').write_text(s)\"",
        ]:
            with self.subTest(command=command):
                self.assertTrue(skill_usage.bash_writes_code(command))

    def test_ignores_reads_and_non_code_writes(self):
        for command in [
            "ls > out.txt",
            "cmd 2>/dev/null",
            "echo hi >&2",
            "cat app/A.swift",
            "sed 's/a/b/' x.py",
            "grep foo x.py > /dev/null",
            "python3 -c \"print(open('x.py').read())\"",
            "make 2>&1 | tee build.log",
            "git commit -m \"move A -> app/Foo.php\"",
            "git commit -m \"rename map => lib/a.py\"",
        ]:
            with self.subTest(command=command):
                self.assertFalse(skill_usage.bash_writes_code(command))


    def test_many_lines_without_sed_i_are_fast(self):
        start = time.monotonic()
        self.assertFalse(skill_usage.bash_writes_code("\n".join(["sed x"] * 20000)))
        self.assertLess(time.monotonic() - start, 1)


class ScanSessionTest(unittest.TestCase):
    def test_counts_bash_writes_as_code_edits(self):
        with tempfile.TemporaryDirectory() as tmp:
            main_file = os.path.join(tmp, "session.jsonl")
            write_transcript(main_file, [
                {"type": "tool_use", "name": "Edit", "input": {"file_path": "/repo/App/A.swift"}},
                bash("cat > tests/test_a.py <<'EOF'\nimport unittest\nEOF"),
                bash("git add -A && git commit -m 'feat: a'"),
                bash("ls"),
            ])
            s = skill_usage.scan_session(main_file)
        self.assertEqual(s["code_edits"], 2)
        self.assertEqual(s["commits"], 1)

    def test_command_writing_two_code_files_is_one_edit(self):
        with tempfile.TemporaryDirectory() as tmp:
            main_file = os.path.join(tmp, "session.jsonl")
            write_transcript(main_file, [bash("echo a > app/a.py && echo b > app/b.py")])
            s = skill_usage.scan_session(main_file)
        self.assertEqual(s["code_edits"], 1)


class SinceTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        write_transcript(os.path.join(tmp.name, "proj-early", "aaaaaaaa-1.jsonl"), [bash("ls")], "2026-10-05T07:00:00Z")
        write_transcript(os.path.join(tmp.name, "proj-late", "bbbbbbbb-2.jsonl"), [bash("ls")], "2026-10-05T08:00:00Z")
        patcher = mock.patch.object(skill_usage, "PROJECTS", tmp.name)
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_main(self, *argv):
        out = io.StringIO()
        with mock.patch.object(sys, "argv", ["skill-usage.py", *argv]), contextlib.redirect_stdout(out):
            skill_usage.main()
        return out.getvalue()

    def test_time_excludes_sessions_that_started_earlier(self):
        out = self.run_main("--since", "2026-10-05T07:31")
        self.assertIn("proj-late", out)
        self.assertNotIn("proj-early", out)

    def test_time_with_a_space_is_accepted(self):
        out = self.run_main("--since", "2026-10-05 07:31")
        self.assertIn("proj-late", out)
        self.assertNotIn("proj-early", out)

    def test_date_includes_the_whole_day(self):
        out = self.run_main("--since", "2026-10-05")
        self.assertIn("proj-early", out)
        self.assertIn("proj-late", out)

    def test_invalid_value_is_an_argparse_error(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.run_main("--since", "2026-13-40")


if __name__ == "__main__":
    unittest.main()
