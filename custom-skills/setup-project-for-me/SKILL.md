---
name: setup-project-for-me
description: Initialize a long-running project for AI collaboration and project memory. Use when a user wants a /init-like setup for a project workspace, with owner-first README structure, AGENTS.md, inputs and deliverables indexes, docs for decisions/knowledge/work/current state, AI handoff conventions, and lightweight static project scanning. Do not use for ordinary code scaffolding, dependency installation, git initialization, CI/CD setup, deployment, or automatic external sync.
---

# Setup Project For Me

Use this skill to help a non-technical project owner collaborate with AI over many sessions without letting the workspace become an unreadable pile of outputs.

The north star is: keep AI execution powerful, but make every long-lived structure, task, decision, input, deliverable, and handoff readable and easy for a future human or AI to resume.

## Workflow

1. Start with one goal question:
   - "这个项目的长期目标是什么？"
2. Clarify around that goal for at most 3 rounds.
   - If the answer does not reveal the workspace shape, ask whether this folder is the deliverable itself or an AI collaboration workspace that may produce GitHub/Feishu/other deliverables.
   - Stop once you can write a clear long-term goal plus a workspace type.
   - If the user asks for quick mode or no interview, skip this step and use TODO values.
3. Run a lightweight static scan. Do not install dependencies, run tests, initialize git, call network services, deploy, or sync external systems.
4. Run the setup script in dry-run mode first for self-check.
5. Apply the setup unless the user explicitly asked for preview only or the dry-run shows unusually broad changes.
6. Summarize what was created, what was appended, and which TODOs remain.

## Default Structure

The setup creates missing files and appends managed sections without overwriting existing files:

```text
README.md
AGENTS.md
inputs/
  README.md
deliverables/
  README.md
docs/
  README.md
  integrations.md
  knowledge/
    README.md
    glossary.md
  decisions/
    README.md
    0000-template.md
  operations.md
  work/
    README.md
    current.md
    tasks/
      README.md
      0000-template.md
    handoffs/
      README.md
      0000-template.md
      YYYY-MM-DD-initial-project-setup.md
.agents/
  README.md
  briefs/
    README.md
    0000-template.md
```

## Core Concepts

- `README.md` is owner-first by default. In an AI collaboration workspace, it acts as the Workspace README; when the current directory is itself a deliverable repository, the script appends a smaller project-collaboration entry instead of redefining the public deliverable README.
- `AGENTS.md` is the project-specific AI collaboration guide. Keep it Chinese-first and practical.
- `inputs/README.md` indexes user-provided materials and their processing status. Inputs may be stored, linked, summarized, or intentionally not retained.
- `deliverables/README.md` indexes things the project intends to deliver or has delivered. It is not a task list and not an internal docs bucket.
- `docs/README.md` is a document map and placement decision tree.
- `docs/work/current.md` is the short, latest project-state summary. Detailed continuation context belongs in dated handoffs.
- `.agents/` stores AI execution briefs, not the source of project truth.

## Script Usage

Use the bundled script from the skill directory:

```bash
python scripts/setup_project_for_me.py --dry-run --goal "..." --workspace-type "..."
python scripts/setup_project_for_me.py --apply --goal "..." --workspace-type "..."
```

Useful options:

- `--root PATH`: initialize a project other than the current directory.
- `--project-name NAME`: override the detected project name.
- `--date YYYY-MM-DD`: set the date used for initial handoff naming.
- `--quick`: skip goal-specific content and use TODO placeholders.

The script is intentionally standard-library only.

## Safety Rules

- Be idempotent: create missing files, append managed sections only once, and never overwrite existing project files.
- Existing `README.md` and `AGENTS.md` may receive a small managed section, but their existing content must stay intact.
- Do not create ordinary app/code scaffolds.
- Do not install packages, run project commands, initialize git, configure CI/CD, deploy, push, or sync external systems.
- If a newly created long-lived structure or deliverable appears during follow-up work, update the relevant README or index so future agents can understand it.

## Language

Generate project-facing documentation in Chinese by default. Keep file names, paths, commands, package names, and technical identifiers in their original language.
