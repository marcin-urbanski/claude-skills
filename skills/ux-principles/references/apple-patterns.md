# Apple platforms: components and flows

Native component choices and app flows for iPhone, iPad and Mac: alerts, sheets, lists and controls, launch and onboarding, permissions, settings, accounts, In-App Purchase, ratings, notifications, widgets and documents. Based on Apple's Human Interface Guidelines. Read `app-patterns.md` first for the cross-platform rules these specialise, and `apple-platforms.md` for foundations. Items marked **(App Review)** are requirements Apple enforces, not just advice.

## Contents
1. Alerts and action sheets
2. Sheets, popovers and full-screen views
3. Lists and controls
4. Text input
5. Launch and onboarding
6. Permissions and privacy
7. Settings
8. Accounts and sign-in
9. Paywalls, subscriptions and In-App Purchase
10. Ratings and reviews
11. Notifications
12. Widgets, Live Activities and shortcuts
13. Documents, files and sharing

---

## 1. Alerts and action sheets

The cross-platform rules (when to alert, title, button naming and order, Cancel, default and destructive roles) are in `app-patterns.md` section 1. Native specifics:

- **Alert or action sheet (`confirmationDialog`)?** Alerts are for unexpected problems. Choices that follow an action the person just started (discard or save a draft, delete this photo, which account to post from) go in an action sheet.
- **Action sheets:**
  - Destructive options use the destructive role (red) and come first; Cancel is last (`confirmationDialog` adds it).
  - Keep the title to one line.
  - Neither alerts nor action sheets should scroll at large text sizes.
- **Alert fields:** a text field in an alert only when the input resolves the situation (a password to continue).
- **Mac alerts:**
  - Show the app icon automatically. Use the caution symbol only for unexpected data loss, never for routine confirmations like emptying the Trash.
  - For an alert that repeats, add a "Don't show again" checkbox.
  - Command-Period and Esc cancel.
- **Mac help button:**
  - At most one per window, in the bottom corner of the dialog opposite OK/Cancel.
  - Never in the toolbar; it opens the help topic for the current context.
- **Button labels:** default to title case for buttons, menu items and alert buttons ("Add to Cart", "Delete Photo"), as Apple's apps do. Alert messages and body text use sentence case. (The HIG alerts page itself suggests sentence case for alert buttons; if you follow it, do so in every alert.)
- **Undo after deleting on iPhone:** there's no system undo toast, and shake to undo is hard to discover. Prefer a restorable "Recently Deleted" area, or a brief in-app banner with Undo. Confirm with an action sheet only when the deletion can't be reversed.

---

## 2. Sheets, popovers and full-screen views

- **Choose by task:**
  - Sheet for a short task scoped to the current context.
  - Full-screen modal for media, camera, markup or multi-step editing.
  - On iPad and Mac, a separate window when people will work in it alongside the main window.
- **iPhone sheets:**
  - Cancel on the leading edge of the sheet's toolbar and Done (or Save, Add) on the trailing edge.
  - Never show Cancel, Done and Back at once, and Back never dismisses the sheet.
  - Support swipe-down to dismiss; with unsaved changes, confirm with an action sheet (Discard Changes / Keep Editing) instead of discarding.
  - Detents: a medium (about half height) detent suits progressive tasks like sharing; leave it out when the content needs the full height (compose).
  - A resizable sheet has a grabber.
- **iPad sheets:** page or form sheet, centred over a dimmed background.
- **Non-modal tools** that change the view while people keep working (formatting, find and replace): a non-modal sheet on iPhone, a panel on Mac.
- **Mac sheets:**
  - Attached to their window and block only that window; the rest of the app stays usable.
  - Give them a sensible default size, resizable when useful.
  - Buttons sit in the content area, ordered as in alerts (default on the trailing side).
- **Popovers:**
  - iPad and Mac only: in compact width (iPhone), the same content becomes a sheet.
  - One at a time; only an alert may appear over one.
  - On Mac, a popover can be dragged off to become a detached panel.
- **One modal at a time,** as in `app-patterns.md` section 2.

---

## 3. Lists and controls

- **Grouped lists (inset grouped style)** for settings and forms, with section headers and footers; plain lists for content. Footers explain the setting above them.
- **Row accessories:**
  - A chevron drills into a detail view.
  - The info button shows details without navigating.
  - A checkmark marks the chosen option.
  - Don't combine an A-Z section index with trailing accessories; they compete for the same edge.
- **Swipe actions** on rows for frequent actions, with a destructive one on the trailing side, styled red. Every swipe action also exists in the context menu or detail view.
- **Editing:** iPhone lists enter an edit mode for multi-select and bulk actions; allow reordering where order matters, even if items can't be added or deleted.
- **Switches:**
  - iOS: a switch belongs in a list row, where the row text is its label; outside lists, use a toggle-style button that changes its background when on.
  - macOS: a checkbox is the default for a single setting; a switch is for an important setting that turns a group on or off. Checkboxes and switches never go in the toolbar.
- **Segmented control vs tab view:**
  - iOS: a segmented control switches closely related views within one screen, with at most about five segments; separate sections use the tab bar.
  - Mac: a tab view switches panes in the window body (up to about six tabs), and segmented controls belong in toolbars and inspectors.
- **Pickers:**
  - Show them in context (inline, at the bottom of the view, or in a popover), never on a separate screen.
  - Short lists go in a menu, medium-length predictable lists in a picker, very long lists in a searchable list.
  - Minute intervals divide 60 evenly.
- **Date pickers:**
  - iOS: the compact style when space is tight (a button showing the value, opening a calendar), inline or wheels otherwise.
  - Mac: textual for precise entry, graphical for browsing a calendar or picking ranges.
- **Pull-down vs pop-up buttons (SwiftUI `Menu` vs `Picker`):** a pull-down lists commands related to the button's purpose; a pop-up lists mutually exclusive options and shows the current one.
- **Mac specifics:**
  - A push button whose action opens another window or asks for more input ends with an ellipsis ("Export…").
  - Square +/- buttons sit directly under the table they act on.
  - Sortable, resizable table columns; outline views for hierarchies; Finder-style column views only for deep hierarchies.
- **Progress:** use the system progress views; on Mac a small spinner can sit inside a field or next to a button, unlabelled.
- **Pull to refresh** (`refreshable`) as an extra, with a title only if it carries information ("Updated 2 min ago").
- **Page dots** only for a short, flat sequence of peer pages (about 10 at most); not available on Mac.

---

## 4. Text input

- Match the keyboard and autofill to the data (`keyboardType`, `textContentType`): email, URL, phone, number pad, decimal pad, one-time code, new password.
- Set the Return key to the action (`submitLabel`: Search, Go, Next, Done).
- Use `SecureField` for passwords, never pre-fill them, and let the system offer passkeys and password autofill.
- Keep the focused field and the controls near it visible above the keyboard.
- A toolbar above the keyboard holds only controls for the current task.
- iOS text fields get a trailing clear button; an optional leading icon can show the field's purpose.
- Validate as people go: email when the field loses focus; password and username rules live as they type; digit-only fields immediately.
- Numeric fields use a formatter (currency, percent, decimals) per locale, never hard-coded formats.
- Mac: choose where clipped text truncates (start, middle, end) and show the full value in a tooltip.

---

## 5. Launch and onboarding

- **Launch screen:**
  - Looks like the app's first screen without content (or a plain background) and matches light or dark appearance.
  - No text (it isn't localised), no logo unless the first screen has one, and no advertising.
  - Never a splash screen held on purpose.
- **Launch fast** and restore where people left off: screen, scroll position, selection, window size and position on Mac. First launch never waits on a download; bundle enough to start.
- **Onboarding:**
  - Prefer small tips at the moment a feature is relevant over an upfront tour. If a flow is essential, keep it short, interactive and skippable.
  - Once skipped, it isn't shown again automatically, but it stays reachable from Help or Settings.
  - Don't teach OS basics, don't collect optional setup, and don't show licence text (the App Store handles agreements).
  - Ship defaults good enough that most people never configure anything.
- **Tips (TipKit):**
  - Only for features doable in three actions or fewer.
  - One or two action-focused sentences, no promotion.
  - Shown only to people who haven't used the feature, and paced (for example one a day).
- **No rating prompts or permission prompts during onboarding** unless the app can't work without that permission.

---

## 6. Permissions and privacy

- **When to ask:** when the person first uses the feature that needs it. At launch only when the app can't function without it (location in a navigation app).
- **Narrowest scope:** approximate location, a limited photo selection, "while using the app". `LocationButton` grants one-time location after a single first-use confirmation, and `PhotosPicker` needs no photo-library permission at all.
- **Purpose strings** (the Info.plist text in the system prompt for camera, microphone, location, photos, contacts and similar; notifications have none, so explain the benefit in the UI before asking):
  - One short, complete sentence in the active voice, sentence case, full stop, saying how the data is used.
  - For example: "Uses your location to show nearby charging points."
  - No vague benefit claims.
- **Pre-permission screen (optional):**
  - A step inside a flow the person started, not a pop-up. It explains the benefit, then has exactly one button, "Continue" or "Next", which opens the system prompt.
  - No Skip, no Close, and never "Allow"; the system prompt is where people say no.
- **App Tracking Transparency (App Review):** no incentives for allowing, no screens that imitate the system prompt, no arrows or images pointing at it.
- **If denied:** the feature explains what's missing and offers a button that opens the app's page in Settings. Never re-prompt in a loop.
- **Data handling:**
  - Process on device where possible.
  - Keep secrets in the Keychain.
  - Use passkeys, Sign in with Apple or Password AutoFill rather than a custom login scheme.
- **Mac:**
  - Apps outside the Mac App Store are signed with a Developer ID; the Mac App Store requires sandboxing.
  - Several users can be signed in at once, so don't assume a single user.

---

## 7. Settings

The cross-platform rules for what belongs where are in `app-patterns.md` section 10.

- **Three tiers:**
  - Options for the current view live in that view (sort, filter, show/hide).
  - General options live in the app's own settings screen.
  - iPhone and iPad only: the most rarely changed can go in the app's page in the system Settings app, with a link from the app that opens it directly.
- **Don't duplicate system settings:** appearance, interface text size, accessibility, Face ID or passcode, scrolling. Follow them. Content settings (an editor's font and size on Mac) are fine.
- **Mac Settings window:**
  - Opened with Command-Comma from the App menu, never from a toolbar button. Document-level options go in the File menu instead.
  - A `Settings` scene with a fixed toolbar of panes (not customisable) that shows the active pane.
  - Minimise and zoom disabled.
  - The window title is the pane name, or "AppName Settings" if there's only one pane.
  - It reopens on the last pane viewed, and changes apply immediately without a Save button.
- **iPad:** Settings in the menu bar opens the app's page in the system Settings app; link an in-app settings screen as a separate item.

---

## 8. Accounts and sign-in

- **Account only when needed:**
  - Let people explore first and sign in to save, sync or buy; say in the sign-in view why an account is needed.
  - Reuse what's already known (Apple Pay name and email) instead of asking again.
- **Sign-in methods:** passkeys, Sign in with Apple or Password AutoFill; if passwords remain, require two-factor authentication.
  - Name the method on the button ("Sign In with Face ID"), and only mention methods this device supports.
  - Don't add an in-app toggle for Face ID; it's a system setting.
- **Sign in with Apple:**
  - The button is at least as prominent as other sign-in options, visible without scrolling, and uses the system styles (black, white, white with outline; "Sign in / Sign up / Continue with Apple").
  - Never ask for a password or for a "real" email when the person chose a private relay address.
  - Show "Using Sign in with Apple" in account settings.
- **After signup:**
  - Welcome people by the name they shared and let them use the app straight away.
  - Mark extra fields as required or optional (with the benefit), and ask for optional data later, in context.
  - Never lock features for declining optional data.
- **Account deletion (App Review):**
  - If an account can be created in the app, it can be deleted from the app. That means real deletion, not deactivation, or a direct, easy-to-find link to a deletion page (not buried in the privacy policy).
  - Scheduled deletion only alongside an immediate option; say when it will finish and confirm when done.
  - Explain that an App Store subscription keeps renewing until cancelled separately, and link to managing it.
  - Revoke Sign in with Apple tokens.

---

## 9. Paywalls, subscriptions and In-App Purchase

These specialise `persuasion-psychology.md` sections 3, 5 and 6 and the Guardrails for App Store apps.

- **What to use:**
  - Digital goods, features and subscriptions go through In-App Purchase.
  - Physical goods, real-world services and donations use Apple Pay or another payment method.
- **Paywall contents (App Review):**
  - Subscription name, duration and what each period includes.
  - The billed price, localised for each currency and region.
  - A way for existing subscribers to sign in or restore purchases.
  - Links to the Terms of Use and Privacy Policy.
- **Price prominence:** the billed amount ("£29.99 per year") is the most prominent price. A per-month equivalent ("£2.50/month") is secondary text next to it, never in its place.
- **Free trials:** state the trial length and the exact amount that will be charged automatically when it ends. Introductory offers state the intro price, how long it lasts and the standard price after.
- **When to ask:**
  - Let people experience the app first (freemium, metered access or a trial).
  - Prompt at a meaningful moment (reaching a free limit) and keep a subscribe entry in settings.
  - Apple encourages showing subscription benefits during onboarding. My rule on top: an onboarding paywall must be dismissible to free content or a trial.
  - Never show subscribe prompts to people who already subscribe.
- **Use the system purchase sheet unchanged.** If the device can't make payments (parental restrictions), hide the store or explain why.
- **Managing subscriptions:**
  - Inside the app, with the next renewal date next to a Manage option; cancellation easy to find.
  - At cancellation, one reminder of what's lost or an alternative plan is fine; then let them go (SKILL.md Guardrails).
- **Refunds:** a plainly labelled "Request a Refund" option with the refund button visible without scrolling.
- **Offer codes:** a "Redeem Code" button (paywall, onboarding or settings) opens the system sheet.
- **Family Sharing:** if enabled, say so in the product name and on the paywall, and write copy that also makes sense to family members.

---

## 10. Ratings and reviews

- Use the system review prompt (`requestReview`). The system shows it at most three times per app in 365 days and skips people who have already rated, so it may not appear.
- Never tie it to a "Rate us" button; a button should open the App Store review page directly.
- Ask only after real engagement (a completed significant task), never on first launch, during onboarding or mid-task; wait for a natural pause.
- Leave at least a week or two between requests.

---

## 11. Notifications

The cross-platform rules (one per event, opt-in for marketing, no foreground notifications, copy, badges) are in `app-patterns.md` section 9.

- **Marketing notifications (App Review):** need explicit opt-in with a clear description of what will be sent, and an in-app setting to change it later.
- **Interruption levels, set honestly:**
  - Passive: read when convenient.
  - Active: the default.
  - Time Sensitive: something happening now or within an hour. It breaks through Focus, and people can turn it off for the app, so never use it for marketing.
  - Critical: health and safety only, and requires an Apple entitlement.
- **Copy:**
  - The title is short, title case, without the app name (the system shows it). User-created names (a habit, a contact) appear as typed. Leave the title out when the only possible title is generic.
  - The body is full sentences in sentence case.
  - Provide a generic body for when previews are hidden ("New comment").
- **Actions:**
  - Up to four, each a common task (Reply, Mark as Done) with a short title-case label and an SF Symbol.
  - No "Open" action; tapping already opens the app.
  - Destructive actions are marked.
- **Badges** show only the number of unread notifications, clear as soon as items are seen, and are never the only place important information appears.

---

## 12. Widgets, Live Activities and shortcuts

- **Widgets:**
  - One simple idea tied to the app's purpose, with content that changes through the day. Design one great size rather than stretching one design across all of them.
  - A tap opens the exact related screen; interactions stay simple (a button or toggle), never app-like.
  - Standard margins (16pt, 11pt for tight groupings); text 11pt or larger.
  - Colour never carries meaning alone, because tinted, clear and monochrome modes remove it.
  - Show "last updated" when people check more often than the widget refreshes.
  - Signed out: say what signing in adds.
  - The gallery description starts with a verb ("Track today's habits").
  - A logo only in a small corner, and only when the content comes from several sources.
  - Widgets aren't real-time; use a Live Activity for that.
- **Live Activities:**
  - Only for something with a clear start and end that lasts up to eight hours (a delivery, a match, a timer). No ads.
  - Update only when content changes; alert only for essential updates, and never also push a notification for the same update.
  - Design all presentations: compact, minimal, expanded and Lock Screen.
  - End it as soon as the task ends, with a short dismissal time (15-30 minutes); otherwise it lingers on the Lock Screen for up to four hours.
  - Show a harmless summary instead of sensitive details.
- **Home Screen quick actions:**
  - One to four, for high-value tasks. The title states the result ("New Invoice"), and an optional subtitle adds live context ("3 unread").
  - An SF Symbol, never an emoji. No app name.
- **App Shortcuts / App Intents:**
  - Up to ten (the App Intents limit), the most generally useful first.
  - Phrases are short and include the app name. Results work without looking at the screen.
  - They power Siri, Spotlight, the Action button and Shortcuts.
  - Action button labels are at most three words and start with a verb ("Start Timer").
- **Controls (Control Center, Lock Screen):**
  - The symbol carries the meaning alone, with separate on and off symbols for toggles.
  - Hide sensitive values while locked; require unlocking for security actions.

---

## 13. Documents, files and sharing

- **Autosave:** save continuously; never rely on a manual Save. On Mac, Duplicate replaces Save As. The unsaved-changes dot on the close button appears only when autosave is off; an "Edited" title suffix may appear in either mode and clears on save.
- **Document apps:**
  - Use the system document browser or launcher unless there's a strong reason not to.
  - Always offer New (a + button, File > New, Command-N).
  - New documents are named "Untitled".
  - Hide file extensions by default.
  - Use Quick Look for files the app can't open.
- **Undo:**
  - Mac: Undo and Redo at the top of the Edit menu, with Command-Z and Shift-Command-Z.
  - iPad: keyboard shortcuts.
  - iPhone: shake and three-finger swipe.
  - On-screen undo buttons only when essential, in the toolbar with the standard symbols.
- **Drag and drop:**
  - Within a container, dragging moves; between containers or apps, it copies; Option forces a copy.
  - Multi-item drags show a count badge on Mac.
  - Keep dropped content selected at its destination.
- **Sharing:**
  - Share sits in the toolbar and uses the system share sheet (`ShareLink`). Don't duplicate system actions like Print or Copy.
  - Custom share actions are verb phrases without the company name.
  - Collaboration permissions are summarised in short phrases ("Only invited people can edit").
- **Printing:**
  - Offer Print only when something printable and a printer exist; on Mac, dim it otherwise.
  - Use the system print panel, with app options in a category named after the app.
- **Search:**
  - Index content for Spotlight.
  - Provide Quick Look previews for custom file types.
  - Use the system open and save panels.
