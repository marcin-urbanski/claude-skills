# App patterns

Rules for the parts of an app people use every day rather than look at: confirmations and undo, modals, menus, controls, tables, search, loading, keyboard, notifications, accounts and AI features. They apply to web apps, admin panels and native apps alike; `apple-platforms.md` and `apple-patterns.md` add the Apple-specific details. Most of these rules are adapted from Apple's Human Interface Guidelines, where they hold across platforms.

## Contents
1. Confirmations, alerts and undo
2. Modals, sheets and popovers
3. App menus and context menus
4. Choosing a control
5. Lists and tables
6. Search
7. Loading, progress and saving
8. Keyboard, focus and gestures
9. Notifications and badges
10. Accounts, permissions and settings
11. AI features
12. Interface copy

---

## 1. Confirmations, alerts and undo

**Rule:** Interrupt only for what is critical and actionable. Make actions reversible instead of asking "Are you sure?".

**Apply:**
- **Undo beats confirmation.** Common destructive actions that can be reversed (delete an email, archive, move to Trash, remove a row) happen immediately with an Undo option. Confirm only destructive actions that are uncommon *and* irreversible (delete permanently, empty Trash, cancel a subscription).
- **No alert just to inform.** Passive status sits next to what it describes ("Offline" in the toolbar, an unread count). Confirm success only for significant actions such as payments; otherwise report only failures, and when a command can't run, say why.
- **No alert at launch.** For a start-up problem such as no connection, show cached content with a small status label.
- **Anatomy:** a title, an optional message, at most three buttons.
  - Title says what happened, where and why, in two lines at most. Never "Error" or "Error 329347".
  - A message only when it adds something; never explain the buttons.
  - Buttons are verbs tied to the title, one or two words where possible: "Delete", "Discard", "Reply", "View all". Never "Yes" / "No".
  - The button that backs out of the alert's action is always "Cancel". When the alert only reports something and there's nothing to cancel, its dismiss button is "OK", "Done" or "Close", never "Cancel".
  - If an action's natural name contains "cancel" (an import, a subscription), name it differently ("Stop import", "End subscription") so it can't be confused with the Cancel button.
- **Button order:** the likely or default choice on the trailing side (right in left-to-right languages) or at the top of a stack; Cancel on the leading side or at the bottom.
- **Default and destructive:**
  - A destructive button never gets the default role; Enter/Return must not delete.
  - Whenever there's a destructive option, include Cancel, and Cancel is not the default either. To make people read, have no default button at all.
  - Destructive buttons use the destructive (danger) style so they're recognisable, in dialogs and menus alike.
  - Esc always cancels.
- **Undo is labelled and reachable:**
  - Name what it undoes ("Undo delete", "Undo typing"), not a bare "Undo".
  - Web and phone: a toast with Undo after the action, and/or a restorable "Recently deleted" area. Desktop apps with a menu bar: the named Edit > Undo item is the main route; a toast is optional.
  - If the affected item is off-screen, scroll to it and highlight it so the undo is noticeable.
  - In editors, don't cap undo history at one step.
- **Bulk actions** follow the same rule when they're reversible. When the selection reaches beyond what's visible (select all across pages), confirm first and show the count.

**Example:** "Are you sure you want to delete this invoice? [Yes] [No]" becomes: the row disappears at once, and a toast reads "Invoice INV-0142 deleted. [Undo delete]". Bulk permanent deletion gets an alert: "Delete 12 invoices permanently?" / "This can't be undone." [Cancel] [Delete], with neither button as the default.

**The line:** Toasts that disappear on a timer fail slow readers and screen-reader users. Keep an undo toast up for about 10 seconds or more, pause the timer on hover or focus (or make it persistent with a close button), and keep undo reachable elsewhere (Edit menu, Cmd/Ctrl+Z, an activity log).

---

## 2. Modals, sheets and popovers

**Rule:** Use a modal only for a short, self-contained task, critical information, or deep focus. Everything else stays in the flow.

**Apply:**
- **Choose by task size:** a popover (desktop) or bottom sheet (phone) for a small choice; a sheet or dialog for a short task; a full-screen view or separate page for long, multi-step or media-heavy work.
- **Title every modal** with the task it performs ("New invoice", not "Form").
- **No app inside the modal.** No navigation hierarchy in a modal; if it needs steps, one linear path.
- **One at a time.** Never stack modals. Close one before opening the next; only an alert may appear on top of a modal.
- **Always an obvious way out:** a visible Cancel or Close button plus Esc, and swipe-down on phone sheets. If closing would lose what the person typed, stop and offer Save / Discard / Keep editing rather than discarding silently.
- **Popovers:**
  - Small content, sized to it, pointing at the control that opened it, without covering that control.
  - Close on an outside click or when an item is picked; changes are kept when a popover closes itself, and discarded only on explicit Cancel.
  - Never use one for a warning; people dismiss them by accident.
  - On narrow screens, a popover becomes a bottom sheet.

---

## 3. App menus and context menus

This covers menus inside an app (action menus, context menus, a native menu bar). For website navigation and mega menus, see `interaction-patterns.md` section 6.

**Rule:** Menus are lists of commands people scan in a second. Short verb labels, predictable order, related items together.

**Apply:**
- **Labels:** a verb phrase naming the result ("Duplicate invoice", "Export as CSV…"). End with an ellipsis when the command needs more input before it runs ("Rename…", "Export…"). A toggle item can flip its label with state ("Show sidebar" / "Hide sidebar").
- **Order and grouping:** most-used items first; related items grouped with separators; destructive items last, and marked. Exceptions: standard menus keep their fixed order (Edit > Delete), and iOS action sheets put destructive options first. Keep rarely used relatives in the same group as their frequent siblings.
- **Submenus:** sparingly, one level deep. Create one when a word repeats across three or more items ("Sort by" > Date, Name, Size). Menus of more than about five items in a submenu are better split.
- **Icons:** only where a well-known symbol fits, and either every item in a group has one or none do.
- **Dim or hide:**
  - A main menu or menu bar keeps its items and dims the unavailable ones, so people learn what the app can do.
  - A context menu shows only what applies to the current object and hides the rest.
- **Context menus:**
  - Only the most relevant commands for that object, in about three groups at most.
  - Offer them on every comparable object or on none.
  - Every command in them also exists somewhere visible (toolbar, menu, button); a right-click is never the only way.
- **Action menus ("…" or a pull-down button):**
  - Worth it only with three or more items; for one or two, show buttons.
  - Never hide the screen's primary action inside one.

---

## 4. Choosing a control

**Rule:** Pick the control from the kind of choice, not from what looks neat.

**Apply:**

| Choice | Control |
|---|---|
| One setting, on or off | Toggle/switch in settings lists; checkbox in forms and dense desktop settings |
| 2-5 mutually exclusive options, all worth seeing | Segmented control or radio buttons/chips |
| Switching between closely related views of the same content | Segmented control (at most about 5 segments on a phone, 5-7 on wide screens) |
| Switching between app sections | Tab bar or sidebar, not a segmented control |
| Many mutually exclusive options | Select / pop-up menu showing the current value |
| Commands related to one button's purpose | Pull-down / action menu |
| Small numeric adjustments | Stepper next to the visible value, plus a text field when big jumps are likely |
| A value on a continuous range | Slider (minimum on the leading side), plus a field when exact values matter |
| Free text with suggestions | Combo box / autocomplete; typed custom values are allowed |

- A control either selects or performs actions, never both in one group.
- Segments are equal width, all text or all icons, with short noun labels.
- Toggles are only for two opposite states. Several options are a select or radio group, not a stack of toggles.
- A select defaults to what most people want, and its label or current value makes the options predictable without opening it. Add "Custom…" for rare values.
- Nested checkbox settings: children indented, parent shows a mixed state when children differ.

---

## 5. Lists and tables

**Rule:** Text-led items go in a list or table; image-led or varied-size items go in a grid. Keep rows short and push detail to a detail view.

**Apply:**
- **Truncate on purpose.** When width varies, truncate long file names and IDs in the middle ("Invoice-2024…-final.pdf") so start and end stay visible; show the full text on hover or in the detail view.
- **Column headings** are short nouns, no trailing colon.
- **Data tables (admin panels included):**
  - Click a heading to sort, click again to reverse, with the sort direction shown.
  - Columns resizable where content varies.
  - Alternating row shading for wide tables where the eye has to track across.
  - Hierarchical data goes in a tree table where only the first column shows the hierarchy.
- **Selection feedback depends on the job:**
  - A list that navigates (master-detail) keeps the selected row highlighted, showing where you are.
  - A list of options shows a checkmark on the chosen one.
- **Row affordances:** a chevron means "opens a detail view". An info button shows details about the row without navigating away.
- **Scrolling:**
  - Never nest two scroll areas that scroll in the same direction.
  - Auto-scroll only to bring something relevant into view (a search match, a new item, the insertion point).
- **Motion:** animate insertions, deletions and reordering. Don't reflow a list or grid while someone is interacting with it.

---

## 6. Search

**Rule:** If search matters, give it a primary, predictable place and show what's being searched.

**Apply:**
- The placeholder names the scope ("Search invoices", "Search all notes").
- Before typing, show recent searches; while typing, show suggestions and update results live.
- Most relevant results first, grouped by type when mixed.
- Clear categories get a scope bar or filter chips, starting with the broadest; common filters (a person, a type, a date) can become tokens inside the field.
- One global search that covers everything, plus local filter fields only in clearly separate sections.
- Search history is private: offer a way to clear it and consider who else can see the screen.
- No results: repeat the query and offer the fix (`interaction-patterns.md` section 3).

---

## 7. Loading, progress and saving

**Rule:** Never show a blank screen, and never let progress lie.

**Apply:**
- **Loading:**
  - Show the screen's static structure straight away, with placeholder shapes (bars of different widths for text lines, boxes for images), and swap real content in as it arrives.
  - Keep the rest of the app usable while something loads.
  - When fresh data is late, show the old data with "Updated 5 min ago" rather than hiding it.
- **Progress indicators:**
  - Beyond a moment or two, show one: determinate whenever the duration or amount is knowable, indeterminate otherwise.
  - Switch an indeterminate bar to determinate once the total becomes known; never swap a spinner for a bar or back.
  - Progress moves at an honest, even pace: 90% in five seconds and then five minutes for the rest reads as broken.
  - Keep it moving; if the work genuinely stalls, say what's wrong and what to do.
  - Status text names the real step ("Importing row 8,400 of 20,000"), never just "Loading…" or "Processing…".
  - Show progress in the same place every time.
- **Cancelling:** offer Cancel when stopping is harmless; offer Pause and Cancel when cancelling would lose work, and confirm before throwing away partial progress.
- **Actions that take a moment:** show a spinner in the button and change the label to the ongoing verb ("Save" → "Saving…"), so people don't click twice.
- **Saving:**
  - Save automatically as people work; never make a manual Save the only thing standing between them and losing work.
  - On return, restore where people left off: tab, filters, scroll position, selection, draft.
- **Pull to refresh** is an extra, not the only way content updates.

**Bad rows don't stop a long import.** Skip invalid rows, keep going, and report them at the end with a downloadable list. Stop only when the system fails (connection lost, worker crashed), and make resuming safe.

**Example:** A 20,000-row CSV import loses its database connection at row 8,400. Not "Import failed. [OK]". Instead: "Import stopped at row 8,400 of 20,000" / "The connection was lost while saving row 8,401. The first 8,400 rows were imported and kept." [Close] [Download report] [Resume import]. When it finishes with bad rows: "Imported 19,912 of 20,000 rows. 88 rows were skipped." [Download skipped rows].

---

## 8. Keyboard, focus and gestures

**Rule:** Everything works from the keyboard, standard shortcuts keep their standard meaning, and no action depends on a gesture alone.

**Apply:**
- **Never repurpose standard shortcuts:** new, open, save, print, close, quit, undo/redo, cut/copy/paste, select all, find, bold/italic/underline, settings. On the web, don't hijack browser shortcuts either. A standard shortcut may be reused only when its usual action doesn't exist in the app.
- **Custom shortcuts:** only for the most frequent app-specific commands.
  - Cmd/Ctrl is the base modifier, Shift the secondary one, Alt/Option for rarer variants.
  - Never make an unrelated command by adding a modifier to an existing shortcut (Shift+Cmd+Z must stay related to undo).
  - Show shortcuts next to menu items; don't show them in context menus.
- **Esc** closes the topmost modal, popover or menu. **Enter** triggers the default button, never a destructive one.
- **Focus:**
  - Never move focus without a user action. The exception: if the focused item disappears, move focus to its neighbour.
  - Tab moves between areas (sidebar, list, toolbar); arrow keys move within an area (the roving-tabindex pattern).
  - Focus is visible: a ring on fields, a full-row highlight in lists.
- **Gestures:**
  - Every gesture has a visible equivalent: swipe-to-delete also has a menu item or button, and swiping between pages also has Previous/Next buttons.
  - Standard gestures keep their standard meaning (tap selects, touch-and-hold opens more options, pinch zooms). Custom gestures are only shortcuts for frequent tasks.
- **Pointer:** controls that fade out (video controls, collapsed toolbars) come back on hover. Cursors keep their meaning: pointing hand for links, I-beam for text, grab hand for panning, not-allowed over invalid drop targets.
- **Drag and drop:**
  - Always offer a non-drag way to do the same thing.
  - Highlight a drop target only while hovering over it, and only if it accepts the item.
  - A failed drop animates back.
  - Drops are undoable.

---

## 9. Notifications and badges

**Rule:** A notification is an interruption the person didn't ask for at that moment. Send it only when it's worth that.

**Apply:**
- One notification per event; no repeat nudges when people don't respond.
- Marketing notifications need their own explicit opt-in that says what will be sent, and a settings screen where people can change it later (also required by Apple for iOS apps).
- No notification while the person is looking at the app; update the view or the badge instead.
- Errors belong in the app (inline, or in an in-app notification centre), not in a push or system notification.
- Copy:
  - Title: short and specific (the event, the sender, the subject).
  - Body: full sentences.
  - Don't repeat the app name, and keep private details out of the text shown on a lock screen.
- Actions on a notification: at most a few, each a common task that saves opening the app ("Reply", "Mark as paid"). No "Open app" action.
- A badge shows only a count of unread or pending items: never promotions or other data. Clear it as soon as the items are seen. Never draw fake badges to pull attention.

---

## 10. Accounts, permissions and settings

**Rule:** Ask for as little as possible, as late as possible, and explain why at the moment of asking.

**Apply:**
- **Accounts:**
  - Require an account only when core features need one.
  - Let people browse and try first. In commerce, allow guest checkout and offer an account after purchase.
  - After signup, ask only for what's required; ask for optional details later, in context (a phone number when they turn on SMS updates), with the benefit stated.
- **Account deletion:** if people can create an account in the app, they can delete it there too: real deletion, not deactivation, as easy to find as signup. Say when deletion completes, and remind them that app-store subscriptions must be cancelled separately.
- **Sign-in:** prefer passkeys and platform sign-in (Sign in with Apple/Google) over passwords; require two-factor if passwords remain. Name the method on the button ("Sign in with Face ID").
- **Permissions (camera, location, notifications, contacts):**
  - Ask when the person first uses the feature that needs it, not at launch, unless the app can't work at all without it.
  - Ask for the narrowest scope.
  - A pre-permission explainer has one button, "Continue", which opens the system prompt. No "Allow" lookalike, no fake prompt.
- **Where settings live:**
  - View-specific options (sort, filter, show/hide) in the view they affect.
  - Rarely changed, app-wide options in Settings.
  - Keep settings few, and detect instead of asking wherever possible.
  - Don't duplicate what the OS already controls (appearance, interface text size, reduced motion); follow the system by default. Settings for the app's own content, such as an editor's font and size, are fine.
- **Settings labels** say what the "on" state does.

---

## 11. AI features

**Rule:** Be clear where AI is involved, keep the person in control of the result, and never let AI act destructively on its own.

**Apply:**
- Label AI-generated content and AI actions; AI never passes as a human.
- State what the feature can and can't do up front. For open-ended prompts, offer example inputs.
- Next to generated output, offer Edit, Retry and Undo. When intent is ambiguous, offer a few distinct versions.
- Progress copy names the real step ("Summarising 42 support tickets…"). Errors are plain language with a next step; when a request is refused, suggest a request that would work.
- Confirm before significant actions taken on the person's behalf; never automate deleting, sending or paying.
- Say when data leaves the device and whether it's stored or used for training; ask before using personal data, and allow opting out.
- Provide a non-AI path when the model is unavailable.
- Feedback (thumbs up/down) is optional and never interrupts.

---

## 12. Interface copy

**Rule:** Plain, specific, consistent. The interface talks about the person's task, not about itself.

**Apply:**
- Buttons are verbs that describe the result ("Send invoice", "Save draft"). Plain beats clever.
- Links name their destination, never "Click here".
- A flow uses one forward word throughout ("Continue" or "Next", not both) and ends with "Done".
- Capitalisation: one style per element type, used everywhere. Web: sentence case throughout (as in `product-pages.md`), which is how the examples in this file are written. Native Apple apps: title case for buttons, menu items, tabs and titles, sentence case for messages and body text (`apple-patterns.md` section 1).
- Errors:
  - Sit next to the problem.
  - Never blame the person; state the fix with the real constraint ("Use at least 12 characters", not "Password too short").
  - No "Oops", no robotic "Invalid input".
  - If many people hit the same error, redesign the interaction rather than the message.
- No "we" in errors ("Couldn't load invoices", not "We couldn't load your invoices").
- Possessives sparingly ("Favourites", not "Your Favourites"); never mix "my" and "your".
- Match the input: "tap" on touch devices, "click" on desktop.
- Avoid idioms and jokes in UI text; they don't translate.
- Useful text is selectable and copyable: error messages, IDs, serial numbers, addresses.
