---
name: verify
description: Check a change to PROJECT in the running app before committing it or opening a PR - start it with safe data, drive the changed flow, read the result. Use for any change a user can see or that changes behaviour, and whenever asked to check that PROJECT works.
---

# Verify <PROJECT>

Run `.claude/skills/verify/checks.sh` first; it is the fast part. Then check the changed flow in the running app as below. Report each flow you checked with its evidence (screenshot path, output lines, response), and name every flow you could not check and why.

## Start

<Exact commands to build and start the app with safe data (demo, seed or fixture mode). How to tell it is up. How to stop it. Typical time.>

## Drive

<The tool that drives this app and how to reach a flow with it: a URL, a menu path, a shortcut, a demo state, a command.>

## Inspect

<What to read after each step: the screenshot, runtime errors or console log (with the command), a database query on the demo data, the response body.>

## Feature map

| Flow | How to reach it | Expected result |
| --- | --- | --- |
| <the flow in the user's words> | <URL, menu path, shortcut, demo state or command> | <what the user should see or get> |

## Known pitfalls

<Steps that need the user (a permission, a sign-in), slow steps, and what a false failure looks like.>
