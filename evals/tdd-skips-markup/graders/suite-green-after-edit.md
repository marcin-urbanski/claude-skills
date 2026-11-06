---
type: regex
target: trace
pattern: '(?:"file_path":"[^"]*/index\.html","(?:old_string|content)"|"command":"(?:[^"\\]|\\.)*?(?:(?<!\w)|(?<=\\n))sed +(?:-[A-Za-z]+ +)*-[A-Za-z]*i(?:[^"\\]|\\.)*?(?<![\w-])index\.html(?![\w.]))[\s\S]*?Ran \d+ tests? in [\d.]+s\\n\\nOK(?![\s\S]*?FAILED \()'
---
After index.html is first changed (Edit, Write or `sed -i`), a unittest run passes and no later run fails.
