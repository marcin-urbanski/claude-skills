---
name: playbook-<slug>
description: <When to use it, in the words the request or the symptom arrives in, for example "The client asks for the monthly sales export" or "The nightly import fails with Lock wait timeout". One or two sentences, no angle brackets.>
---

# <Title>

Kind: recurring task | known failure
Risk: read-only | changes data | production
Owner: <who knows this best>
Last verified: <YYYY-MM-DD>

## When

<Who asks or what breaks, how often, and how it shows up.>

<!-- A recurring task has Steps. A known failure has Symptom, Cause and Fix instead. -->

## Steps

1. <What to do and why, in one line.>
   ```bash
   <command, or a pointer to the file that holds the query>
   ```
2. **changes data** <A step that writes, deletes or migrates is marked like this.>

## Symptom

<What the user, the client or the logs show. Exact error text where there is one.>

## Cause

<Why it happens.>

## Fix

1. <Steps, as under Steps.>

## Verify

<How to tell it worked: a command and what a good result looks like, described without real data.>

## Pitfalls

- <What went wrong before, and what not to do.>
