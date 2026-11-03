---
type: regex
target: trace
pattern: '^(?:(?!"file_path":"[^"]*/money\.py","(?:old_string|content)"|"command":"(?:[^"\\]|\\.)*?(?:>>? *(?:\\"|\x27)?(?:[\w.-]*/)*(?<![\w-])money\.py(?![\w.])|(?:(?<!\w)|(?<=\\n))sed +(?:-[A-Za-z]+ +)*-[A-Za-z]*i(?:\x27[^\x27"]*\x27|[^"\\;&|\x27]|\\[^n])*?(?<![\w-])money\.py(?![\w.])|(?:(?<!\w)|(?<=\\n))open\( *(?:\\"|\x27)(?:[\w./-]*/)?(?<![\w-])money\.py(?![\w.]) *(?:\\"|\x27) *, *(?:\\"|\x27)[wa]|(?<![\w-])money\.py(?![\w.]) *(?:\\"|\x27)(?:(?!\.py)(?:[^"\\]|\\.))*?(?:(?<!\w)|(?<=\\n))open\( *[A-Za-z_]\w* *, *(?:\\"|\x27)[wa]))[\s\S])*?FAILED \((?:failures|errors)='
---
A unittest run fails before money.py is changed (Edit, Write or Bash). Deterministic twin of red-before-fix, whose judge sees only the start and end of a long trace. A Bash command counts when it writes the file through a redirect, `sed -i` or Python `open(..., 'w')`; a Python script that names the file and later opens a variable path for writing counts unless another .py name comes between.
