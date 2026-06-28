# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Layout

This repo uses a multi-context domain documentation convention.

- `CONTEXT-MAP.md` at the repo root points to each context-specific `CONTEXT.md` file when those docs exist.
- `docs/adr/` contains system-wide architectural decisions.
- Context-specific ADRs may live beside each context, commonly under `src/<context>/docs/adr/` or another path listed in `CONTEXT-MAP.md`.

If any of these files do not exist yet, proceed silently. Do not flag their absence or create them upfront. The `/domain-modeling` skill, reached through `/grill-with-docs` and `/improve-codebase-architecture`, should create or extend them when terms or decisions are actually resolved.

## Before exploring, read these

- Read `CONTEXT-MAP.md` first if it exists.
- Read the `CONTEXT.md` files relevant to the task or context named by the user.
- Read ADRs in `docs/adr/` that touch the area being changed.
- In context-specific work, also check the context's own ADR directory if one is listed or discoverable.

## Expected structure

```text
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/
│       └── 0001-example-system-decision.md
└── src/
    └── example-context/
        ├── CONTEXT.md
        └── docs/
            └── adr/
                └── 0001-example-context-decision.md
```

## Use the glossary's vocabulary

When your output names a domain concept in an issue title, refactor proposal, hypothesis, or test name, use the term as defined in the relevant `CONTEXT.md`. Do not drift to synonyms the glossary explicitly avoids.

If the concept you need is not in the glossary yet, treat that as a signal: either the language is being invented and should be reconsidered, or there is a real gap to note for `/domain-modeling`.

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> Contradicts ADR-0007 (example decision) -- but worth reopening because...
