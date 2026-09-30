---
name: "ux-principles"
description: Marcin's personal UI/UX rulebook. Use it whenever the task involves designing, building, reviewing or writing copy for any user-facing interface - websites, landing, pricing and product pages, checkout, forms, onboarding, paywalls, dashboards, admin panels, lists, navigation, modals, empty states, button labels or microcopy, and native iPhone, iPad and Mac apps - even if the user doesn't say "UX". Covers avoiding generic AI-looking design, honest conversion psychology (defaults, social proof, trust badges, option selectors, pricing), visual craft (hierarchy, spacing, typography, colour, icons, shadows, motion), interaction patterns (thumb zone, touch targets, menus), app patterns (undo vs confirmation, alerts, controls, search, loading, keyboard, notifications) and Apple's Human Interface Guidelines (Dynamic Type, Liquid Glass, SF Symbols, Mac menu bar, App Review). Also use it when generating UI code (React, Blade, Livewire, WordPress/WooCommerce, SwiftUI) and to critique a screenshot, mockup or Figma frame.
---

# UX Principles

This skill holds the rules I want every interface to follow: how a screen guides decisions, how it looks and holds together, and how product pages sell. Where another design skill also applies, use it for aesthetic direction and this skill for the rules; if they conflict, this skill wins.

## Design ambition comes first

Design leads; the build follows. Nothing in this skill caps how ambitious, immersive or motion-rich a design can be, and the tech stack never decides what gets designed.

- **Hard limits** are only the Guardrails below: honesty, UK consumer law, and accessibility. Accessibility is met by how an ambitious design is executed (fallbacks, reduced-motion states, focus handling), never by designing the ambition out.
- **The design mode sets the defaults.** Creative mode relaxes restraint rules that Corporate and App modes keep.
- **Everything else is a default** for when the brief is silent. A client's request, a reference site they point to, or a deliberate concept overrides it. "Restraint" rules target effects added by reflex, not effects that are the idea.
- **Implementation notes** (WooCommerce, Filament, CSS-first motion) describe how to build well, not what may be designed. If a design needs WebGL, GSAP, video or custom interaction, design it, then flag the build implications (performance budget, fallbacks, who maintains it) as notes for the build stage, not as reasons to simplify.
- Design with realistic content shapes, since the build will populate real data: long titles, missing images, empty lists, 1 vs 999 items. See `visual-craft.md` section 2.

## How to work

1. **Choose the design mode** (`design-modes.md`): Creative, Corporate, Landing page, E-commerce, or App and dashboard. Use the mode the user names; otherwise pick from the signals and state it in one line. The mode sets how much layout freedom and motion the design has, the content-to-imagery balance, CTA placement, and which references to load. Then identify the surface within it (form, pricing, product page, onboarding, etc.).
2. **Read only the references that apply.** Don't load everything for a single button label.
3. **Set the direction** for any new site or page (`anti-slop.md` section 1): three genuinely different directions first, then one chosen. Skip only when the client's own design system decides it; in a native Apple app the platform's conventions decide the chrome, so set a direction only for the parts that carry identity (`apple-platforms.md` section 1). For a narrow edit, don't widen the task: fix what was asked without adding new slop.
4. **Rank the information.** Before any layout, list what's on the screen and rank it by importance to the user's goal (`visual-craft.md` section 1). Everything else follows from that ranking.
5. **Build or review against the rules.**
   - When *building*: apply the rules silently in the output. Don't narrate psychology theory unless asked.
   - When *reviewing*: use the review format below.
6. **Run the honesty check** (see Guardrails) on anything persuasive.
7. **Run the anti-slop check** (`anti-slop.md` section 7) before handing over any new design.

## Reference files

| File | Read when the task involves |
|---|---|
| `references/design-modes.md` | Always, at the start of any design task: choosing Creative, Corporate, Landing page, E-commerce or App mode and what each allows |
| `references/anti-slop.md` | Every new screen, page or site: setting a design direction, the tells of generic AI-generated UI, clusters of generic AI-UI tells, the removal test, auditing an existing design, and the final check before handover |
| `references/persuasion-psychology.md` | Forms, defaults, option selectors, progressive disclosure, onboarding progress, signup walls, paywalls, upgrade/retention prompts, pricing and add-ons |
| `references/visual-craft.md` | Any screen being built or visually reviewed: hierarchy, spacing, alignment, colour, typography, labels/badges, icons, dividers, UI over imagery, shadows, motion |
| `references/interaction-patterns.md` | Any screen with content to reach or act on: interaction cost, banners that hide content, mobile thumb zone and touch targets, empty states, scanning cues, forms (labels, spacing, field widths), navigation and mega menus |
| `references/marketing-pages.md` | Landing pages and pricing pages: message match, objection-led structure, proof placement, plan cards, pricing transparency, noindex and FAQ SEO |
| `references/app-patterns.md` | Any app, web or native: confirmations vs undo, alerts, modals and popovers, app menus and context menus, choosing a control, tables, search, loading and progress, keyboard and focus, notifications, accounts and permissions, AI features, interface copy |
| `references/apple-platforms.md` | Native iPhone, iPad or Mac apps: platform conventions, sizes in pt, text styles and Dynamic Type, semantic colours and Dark Mode, Liquid Glass, navigation structure, toolbars, windows, the Mac menu bar, shortcuts, SF Symbols, app icon, accessibility |
| `references/apple-patterns.md` | Native Apple app components and flows: alerts and action sheets, sheets, lists and controls, text input, launch and onboarding, permissions, settings, accounts, paywalls and In-App Purchase, ratings, notifications, widgets and Live Activities, documents |
| `references/product-pages.md` | E-commerce product pages and catalogue grids: imagery, status badges, social proof, variant selectors, subscription/bundle cards, add to basket, trust badges, sticky mobile bars, quantity presets |

Building a full screen usually needs `anti-slop.md`, `visual-craft.md` and `interaction-patterns.md`; a product page adds `product-pages.md` and `persuasion-psychology.md`; a landing or pricing page adds `marketing-pages.md` and `persuasion-psychology.md`; an app screen with dialogs, menus or long-running tasks adds `app-patterns.md`. A native Apple app loads `apple-platforms.md`, `apple-patterns.md` and `app-patterns.md` (plus `persuasion-psychology.md` for onboarding and paywalls), and those take precedence over web sizing rules in the other files.

New principle sets are added as new files here. If a reference file conflicts with this SKILL.md, this file wins.

## Review format

When asked to critique a flow, screen, page or copy:

1. **Verdict:** one short paragraph on the dominant problems and what to fix first.
2. **Findings:** the 5-8 highest-impact issues, repeated instances grouped under one root cause, in a table:

| Priority | Problem (named precisely, with location) | Rule broken | Fix |
|---|---|---|---|

   The Fix column gives the concrete design change *and* the rewritten copy. Never "consider improving the CTA"; write the CTA.

   Priorities: **P0** blocks the task, is a serious accessibility failure, or is deceptive (fake proof, dark pattern). **P1** materially harms understanding, trust or interaction. **P2** repeated slop or inconsistency weakening hierarchy and identity. **P3** minor polish.
3. **Unknowns:** anything that couldn't be checked (states, breakpoints, behaviour).
4. End with the single change that would improve it most.

Skip praise, generic best-practice lists and empty sections.

## Measuring changes

For changes meant to improve conversion or engagement (not every spacing fix), add one line: the metric it should move and how to check it. E.g. "Track add-to-basket rate on this template, 4 weeks before vs after."

Only propose an A/B test when the page has the traffic for it: as a rough guide, a few hundred conversions per variant over a few weeks. Most client sites don't. Below that, use a before/after comparison in analytics, session recordings, or a quick five-person usability test, and say which.

## Guardrails

These are the only hard limits in this skill. They override any persuasion rule and any default in the reference files. Most of my work is for UK clients, and since April 2025 the Digital Markets, Competition and Consumers Act 2024 lets the CMA fine businesses directly (up to 10% of global turnover) for unfair commercial practices, including manipulative interface design. A pattern that "converts" but misleads is a client liability, not a win.

- **Only real deadlines.** No countdown timers, "offer ends soon" or low-stock claims unless they reflect something that genuinely happens at that time.
- **No confirmshaming.** Dismiss options are neutral and plain ("Keep the free plan", "Not now"), never guilt-tripping ("No thanks, I don't like saving money", "I'll risk it").
- **Progress must be real.** Pre-filled progress counts only steps the user has actually completed.
- **Prices must be true.** No invented "was" prices or reference prices that never applied. Relative framing ("2.6% of your order") must be arithmetically correct.
- **Social proof and claims must be real.** Exact review counts, sales figures from actual orders, badges and certifications the client can evidence. Fake reviews are banned outright under the DMCC Act. Never present statutory rights (e.g. 14-day online returns) as a special feature.
- **Defaults must serve the user.** Pre-select the most common *genuine* choice. Never pre-tick marketing consent, paid add-ons, subscriptions or auto-renewal upsells - under UK GDPR, pre-ticked consent is not valid consent anyway.
- **Cancellation is as easy as signup.** Retention flows can remind users what they'll lose, once, then let them leave.
- **Accessibility is not traded for aesthetics.** Text 4.5:1 contrast (large text 3:1), icons and controls 3:1, touch targets 48x48px by default and never below 44x44px on the web. Native Apple apps follow the platform sizes in `apple-platforms.md` section 3 (iOS 44x44pt, macOS 28x28pt by default). "Softer" and "calmer" stay above these lines.

If a request asks for something that breaks a guardrail, build the honest version and say in one line why.

## Personal taste

Rules specific to how I like interfaces to look and behave go here as short bullets, added over time.

- (none yet)

## Sources

Much of `interaction-patterns.md`, `visual-craft.md` and principle 7 of `persuasion-psychology.md` builds on uxpeak's [UI/UX Playbook](https://www.uxpeak.com) (free preview); principles 1 to 6 on their video [The UX Psychology Behind Apps People Can't Stop Using](https://www.youtube.com/watch?v=2TlIg3VokY8). The rules here are rewritten and extended, not copied.

`app-patterns.md`, `apple-platforms.md` and `apple-patterns.md` are based on Apple's [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) (read September 2026), paraphrased as rules and combined with my own judgement; they don't reproduce Apple's text.
