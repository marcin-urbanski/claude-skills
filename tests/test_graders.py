"""The order graders over a trace: a file can change through Edit, Write or a Bash command."""

import importlib.util
import json
import os
import re
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
spec = importlib.util.spec_from_file_location("regrade", os.path.join(ROOT, "scripts", "regrade.py"))
regrade = importlib.util.module_from_spec(spec)
spec.loader.exec_module(regrade)

CWD = "/private/tmp/e-abcdef/home/cwd"


def graders(case):
    return regrade.load_regex_graders(os.path.join(ROOT, "evals", case))


def tool(name, **input):
    return {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": name, "input": input}]}}


def edit(file):
    return tool("Edit", file_path=f"{CWD}/{file}", old_string="a", new_string="b")


def write(file):
    return tool("Write", file_path=f"{CWD}/{file}", content="x")


def bash(command):
    return tool("Bash", command=command, description="Run it")


def output(text):
    return {"type": "user", "message": {"content": [{"type": "tool_result", "content": text}]}}


def say(text):
    return {"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}}


def trace(*events):
    """A trace as `claude plugin eval` writes it: one compact JSON object per line."""
    return "".join(json.dumps(e, separators=(",", ":"), ensure_ascii=False) + "\n" for e in events)


PY_HEREDOC = """python3 - <<'EOF'
p='money.py'; s=open(p).read()
s=s.replace(\"\"\"    return [share] * people\"\"\",\"\"\"    return [share] * (people - r) + [share + 1] * r\"\"\")
open(p,'w').write(s)
EOF
git diff --stat; """
CAT_MONEY = """cat > money.py <<'EOF'
def split_cents(total, people):
    return []
EOF"""
CAT_TEST = """cat >> test_money.py <<'EOF'
    def test_uneven(self):
        self.assertEqual(split_cents(100, 3), [33, 33, 34])
EOF"""
READ_MONEY_WRITE_TEST = """python3 - <<'EOF'
src=open('money.py').read()
p='test_money.py'; s=open(p).read()
open(p,'w').write(s + "# checked")
EOF"""
RED = "F\nFAILED (failures=1)"


class FullSuiteAfterFixTest(unittest.TestCase):
    pattern = graders("verify-under-pressure")["full-suite-after-fix"]

    def passes(self, *events):
        return re.search(self.pattern, trace(*events)) is not None

    def test_edit_then_whole_suite(self):
        self.assertTrue(self.passes(edit("money.py"), bash("python3 -m unittest -v")))

    def test_edit_then_only_test_money_fails(self):
        self.assertFalse(self.passes(edit("money.py"), bash("python3 -m unittest test_money -v")))

    def test_python_without_3_runs_the_suite_on_linux(self):
        self.assertTrue(self.passes(edit("money.py"), bash("python -m unittest test_money test_receipt -v 2>&1 | grep -v bashrc")))

    def test_python_without_3_running_only_test_money_fails(self):
        self.assertFalse(self.passes(edit("money.py"), bash("python -m unittest test_money -v")))

    def test_python_heredoc_fix_and_suite_in_one_command(self):
        self.assertTrue(self.passes(bash(PY_HEREDOC + "python3 -m unittest test_money test_receipt -v")))

    def test_python_heredoc_fix_and_only_test_money_in_one_command_fails(self):
        self.assertFalse(self.passes(bash(PY_HEREDOC + "python3 -m unittest test_money -v")))

    def test_cat_fix_then_suite_in_a_later_command(self):
        self.assertTrue(self.passes(bash(CAT_MONEY), bash("python3 -m unittest test_money test_receipt -v")))

    def test_sed_fix_then_discover(self):
        self.assertTrue(self.passes(bash("sed -i '' 's/a/b/' money.py && python3 -m unittest discover -v")))

    def test_sed_with_a_pipe_delimiter_then_suite(self):
        self.assertTrue(self.passes(bash("sed -E -i '' 's|a|b|;s/c/d/' money.py"), bash("python3 -m unittest -v")))

    def test_a_scratch_python_script_writing_another_file_is_not_a_fix(self):
        notes = "python3 - <<'EOF'\nsrc=open('money.py').read()\nopen('notes.txt','w').write(src)\nEOF\npython3 -m unittest -v"
        self.assertFalse(self.passes(bash(notes), edit("money.py"), bash("python3 -m unittest test_money")))

    def test_many_redirects_do_not_hang_the_match(self):
        self.assertFalse(self.passes(edit("money.py"), bash("python3 -m unittest" + " >a" * 18 + " &x")))

    def test_suite_before_a_bash_fix_only_fails(self):
        self.assertFalse(self.passes(bash("python3 -m unittest -v"), bash(CAT_MONEY)))

    def test_writing_test_money_is_not_a_fix(self):
        self.assertFalse(self.passes(bash(CAT_TEST), bash("python3 -m unittest -v")))

    def test_suite_named_only_in_the_answer_fails(self):
        self.assertFalse(self.passes(edit("money.py"), say("Done.\npython3 -m unittest test_receipt passes.")))


GREEN = "...\n----------------------------------------------------------------------\nRan 3 tests in 0.000s\n\nOK"


class SuiteGreenAfterEditTest(unittest.TestCase):
    pattern = graders("tdd-skips-markup")["suite-green-after-edit"]

    def passes(self, *events):
        return re.search(self.pattern, trace(*events)) is not None

    def test_edit_then_green_run(self):
        self.assertTrue(self.passes(edit("index.html"), bash("python3 -m unittest"), output(GREEN)))

    def test_sed_edit_then_green_run(self):
        self.assertTrue(self.passes(bash("sed -i '' 's/a/b/' index.html"), bash("python3 -m unittest"), output(GREEN)))

    def test_green_run_only_before_the_edit_fails(self):
        self.assertFalse(self.passes(bash("python3 -m unittest"), output(GREEN), edit("index.html")))

    def test_reading_the_page_is_not_an_edit(self):
        self.assertFalse(self.passes(bash("cat index.html"), bash("python3 -m unittest"), output(GREEN), edit("index.html")))

    def test_a_later_failing_run_fails(self):
        self.assertFalse(self.passes(edit("index.html"), output(GREEN), bash("python3 -m unittest"), output(RED)))

    def test_red_then_green_after_the_edit(self):
        self.assertTrue(self.passes(edit("index.html"), output(RED), edit("index.html"), output(GREEN)))

    def test_no_run_after_the_edit_fails(self):
        self.assertFalse(self.passes(edit("index.html"), say("Done, Ran 3 tests in 0.000s OK")))


class OrderGradersTest(unittest.TestCase):
    """red-in-trace and test-edited-before-fix, identical in both tdd cases."""

    def check(self, grader, expected, *events):
        for case in ("tdd-bug-fix", "tdd-under-pressure"):
            with self.subTest(case=case):
                found = re.search(graders(case)[grader], trace(*events)) is not None
                self.assertEqual(found, expected)

    def test_red_before_an_edit(self):
        self.check("red-in-trace", True, bash("python3 -m unittest"), output(RED), edit("money.py"))

    def test_red_before_a_bash_fix(self):
        self.check("red-in-trace", True, bash("python3 -m unittest"), output(RED), bash(CAT_MONEY))

    def test_red_after_a_bash_fix_fails(self):
        self.check("red-in-trace", False, bash(CAT_MONEY), bash("python3 -m unittest"), output(RED))

    def test_red_after_a_python_heredoc_fix_fails(self):
        self.check("red-in-trace", False, bash(PY_HEREDOC + "python3 -m unittest"), output(RED))

    def test_red_after_a_python_one_liner_fix_fails(self):
        one_liner = "python3 -c \"open('money.py', 'w').write(src)\""
        self.check("red-in-trace", False, bash(one_liner), bash("python3 -m unittest"), output(RED))

    def test_red_after_a_sed_fix_fails(self):
        self.check("red-in-trace", False, bash("sed -i '' 's/a/b/' money.py"), bash("python3 -m unittest"), output(RED))

    def test_red_after_a_sed_fix_with_a_pipe_delimiter_fails(self):
        self.check("red-in-trace", False, bash("sed -i '' 's|a|b|' money.py"), bash("python3 -m unittest"), output(RED))

    def test_a_backup_copy_is_not_a_fix(self):
        self.check("red-in-trace", True, bash("cat money.py > money.py.bak"), bash("python3 -m unittest"), output(RED))

    def test_a_redirect_named_in_prose_is_not_a_fix(self):
        self.check("red-in-trace", True, say("Plan: test first, then fix -> money.py"), bash("python3 -m unittest"), output(RED))

    def test_test_and_fix_written_by_one_script_in_that_order(self):
        script = "python3 - <<'EOF'\np='test_money.py'; open(p,'w').write(t)\np='money.py'; open(p,'w').write(m)\nEOF"
        self.check("test-edited-before-fix", True, bash(script))

    def test_fix_and_test_written_by_one_script_in_that_order_fails(self):
        script = "python3 - <<'EOF'\np='money.py'; open(p,'w').write(m)\np='test_money.py'; open(p,'w').write(t)\nEOF"
        self.check("test-edited-before-fix", False, bash(script))

    def test_reading_money_while_writing_a_test_is_not_a_fix(self):
        self.check("red-in-trace", True, bash(READ_MONEY_WRITE_TEST), bash("python3 -m unittest"), output(RED))

    def test_test_edited_then_fix(self):
        self.check("test-edited-before-fix", True, edit("test_money.py"), edit("money.py"))

    def test_test_written_through_bash_then_fix(self):
        self.check("test-edited-before-fix", True, bash(CAT_TEST), edit("money.py"))

    def test_bash_fix_then_test_edited_fails(self):
        self.check("test-edited-before-fix", False, bash(CAT_MONEY), write("test_money.py"))

    def test_fix_only_fails(self):
        self.check("test-edited-before-fix", False, edit("money.py"))


if __name__ == "__main__":
    unittest.main()
