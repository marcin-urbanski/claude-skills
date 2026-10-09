# Review checklist

Used for self-review after each task and by the reviewer subagent. Every finding needs a `file:line`.

## Reuse and duplication
- Does the change re-implement something that already exists in the codebase or its dependencies (helper, service, component, validator, query, API client, config)? Search for it; do not guess.
- Is there now more than one way to do the same thing? The old one must be reused, extended or removed, not left beside a new copy.
- Does it follow the patterns already used in the project (structure, naming, error handling, how tests are written)?

## Security
- **Input**: all untrusted input (request data, query params, headers, files, webhooks, third-party API responses) is validated on the server.
- **Injection**: no string-built SQL, shell commands, file paths or HTML. Use the framework's query builder / bound parameters, escaping and path handling.
- **Output**: user content is escaped for its context (HTML, attribute, JS, URL). No raw output helpers on user data.
- **Authorisation**: every new route, action, job and API endpoint checks who may do it (policy, gate, capability, middleware). Object-level checks: a user cannot read or change another user's records by changing an ID.
- **CSRF / nonces** on state-changing requests where the framework expects them.
- **Secrets**: none in code, tests, fixtures, logs or commits. Read from env/config. `.env` values never printed.
- **No hidden behaviour**: no backdoors, debug routes, hardcoded users or passwords, bypass flags, "temporary" admin checks, disabled TLS verification, `eval`/dynamic code execution, obfuscated code, or unexplained outbound network calls.
- **Dependencies**: any new package is well known, maintained and necessary; its name is spelled correctly (typosquatting); the lock file is updated.
- **Data**: sensitive data (passwords, tokens, personal data) is hashed/encrypted as appropriate, not logged, not exposed in API responses or errors.
- **Uploads and files**: type and size checked, stored outside the web root or with safe names, never executed.
- **Mass assignment**: only intended fields are fillable.
- **Errors**: no stack traces or internals shown to users; failures are not silently swallowed.

## Scope and simplicity
- Every changed line traces back to the task. No reformatting, "improvements" or refactors of unrelated code.
- No speculative code: features, options, abstractions or error handling that nothing asked for. Could it be noticeably shorter?
- Imports, variables and functions made unused by this change are removed; pre-existing dead code is only reported.

## Best practices
- Uses the framework's built-in way before custom code (validation, auth, queues, caching, migrations).
- Clear names; small functions; no dead code, commented-out code or leftover debug output.
- Migrations are reversible and safe for existing data.
- No N+1 queries or unbounded loops over large data sets introduced.
- Error handling is explicit and consistent with the rest of the project.

## Tests and spec
- Each acceptance criterion is covered by a test, or the gap is named.
- Tests assert real behaviour, not mocks; they would fail if the feature broke. Name the production change that would make each new test fail. Tests that lie:
  - **Tautological**: restates the implementation (`expect(MAX)->toBe(30)`), so it breaks on a rename and passes when the behaviour breaks.
  - **Structural**: checks how the code is written (file contents, element order in source, private methods) instead of what it does through its public interface.
  - **Cannot fail**: mocks the very thing under test, or so much around it that no real failure path is left.
- Nothing was built that the spec did not ask for.

## Code smells (judgement calls)
Report each as "possible <smell>" with the hunk, never as a hard violation; a project standard that endorses the pattern wins.
- **Feature envy**: a method that works mostly with another object's data; move it there.
- **Data clumps / primitive obsession**: the same fields travel together, or a string or number stands in for a domain concept; give it a type.
- **Repeated switches**: the same `switch` or `if` cascade on the same type in several places.
- **Shotgun surgery**: one logical change scattered across many files; gather what changes together.
- **Middle man**: a class or function that only passes calls on.
