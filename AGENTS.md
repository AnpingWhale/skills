# Repository Agent Guidance

## Agent skills

### Issue tracker

Issues and PRDs are tracked as local markdown files under `.scratch/<feature-slug>/`. External PRs are not a triage surface for this local tracker. See `docs/agents/issue-tracker.md`.

### Triage labels

The repo uses the default mattpocock/skills triage labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Domain documentation uses a multi-context layout: root `CONTEXT-MAP.md` points to context-specific `CONTEXT.md` files when present, with ADRs at `docs/adr/` and context-level ADRs where relevant. See `docs/agents/domain.md`.
