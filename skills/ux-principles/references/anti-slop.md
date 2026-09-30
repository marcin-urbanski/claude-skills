# Anti-slop

Generated UI looks generic because it falls back to the statistically average choice at every decision: the default font, palette, section order, effects and copy. No single choice is wrong; together they read as "made by AI in ten minutes".

**Slop is not a specific colour, font, gradient, card or animation. It is a choice made by reflex rather than for this product.** Treat a choice as suspect when several of these are true:

- it could be pasted into an unrelated product unchanged
- it repeats a familiar generated-design pattern (section 2)
- it conflicts with the design system or the sections around it
- it communicates nothing: no information, state, action, hierarchy or brand meaning
- it competes with the content, weakens trust or makes the interface harder to use

Judge the visible result, never whether AI made it. A gradient that carries the brand is fine; a gradient that's there because heroes usually have one is not. Don't swap one reflex for another either: replacing Inter with a trendy serif, or purple with cream, is still a default.

Read this for every new screen or page, and run the final check before handing anything over. For a narrow edit (one component, one fix), don't turn the task into a site audit: fix what was asked without introducing new slop.

## Contents
1. Set a direction before building (three directions first)
2. The tells, grouped by root cause
3. What craft looks like instead
4. Iterating
5. The removal test
6. Auditing an existing design
7. Final check

---

## 1. Set a direction before building

Most slop comes from building without a point of view. Before writing markup, read what exists (design system, tokens, components, brand assets, references), then settle these in a few lines, stating assumptions where the brief is silent:

- **Mode:** Creative, Corporate, Landing page, E-commerce or App (`design-modes.md`), per page or section if the site mixes them.
- **Who and what for:** the audience, the one job of this page or screen, and its primary action.
- **Visual thesis:** one sentence on the idea the design expresses, drawn from the client's brand, product, industry and audience, not "modern SaaS". A garden centre, a law firm and a fintech app should not share a hero. Type, colour, imagery and motion all serve this one idea.
- **One focal point per viewport** and one signature element the design is remembered by. One strong authored moment beats five unrelated effects.
- **Compact system**, if none exists: type roles, spacing rhythm, palette (one accent; neutrals tinted toward the brand; never Tailwind's default indigo unless it is the brand colour), radii, border and shadow rules, image style, icon family, motion rules. Define it before polishing anything.
- **Content:** what real copy, product shots and data exist. Design around them.
- **References:** taste is carried by examples, not adjectives. Keep supplied references in the project (e.g. a git-ignored `refs/` folder) and name what to take from each: hierarchy, pacing, contrast, image treatment, motion. Translate principles; never copy a reference's identity, layout, assets or copy.

An existing design system or site **belonging to this client or project** overrides all of this; preserve its decisions unless the user asks for a redesign. A design system from another brand or project is not this client's and never applies.

### Three directions before one design

Rules that only remove things converge on the same safe result every time. To get something specific, diverge first. For any new site or page without the client's own design system, write three directions before designing anything:

- **A, expected:** what a good agency would do for this sector.
- **B, client-led:** built from the client's own world: their place, history, trade, materials, people or product. For a Southampton accountant that might be port and shipping heritage, ledger and stamp typography, or the founders themselves; for a garden centre, the plants and the seasons.
- **C, unexpected:** a visual lane nobody in this sector uses that still suits the audience.

Each direction gets: a name, a one-sentence visual thesis, typefaces with the reason they fit this client, a palette in hex, the hero composition in a sentence, one signature device, and the photography or illustration style.

They must be genuinely different. If two share a typeface, palette family or hero layout, rework one. Then ask the user to choose (in Claude Design, show them as three hero artboards). If the user wants a finished design without discussion, build the most client-specific direction (usually B) and say why, not A.

---

## 2. The tells, grouped by root cause

Tells rarely appear alone. Look for clusters; each points to one root cause, which is what to fix. Isolated matches are not findings.

**The restrained house default** (root cause: no direction; the look generated UI falls into when it avoids the obvious tells)
- Warm off-white or pale grey background, one deep green or teal accent, a single neutral grotesque (Inter, Public Sans, Geist and similar), hairline borders, 8px radii everywhere.
- The standard skeleton: white header with CTA top right; hero with text on the left and a card or screenshot on the right; three-up cards; a numbered three-step process; image-and-text split; full-width dark CTA band; footer.
- Tidy, credible and interchangeable: it would suit an accountant, a SaaS tool and a charity equally. It is a starting point to move away from, not a finish.

**Generic AI SaaS** (root cause: no direction)
- Tracked uppercase eyebrow above every heading; a hero pill repeating the headline ("New: ...").
- Oversized sentence-length headline, gradient text on one word or on metrics.
- Purple/indigo gradients, cyan-on-dark "futuristic" accents, glowing orbs and radial lights with no source.
- Centred hero formula: pill, headline, grey subheading, primary + ghost buttons, "Trusted by" logo row.
- Default section sequence regardless of the buying journey: hero, logos, stats, bento features, testimonials, pricing, FAQ, "Ready to get started?" band.

**Card overload** (root cause: containers instead of spacing and hierarchy)
- Every block in a rounded card; cards nested in cards; bento grid for content of equal importance.
- Repeated icon-in-rounded-square + heading + two lines, until nothing stands out.
- A border and a diffuse shadow defining the same edge; thick accent stripe on one side of a rounded card; drifting radii.
- Pills for content that isn't a status, tag, filter or action.

**Motion theatre** (root cause: motion with no concept behind it; not the same as motion-led design)
- Every section fades up on scroll; content hidden until JavaScript runs.
- Marquees, pulsing "live" dots on static data, fake blinking cursors, scale-on-hover on every card.
- Smooth scroll or parallax added by habit rather than as part of the concept, or implemented so it hurts reading.

**Fake sophistication** (root cause: styling pretending to be substance)
- Tiny monospaced labels and 01/02/03 numbering on ordinary content.
- Decorative grid lines, dot grids, noise and grain with no technical or canvas purpose.
- Browser frames, code windows and dashboards that show no real product behaviour.
- The "tasteful" default: cream background, italic serif headline, muted everything, chosen because it signals taste rather than because it fits.

**Fake proof** (root cause: no real evidence; also a legal risk, see SKILL.md Guardrails)
- Invented metrics, round-number stats rows, placeholder testimonials (John Doe, Sarah J. CEO), stock or generated faces presented as customers, logo walls implying clients that aren't.

**Imported section** (root cause: pattern pasted in without adapting)
- A section with its own fonts, radii, accent colours, density or motion that don't match the page around it.

**Polish before truth** (root cause: effects before content and function)
- Beautiful effects over vague copy, weak actions, missing states or broken mobile layouts.
- Copy: unlock, elevate, supercharge, seamless, effortless, transform your workflow, all-in-one, built for the modern X, reimagined; manufactured contrasts ("It's not X. It's Y."); headlines that fit any product.
- Emoji as icons; default icon library used unadapted; hand-drawn SVG mascots or scenery.

---

## 3. What craft looks like instead

- **Real content first.** Real screenshots, photography, copy and data shapes. Unavoidable placeholders are obviously placeholders and listed for the client.
- **Proximity before containers; hierarchy before labels.** Group with spacing first, and let size, weight and position show importance before reaching for cards, pills or eyebrows.
- **Layout follows content.** One big idea gets a big, simple layout; dense comparison gets a table; dashboards get dashboard density, not marketing-page spacing. Vary width, alignment and rhythm; asymmetry is allowed.
- **Mobile is re-prioritised, not just stacked.** Decide what comes first on a phone rather than collapsing the desktop columns in order.
- **Coherence over quantity.** Every effect serves the visual thesis. Effects doing the same job twice, or telling different stories, go. A motion-led or immersive concept can carry a lot of motion and depth when it's one coherent idea; five unrelated effects on a plain brochure site cannot. Motion follows `visual-craft.md` section 10.
- **No model-drawn illustration.** Don't draw scenery, mascots or illustrations in SVG, CSS or canvas; they read as placeholders. Use real photography, licensed or commissioned illustration, or leave it out. Icons, simple brand marks and data graphics are fine.
- **Typographic detail:** tabular figures for numbers (`font-variant-numeric: tabular-nums`), real quotes and apostrophes, `text-wrap: balance` on headings, no buttons wrapping to two lines.
- **All the states:** hover, focus-visible, active, selected, disabled, loading, empty, error, success. Generated UI usually ships only the happy path.
- **Specific copy:** concrete nouns, numbers and the customer's words. "Book a boiler service in Southampton this week" beats "Seamless home solutions". Use the `humanize-text` skill for copy.
- **Edges hold up:** 360px to 1440px+, long names, translations, large text settings.

---

## 4. Iterating

- First pass: layout, hierarchy and real copy. Effects, motion and micro-detail come after.
- Change one or two things per iteration and say which.
- When direction is uncertain, show two or three genuinely different variants (different layout or type, not different shades) rather than rerolling one idea.
- Name problems precisely. "Remove the tracked eyebrow; the heading already carries the hierarchy" or "Flatten the nested cards; group with spacing" gets a surgical fix. "Make it better" gets a random restyle.

---

## 5. The removal test

For every suspect element:

1. Name it precisely (eyebrow, nested card, radial light, icon tile, marquee, fake proof).
2. State the job it does: information, state, action, hierarchy or brand meaning.
3. Remove it mentally. If the job survives and clarity improves, delete it.
4. If removing it loses something real, make the smallest correction using the existing system.
5. Add a replacement only when the interface genuinely needs one. Never compensate with a new effect.

Default to subtraction.

---

## 6. Auditing an existing design

When reviewing rather than building:

- Preserve its direction and personality. Aim for the smallest set of removals or corrections, not a redesign in your own taste. Don't prescribe a new font, palette or art direction unless asked.
- Every finding cites a specific element, location or line of copy. No findings about a technique in isolation ("uses a gradient"), and no numeric score or guess about AI authorship.
- Classify each finding: **quality defect** (usability, accessibility, content, responsive or runtime problem) or **slop pattern** (reflex default with no role).
- Group repeated instances under their root cause; report the 5-8 highest-impact findings, using the priority levels and format in SKILL.md.
- Mark anything that couldn't be checked (states, breakpoints, interactions) as unknown rather than guessing.
- Don't edit the design during an audit unless asked.

---

## 7. Final check

Before handing over any new screen or page:

1. Go through the clusters in section 2 and the five tests at the top. Remove each match or state why it stays.
2. **Skeleton check:** write the page as a list of section layouts (e.g. split hero with card, three-up cards, numbered steps, image/text split, CTA band). If it matches the standard skeleton, restructure at least two sections so their layout comes from their content, and make sure at least one moment breaks the grid or the expected rhythm.
3. Could this layout go on a competitor's site with only the logo changed? If yes, go back to the visual thesis and the content.
4. For native apps, use the device and size checks in `apple-platforms.md` section 1 instead. Where a browser is available (Claude Code with Playwright, Claude in Chrome), render at 390px and 1440px and review the screenshots, not just the code. Check that text doesn't clip, overlap or overflow; controls are labelled, reachable and focusable; nothing stays invisible if scripts fail; every decorative layer has a job.
5. Confirm the result is more specific to this product, not merely more fashionable.
6. When reporting, list the material removals or corrections and why each helped.
