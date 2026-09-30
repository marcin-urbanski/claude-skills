# Design modes

Every project starts by choosing a mode. The mode decides what leads the design, how much motion and layout freedom it has, how content and imagery are balanced, and how hard it pushes toward conversion. Rules elsewhere in this skill are defaults *within* a mode; the Guardrails in SKILL.md apply to every mode.

If the user names a mode, use it. Otherwise pick from the signals below and state the choice in one line in the direction step. A site can mix modes by page or section (a corporate site with a creative homepage hero, a creative site with a plain contact page); say which applies where.

## Contents
1. Creative
2. Corporate
3. Landing page
4. E-commerce
5. App and dashboard
6. Quick comparison

---

## 1. Creative

**Purpose:** make people feel something and remember the brand. The experience is the product.

**Signals:** agency, studio, portfolio, launch or campaign microsite, luxury, fashion, architecture, events, culture; the client points at an Awwwards-style reference or asks for "wow".

**What leads:** the visual thesis and the story. Layout, type, imagery and motion all tell it together.

- **Layout:** free. Asymmetry, overlap, full-bleed media, broken grids, oversized type, horizontal sections, unusual navigation, all allowed when they serve the concept.
- **Motion:** is the concept. GSAP timelines, ScrollTrigger pinning and scrubbing, word-by-word reveals, page transitions, WebGL and Three.js scenes, smooth scroll. Choreographed as one narrative (`visual-craft.md` section 10, motion-led).
- **Content and imagery:** image and media-led. Short, confident copy; text supports the visuals rather than explaining everything.
- **Conversion:** understated but always reachable. The enquiry or contact route is visible from every screen even when the storytelling is long.
- **Relax:** the restraint defaults, the one-accent palette if the concept needs more, standard section patterns.
- **Keep:** readable before the show finishes, designed reduced-motion state, static fallbacks, performance budget, keyboard access.
- **Typical failure:** effects without a story (motion theatre), or a template with animations added on top. Creative means authored, not decorated.

---

## 2. Corporate

**Purpose:** build trust and credibility, explain what the organisation does, and turn interested visitors into enquiries.

**Signals:** service businesses, B2B, professional services, manufacturing, charities, education, local businesses, most multi-page agency client sites.

**What leads:** clarity and credibility, then conversion.

- **Layout:** structured information, distinctive expression. Navigation and content stay predictable and easy to find; typography, colour, photography, composition and one signature device carry the personality. Corporate is not a licence for the house default skeleton.
- **Motion:** subtle. Hover and focus states, a few purposeful reveals on key moments, gentle image transitions. Roughly 200-400ms, no scroll hijacking, no pinned sequences, nothing that delays reading.
- **Content and imagery:** balanced. Every section has a visual anchor (real photography of people, work, premises, product); no more than a screen or so of text without an image, diagram or data. Real team and project photos over stock whenever the client can supply them.
- **Conversion:** primary action (call, book, enquire, quote) in the header on every page; contextual CTAs at the end of service sections and case studies, not after every block. Trust signals (accreditations, case studies, reviews, named clients with permission) close to the claims they support.
- **Load:** `visual-craft.md`, `interaction-patterns.md`, `anti-slop.md`; `persuasion-psychology.md` for forms and enquiry flows.
- **Typical failure:** the restrained house default (off-white, one green accent, neutral sans, split hero with card, three-up cards, three steps, dark CTA band), the generic SaaS formula applied to a plumber or a law firm, or dense walls of text with a stock photo on top.

---

## 3. Landing page

**Purpose:** one offer, one audience, one action. Everything on the page earns its place by moving the visitor toward that action.

**Signals:** paid ad and email campaigns, lead magnets, product or service launches, event sign-ups, single-offer pages.

**What leads:** the conversion path.

- **Layout:** a single column of argument, ordered by the visitor's objections (`marketing-pages.md`). Usually no main navigation, or a minimal one, so there's nowhere to leak to.
- **Motion:** minimal and functional. Only what draws attention to the product, demonstrates it (a short product clip), or gives feedback. Nothing delays the headline or CTA.
- **Content and imagery:** a visual in every section, and the real product or service shown in the hero. Copy is tight and specific; proof sits next to each claim.
- **CTA placement:** primary CTA above the fold; repeated after the key proof and argument points (typically after the strongest benefit, after social proof, and at the end); a sticky CTA bar on mobile for long pages. One action throughout, same wording each time.
- **Load:** `marketing-pages.md`, `persuasion-psychology.md`, `anti-slop.md`, `visual-craft.md`.
- **Typical failure:** the stock hero/benefits/testimonials/FAQ template regardless of the offer, several competing CTAs, or proof collected at the bottom.

---

## 4. E-commerce

**Purpose:** help people find the right product and buy it with confidence.

**Signals:** WooCommerce, Shopify, catalogues, product and category pages, basket and checkout.

**What leads:** the product and the path to purchase.

- **Layout:** grid-led and consistent so products compare easily; product pages cluster identity, trust, price and purchase (`product-pages.md`).
- **Motion:** functional: add-to-basket feedback, gallery transitions, filter updates. Brand storytelling moments (homepage, collection launches) can borrow from Creative mode.
- **Content and imagery:** photography leads; consistent packshots in grids, in-use shots on product pages; copy answers buying questions.
- **Conversion:** purchase cluster always reachable (sticky on mobile), clear delivery and returns information at the decision point.
- **Load:** `product-pages.md`, `persuasion-psychology.md`, `visual-craft.md`, `interaction-patterns.md`.
- **Typical failure:** inconsistent product imagery, hidden costs, badges and trust claims that aren't true.

---

## 5. App and dashboard

**Purpose:** help people get tasks done quickly and repeatedly.

**Signals:** SaaS products, admin panels (Filament), client portals, internal tools, mobile apps.

**What leads:** the user's task and information density.

- **Layout:** efficient, dense where the data is dense, consistent components, predictable navigation. No marketing-page spacing.
- **Motion:** fast and functional only (150-200ms): state changes, panels, feedback. Nothing decorative.
- **Content and imagery:** data and real content; icons and avatars for scanning; illustrations only in empty states of consumer products.
- **Conversion:** only at upgrade, onboarding and retention moments (`persuasion-psychology.md`), never interrupting the work.
- **Load:** `visual-craft.md`, `interaction-patterns.md`, `app-patterns.md`, `persuasion-psychology.md`. Native iPhone, iPad and Mac apps also load `apple-platforms.md` and `apple-patterns.md`, and follow the platform's components, sizes and navigation structure.
- **Typical failure:** cards everywhere, hero-sized headings in a tool, happy-path-only states; in native apps, web patterns and custom chrome where the platform already has a convention.

---

## 6. Quick comparison

| | Creative | Corporate | Landing page | E-commerce | App |
|---|---|---|---|---|---|
| Leads with | Story and experience | Clarity and trust | The one action | Product | The task |
| Layout freedom | High | Medium | Low | Low-medium | Low |
| Motion | Concept-level | Subtle | Minimal, purposeful | Functional | Functional, fast |
| Imagery | Media-led | Balanced, real | Product in every section | Photography-led | Data and icons |
| CTA | Understated, always reachable | Header + end of sections | Above fold, repeated, sticky on mobile | Purchase cluster | At key moments only |
