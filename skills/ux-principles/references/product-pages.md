# Product pages

Rules for e-commerce product pages and catalogue grids (WooCommerce, Shopify, custom). A buyer is answering four questions in order: what is it, can I trust it, what will it cost me, what could go wrong. The page should answer the first three in one glance, handle the fourth at the button, and make acting easy from anywhere. Read `visual-craft.md` for layout, type and colour, and `persuasion-psychology.md` for option selectors and defaults.

## Contents
1. Product imagery
2. Identity, trust and price as one cluster
3. Social proof
4. Option selectors
5. One-time, subscription and bundles
6. The purchase cluster
7. Trust badges
8. Scroll behaviour on mobile
9. Presets for common choices

---

## 1. Product imagery

**Rule:** Images must close the imagination gap on the product page *and* stay consistent in the catalogue grid. These are different jobs, so they use different shots.

**Apply:**
- **Grid thumbnail:** clean packshot, consistent background, lighting, angle and crop across the catalogue. A grid of mixed styles looks like a marketplace, not a brand.
- **Product page hero:** for sensory products (food, drink, cosmetics, homeware, clothing) lead with the product *in use or with its outcome*: the tub next to the prepared drink, the cream on skin, the lamp lit in a room. The packshot comes second. For technical products (tools, electronics) a clear packshot can lead. For digital and content products (ebooks, courses, templates, software) show the inside: real pages, screens or lessons, not just the cover.
- The product stays the focal point. Hands, people and props show scale or use; they don't take over.
- Show what is actually sold. Sold by weight: don't show a single piece. Pack of 6: show 6. If the hero shows serving suggestions not included, say so in the alt text or caption.
- Honesty matches context: fresh, organic and handmade products need real-looking photography, not heavy styling.

- When the hero image is a conversion question, offer three variants to test: product alone, product with 2-3 value points, product with a preview of real content. Revealing real content usually wins on trust, but treat it as a hypothesis (see Measuring changes in SKILL.md).

**When reviewing:** flag images that would break the grid, and propose a shot list (grid packshot spec + 3-5 gallery shots with purpose for each) the client can hand to a photographer.

---

## 2. Identity, trust and price as one cluster

**Rule:** Status badge, title, rating and price sit together at the top of the details.

**Apply:**
- Optional single status badge directly above the title: "Best-seller", "Top rated", "New". It frames everything below it, so it must be backed by a rule in the data (e.g. top 10 by units in the last 30 days), not picked by hand. One badge only.
- Rating (stars + count, e.g. "4.7 · 312 reviews") directly under or beside the title, linking to the reviews section.
- Price immediately after. Drop redundant labels like "Price:" when the currency symbol makes it obvious.
- The title names the product; variable parameters (weight, size, quantity) belong in the selector. "Organic Hass Avocados", not "Organic Hass Avocados 1kg" when weight is selectable.
- Show the unit price where it helps comparison ("£4.50 / kg"). For many grocery-type products in the UK it's a legal requirement anyway.

---

## 3. Social proof

**Rule:** Show real, exact numbers near the decision. Specific reads as true; rounded reads as estimated.

**Apply:**
- Display the actual count and rating: "4.8 · 221 reviews", not "200+ reviews" or "5-star rated".
- Recent-demand lines ("140 sold this week") only when calculated from real orders over the stated period. Show them only above a sensible threshold; "3 sold this week" hurts more than it helps, so hide it below the threshold rather than inflating it.
- In mockups and prototypes, use obviously placeholder values and mark them as such. Never choose "believable-looking" numbers for production.

**Implementation note:** on WooCommerce, recent sales counts mean an orders query per product. Calculate on a schedule (Action Scheduler or cron) and store as product meta or a transient, never on page load.

**The line:** Fake or selectively curated reviews and invented sales figures are banned outright under the DMCC Act 2024. Not a grey area.

---

## 4. Option selectors

**Rule:** Small option sets are visible chips or swatches, not dropdowns. See `persuasion-psychology.md` section 7 for the general rule.

**Apply on product pages:**
- Flavours and colours: swatches (colour dot or small thumbnail) with the name visible or on selection. Sizes: chips.
- Show out-of-stock options crossed out but selectable-for-notification, not hidden, so the range is clear.
- Answer the main hesitation per option with one short line under the selector that updates with the selection ("Rich and creamy, not too sweet"; "Runs small, size up"). Hover tooltips don't exist on mobile, so don't rely on them.

---

## 5. One-time, subscription and bundles

**Rule:** Present purchase types as comparable cards, emphasise the better-value option honestly, and let the user choose.

**Apply:**
- Two side-by-side cards instead of radio buttons: "One-time · £24" and "Subscribe · £20.40 every 4 weeks (save 15%)".
- Emphasise the subscription card visually (border, "Save 15%" tag). A "Most popular" tag only if it's true from order data.
- Put the key terms inside the card, in plain view: price per delivery, frequency, "Skip or cancel anytime in your account". If there's a minimum term, it goes here, not in the small print.
- **Pre-select one-time, not subscription.** This deliberately departs from the video: pre-selecting a recurring payment is the classic subscription trap, and it conflicts with the defaults guardrail in SKILL.md. The visual emphasis does the persuading; the default stays with the lower-commitment choice.
- When one-time is selected, reveal bundle tiers with progressive disclosure: "1 tub · £24", "2 tubs · £43.20 (save 10%)", "3 tubs · £57.60 (save 20%)". Single tub stays selected by default.
- Discounts are calculated from the real everyday price, not an inflated reference price.

---

## 6. The purchase cluster

**Rule:** Selection, total and button form one tight unit. The user picks, sees the cost, acts.

**Apply:**
- Selectors sit directly above the button, not elsewhere on the page.
- Button label stays functional, with the live total: "Add to basket · £43.20". It must update instantly with any change; a stale total is worse than none.
- Outcome framing goes in the line *above* the button, not inside it ("Makes 30 creamy shakes"). Outcome phrases inside buttons lengthen them, blur what the button does, and for food and supplements often turn into health claims (see Trust badges).
- Primary but not shouting: on premium brands drop all caps and oversized buttons; sentence case, solid primary colour and generous padding is enough.
- Delivery cost or threshold near the cluster if it affects the decision ("Free delivery over £40").

**Implementation note:** on WooCommerce variable products the live total needs JS listening to the variation form events; keep it to a small script rather than a plugin.

---

## 7. Trust badges

**Rule:** Badges answer the buyer's specific fears for this product, directly under the button. Generic claims everyone makes add nothing.

**Apply:**
- Name the top 2-3 real risks first (Is it safe? Will it work? Can I return it? What's in it?), then write one badge per risk: icon + 2-4 words. "Third-party tested", "60-day money-back guarantee", "No added sugar".
- Drop table-stakes claims ("Secure checkout", "Free UK delivery" if every competitor offers it) unless they genuinely differ.

**The line:**
- Every claim needs evidence the client can produce on request: the test certificate, the written guarantee policy, the ingredient spec. If the client can't produce it, the badge doesn't ship.
- Don't present legal rights as a selling point. "14-day returns" on an online order is the statutory minimum in the UK; advertising it as a feature is itself a banned practice. A guarantee must go beyond what the law already gives.
- Certification marks (Vegan Society, Soil Association, B Corp) are trademarks and need a licence; use them only if the product is actually certified.
- Food and supplements: "boosts energy", "supports immunity" and similar are health claims and must match the authorised wording on the GB nutrition and health claims register. Flag these for the client rather than writing them.

---

## 8. Scroll behaviour on mobile

**Rule:** Context and the ability to act should stay available through the whole scroll.

**Apply:**
- Once the main image scrolls out, show the product name (and optionally price) in the top bar.
- Sticky bottom bar with the purchase cluster (current selection + button with total), appearing once the inline button leaves the viewport rather than duplicating it on screen.
- A details card that slides up over the image separates media from content without losing either.

**The line:** Sticky elements cost screen space. Maximum one sticky bar top and one bottom; account for the iOS safe area (`env(safe-area-inset-bottom)`); add bottom padding so the bar never covers the last content; check it doesn't stack on top of cookie banners or chat widgets.

---

## 9. Presets for common choices

**Rule:** The most common choices are one tap; a flexible control covers everything else.

**Apply:**
- 2-4 preset chips for common values (500g · 1kg · 2kg) plus a stepper or custom input.
- Base presets on real order data. If none is available, state the assumption ("presets assume most orders are 500g-1kg") so the client can confirm it.
- Pre-select the most common preset (Smart defaults, `persuasion-psychology.md`).

**Example:** A loose-weight product with only a +/- stepper in 100g steps takes 10 taps to reach 1kg. Presets 500g / 1kg / 2kg with 1kg selected, stepper below for adjustments, gets most buyers there in zero or one tap.
