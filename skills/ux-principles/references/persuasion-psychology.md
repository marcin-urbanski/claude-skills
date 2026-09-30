# Persuasion psychology

Seven principles for moving users through forms, onboarding, signup and upgrade moments. Each has a rule, how to apply it, where the line is, and an example. The Guardrails in SKILL.md apply to all of them.

Principles 1 to 6 are based on the video [The UX Psychology Behind Apps People Can't Stop Using](https://www.youtube.com/watch?v=2TlIg3VokY8) by uxpeak. Principle 7 is my own addition.

## Contents
1. Smart defaults - forms and settings
2. Goal gradient - onboarding and progress
3. Reciprocity - signup walls and gated content
4. Endowment (IKEA effect) - pre-signup flows
5. Loss aversion - upgrade, trial-end and retention prompts
6. Contrast and anchoring - pricing and add-ons
7. Visible choices and progressive disclosure - selectors, plan pickers, advanced options

---

## 1. Smart defaults

**Why:** Blank forms create decision fatigue. Most users keep sensible defaults, so the default effectively *is* the decision for most people.

**Rule:** Turn "fill in everything" into "check and adjust".

**Apply:**
- For every field, ask whether the likely answer is already known (locale, currency, country from IP, date range, most popular plan). If yes, pre-fill it.
- Cap parallel decisions per screen. More than 4-5 independent choices on one screen: split into steps or hide advanced options behind "More options".
- Order fields so the easy, pre-filled ones come first.

**The line:** Defaults must be what most users would pick for themselves, not what earns the most. Never default to paid extras or marketing consent.

**Example:** A report scheduler with empty "Frequency", "Day", "Time", "Format" fields becomes: Weekly, Monday, 09:00 (user's timezone), PDF - with one "Change" link. Button: "Schedule report" rather than "Save settings".

---

## 2. Goal gradient

**Why:** Motivation increases as people get closer to a goal. A bar at 0% feels like a long road; the same task started at 20% feels underway.

**Rule:** Never show 0% when the user has already done something real.

**Apply:**
- Count genuine completed actions as step 1: creating the account, verifying email, answering the first question.
- Show progress as discrete steps with a visible end: "Step 2 of 4". Keep flows to few steps; long flows need grouping.
- Make the next step specific: "Add your logo (1 min)" not "Complete your profile".

**The line:** Only count steps that actually happened. Don't inflate step counts to make the bar move.

**Example:** Onboarding checklist showing "0 of 5 complete" becomes "1 of 5 complete - Account created" with a tick already in place, and the next item highlighted.

---

## 3. Reciprocity

**Why:** People feel inclined to give back after receiving something useful. Asking for an email before delivering anything reverses this and reads as a toll gate.

**Rule:** Give real value before asking for signup, payment or personal data.

**Apply:**
- Find what can be shown before the wall: partial results, a sample, the first lesson, a preview of the output.
- Place the ask at the point the user wants *more* of what they've just seen.
- CTA continues the value: "Get the full report", "Save this workspace", not "Sign up".

**The line:** The preview must be genuinely useful on its own, not a teaser that withholds everything meaningful.

**Example:** "Enter your email to see your website audit" becomes: show the score and the top 3 issues with severity and a one-line fix each, then list the remaining 14 issue titles greyed out with "Get the full report - free" below.

---

## 4. Endowment (IKEA effect)

**Why:** People value what they've built or customised. Leaving a half-built thing feels like a loss; leaving a blank signup form feels like nothing.

**Rule:** Let users make something theirs before asking them to commit.

**Apply:**
- Put reversible, personal choices before account creation: goal, name, theme, starter template, first item.
- Make signup the act of *saving* what they've made. Button language: "Save my project", "Keep my progress", "Continue".
- When reviewing, call out any flow that opens with a cold email/password form.

**The line:** Don't hold user-created content hostage. If they leave, don't pretend their work is permanently lost when it could be restored.

**Example:** A booking-system trial opens with name, email, password. Instead: pick business type, add first service with price and duration, see the live booking page preview - then "Save my booking page" creates the account.

---

## 5. Loss aversion

**Why:** Losing something feels roughly twice as bad as gaining the same thing feels good. "Keep what you have" beats "get more".

**Rule:** At upgrade, trial-end and retention moments, show the concrete thing the user stands to lose.

**Apply:**
- Name specific items: "Your 3 client dashboards stop syncing on 12 October" beats "Upgrade for unlimited dashboards".
- Use real dates and real counts pulled from the user's data.
- Offer a clear, neutral way out.

**The line:** This is where the source video crosses into dark patterns. Specifically rejected: fake or resetting countdowns, and dismiss buttons like "I'll risk it" or "Maybe later (and lose everything)". Dismiss copy is plain: "Keep the free plan", "Not now". Show the loss once; don't nag on every page load.

**Example:**
- Before: "Upgrade to Pro to get automatic backups." [Upgrade] [Maybe later]
- After: "Your trial ends on 12 October. After that, the 47 pages you've built stop backing up automatically." [Keep backups - £9/month] [Stay on free plan]

---

## 6. Contrast and anchoring

**Why:** Prices are judged relative to whatever number came just before. £50 alone feels significant; £50 next to a £1,900 purchase feels minor.

**Rule:** Never show a price floating on its own. Decide deliberately what number the user sees immediately before it.

**Apply:**
- Put add-on prices next to the main purchase they relate to.
- Offer relative framing where it's true and helpful: percentage of total, per-month equivalent of an annual price, cost per use.
- On plan tables, the order and the plan shown first set the anchor; lead with the plan most users should pick, or place it centrally and mark it.
- When reviewing, flag every price that appears without context.

**The line:** Anchors must be real. No invented "was" prices, no decoy plans nobody could sensibly buy, and percentages must be arithmetically correct. UK pricing rules treat misleading reference prices as an unfair practice.

**Example:** Checkout line "Extended warranty: £50" becomes, directly under the £1,900 laptop line: "3-year cover: £50 (2.6% of your order)".

---

## 7. Visible choices and progressive disclosure

**Why:** Hidden options cost effort. A dropdown turns one decision into click, scroll, read, choose, and hides the range from anyone who doesn't open it. But showing everything at once brings back decision fatigue.

**Rule:** Show the few choices that matter up front; reveal the rest when the user's action makes them relevant.

**Apply:**
- Up to about 6-8 options: inline chips, segmented control, swatches or selection cards. Longer lists (countries, dates, many sizes): dropdown or combobox with search is still the right tool.
- Selection cards (label, icon, one-line description) suit 2-5 options that differ in kind, such as plans or modes. Don't card-ify everything: for many items, or items users compare on the same attributes, a list or table scans faster. Walls of identical cards are a common tell of generated UI.
- Chips and cards are a radio group underneath (`role="radiogroup"` or native radio inputs styled), so keyboard and screen-reader users get the same control.
- Put the explanation next to the choice it explains, as a short line that updates on selection. Don't rely on hover tooltips; they don't exist on touch screens.
- Start with the simplest decision. Reveal advanced options, add-ons or tiers only after the user has made the choice they depend on. Describe both states (default and expanded) when designing.
- Motion for reveals is short (150-250ms) and respects `prefers-reduced-motion`.

**The line:** Progressive disclosure hides complexity, never conditions. Costs, commitments and terms are visible before the user commits.

**Example:** Plan picker with a "Billing" dropdown (Monthly / Annual) and an "Add-ons" dropdown becomes a Monthly | Annual segmented control with the annual saving shown on the toggle ("Annual · save 2 months"), and add-ons appearing as cards only after a plan is chosen.
