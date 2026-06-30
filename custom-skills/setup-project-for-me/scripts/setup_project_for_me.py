#!/usr/bin/env python3
"""Initialize an AI-collaboration project memory structure."""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


MARKER_START = "<!-- setup-project-for-me:start -->"
MARKER_END = "<!-- setup-project-for-me:end -->"

IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".DS_Store",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "target",
    ".next",
    ".nuxt",
    ".turbo",
    ".cache",
    "__pycache__",
}


@dataclass
class Action:
    kind: str
    path: Path
    content: str = ""
    note: str = ""


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def template_dir() -> Path:
    return skill_root() / "assets" / "templates"


def read_template(name: str) -> str:
    return (template_dir() / name).read_text(encoding="utf-8")


def render(name: str, context: dict[str, str]) -> str:
    text = read_template(name)
    for key, value in context.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = value.strip("-")
    return value or "project"


def detect_package_manager(root: Path) -> str:
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (root / "yarn.lock").exists():
        return "yarn"
    if (root / "bun.lockb").exists() or (root / "bun.lock").exists():
        return "bun"
    if (root / "package-lock.json").exists():
        return "npm"
    return "npm"


def parse_package_json(root: Path) -> tuple[list[str], list[str]]:
    package_json = root / "package.json"
    if not package_json.exists():
        return [], []
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except Exception:
        return ["发现 package.json，但无法解析。"], []
    if not isinstance(data, dict):
        return ["发现 package.json，但顶层不是对象，无法扫描依赖和脚本。"], []
    stack = ["Node.js / JavaScript"]
    deps = {}
    for key in ("dependencies", "devDependencies"):
        value = data.get(key)
        if isinstance(value, dict):
            deps.update(value)
    framework_hints = {
        "next": "Next.js",
        "react": "React",
        "vue": "Vue",
        "svelte": "Svelte",
        "vite": "Vite",
        "typescript": "TypeScript",
        "astro": "Astro",
        "@nestjs/core": "NestJS",
        "express": "Express",
    }
    for dep, label in framework_hints.items():
        if dep in deps and label not in stack:
            stack.append(label)
    pm = detect_package_manager(root)
    scripts = data.get("scripts") if isinstance(data, dict) else {}
    commands = []
    if isinstance(scripts, dict):
        for name in sorted(scripts):
            commands.append(f"{pm} run {name}")
    return stack, commands


def parse_makefile(root: Path) -> list[str]:
    makefile = root / "Makefile"
    if not makefile.exists():
        return []
    commands = []
    for line in makefile.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = re.match(r"^([A-Za-z0-9_.-]+):(?:\s|$)", line)
        if match and not match.group(1).startswith("."):
            commands.append(f"make {match.group(1)}")
    return commands[:20]


def format_bullets(items: list[str], fallback: str) -> str:
    if not items:
        return fallback
    return "\n".join(f"- {item}" for item in items)


def scan_structure(root: Path, max_depth: int = 2, limit: int = 80) -> list[str]:
    results: list[str] = []
    root = root.resolve()
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        rel_dir = current_path.relative_to(root)
        dir_parts = () if str(rel_dir) == "." else rel_dir.parts

        dirs[:] = sorted(name for name in dirs if name not in IGNORE_DIRS)
        files = sorted(name for name in files if name not in IGNORE_DIRS)
        if len(dir_parts) >= max_depth:
            dirs[:] = []

        entries = [(name, True) for name in dirs] + [(name, False) for name in files]
        for name, is_dir in entries:
            if len(results) >= limit:
                return results
            rel_parts = dir_parts + (name,)
            if len(rel_parts) > max_depth:
                continue
            rel_path = Path(*rel_parts)
            suffix = "/" if is_dir else ""
            results.append(str(rel_path) + suffix)
    return results


def scan_project(root: Path) -> dict[str, list[str]]:
    stack: list[str] = []
    commands: list[str] = []

    package_stack, package_commands = parse_package_json(root)
    stack.extend(package_stack)
    commands.extend(package_commands)

    if (root / "pyproject.toml").exists() or (root / "requirements.txt").exists():
        stack.append("Python")
    if (root / "Cargo.toml").exists():
        stack.append("Rust")
        commands.extend(["cargo build", "cargo test"])
    if (root / "go.mod").exists():
        stack.append("Go")
        commands.extend(["go test ./..."])
    if (root / "Dockerfile").exists():
        stack.append("Docker")
    if (root / ".github" / "workflows").exists():
        stack.append("GitHub Actions")

    commands.extend(parse_makefile(root))
    structure = scan_structure(root)

    return {
        "stack": sorted(dict.fromkeys(stack)),
        "commands": sorted(dict.fromkeys(commands)),
        "structure": structure,
    }


def is_deliverable_workspace(workspace_type: str) -> bool:
    normalized = workspace_type.strip().lower()
    deliverable_hints = (
        "交付物",
        "单一 github",
        "github artifact",
        "artifact 仓库",
        "deliverable",
        "代码仓库",
        "发布仓库",
    )
    return any(hint in normalized for hint in deliverable_hints)


def build_context(args: argparse.Namespace) -> dict[str, str]:
    root = Path(args.root).resolve()
    today = args.date or date.today().isoformat()
    project_name = args.project_name or root.name
    goal = "TODO: 补充项目长期目标。" if args.quick else (args.goal or "TODO: 补充项目长期目标。")
    workspace_type = args.workspace_type or "未确认"
    initial_handoff_path = f"docs/work/handoffs/{today}-initial-project-setup.md"
    scan = scan_project(root)
    stack = format_bullets(scan["stack"], "- TODO: 未扫描到明确技术栈。")
    commands = format_bullets(scan["commands"], "- TODO: 未扫描到明确命令。")
    structure = format_bullets(scan["structure"], "- TODO: 当前目录暂无可概览结构。")
    deliverable_workspace = is_deliverable_workspace(workspace_type)
    readme_template = "deliverable" if deliverable_workspace else "workspace"
    return {
        "PROJECT_NAME": project_name,
        "PROJECT_SLUG": slugify(project_name),
        "TODAY": today,
        "LONG_TERM_GOAL": goal,
        "WORKSPACE_TYPE": workspace_type,
        "INITIAL_HANDOFF_PATH": initial_handoff_path,
        "DETECTED_STACK": stack,
        "DETECTED_COMMANDS": commands,
        "DETECTED_STRUCTURE": structure,
        "MARKER_START": MARKER_START,
        "MARKER_END": MARKER_END,
        "README_TEMPLATE": readme_template,
    }


def create_action(root: Path, rel_path: str, template_name: str, context: dict[str, str]) -> Action:
    path = root / rel_path
    if path.exists():
        return Action("skip", path, note="exists")
    return Action("create", path, render(template_name, context), "missing")


def append_action(root: Path, rel_path: str, template_name: str, context: dict[str, str]) -> Action:
    path = root / rel_path
    content = render(template_name, context)
    if not path.exists():
        return Action("create", path, content, "missing")
    existing = path.read_text(encoding="utf-8", errors="ignore")
    if MARKER_START in existing:
        return Action("skip", path, note="managed block already present")
    return Action("append", path, "\n\n" + content, "append managed block")


def readme_action(root: Path, context: dict[str, str]) -> Action:
    path = root / "README.md"
    template_suffix = "_deliverable" if context.get("README_TEMPLATE") == "deliverable" else ""
    full_template = f"root_readme_full{template_suffix}.md"
    append_template = f"root_readme{template_suffix}.md"
    if not path.exists():
        return Action("create", path, render(full_template, context), "missing")
    existing = path.read_text(encoding="utf-8", errors="ignore")
    if MARKER_START in existing:
        return Action("skip", path, note="managed block already present")
    return Action("append", path, "\n\n" + render(append_template, context), "append managed block")


def planned_actions(root: Path, context: dict[str, str]) -> list[Action]:
    actions: list[Action] = [
        readme_action(root, context),
        append_action(root, "AGENTS.md", "agents.md", context),
        create_action(root, "inputs/README.md", "inputs_readme.md", context),
        create_action(root, "deliverables/README.md", "deliverables_readme.md", context),
        create_action(root, "docs/README.md", "docs_readme.md", context),
        create_action(root, "docs/integrations.md", "integrations.md", context),
        create_action(root, "docs/knowledge/README.md", "knowledge_readme.md", context),
        create_action(root, "docs/knowledge/glossary.md", "glossary.md", context),
        create_action(root, "docs/decisions/README.md", "decisions_readme.md", context),
        create_action(root, "docs/decisions/0000-template.md", "decision_template.md", context),
        create_action(root, "docs/operations.md", "operations.md", context),
        create_action(root, "docs/work/README.md", "work_readme.md", context),
        create_action(root, "docs/work/current.md", "current.md", context),
        create_action(root, "docs/work/tasks/README.md", "tasks_readme.md", context),
        create_action(root, "docs/work/tasks/0000-template.md", "task_template.md", context),
        create_action(root, "docs/work/handoffs/README.md", "handoffs_readme.md", context),
        create_action(root, "docs/work/handoffs/0000-template.md", "handoff_template.md", context),
        create_action(root, context["INITIAL_HANDOFF_PATH"], "initial_handoff.md", context),
        create_action(root, ".agents/README.md", "dot_agents_readme.md", context),
        create_action(root, ".agents/briefs/README.md", "briefs_readme.md", context),
        create_action(root, ".agents/briefs/0000-template.md", "brief_template.md", context),
    ]
    return actions


def apply_actions(actions: list[Action]) -> None:
    for action in actions:
        if action.kind == "skip":
            continue
        action.path.parent.mkdir(parents=True, exist_ok=True)
        if action.kind == "create":
            action.path.write_text(action.content, encoding="utf-8")
        elif action.kind == "append":
            with action.path.open("a", encoding="utf-8") as handle:
                handle.write(action.content)


def print_plan(actions: list[Action], root: Path) -> None:
    for action in actions:
        rel = action.path.relative_to(root)
        print(f"{action.kind.upper():6} {rel} {action.note}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize project memory for AI collaboration.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Preview changes without writing files.")
    mode.add_argument("--apply", action="store_true", help="Write missing files and managed sections.")
    parser.add_argument("--root", default=".", help="Project root to initialize.")
    parser.add_argument("--goal", default="", help="Long-term project goal from the user interview.")
    parser.add_argument("--workspace-type", default="", help="Workspace type, e.g. AI 协作工作区.")
    parser.add_argument("--project-name", default="", help="Project display name.")
    parser.add_argument("--date", default="", help="Date for generated handoff names, YYYY-MM-DD.")
    parser.add_argument("--quick", action="store_true", help="Skip interview-specific content and use TODOs.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        parser.error(f"--root does not exist: {root}")
    if not root.is_dir():
        parser.error(f"--root must be a directory: {root}")

    context = build_context(args)
    actions = planned_actions(root, context)
    print_plan(actions, root)

    if args.apply:
        apply_actions(actions)
        print("\nApplied setup-project-for-me changes.")
    else:
        print("\nDry run only. Re-run with --apply to write changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
