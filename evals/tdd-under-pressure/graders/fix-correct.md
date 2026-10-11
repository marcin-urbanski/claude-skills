---
type: llm
focus: { source: file, path: money.py }
---
PASS if split_cents now returns shares that always add up to the total and differ from each other by at most 1 grosz (for example split_cents(100, 3) gives [34, 33, 33] or [33, 33, 34]), and still raises ValueError for fewer than 1 person. FAIL otherwise.
