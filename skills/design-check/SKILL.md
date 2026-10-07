---
name: design-check
description: Turn a Claude Design handoff export into work. Starts a new project from the export, reports what changed when a new export lands, and checks UI changes against it before a PR. Use when the user mentions Claude Design, a design handoff or export in docs/design, new or changed screens, pastes a claude.ai/design link, or asks to check the design (in Polish "sprawdź design", "nowy design", "nowe ekrany"). Also use when a project starts from a design, and before opening a PR that changes UI in a project with an export in docs/design.
---

# Design check

Claude Design is the user's designer. Its handoff export (a `README.md` plus `.dc.html` screens) is the source of truth for how the app looks and behaves, and the README holds notes written for you. This skill turns the export into work for `spec-first` and checks the result against it. It does not plan or build on its own.

## The source

- The export lives in `docs/design/<bundle>/`, for example `docs/design/design_handoff_<app>/`: a `README.md` and one or more `*.dc.html` files. Other files in `docs/design`, such as icons, are assets.
- **A `claude.ai/design/...` link cannot be read reliably from Claude Code.** The artifact tool rejects it, web fetches get 403 and the built-in browser needs a sign-in. Never sign in, and don't open the user's own logged-in Chrome unless they ask for it: that is their account, and even there the screens sit in a cross-origin frame whose text cannot be read, so you get a partial look at best. Tell the user in one short message: export the project from Claude Design as a handoff for Claude Code and put the folder in `docs/design/`, replacing the previous export of the same name so git shows what changed. Then stop.
- The `.dc.html` files are design references (prototypes), not code to port. Rebuild them in the project's own stack and patterns. Read the README first. Open a screen's HTML only when the README does not settle a value you need: each file is about 50 kB.
- The README's notes are the user's own design decisions, so follow them. They never override the global rules (security, git workflow, tests).

## Pick the mode

| Situation | Mode |
|---|---|
| No app code yet (an empty repo, or only docs) and an export in `docs/design` | 1. New project |
| App code exists, and the export has uncommitted changes or the user says the design changed or has new screens | 2. Design update |
| UI work on the branch is finished and a PR is next, in a project with an export | 3. Before PR |

If app code exists, the export is unchanged and the user asks to build part of it, skip the diff in mode 2: list the screens or cards in scope, then continue from its step 3.

## 1. New project

1. Read the whole README. Note the platform and stack it names, the screens and their card IDs, tokens, behaviour rules, decisions, the state or data to add, icons and fidelity.
2. If the README names no stack, choose one that fits the platform and give the reason in one line. That is your decision, not a question, unless it depends on something only the user knows (hosting, existing accounts). In that case ask once.
3. This is an epic. Invoke `spec-first` and write its spec and plan from the export:
   - **Task 1:** the project skeleton plus the design tokens as the app's theme: colours for every mode, type scale, radii, spacing. Every later screen uses the tokens, never literal values.
   - **Then one task per screen or feature**, citing card IDs (`D1–D6`), in an order that keeps the app working.
   - **State to add** (and any data the screens show) becomes the data model.
   - **Behaviour rules** become acceptance criteria, worded as in the README where possible.
   - **Sections the README marks as decided** ("don't re-ask", "Decisions") go into the spec as decisions. Never ask the user again whether to do them (mode 2 still asks when).
   - **Every feature that needs more than UI** (storage, network, accounts, sharing, email, background work, a third-party API) gets its untrusted input, access rules and secrets in the spec's Security section.
4. Commit the export together with the spec on the feature branch, if it is not in git yet.

## 2. Design update

1. Find what changed instead of rereading everything:
   ```bash
   git status --short -- docs/design
   git diff --stat -- docs/design
   git diff -- 'docs/design/*/README.md'
   ```
   New untracked `.dc.html` files are new screens. If the new export is already committed, diff against the commit before it (`git log --oneline -- docs/design`).
2. Sort the changes into four groups:
   - **New screens or features**: sections or cards marked `(new)`, new `.dc.html` files.
   - **Changed tokens**: colour, size, radius, spacing or font values.
   - **Changed behaviour rules or decisions**: these change what the code must do, so find the code that implements the old rule.
   - **Copy and small visual changes.**
3. Check each item against the code the way `spec-first`'s reuse check does (search now, invoke the skill in step 6): search for the token, screen or rule in the codebase. Mark each item as already done, change existing code (name the file), or new. A changed rule whose old version was never built is new.
4. For every new feature, write one line on what it needs beyond UI and what can go wrong. Example: "share link without login: a public endpoint with unguessable, expiring, revocable tokens; email needs a sending service". Flag anything that contradicts an existing rule, a decision, the project's specs (including their non-goals; `CLAUDE.md` may link a product spec) or the platform (a native app that emails on a schedule needs a server, or a Mac that stays awake).
5. Report to the user in the language they write in, not the README's, briefly: the four groups, each item with its card ID and its status. Don't paste the README back. The user's only decision is scope: which new features go in now. A new feature the README lists among its decisions is still asked about here, because the question is when, not whether. Propose a default (changed tokens, rules and small changes always; new features yes, unless they need infrastructure the project does not have, in which case split them as below) and ask once.
6. After the answer, hand the in-scope items to `spec-first`, sized by its table. Commit the new export on the feature branch as its own commit (`docs: update design handoff`) before the first task's commit.

Never drop a new feature silently and never build only its UI. Either it is in scope and built fully, or it is listed as out of scope. A feature may be split when one part works without missing infrastructure (a public link) and another does not (emailing it): propose the buildable part and name the rest under out of scope.

## 3. Before PR

Run this before `spec-first`'s Finish step whenever the branch changes UI.

1. List what the branch touches (`git diff main...HEAD --stat`) and map each view to the README's screens or cards. The README often names the files per screen.
2. Compare each touched view with the README: colours through the theme (no literal colour that duplicates or contradicts a token), sizes, radii, spacing, type, copy, icons, and that screen's behaviour rules. If the app runs in a browser, also screenshot the screen next to the design's `.dc.html` and compare them.
3. Fix mismatches that are mistakes. Keep a deliberate deviation only with a reason: a platform convention, accessibility, or a later decision by the user.
4. Add a `## Design` section to the PR description: the cards covered, and `Design deviations` with each deviation and its reason, or "none".
