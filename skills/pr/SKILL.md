---
name: pr
description: Format for a pull request body that a human can review fast - a small visual of the change, before-and-after evidence, and a merge danger call (one-way or two-way door, blast radius). Use whenever writing or rewriting a PR description, including at the end of spec-first.
---

# PR body

Adapted from Matt Pocock's `pr` skill (mattpocock/skills, MIT), whose Summary visuals come from Dex Horthy's `show-me` skill (humanlayer/skills, MIT).

The body tells the reviewer in under a minute what changed, whether it works, and how carefully to read it. Write it for a reviewed diff, from the diff, the spec and the test output. Start at `## Summary`, with no preamble, and keep the prose brief.

```markdown
## Summary

<one or two sentences: what and why>

<the smallest visual that makes the change clear>

## Evidence

- **Before:** <failing test, old output, or screenshot>
- **After:** <passing test, new output, or screenshot>

## Merge danger

**Door:** one-way | two-way. <why, one line>

**Blast radius:** <who or what breaks if this is wrong>

## Acceptance criteria
## Notes for the reviewer
## Follow-ups
```

Write the last three sections only when they have content:
- **Acceptance criteria**: when there is a spec, each criterion with how it is met (test name or manual check).
- **Notes for the reviewer**: reuse decisions, security notes, and review findings that were not fixed, with the reason.
- **Follow-ups**: links to issues created during the work.

## Summary visual

Pick the one view that makes the key point clear; occasionally two. Keep only the calls, files, states and boundaries the reviewer needs.

- Logic or an algorithm: pseudocode.
  ```text
  on(save)
    if content is unchanged
      return cached result
    write new content
  ```
- Runtime control flow: a call tree.
  ```text
  submitOrder
    validateCart
    chargePayment
    sendConfirmation (queued)
  ```
- UI structure: a component tree, with the state and module boundaries that matter.
- A refactor or new files: a shallow file tree with one comment per entry.
- Interaction between components or services: a Mermaid diagram (GitHub renders it).
  ````markdown
  ```mermaid
  sequenceDiagram
      Admin->>App: apply 20% discount
      App->>Queue: DiscountApplied mail
      Queue-->>Customer: email
  ```
  ````
- What changes inside a shape that already exists: a `diff` block of that tree or flow, not of the code.
  ```diff
   submitOrder
     validateCart
  +  applyDiscount
     chargePayment
  ```
- Show a whole code block only when most of it is new and its shape is the point.

## Evidence

Show a before and after, not "tests pass".
- A screenshot is strongest for a visual change. `gh` cannot upload images, so use one only when the user provides it or the repo already hosts it.
- Otherwise name the test that failed before and passes now, or show the command output that changed, trimmed to the lines that matter.
- If something could not be verified (no runner, no device), say so here.

## Merge danger

The door call tells the reviewer where to spend attention: skim a two-way door with a small blast radius, read a one-way door slowly.

- **Two-way door**: a revert undoes it completely. Code-only changes, feature-flagged work, additive migrations.
- **One-way door**: a revert does not undo the effect. Examples: a migration that drops or rewrites columns or data; emails, push notifications or webhooks sent to real people; queued or scheduled jobs that act on production data; payments, refunds, orders or stock (WooCommerce included); a public API or URL change that clients depend on; a Core Data or SwiftData model migration shipped to devices; an App Store submission.
- **Blast radius**: everything that breaks if the change is wrong: which users, screens, integrations or data, and how many. Consider layout shifts, mobile, other consumers of a changed function or API.

You wrote the change, so you are biased toward calling it safe. When in doubt, call it one-way and say what makes it so.
