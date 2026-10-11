---
type: regex
target: trace
pattern: '^(?:(?!"file_path":"[^"]*/money\.py","(?:old_string|content)")[\s\S])*?FAILED \((?:failures|errors)='
---
A unittest run fails before money.py is changed (Edit or Write). Deterministic twin of red-before-fix, whose judge sees only the start and end of a long trace.
