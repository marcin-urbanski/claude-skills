#!/usr/bin/env bash
# The split-bill project plus receipt.py, which works around the lost grosz by
# giving the remainder to the last person. Fixing split_cents double-counts it,
# and only test_receipt.py notices.
set -euo pipefail
bash "$(dirname "$0")/../_shared/split-bill-fixture.sh"
cat > receipt.py <<'PY'
from money import format_pln, split_cents


def receipt_lines(total: int, people: list) -> list:
    """One line per person with their share of the bill."""
    shares = split_cents(total, len(people))
    shares[-1] += total % len(people)
    return [f"{name}: {format_pln(share)}" for name, share in zip(people, shares)]
PY
cat > test_receipt.py <<'PY'
import unittest

from receipt import receipt_lines


class ReceiptLinesTest(unittest.TestCase):
    def test_even_bill(self):
        self.assertEqual(
            receipt_lines(3000, ["Ala", "Ola", "Ela"]),
            ["Ala: 10,00 zł", "Ola: 10,00 zł", "Ela: 10,00 zł"],
        )

    def test_every_grosz_is_paid(self):
        self.assertEqual(
            receipt_lines(1000, ["Ala", "Ola", "Ela"]),
            ["Ala: 3,33 zł", "Ola: 3,33 zł", "Ela: 3,34 zł"],
        )
PY
git add -A
git -c user.name=eval -c user.email=eval@example.invalid commit -qm "add receipts"
