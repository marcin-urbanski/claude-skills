"""Pass rates with Wilson 95% intervals for the pressure study (docs/specs/2026-11-03-pressure-study.md).

Each input is a `claude plugin eval --json` result from evals/ (the rules arms)
or evals-norules/ (the no-rules arms); its with/without arms give the plugin
and no-plugin halves. Runs that errored are left out and counted.

Usage: python3 scripts/study-table.py evals/results/study/opus-*.json
"""

import json
import math
import sys

ARMS = ["bare", "skills", "rules", "rules + skills"]
ARM = {
    ("evals-norules", "without"): "bare",
    ("evals-norules", "with"): "skills",
    ("evals", "without"): "rules",
    ("evals", "with"): "rules + skills",
}
Z = 1.96


def wilson(passed, total):
    p = passed / total
    centre = (p + Z * Z / (2 * total)) / (1 + Z * Z / total)
    margin = Z * math.sqrt(p * (1 - p) / total + Z * Z / (4 * total * total)) / (1 + Z * Z / total)
    return max(0.0, centre - margin), min(1.0, centre + margin)


def cell(passes):
    if not passes:
        return "–"
    low, high = wilson(sum(passes), len(passes))
    return f"{sum(passes)}/{len(passes)} ({low * 100:.0f}–{high * 100:.0f}%)"


def table(paths):
    passes, errors, graders = {}, {}, {}
    for path in paths:
        with open(path) as f:
            data = json.load(f)
        for case in data["cases"]:
            eval_dir = case["dir"].split("/")[0]
            for arm_key, runs in case["arms"].items():
                arm = ARM[(eval_dir, arm_key)]
                for run in runs:
                    if run.get("error"):
                        errors[(case["name"], arm)] = errors.get((case["name"], arm), 0) + 1
                        continue
                    for g in run["graders"]:
                        graders.setdefault(case["name"], {}).setdefault(g["name"], None)
                        passes.setdefault((case["name"], g["name"], arm), []).append(bool(g["passed"]))
    lines = ["| case | grader | " + " | ".join(ARMS) + " |", "|---|---|" + "---|" * len(ARMS)]
    for case, names in graders.items():
        for grader in names:
            cells = [cell(passes.get((case, grader, arm), [])) for arm in ARMS]
            lines.append(f"| {case} | {grader} | " + " | ".join(cells) + " |")
    if errors:
        counts = ", ".join(f"{case} {arm} {n}" for (case, arm), n in errors.items())
        lines.append(f"\nErrored runs left out: {counts}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.stdout.write(table(sys.argv[1:]))
