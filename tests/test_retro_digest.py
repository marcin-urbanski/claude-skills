import importlib.util
import json
import os
import tempfile
import time
import unittest
from unittest import mock

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "skills", "retro", "digest.py")
spec = importlib.util.spec_from_file_location("retro_digest", SCRIPT)
retro_digest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retro_digest)

TS = "2026-10-09T18:07:36.000Z"


def user(content, **extra):
    return {"type": "user", "timestamp": TS, "message": {"role": "user", "content": content}, **extra}


def assistant(*blocks):
    return {"type": "assistant", "timestamp": TS, "message": {"role": "assistant", "content": list(blocks)}}


def call(name, tool_id="t1", **inp):
    return {"type": "tool_use", "id": tool_id, "name": name, "input": inp}


def result(text, tool_id="t1", error=False):
    return user([{"type": "tool_result", "tool_use_id": tool_id, "content": text, "is_error": error}])


class DigestTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = os.path.join(self.tmp.name, "abc123.jsonl")

    def write(self, *entries, path=None):
        with open(path or self.path, "w") as f:
            for entry in entries:
                f.write(json.dumps(entry) + "\n")

    def test_shows_user_messages_with_time_and_skips_meta_and_reminders(self):
        self.write(
            user("fix the login bug<system-reminder>internal note</system-reminder>"),
            user([{"type": "text", "text": "skill body"}], isMeta=True),
            user([{"type": "text", "text": "also check logout"}]),
        )
        out = retro_digest.digest(self.path)
        self.assertIn("[18:07] USER: fix the login bug", out)
        self.assertIn("USER: also check logout", out)
        self.assertNotIn("internal note", out)
        self.assertNotIn("skill body", out)

    def test_summarises_each_tool_call_by_its_key_input(self):
        self.write(assistant(
            call("Bash", "t1", command="php artisan test\n--filter Login", description="Run tests"),
            call("Read", "t2", file_path="/repo/app/Login.php"),
            call("Skill", "t3", skill="tdd"),
            call("Agent", "t4", subagent_type="reviewer", description="Review branch", prompt="long..."),
            call("Grep", "t5", pattern="authorize", path="app"),
        ))
        out = retro_digest.digest(self.path)
        self.assertIn("Bash: php artisan test", out)
        self.assertNotIn("--filter Login", out)
        self.assertIn("Read: /repo/app/Login.php", out)
        self.assertIn("Skill: tdd", out)
        self.assertIn("Agent(reviewer): Review branch", out)
        self.assertIn("Grep: authorize in app", out)

    def test_shows_errors_and_hides_successful_results(self):
        self.write(
            assistant(call("Bash", "t1", command="composer test")),
            result("Exit code 1\nFailed asserting that 302 is 200", "t1", error=True),
            assistant(call("Bash", "t2", command="ls")),
            result("app\nroutes", "t2"),
        )
        out = retro_digest.digest(self.path)
        self.assertIn("ERROR: Exit code 1 Failed asserting that 302 is 200", out)
        self.assertNotIn("routes", out)

    def test_flags_large_results(self):
        self.write(assistant(call("Read", "t1", file_path="big.json")), result("x" * 45_000, "t1"))
        self.assertIn("[result 45k chars]", retro_digest.digest(self.path))

    def test_marks_repeated_identical_calls(self):
        self.write(*[assistant(call("Bash", f"t{i}", command="npm test")) for i in range(3)])
        out = retro_digest.digest(self.path)
        self.assertIn("Bash: npm test [repeat #3]", out)
        self.assertEqual(out.count("[repeat"), 2)

    def test_calls_sharing_only_a_first_line_are_not_repeats(self):
        self.write(assistant(call("Bash", "t1", command="cat >> log.md <<'EOF'\nstep 1\nEOF"),
                             call("Bash", "t2", command="cat >> log.md <<'EOF'\nstep 2\nEOF")))
        self.assertNotIn("[repeat", retro_digest.digest(self.path))

    def test_truncates_long_text(self):
        self.write(user("a" * 2_000), assistant(call("Bash", "t1", command="b" * 2_000)))
        for line in retro_digest.digest(self.path).splitlines():
            self.assertLess(len(line), 400)

    def test_header_counts_calls_and_errors(self):
        self.write(
            assistant(call("Bash", "t1", command="x"), call("Bash", "t2", command="y"), call("Read", "t3", file_path="z")),
            result("boom", "t1", error=True),
        )
        header = retro_digest.digest(self.path).splitlines()[0]
        self.assertIn("abc123", header)
        self.assertIn("3 tool calls", header)
        self.assertIn("1 errors", header)
        self.assertIn("Bash 2", header)

    def test_lists_subagents_with_description_and_counts(self):
        self.write(user("go"))
        sub_dir = os.path.join(self.tmp.name, "abc123", "subagents")
        os.makedirs(sub_dir)
        sub = os.path.join(sub_dir, "agent-x1.jsonl")
        self.write(assistant(call("Read", "s1", file_path="a"), call("Bash", "s2", command="b")),
                   result("nope", "s2", error=True), path=sub)
        with open(os.path.join(sub_dir, "agent-x1.meta.json"), "w") as f:
            json.dump({"agentType": "implementer", "description": "Task 2: login form"}, f)
        out = retro_digest.digest(self.path)
        self.assertIn("implementer: Task 2: login form (2 tool calls, 1 errors)", out)
        self.assertIn(sub, out)


class SessionFileTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = os.path.join(self.tmp.name, "-Users-me-Developer-my-app")
        os.makedirs(self.project)
        patcher = mock.patch.object(retro_digest, "PROJECTS", self.tmp.name)
        patcher.start()
        self.addCleanup(patcher.stop)

    def touch(self, name, age=0):
        path = os.path.join(self.project, name)
        open(path, "w").close()
        os.utime(path, (time.time() - age, time.time() - age))
        return path

    def test_defaults_to_newest_session_of_the_working_directory(self):
        self.touch("old.jsonl", age=100)
        newest = self.touch("new.jsonl")
        self.assertEqual(retro_digest.session_file(None, "/Users/me/Developer/my.app"), newest)

    def test_accepts_a_path_or_a_session_id(self):
        path = self.touch("0ec51c34-aaaa.jsonl")
        self.assertEqual(retro_digest.session_file(path, "/elsewhere"), path)
        self.assertEqual(retro_digest.session_file("0ec51c34-aaaa", "/elsewhere"), path)


if __name__ == "__main__":
    unittest.main()
