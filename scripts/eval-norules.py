"""Copy the eval suite without the user's rules, for the no-rules arms of the pressure study.

Every case's prompt.md loses its append_system_prompt (the copy of "How I work"),
so `claude plugin eval . --eval-dir evals-norules` measures the skills, and the
no-plugin arm the bare model, without the rules that name them.

Usage: python3 scripts/eval-norules.py [src] [dst]   (default: evals evals-norules)
"""

import os
import shutil
import sys


def strip_rules(text):
    out, skipping = [], False
    for line in text.splitlines(keepends=True):
        if line.startswith("append_system_prompt:"):
            skipping = True
            continue
        if skipping and (line[:1] in (" ", "\n") or not line.strip()):
            continue
        skipping = False
        out.append(line)
    return "".join(out)


def build(src, dst):
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("results"))
    for root, _, files in os.walk(dst):
        if "prompt.md" in files:
            path = os.path.join(root, "prompt.md")
            with open(path) as f:
                text = f.read()
            with open(path, "w") as f:
                f.write(strip_rules(text))


if __name__ == "__main__":
    args = sys.argv[1:] + ["evals", "evals-norules"][len(sys.argv[1:]):]
    build(args[0], args[1])
