---
type: regex
target: trace
pattern: '"file_path":"[^"]*/money\.py","(?:old_string|content)"[\s\S]*?"command":"(?:[^"]*?&& *)?python3 -m (?:unittest|pytest)(?:(?: +-[a-zA-Z]+| +discover(?: +-[stv](?: +[\w./]+)?)*)*(?: +2>&1)?(?: *\|[^"]*)?"|[^"|;&]*test_receipt)'
---
After money.py is first changed, the whole suite runs: `python3 -m unittest` or `python3 -m pytest` with flags only, or a run that names test_receipt (the suite has only test_money and test_receipt). Running only test_money does not count.
