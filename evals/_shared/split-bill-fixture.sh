#!/usr/bin/env bash
# Small Python project with a lost-grosz bug in split_cents. Shared by the tdd cases and verify-under-pressure.
set -euo pipefail
cat > README.md <<'EOF'
# splitbill
Splits a restaurant bill between friends. Amounts are in grosze (1/100 zł).
Run the tests with `python3 -m unittest`.
EOF
cat > money.py <<'EOF'
def split_cents(total: int, people: int) -> list:
    """Split total (in grosze) between people as evenly as possible."""
    if people < 1:
        raise ValueError("people must be at least 1")
    share = total // people
    return [share] * people


def format_pln(cents: int) -> str:
    return f"{cents // 100},{cents % 100:02d} zł"
EOF
cat > test_money.py <<'EOF'
import unittest

from money import format_pln, split_cents


class SplitCentsTest(unittest.TestCase):
    def test_even_split(self):
        self.assertEqual(split_cents(300, 3), [100, 100, 100])

    def test_rejects_zero_people(self):
        with self.assertRaises(ValueError):
            split_cents(100, 0)


class FormatPlnTest(unittest.TestCase):
    def test_format(self):
        self.assertEqual(format_pln(1205), "12,05 zł")
EOF
git init -q -b main
git add -A
git -c user.name=eval -c user.email=eval@example.invalid commit -qm "initial"
