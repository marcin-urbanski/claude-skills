---
type: regex
target: trace
pattern: '^(?:(?!"file_path":"[^"]*/money\.py","(?:old_string|content)")[\s\S])*?"file_path":"[^"]*/test[^"/]*\.py","(?:old_string|content)"'
---
A test file is changed (Edit or Write) before money.py is.
