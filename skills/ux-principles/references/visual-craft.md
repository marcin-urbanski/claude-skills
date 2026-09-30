# Visual craft

Rules for making any interface feel calm, consistent and trustworthy. Small inconsistencies (a misaligned edge, a third font, a mismatched icon) rarely get noticed individually but add up to "this looks cheap". The Guardrails in SKILL.md still apply.

## Contents
1. Hierarchy
2. Design for the system, not the screenshot
3. Spacing and alignment
4. Colour
5. Typography
6. Labels and badges
7. Icons
8. Dividers and white space
9. Depth and shadows
10. Motion

---

## 1. Hierarchy

**Rule:** Decide what matters before deciding how it looks. The 1-3 things the user came for must be the first things a scanning eye lands on.

**Apply:**
- Before laying out, list every element on the screen (values, labels, actions, status, help text) and rank it by importance to the user's goal on this screen.
- Style follows the ranking: the top items get size, weight and contrast; labels, metadata and secondary actions recede (smaller, lighter weight, muted colour).
- In label + value pairs, the value leads and the label recedes. "Revenue" in small grey text above "£12,480" in large bold, never both at the same size and weight.
- Use more than size: weight, colour, position and an icon can each lift or lower an element. Emphasising by making something bigger is usually the least elegant option.
- Where an icon or unit makes a value self-explanatory, drop the label: "5 bed · 3 bath · 1,634 sq ft" with small icons beats a five-row "Bedrooms: 5" table. Keep the short unit text next to the icon; an icon alone is ambiguous and invisible to screen readers.
- One primary action per view. Secondary actions are outline or text buttons; destructive actions are never styled as the primary.

**Example:** A dashboard tile reading "Active users: 1,204 | Change: +8% | Period: Last 30 days" in one style becomes: "1,204" large and bold, "Active users" small and muted above it, "+8%" in green with an up arrow beside the number, "Last 30 days" as a caption.

---

## 2. Design for the system, not the screenshot

**Rule:** Every component must work across all the content it will realistically hold, not just the example in the mockup.

**Apply:**
- Test mentally (or in code, with real data) against extremes: very bright and very dark images, busy photos, long titles, missing images, 0 and 999+ counts, long translated strings.
- Never put text or icons directly on raw imagery. Use a container: solid or translucent background, scrim gradient, or backdrop blur.
- Icons and controls over images need at least 3:1 contrast against whatever sits behind them (WCAG 1.4.11); text needs 4.5:1.

**Example:** A white outline heart icon top-right of product photos disappears on a pale packshot. Fix: 32px white circle at 90% opacity with a subtle shadow, dark icon inside. It now reads on any image.

---

## 3. Spacing and alignment

**Rule:** Use one spacing scale and one content margin, and make everything snap to them.

**Apply:**
- Base unit of 4px or 8px; spacing values come only from the scale (4, 8, 12, 16, 24, 32, 48, 64). In code these are tokens or Tailwind's default scale, never ad hoc pixel values.
- One horizontal content margin per breakpoint (e.g. 16px or 24px on mobile). Every left edge aligns to it unless something is deliberately full-bleed.
- Related items sit closer than unrelated ones. Spacing inside a group is always smaller than spacing between groups.
- Same kind of section, same spacing. If two cards have different internal padding, one of them is wrong.

**When reviewing:** infer the scale the design seems to intend, then list the elements that break it.

---

## 4. Colour

**Rule:** Colour creates hierarchy. If everything is saturated, nothing stands out.

**Apply:**
- Build the palette around the product's context (natural tones for fresh food, restrained neutrals for premium, brighter for playful) rather than the loudest brand colour everywhere.
- Reserve the most saturated colour for the primary action and genuine states (error, success, sale). One primary colour per screen.
- Decide per element whether it should lead or recede, and colour it accordingly.

**The line:** "Calmer" never means below contrast minimums. Body text 4.5:1, large text 3:1.

---

## 5. Typography

**Rule:** One font family, a small set of styles, hierarchy from size and weight.

**Apply:**
- Default to a single family. A second family only for a clear purpose (display headings, code), never more than two.
- Define a fixed set of styles, e.g. Display, H1, H2, H3, Body, Small, Caption, and use nothing outside it.
- Headings: bold and clear, not oversized relative to the content. If a heading dominates the product it describes, it's too big. Line-height tight, around 1.1-1.25.
- Body: line-height 1.5-1.6. Heading line-height is always tighter than body; the reverse makes the page feel disjointed.
- Size: 16px minimum for body copy people actually read (articles, descriptions, forms). 14px is fine for dense UI (cards, tables, dashboards, metadata), 12px only for captions and labels.
- Line length 45-75 characters; in CSS, `max-width: 65ch` on text containers.
- Colour: body a step softer than headings. Dark grey instead of pure black is a stylistic choice, not a readability rule, and it must still pass 4.5:1.
- Weight difference between heading and body must be obvious (e.g. Bold vs Regular). Medium vs Regular reads as the same.
- Alignment: centre only for headings and text up to about three lines. Anything longer is left-aligned; centred paragraphs lose the consistent line start that makes reading fast.

**When reviewing:** list every distinct text style in use, then map each to the minimal set and flag the leftovers.

---

## 6. Labels and badges

**Rule:** Small labels must be readable at a glance and must not compete with the product.

**Apply:**
- Shortest wording that still works: "20% off", not "20% off discount" with an icon.
- Small uppercase text gets slight letter-spacing (roughly 0.04-0.08em) and no smaller than 11-12px.
- One badge per card where possible; if several apply, pick the one that matters most to the decision.
- Badges sit on the image corner or next to the price, not across the product itself.

---

## 7. Icons

**Rule:** Icons are a system; one style throughout.

**Apply:**
- One library or one drawn style: same stroke width, same fill approach (outline or filled, not mixed), same corner treatment, same optical size.
- Icons in the same row share one colour unless colour carries meaning (e.g. green tick vs red cross).
- Feature/benefit rows are tight, aligned units, visually below the main product information.
- Icons next to text are vertically centred on the text's cap height, not its box.

---

## 8. Dividers and white space

**Rule:** Structure should be felt, not seen.

**Apply:**
- Prefer spacing or a subtle background change to lines. When a divider is needed, 1px in a light neutral, never full-contrast.
- No huge gaps that detach a section from what it belongs to. Large gaps signal "new topic"; use them only there.
- If a page looks like stacked boxes, remove dividers first, then rebalance spacing, before adding anything.

---

## 9. Depth and shadows

**Rule:** Depth should be felt, not noticed. Soft, diffused shadows; one light direction; few elevation levels.

**Apply:**
- Default shadow: small vertical offset, large blur, low opacity. E.g. `0 4px 16px` at 6-10% opacity for cards; larger offset and blur for modals and popovers only.
- Define 2-3 elevation levels (resting card, raised/hover, overlay) as tokens and use nothing else.
- On a coloured background, tint the shadow toward that colour (a darker, transparent version of it) rather than neutral grey or black, which looks dirty on colour.
- Don't stack a strong border and a shadow on the same element; pick one.
- Dark mode: shadows barely read. Show elevation with lighter surface colours instead.

---

## 10. Motion

**Rule:** Motion has a job: it explains a state change, shows cause and effect or spatial movement, carries the narrative, or *is* the brand experience. Motion without a job (fade-up on everything because that's what pages do) is the problem, not motion itself.

How much motion a design carries is set by its design mode (`design-modes.md`): Creative mode is motion-led; Corporate is subtle; Landing page, E-commerce and App are functional. The two subsections below cover interface motion (all modes) and motion-led design (Creative, and brand moments in other modes).

### Interface motion (every project)

**Apply:**
- UI feedback (hover, press, toggle, open/close): 150-250ms, ease-out, CSS transitions only. No bounce or elastic easing on ordinary state changes.
- Define motion as tokens (2-3 durations, 1-2 easings) like spacing and colour.
- Animate `transform` and `opacity` only. Animating width, height, margin or padding causes layout jank.
- Hover must not move the target away from the pointer or shift nearby layout.
- Scroll reveals in a non-motion-led design: reserve them for key moments rather than every section. Content must be visible by default and enhanced by script, so nothing stays invisible if JavaScript fails.
- Every page has a complete static first frame; the hero's message and CTA are readable and usable before any intro animation finishes.
- `prefers-reduced-motion: reduce` shows the final state immediately; don't just shorten the animation.

### Motion-led and immersive design

When motion, 3D or scroll storytelling is the concept (the client wants the experience of a reference site, or the visual thesis depends on it), design it fully: choreographed intros, pinned and scrubbed sequences, word-by-word reveals, WebGL scenes, smooth scroll. The rules shift from "how much" to "how well":

- **Choreography, not scatter.** One motion narrative for the page: consistent easing and timing tokens, sections sequenced deliberately, the same kind of element always moving the same way.
- **Readable before the show finishes.** Navigation, primary message and CTA are usable before intro sequences complete; pinned sections don't trap the user longer than the content justifies.
- **WebGL with one job.** A canvas has a clear responsibility and sits beneath semantic content and controls. Cap device pixel ratio, pause rendering when offscreen or the tab is hidden, dispose resources on teardown, handle context loss, and provide a static poster image when WebGL is unavailable.
- **One scroll engine.** If smooth scrolling is part of the experience, use one library (Lenis or Locomotive, never both), wire it to ScrollTrigger properly, and check keyboard scrolling, anchor links and scroll restoration.
- **Reduced motion is a designed state,** not an afterthought: static compositions with the final frames, posters in place of canvases, native scrolling. Design this version too; it's what some users see.
- **Performance is part of the design.** Note the budget: lazy-load below-the-fold media, bound blur and filter effects, keep large effects off low-power devices where needed.

**Stack is not a design constraint.** GSAP (free, including its plugins) and Three.js run in any stack, WordPress included, via enqueued scripts in the theme or a block. A client wanting a GSAP or Three.js site doesn't require moving to Next.js. For restrained, non-motion-led sites, CSS transitions plus a small IntersectionObserver are usually enough, and that's a build choice rather than a design limit.

**Split text:** when headings animate word by word, keep the full heading as the accessible name, hide the split fragments from screen readers, and never split links or inline markup.

