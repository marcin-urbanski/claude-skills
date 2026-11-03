"""Re-apply the regex graders to saved transcripts, without re-running the agents.

A fixed regex grader then changes the scores of runs already paid for. Each run
is matched to its transcript by the run's temp folder (e-XXXXXX on macOS,
claude-eval-XXXXXX on Linux), which appears
in both the result's tracePath and the transcript's cwd, so transcript file
names do not matter. Graders are read from evals/<case>/graders, also for
results from evals-norules/, whose graders are copies of them.

Each run's score is recomputed as `claude plugin eval` computes it (the weighted
mean of scored graders, passed at 1). The case and suite aggregates are dropped
rather than left stale: the runner's rules for errored runs are not reproduced,
and scripts/study-table.py does not read them.

Usage: python3 scripts/regrade.py --traces DIR --out DIR [--evals DIR] RESULT.json...
"""

import argparse
import json
import os
import re
import sys

RUN_ID = re.compile(r"/((?:claude-eval|e)-[A-Za-z0-9]+)/")
EVALS = os.path.join(os.path.dirname(__file__), "..", "evals")


def frontmatter(path):
    with open(path) as f:
        text = f.read()
    fields = {}
    for line in text.split("---")[1].strip().splitlines():
        key, _, value = line.partition(":")
        value = value.strip()
        if value.startswith("'") and value.endswith("'"):
            value = value[1:-1].replace("''", "'")
        fields[key.strip()] = value
    return fields


def load_regex_graders(case_dir):
    graders = {}
    folder = os.path.join(case_dir, "graders")
    for name in sorted(os.listdir(folder)):
        fields = frontmatter(os.path.join(folder, name))
        if fields.get("type") == "regex":
            if fields.get("target", "trace") != "trace" or fields.get("match", "contains") != "contains" or fields.get("flags"):
                sys.exit(f"{folder}/{name}: only target trace, match contains and no flags are supported")
            graders[name[: -len(".md")]] = fields["pattern"]
    return graders


def index_traces(traces_dir):
    traces = {}
    for name in sorted(os.listdir(traces_dir)):
        if not name.endswith(".jsonl"):
            continue
        path = os.path.join(traces_dir, name)
        with open(path) as f:
            for line in f:
                event = json.loads(line)
                if event.get("subtype") == "init":
                    found = RUN_ID.search(event["cwd"])
                    if found:
                        traces[found.group(1)] = path
                    break
    return traces


def score(run):
    scored = [g for g in run["graders"] if g["scored"]]
    return sum(g["weight"] * g["passed"] for g in scored) / sum(g["weight"] for g in scored)


def regrade(data, traces, evals_dir):
    flips = []
    for case in data["cases"]:
        eval_dir = case["dir"].split("/")[0]
        patterns = load_regex_graders(os.path.join(evals_dir, case["name"]))
        for g in case.get("graders", []):
            if g["name"] in patterns:
                g["config"]["pattern"] = patterns[g["name"]]
        for arm, runs in case["arms"].items():
            for i, run in enumerate(runs):
                if run.get("error") or not run["graders"]:
                    continue
                run_id = RUN_ID.search(run["tracePath"]).group(1)
                if run_id not in traces:
                    sys.exit(f"no transcript for {case['name']} {eval_dir} {arm} {i} ({run_id})")
                with open(traces[run_id]) as f:
                    trace = f.read()
                for g in run["graders"]:
                    if g["name"] not in patterns:
                        continue
                    passed = re.search(patterns[g["name"]], trace) is not None
                    g["explanation"] = f"matched {patterns[g['name']]}" if passed else "pattern not found in trace"
                    if passed != g["passed"]:
                        flips.append((case["name"], eval_dir, arm, i, g["name"], g["passed"], passed))
                        g["passed"] = passed
                run["score"] = score(run)
                run["passed"] = run["score"] >= 1
        case.pop("aggregates", None)
    data.pop("aggregates", None)
    return flips


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--traces", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--evals", default=EVALS)
    parser.add_argument("results", nargs="+")
    args = parser.parse_args(argv)
    traces = index_traces(args.traces)
    os.makedirs(args.out, exist_ok=True)
    for path in args.results:
        with open(path) as f:
            data = json.load(f)
        for case, eval_dir, arm, i, name, old, new in regrade(data, traces, args.evals):
            print(f"{case} {eval_dir} {arm} {i} {name}: {'PASS' if old else 'FAIL'} -> {'PASS' if new else 'FAIL'}")
        with open(os.path.join(args.out, os.path.basename(path)), "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
