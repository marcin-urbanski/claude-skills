# CODING_STANDARDS.md template

`spec-first` uses this to start a project's `CODING_STANDARDS.md`; `retro` uses it to add, sharpen and remove rules later. This file is the one place that sets the format, the limit and what a new rule replaces.

## How the file works

- The `reviewer` checks every rule against every diff, and the `implementer` reads the file before writing code. Every rule costs on every task, so the file holds at most 15.
- **Core**: the few things most expensive to get wrong in this product, chosen when the project starts. **From evidence**: added only when review found the same problem at least twice (each human or reviewer comment is one finding, earlier PRs included; in a repository with no review comments, each bug-fix commit or PR that names the root cause is one), or the user asked for the rule.
- A rule is checkable on a diff: it names the code shape a reviewer can point at (an API, a type, a folder, a call). It states the target behaviour first, then the exceptions the code relies on, and ends with *Why:* (one real consequence) and the number of findings so far.
- Stays out of the file:
  - anything a compiler, linter, test or hook can enforce: add that check instead;
  - what `reviewer-checklist.md` in this folder already covers (security, scope, test quality, code smells), unless the rule names a concrete API or anti-pattern of this framework or project that the checklist does not name (`__return_true` in a WordPress `permission_callback`, the one way this app shows errors);
  - what `CLAUDE.md` or the framework guidelines it loads already say, such as the Laravel Boost block;
  - where things live: that is a navigation line in `CLAUDE.md`.
- Before a rule goes in, grep the code for what it requires or forbids. If existing code breaks it on purpose, the rule is too wide: narrow it or name the exception. Words such as *every*, *never* and *first* are where that happens most. An accidental violation becomes a task when the current work touches that code, and a follow-up issue otherwise.
- At 15 rules, a new one merges with or replaces an old one. Remove first a rule that an existing check already enforces, then the From evidence rule with the fewest findings; a Core rule leaves only through a check. The user picks.

## Skeleton

```markdown
# Coding standards

Rules the reviewer checks on every diff, on top of its general checklist. Breaking one is at least Important.
Keep this file to 15 rules at most: a new rule replaces or merges an old one, and anything a compiler or test can
enforce goes there instead.

## Core

The few things that are most expensive to get wrong in <product>.

1. **<Target behaviour in a few words>.** <What the code does, with the project's names; the exceptions.>
   *Why:* <what goes wrong for the user>. (0 findings)

## From evidence

Each rule has at least two findings, or the user asked for it.
```

Add one line to the project's `CLAUDE.md`, so a session that writes code without the `implementer` finds the file:

```markdown
- Before writing code, read `CODING_STANDARDS.md`: the rules the reviewer checks on every diff.
```

## Core candidates

Pick 3 to 5 that fit the project and rewrite them with its own names. Then add the product's own risk from the spec: what costs the most when it is wrong (money, time, another user's data, a delete, a message sent twice). Core holds 5 to 7 rules in total. For a stack not listed here, write all of them from the spec's risks in the same format.

### Swift / SwiftUI

From TimeTracker, where each of these came up in review several times.

- **Time comes in through parameters.** Logic takes `now:` and `calendar:` (a long-lived object takes a `() -> Date`); only a public entry point the app calls may default them to `Date()` or `.current`. Tests pin the time zone and the instant, and a test of day or month grouping has an entry across local midnight. *Why:* time logged near midnight lands on the wrong day.
- **Logic lives in the package, with tests.** Rules about what is counted, filtered, sorted or stored live in the Swift package that has tests; app services schedule, coordinate and talk to the platform; views lay out and forward actions. *Why:* the app target has no tests.
- **Failures of user actions are shown.** No `try?` or empty `catch` on something the user did; the rule names the one way this project shows it (an alert, an inline message, a status). *Why:* a silent failed delete looks like success.
- **Views don't fetch in `body` or `init`.** Loaded data goes into `@State` from `.task` or an observer; `.task(id:)` keys are stable, never derived from `Date()`. *Why:* `body` runs on every state change, so a fetch there repeats and stutters.
- **Order is deterministic.** A sort, `min` or `max` whose result reaches the UI, storage or a test ends with a unique tie-break such as the id. *Why:* rows with equal names swap places on every refresh.

### Laravel / PHP

When the project has Laravel Boost, it already puts the framework's conventions in `CLAUDE.md` (Eloquent before `DB::` for queries, though `DB::transaction()` is fine; Form Requests, eager loading, `$fillable`, `casts()`, queued jobs, `config()` over `env()`, Pest and factories), and its `search-docs` answers how the installed version behaves. Do not repeat either here; these candidates cover what Boost does not.

- **Money is integer minor units.** Amounts are stored and computed as integer cents (an integer column, an `int` cast or the project's money object); a percentage is applied once, through one named rounding helper. Never `float`, and never arithmetic on a decimal column's string value. *Why:* float rounding makes a total one cent off the invoice.
- **Time is stored in UTC and grouped in the business's time zone.** Comparisons run in UTC; day and month boundaries are computed in the zone the business or user works in. Tests freeze time (`$this->travelTo()`) and include a case across local midnight. *Why:* an entry at 00:30 lands in the previous month's report.
- **Writes that span rows are atomic.** A change that writes more than one row or table runs in `DB::transaction()`, and mail, HTTP calls and dispatched jobs that depend on it run after commit (`afterCommit()`). *Why:* a failure half-way leaves an invoice without its lines, or emails a rolled-back order.
- **Jobs and webhooks can run twice.** A queued job or webhook handler keys its work on the external id (a unique index with `upsert` or `firstOrCreate`), so a retry changes nothing. *Why:* the payment provider retries a webhook and the customer is credited twice.
- **Each outside service has one client.** One class wraps each external API (`Http::` or the vendor's SDK), with a timeout, retries and errors mapped to the project's exceptions. Tests fake that class or use `Http::fake()`, and the base test case calls `Http::preventStrayRequests()`. *Why:* an unfaked test call reaches the real service and can charge a real card.

### WordPress (plugins, themes, WooCommerce)

PHPCS with the `WordPress-Extra` standard enforces escaping, nonces, input sanitising, prepared SQL, prefixes and the text domain. Set it up as a check (composer script, pre-commit or CI) instead of writing those as rules.

- **Writes check a capability on the object.** A REST route's `permission_callback`, an AJAX handler or an admin action checks a specific capability on the object it changes (`current_user_can( 'edit_post', $id )`); never `__return_true` or only `is_user_logged_in()` on a write. *Why:* any subscriber can change another user's post.
- **WooCommerce data goes through its CRUD objects.** Orders and products are read and written with `wc_get_order()`, `wc_get_orders()`, `get_meta()`, `update_meta_data()` and `save()`, never `get_post_meta()` or `WP_Query` on orders, and the plugin declares HPOS compatibility. *Why:* with HPOS on, post meta on orders is empty.
- **Change other code through hooks.** Behaviour of WordPress, WooCommerce, other plugins or a parent theme changes only through actions, filters and child-theme template overrides, never by editing their files. *Why:* the next update overwrites the edit.
- **Front-end requests stay bounded.** No `posts_per_page => -1` or unbounded `get_posts()` on the front end; large or rarely used options are saved with autoload off; expensive results are cached in transients with an expiry. *Why:* every autoloaded option loads on every page view.
- **Background work survives a retry.** Scheduled work runs through Action Scheduler (with WooCommerce) or WP-Cron, in batches, and a handler that runs twice changes nothing. *Why:* WP-Cron runs on page loads and can fire the same event twice.

### Next.js (App Router, TypeScript)

`eslint-config-next` and the TypeScript compiler cover the framework's own conventions. A call that is known to break in the installed version is banned with ESLint's `no-restricted-syntax` instead of a rule, such as `router.refresh()` after a server action, which a Next 16 production build can drop and leave the router stuck.

Leave out **Freshness is explicit** only when nothing opts into caching (`cacheComponents`, `'use cache'`, `unstable_cache`, `fetch` with `force-cache` or `revalidate`, a segment `revalidate`, `force-static`, `generateStaticParams`) and every route that reads data renders per request, because it reads cookies, headers or `searchParams` or is `force-dynamic`. Without Cache Components, a route with none of these is prerendered at build and served stale.

- **Server code stays on the server.** Database access, secrets and SDK clients live in modules that `import 'server-only'`, except modules that a separately bundled runtime imports, such as a Trigger.dev worker built without the `react-server` condition, where `server-only` throws; there, the rule is that no `'use client'` file imports them, directly or through another module. No secret goes in a `NEXT_PUBLIC_` variable; a client component receives only the fields it renders, and `'use client'` goes on the smallest leaf that needs it. *Why:* props passed to a client component are sent to the browser, secrets included.
- **Every server action and route handler is a public endpoint.** It parses its arguments, form data, `searchParams` and cookies with the project's schema library or its own named parsers, whichever the code already uses, then checks the session and that the user owns the object, trusting nothing from the page that calls it. *Why:* anyone can call a server action directly with any arguments.
- **Freshness is explicit.** Every data read states how fresh it must be (`cache`, `revalidate`, `dynamic` or `'use cache'` with tags, as the installed version supports), and every write revalidates the paths or tags it changes. Check the version's defaults in the docs. *Why:* defaults changed between versions, and a stale page shows an old price after an edit.
- **Independent reads start together.** A server component or action that needs several independent reads starts them at once (`Promise.all`, or separate components under `Suspense`), not one `await` after another. *Why:* each sequential `await` adds a full round trip to the page load.
- **Logic lives in plain modules, with tests.** Rules about what is counted, filtered or stored are plain TypeScript functions with unit tests; components render and call them. *Why:* logic inside a component is tested only through the UI, if at all.
