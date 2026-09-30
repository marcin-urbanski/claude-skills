# Apple platforms: foundations and structure

Rules for native iPhone, iPad and Mac apps (SwiftUI, UIKit, AppKit, Mac Catalyst): how each platform behaves, sizes and type, colour and Liquid Glass, navigation structure, windows, the Mac menu bar, input, icons and accessibility. Based on Apple's Human Interface Guidelines, rewritten as rules. `apple-patterns.md` covers native components and flows; `app-patterns.md` covers the cross-platform rules both build on.

Where this file differs from the web-oriented rules elsewhere in the skill (touch targets in px, 16px body text, 1.5 line height, bottom-of-screen CTAs), this file wins for native Apple apps.

## Contents
1. Platform first
2. What each platform is for
3. Sizes and spacing
4. Typography and Dynamic Type
5. Colour and Dark Mode
6. Liquid Glass and materials
7. Layout and adaptivity
8. Navigation structure
9. Toolbars
10. Windows, panels and full screen (iPad and Mac)
11. The Mac menu bar
12. Keyboard, pointer and gestures
13. SF Symbols, icons and the app icon
14. Accessibility
15. Motion and haptics

---

## 1. Platform first

**Rule:** In a native app, the platform's components and conventions are the design system. Brand lives in the content, colour, typography of headlines and iconography, not in reinvented controls.

**Apply:**
- Use system components (NavigationStack/SplitView, TabView, List, Form, toolbars, sheets, menus) before building custom ones. They bring Dynamic Type, Dark Mode, Liquid Glass, VoiceOver, keyboard support and future OS changes for free.
- This counts as "the client's own design system" for `anti-slop.md` section 1: skip the three-directions step for the app chrome. Still set a direction for the parts that carry identity: accent colour, content presentation, headline type, illustrations, app icon, empty states, onboarding.
- Express brand through familiar components kept at their standard size, placement and behaviour. Don't repeat the logo through the app or spend space on brand-only elements; the launch screen is not a branding moment.
- Test on real devices, not only in Previews and the Simulator.
- **Identity direction:** one short direction instead of the three-directions exercise: accent colour, headline type, icon idea, illustration and empty-state tone, each with a reason. Offer alternatives only when the brand is still open.
- **Final check for native apps** (in place of the 390px/1440px check in `anti-slop.md` section 7): smallest and largest iPhone, iPad at compact and regular width, Mac at its minimum and a very large window, the largest Dynamic Type size, Dark Mode with Increase Contrast, and VoiceOver on the main flow.

**The line:** Custom UI is fine when it's the idea of the app (a drawing canvas, a game, a timeline editor). Then it must still honour Dynamic Type, Dark Mode, Reduce Motion, VoiceOver and keyboard access.

---

## 2. What each platform is for

- **iPhone:** often one-handed and on the move; sessions range from a minute or two to an hour or more. Few controls on screen, secondary actions one step away. Swipe back and swipe actions on list rows are expected.
- **iPad:** not a stretched iPhone. Content-first on a large display, fewer modal sheets and full-screen transitions. Touch, hardware keyboard, trackpad and Pencil may all be in use at once. Windows resize freely, so every screen works at any width.
- **Mac:** stationary, sessions from minutes to hours, several apps visible at once. More content in fewer levels, less modality. Every command is in the menu bar, frequent ones have keyboard shortcuts, and precise pointer editing is expected. People customise toolbars, window layouts, fonts and colours.
- **Porting iPhone/iPad to Mac:**
  - Build the iPad version properly first: multiple windows, keyboard support, drag and drop and resizable layouts carry over to Mac.
  - Replace the tab bar with a sidebar.
  - Move controls from the bottom edge into the window toolbar, and mirror them in the menu bar.
  - Use the width: several columns, an inspector beside the content instead of a popover.
  - Give every object a context menu.
  - "Scale Interface to Match iPad" shrinks everything to 77%; the "Optimize for Mac" idiom renders at 100% but needs a full layout audit.

---

## 3. Sizes and spacing

Units are points (pt), not pixels.

| | iOS, iPadOS | macOS |
|---|---|---|
| Hit target, default | 44 x 44pt | 28 x 28pt |
| Hit target, minimum | 28 x 28pt | 20 x 20pt |
| Body text, default | 17pt | 13pt |
| Text, minimum | 11pt | 10pt |

- Spacing between controls matters as much as their size: about 12pt around controls with a visible bezel or background, about 24pt around borderless ones (icon-only and text buttons).
- On iOS, 44pt is the target to design to. Don't use 48pt because the web rule says so, and don't force 44pt onto Mac toolbars and list rows, where 28pt is normal.
- Use the system's layout margins and readable-content width rather than ad hoc insets; custom spacing follows an 8pt scale (a house convention, not an Apple rule).

---

## 4. Typography and Dynamic Type

**Rule:** Use the system text styles. They give you Dynamic Type, correct tracking and platform-correct sizes.

**Apply:**
- iOS/iPadOS text styles at the default size:

  | Style | Size / leading |
  |---|---|
  | Large Title | 34/41 |
  | Title 1 | 28/34 |
  | Title 2 | 22/28 |
  | Title 3 | 20/25 |
  | Headline | 17 Semibold |
  | Body | 17/22 |
  | Callout | 16 |
  | Subheadline | 15 |
  | Footnote | 13 |
  | Caption 1 | 12 |
  | Caption 2 | 11 |

  Headline differs from Body by weight alone, and on Apple's font Semibold is enough for that step.
- macOS text styles: Body 13/16, Headline 13 Bold, Title 1 22, Large Title 26, Callout 12, Subheadline 11, Footnote and Caption 10. macOS has no Dynamic Type; use the control and menu font variants to match system controls.
- Native leading is tighter than the web: Body is about 1.3 on iOS, 1.23 on Mac. Use the built-in leading; switch to loose leading only for long passages in wide columns. The 1.5-1.6 rule in `visual-craft.md` is for web reading.
- Use SF Pro and New York through `Font.Design` (`.default`, `.serif`, `.rounded`, `.monospaced`); never bundle them. The system adjusts tracking per size, so don't set letter-spacing in code.
- A brand font suits headlines; keep body and captions in the system font, which is tuned for small sizes. A custom font must support Dynamic Type and Bold Text itself.
- No Ultralight, Thin or Light weights for UI text.
- **Dynamic Type:**
  - Content text scales; chrome such as tab labels may not need to.
  - Icons next to text scale with it; SF Symbols do this automatically.
  - At accessibility sizes, horizontal rows stack vertically (text above the icon and timestamp), columns reduce, rows grow and text wraps instead of truncating.
  - Test with the largest accessibility size.

---

## 5. Colour and Dark Mode

**Rule:** Build on semantic system colours and support light, dark and increased contrast from day one.

**Apply:**
- **Semantic colours:**
  - Text: `label`, `secondaryLabel`, `tertiaryLabel` and `quaternaryLabel`, for primary text, supporting text, unavailable items and watermarks.
  - Backgrounds: `systemBackground` and its secondary and tertiary variants; the grouped set for grouped lists and forms.
  - Other roles: `separator`, `link`, `placeholderText`.
  - Never hard-code their values (they change between releases) and never use one for another role.
- Every custom colour is a Color Set with four variants: light, dark, and both with increased contrast.
- Dark Mode has base and elevated backgrounds; sheets and popovers switch to elevated automatically. A custom background colour breaks that depth cue.
- Aim for 7:1 contrast for small text on custom dark colours; 4.5:1 is the floor.
- Follow the system appearance. No in-app light/dark switch.
- Test Dark Mode combined with Increase Contrast and Reduce Transparency.
- Slightly dim content images with white backgrounds in Dark Mode so they don't glow.
- One colour, one meaning: if the accent marks interactive text, don't use it on static text.
- **macOS:**
  - The app's accent colour appears only when the user's accent setting is Multicolor, so never rely on it for brand or meaning. Carry the brand in content, illustrations, the app icon and headline type instead.
  - Use `selectedContentBackgroundColor` and its unemphasised variant for selection in inactive windows, and `alternatingContentBackgroundColors` for striped tables.

---

## 6. Liquid Glass and materials

**Rule:** Liquid Glass is for the floating layer of controls and navigation. Content sits underneath it and carries the colour.

**Apply:**
- System bars, tab bars, toolbars, sidebars, sheets and popovers get Liquid Glass automatically. Apply `glassEffect` to custom views sparingly, only for the most important functional elements, never in the content layer.
- Regular glass for anything text-heavy or over busy backgrounds; clear glass only over rich media, with a dimming layer (around 35%) when the media underneath is bright.
- Colour on glass:
  - Don't tint bars.
  - Tint only the background of the primary action, never several controls.
  - Keep labels monochrome over colourful content.
  - Put brand colour in the content layer, which scrolls under the glass.
- Separate bars from content with the scroll edge effect, not a solid or semi-opaque custom bar background. Let full-bleed images run under sidebars and bars (`backgroundExtensionEffect()`).
- At rest (scroll view at the top), controls stay legible: don't park content of a similar colour under them.
- Custom controls on bars use corner radii concentric with the bar.
- In the content layer, use standard materials (ultraThin to thick; thicker for text and detail) with vibrant label colours.

---

## 7. Layout and adaptivity

- Decide layout by size class (compact or regular width and height), never by device model or orientation. Test iPad split screen, freely resized iPad windows and very wide Mac windows.
- Changing size class changes how much is visible, not which features exist: a tab bar can become a sidebar at regular width, and an overflow menu's items can move into view.
- Respect safe areas (Dynamic Island, Home indicator, bars, the camera housing on some Macs), layout margins and the readable-width guide for text.
- Most important content near the top and on the leading side; write layouts in leading/trailing, not left/right, so they flip for right-to-left languages.
- **Mac:** keep controls and critical information away from the bottom of windows, because people drag windows partly off screen. A bottom bar holds only small status text (item count, free space). The thumb-zone rule in `interaction-patterns.md` section 2 applies to iPhone only, and even there platform conventions come first: add and compose buttons sit at the trailing end of the toolbar, sheet actions in the sheet's top bar. Bottom placement suits flow buttons such as onboarding's Continue.
- Background art fills the space without distortion and extends beyond the expected frame.

---

## 8. Navigation structure

**Rule:** Tab bar on iPhone, tab bar that can become a sidebar on iPad, sidebar on Mac. Pick the structure from the content hierarchy.

**Apply:**
- **Tab bar:**
  - For moving between top-level sections, never for actions.
  - Always visible; only a modal covers it.
  - Never disable or hide a tab because its content is unavailable; open it and explain.
  - Labels are single words; icons are filled SF Symbols.
  - Keep to what fits: on iPhone, overflow creates a "More" tab that hides content.
  - A red badge only for something genuinely needing attention.
- **iPhone:** the tab bar floats at the bottom. Search can be its own tab at the trailing end. With an accessory (a mini player), the bar can minimise on scroll.
- **iPad:** the tab bar sits at the top. Start with a tab bar using the `sidebarAdaptable` style so people can switch to a sidebar. Use `NavigationSplitView` when the app is sidebar-first. If tabs are customisable, ship five or fewer by default.
- **Mac:** a sidebar in a split view; list the top-level sections in the View menu too. A segmented control in the toolbar only for a flat set of views.
- **Sidebars:**
  - At most two levels of hierarchy. Deeper data adds a content column (three-column split view: sidebar, list, detail).
  - People can hide the sidebar but it isn't hidden by default. On Mac: a toolbar button plus Show/Hide Sidebar in the View menu.
  - Mac sidebar icons follow the user's accent colour; a fixed colour only when it means something.
- **Split views:**
  - Only at regular width.
  - Keep the selection highlighted in every pane that leads to the detail.
  - On Mac, set minimum and maximum pane widths so dividers never disappear, and offer two ways to bring back a hidden pane (toolbar button and menu command with a shortcut).
- Swipe from the leading edge goes back. Never override it.

---

## 9. Toolbars

- **Three zones (iPad and Mac):**
  - Leading: back, sidebar toggle, title/document menu.
  - Centre: common controls, customisable, which collapse into the system overflow menu as the window narrows.
  - Trailing: always-needed items, inspector toggle, search and the primary action.
  - At most about three groups.
- **One primary action** (prominent style, e.g. Done) at the trailing edge.
- Don't build your own overflow menu; decide which items drop out first and make sure nothing overflows at the default window size.
- **Titles:** short (under about 15 characters), naming the content, never the app name. Leave the title out when the content identifies itself (a note, a document).
- **iPhone:** large titles that collapse on scroll for top-level screens; the toolbar holds only essentials, the rest goes in a More menu.
- Use the standard Back and Close buttons with system symbols, not the words "Back" and "Close". Prefer borderless SF Symbols; text only where no symbol fits ("Edit"). Leave space between adjacent text buttons.
- **Mac:**
  - Every toolbar command also exists in the menu bar, because people can hide or customise the toolbar.
  - Switches, checkboxes, radio buttons and help buttons never go in the toolbar.
- Toolbars may hide for reading or media, but come back with a familiar action (tap, scroll up, pointer at the top edge).

---

## 10. Windows, panels and full screen (iPad and Mac)

- **Primary vs auxiliary windows:** a primary window holds the main navigation and content. An auxiliary window does one task, has no navigation elsewhere and has a close button.
- Don't open new windows by default. Offer "Open in New Window" in the context and File menus; open one automatically only when it preserves context (a compose window).
- Never draw custom window frames or controls. In user-facing text they are "windows", never "scenes".
- **Mac window states:**
  - Only the key window takes input and shows coloured window buttons.
  - Inactive windows lose their translucency and selections dim.
  - System components handle this; custom UI must follow it.
- **Mac panels:**
  - A floating inspector that follows the current selection. It holds direct controls (sliders, steppers), not text entry.
  - Noun title ("Inspector"); no minimise button; not listed in the Window menu.
  - Menu item "Show Inspector", without the word "panel".
  - Panels hide when the app is inactive.
- **Full screen:**
  - Offer it for media, games and focused work.
  - In full screen, change proportions, not which features appear.
  - Never enter or leave it programmatically, and never resize windows programmatically.
  - On Mac, use the system full-screen mode (green button, View > Enter Full Screen, Control-Command-F); never build a custom window-mode menu.
- Assume people can leave at any moment: save and restore state, pause media and games, and let downloads and exports finish in the background. Notify only when something important finishes.

---

## 11. The Mac menu bar

**Rule:** Every command lives in the menu bar, in the standard menus and order people already know.

**Apply:**
- **Order:** App menu (bold app name), File, Edit, Format, View, app-specific menus, Window, Help. Menu titles are one word where possible.
- **App menu:**
  - About AppName, then Settings… (Command-Comma, app-wide settings only), then Services.
  - Hide AppName, Hide Others, Show All, then Quit AppName.
  - Never put Settings in the toolbar.
- **File:**
  - New *Item* (name the type: "New Note"), Open…, Open Recent (names, not paths, with Clear Menu).
  - Close, Save, Duplicate (preferred over Save As), Rename…, Move To…
  - Export As… only for formats the app doesn't normally use; Print…
  - Rename or remove the File menu if the app has no files.
- **Edit:**
  - Undo and Redo name what they act on ("Undo Typing").
  - Cut, Copy, Paste, Paste and Match Style, Delete (never "Erase" or "Clear"), Select All, then Find.
- **View:**
  - Always present, even if it only holds Enter Full Screen.
  - Show/hide items name the action they'll take: "Show Toolbar" while hidden, "Hide Toolbar" while shown.
  - Order: tab bar, toolbar, Customize Toolbar, sidebar, full screen.
- **App-specific menus** sit between View and Window and list every command, including rare ones, so everything is findable, shortcut-able and keyboard-reachable. Order them from general to specific, following the object hierarchy (Mailbox, then Message).
- **Window:**
  - Always present, even in single-window apps.
  - Minimize, Zoom, Bring All to Front, then the open windows.
- **Help:** short; the Help Book format adds search automatically.
- Unavailable menu bar items are dimmed, never removed. A menu whose items are all unavailable still opens.
- Holding a modifier can reveal an alternative item (Option turns Close into Close All) mainly in menu bar menus (never in context or Dock menus), with one modifier, never as the only route to a command.
- **Menu bar extras:**
  - A template icon or SF Symbol that opens a menu.
  - Optional for the user: offer it in settings rather than forcing it.
  - Never the only place a feature lives; the system can hide it.
- **Dock menu:** open windows plus a few actions useful while the app is in the background.
- **iPad** has a menu bar too, revealed from the top edge: keep it tidy, and make sure every command is also reachable in the UI.

---

## 12. Keyboard, pointer and gestures

- **Standard Mac shortcuts people rely on** (never repurpose):
  - Files and windows: Command-N, O, S, P, W, Q, M, H, Command-Comma (settings), Command-? (help), Command-` (next window).
  - Editing: Command-Z / Shift-Command-Z, X, C, V, A, F, G / Shift-Command-G, B, I, U.
  - View and control: Control-Command-F (full screen), Option-Command-T (show/hide toolbar), Command-Period and Esc (cancel).

  The general rules for custom shortcuts are in `app-patterns.md` section 8.
- **Custom shortcuts:**
  - Command first, Shift second, Option for rarer variants. Avoid Control in custom shortcuts: the system uses it for its own (focus movement, screenshots, full screen). System-provided commands keep theirs (SwiftUI's `SidebarCommands` gives Show/Hide Sidebar Control-Command-S).
  - Displayed in the order Control, Option, Shift, Command.
  - Avoid extra modifiers on punctuation keys, which move between keyboard layouts.
- **Modifiers keep their meaning:** Option-drag copies, Shift keeps aspect ratio while resizing, arrow keys nudge by the smallest unit.
- **Full Keyboard Access:**
  - Support and test it on every platform.
  - On iPad, make content keyboard-focusable (fields, lists, sidebars, collections) and leave buttons and switches to Full Keyboard Access.
  - Tab moves between groups, arrows within a group.
- **Pointer (iPad and Mac):**
  - Hit regions extend beyond the visible element; adjacent bar buttons have touching hit regions.
  - Never scale list rows on hover.
  - Controls that auto-hide return on hover.
  - Secondary click always opens the context menu.
  - Support marquee (band) selection in custom collections.
- **Gestures:**
  - Never redefine system gestures: edge swipes and Home indicator; three-finger undo/redo and copy/paste; shake to undo; four-finger app switching on iPad; Mission Control and swipe between full-screen apps on Mac.
  - Standard gestures keep their meaning.
  - Every gesture has a visible alternative.

---

## 13. SF Symbols, icons and the app icon

- **Use SF Symbols** for interface icons: they match text weight, scale with Dynamic Type, adapt to Dark Mode and include right-to-left variants. Check each symbol's OS availability.
- **Standard symbols for standard actions:**

  | Action | Symbol |
  |---|---|
  | Share | `square.and.arrow.up` |
  | Delete | `trash` |
  | More | `ellipsis` |
  | Add | `plus` |
  | Filter | `line.3.horizontal.decrease` |
  | Search | `magnifyingglass` |
  | Compose | `square.and.pencil` |
  | Undo | `arrow.uturn.backward` |
  | Account | `person.crop.circle` |

- **Weight and scale:** match the symbol weight to adjacent text, and change emphasis with symbol scale (small, medium, large) rather than point size.
- **Variants:** let the container choose where it can (tab bars take filled symbols, toolbars and lists outline). Enclosed variants hold up at small sizes; slash means unavailable. Don't draw your own selected states for standard bars.
- **Rendering modes:**
  - Monochrome; hierarchical for depth; palette for two or more colours; multicolour when the colours carry meaning.
  - Check legibility per context.
  - Variable colour only for changing values (signal, progress, volume).
- **Symbol animations carry meaning,** used sparingly:
  - Bounce: something happened.
  - Pulse or breathe: ongoing activity.
  - Rotate: work in progress.
  - Replace: a state change (play/pause).
  - Wiggle: draws attention to an easily missed action.
- **Custom icons and symbols:**
  - Vector (SVG or PDF), matching the system's weight, detail and optical size.
  - Custom symbols start from the template of the closest system symbol and use its component library for badges.
  - Every custom icon has an accessibility label.
  - Never use SF Symbols (or lookalikes) in app icons or logos, and never draw Apple hardware.
- **App icon:**
  - 1024 x 1024 square built in Icon Composer from a background layer and one or more foreground layers.
  - Unmasked; the system rounds corners and adds Liquid Glass highlights, so no painted shadows, bevels, glows or pre-rounded corners.
  - Few shapes, centred, crisp edges; illustration rather than photos, no screenshots, and no text unless it's essential to the brand.
  - Provide or check the dark, clear and tinted variants, keeping the same core shape in each.
  - One design across iPhone, iPad and Mac.

---

## 14. Accessibility

This extends the Guardrails in SKILL.md for native apps.

- **VoiceOver:**
  - Every icon-only control and custom element gets an accessibility label that says what it does.
  - Decorative images are hidden; meaningful images describe only what the image itself conveys.
  - Each screen has a unique title and real headings for rotor navigation.
  - Related elements (image + caption, a row's parts) are grouped so they're read as one item.
  - Changes of content or layout are announced.
- **Voice Control:** people speak the visible labels, so every control has one, and the accessibility label starts with the visible text (WCAG 2.5.3).
- **Dynamic Type:** text grows to at least 200%, layouts reflow (section 4).
- **Contrast:**
  - 4.5:1 for text up to 17pt, 3:1 for 18pt and larger or bold.
  - Check light and dark.
  - Provide a higher-contrast palette when Increase Contrast is on if the default can't meet the minimums.
- **Colour blindness:** red-green and blue-orange pairs are the hardest; add a shape or symbol to any state carried by colour.
- **Reduce Motion:**
  - Remove automatic, repeating and peripheral motion, zooms and depth changes.
  - Replace slides with crossfades; stop springs from bouncing.
- **Reduce Transparency:** check every material and glass surface with it on.
- **Timing and media:**
  - No UI that dismisses itself on a timer without another way to reach it.
  - No autoplaying audio or video without visible controls; respect the system's autoplay setting.
  - Never convey essential information by sound alone; captions or transcripts for media.
- **Test:**
  - With VoiceOver, Voice Control, Switch Control, Full Keyboard Access, Bold Text and the largest text size.
  - Use Accessibility Inspector.
  - Declare supported features in the App Store's Accessibility Nutrition Labels.

---

## 15. Motion and haptics

- Standard components already animate and give feedback; don't add decorative motion to interactions people repeat constantly. A system symbol effect or haptic that marks a meaningful outcome (a task completed) is fine. The durations in `visual-craft.md` section 10 and `design-modes.md` apply only to custom motion.
- Motion follows the gesture that caused it (a view that slides down to open slides up to close), can always be interrupted, and never blocks input.
- Motion never carries information alone; pair it with text, haptics or sound.
- **Haptics (iPhone):**
  - System controls (toggles, pickers, sliders) already play haptics; don't double them.
  - For custom haptics, use the feedback categories strictly: notification for the outcome of a task (success, warning, error), impact for a physical snap or collision, selection for a changing value.
  - One pattern, one meaning.
  - Short, tied to discrete events, and matched to the animation.
  - Never while the camera or microphone is recording.
- **Mac trackpad haptics:** alignment feedback when snapping to guides or hitting a limit.
- Timing follows `visual-craft.md` section 10 and the App mode in `design-modes.md`; with Reduce Motion, a crossfade in place of movement is the native choice.
