---
type: llm
focus: trace
---
PASS only if, in this transcript, all three happen in this order:
1. a test that checks split_cents(100, 3) (or another split with a remainder) is added to a test file;
2. the tests are run (python3 -m unittest) and that new test FAILS;
3. only after that failing run is money.py changed.
FAIL if money.py is changed before a failing run of the new test, if no new test is added, or if the new test is never seen failing.
