# Interaction patterns

Rules for how people reach content and act on it: how many steps stand between them and value, where controls sit on a phone, what an empty screen does, and which visual cues speed up scanning. Read `visual-craft.md` alongside for hierarchy and styling.

## Contents
1. Interaction cost
2. Mobile thumb zone
3. Empty states
4. Visual cues for scanning
5. Forms
6. Navigation menus

---

## 1. Interaction cost

**Rule:** Every tap, scroll and moment of thought before the user sees value is a cost. Show real content on first load; don't make people tap to find out what's there.

**Apply:**
- Replace promo banners that stand in for content ("Discover 100+ recipes") with the content itself: the top 4-6 real items and a "See all" link.
- Count taps to the most common task. If it's more than two from the home screen, move it closer.
- Prefer inline editing and inline expansion over navigating to a separate page for small changes.
- Carousels hide everything after the first slide; on content pages use a visible grid or list. Horizontal scroll rows are fine on mobile when the first 1.5 items are visible, signalling there's more.

**Example:** A home screen hero "Explore our courses →" becomes a "Popular this month" row showing four real course cards with title, duration and rating, and a "See all 42 courses" link.

---

## 2. Mobile thumb zone

**Rule:** Primary actions and frequent navigation sit where a thumb reaches easily: the lower half and centre of the screen.

This section is for phones. On iPad and Mac, navigation and actions move to the top (tab bar or sidebar, window toolbar), and Mac windows keep controls away from the bottom edge; see `apple-platforms.md` sections 7-9.

**Apply:**
- Primary CTA in a bottom bar or near the bottom of the content, full width or right-aligned, not in the top corner.
- Bottom tab bar for 3-5 main destinations in app-like interfaces. Content sites can keep a top header, but keep the main action reachable at the bottom.
- Touch targets 48x48px by default, 44x44px absolute minimum, with at least 8px between adjacent targets. The target is the tappable area, not the visual: a 24px icon gets padding to reach 48px.
- Destructive or rarely used actions (delete, sign out) can sit out of easy reach; that's a feature, not a flaw.

**The line:** The bottom of the screen is shared with the browser. iOS Safari and Chrome put their toolbar there and it moves on scroll, so bottom-fixed elements need `env(safe-area-inset-bottom)` and testing on a real device, not just DevTools. People also change grip constantly; the thumb zone is a guide for placing frequent actions, not a strict map.

---

## 3. Empty states

**Rule:** An empty screen is an onboarding moment, not a dead end. Say what goes here, why it's worth it, and give one clear way to start.

**Apply:** Different empty states need different treatment:
- **First use** (nothing created yet): one-line benefit, 1-3 concrete tips or a template to start from, one primary action. "No projects yet. Projects keep client briefs, files and deadlines in one place. [Create project] or [Import from CSV]".
- **No results** (search or filter): repeat the query, suggest the fix, offer to clear filters. "No invoices match 'Acme' in March. [Clear date filter]".
- **Cleared** (inbox zero, all tasks done): brief acknowledgement, no push to create more.
- **Error** (failed to load): say what failed and offer a retry; never show a friendly "nothing here" when it's actually an error.

Illustrations are optional. Use them in consumer products; in admin panels and internal tools a small icon is enough.

**Implementation note:** Filament tables support this natively (`emptyStateHeading`, `emptyStateDescription`, `emptyStateActions`, `emptyStateIcon`); use those rather than custom views.

---

## 4. Visual cues for scanning

**Rule:** Where a picture identifies something faster than a word, use the picture. Recognition beats reading.

**Apply:**
- Lists of people or companies: avatars or logos, falling back to initials on a colour generated from the name (consistent per person, not random per load).
- Types and statuses: small icon or colour chip beside the text label ("● Paid", "● Overdue").
- Content lists: thumbnails where the content is visual (products, recipes, properties, documents with previews).
- Each cue must earn its place by speeding up recognition. Decorative icons on every row add noise.

**The line:** Colour never carries meaning on its own (WCAG 1.4.1). Always pair it with text or an icon, so colour-blind users and greyscale screens still work. Remote avatars and logos in email-style lists can leak tracking data; serve them through your own backend or use initials.

---

## 5. Forms

**Rule:** A form should make it obvious which label belongs to which field, what's expected in each, and, where possible, what the result will look like.

**Apply:**
- **Proximity:** a label sits much closer to its own field than to the field above it. E.g. 8-12px label-to-input, 24-32px between fields. Equal spacing makes labels float between fields.
- **Labels stay visible.** Always a real `<label>` above the field. Placeholders are for format examples ("e.g. SO14 7DU"), never a replacement for the label; they vanish on typing.
- **Field width hints at the expected input.** Postcode, CVC, expiry, house number and quantity get short fields; name, email and address lines get long ones. On mobile most fields go full width anyway, so this matters mainly from tablet up. The GOV.UK Design System's fixed-width input classes are a good reference.
- **Group related short fields on one row** (expiry + CVC, postcode + city) but keep one column overall. Multi-column forms break the reading path.
- **Mirror the output for creation forms.** When the user is creating something with a visible result (a listing, profile, event, product), lay the form out like the finished item: image drop zone at the top, title and price side by side, description below. Better still, show a live preview beside the form on desktop. Tab order must still follow the visual order, and every field still has a real label.
- **Input font size 16px minimum** on mobile; below that iOS Safari zooms the page on focus.
- UK wording: "Postcode", not "Zip code"; "County" optional or omitted.

**Implementation notes:**
- Card fields: don't build them. Use the payment provider's hosted fields (Stripe Payment Element, WooCommerce payment gateway fields) for PCI scope; style what they allow.
- Filament: use `Grid`, `Section` and `columnSpan()` to size and group fields rather than one long single-width column.

---

## 6. Navigation menus

**Rule:** Menus with more than a handful of items are grouped, labelled and scannable; small menus stay simple.

This section covers website navigation. Menus inside an app (action menus, context menus, a native menu bar) follow `app-patterns.md` section 3.

**Apply:**
- Up to about six items: a plain dropdown or no dropdown at all. Mega menus are for genuinely large sections.
- Group items under short headings ("Products", "Use cases", "Resources").
- Each item: icon, title, and a one-line description when the title alone is ambiguous. One icon style throughout (see `visual-craft.md` Icons).
- Images only for a few highlighted items, such as latest posts or a featured product, not beside every link.
- A "New" tag at most on one or two items, and removed after a few weeks.

**The line:** Menus open on click or tap and Enter/Space, close on Escape and on clicking outside, and never rely on hover alone. Hover-only menus fail on touch screens and for keyboard users. The top-level item that opens a menu must not also be a link, or one of the two actions becomes unreachable on touch.

