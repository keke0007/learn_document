---
type: knowledge
scope: transferable
status: stable
tags: [agent-skills, codex, claude-code, cursor, npx-skills, sop]
source: ai-discussion
---

# Agent Skills Management SOP

## Purpose

This SOP defines a reusable mechanism for managing agent skills across multiple AI tools without copying the same skill files into multiple runtime directories.

It is meant for both humans and agents to duplicate the mechanism in a new repository or workstation setup.

## Core Design

The pattern has four parts:

1. one canonical source-of-truth directory
2. one exposed install surface for global skills
3. one exposed install surface for project skills
4. one installer and mapping layer, preferably `npx skills`

The key idea is simple:

- author and maintain skills in one place
- expose stable install paths
- let agent runtimes consume those paths through symlinks or an installer
- never manually duplicate skill files into each agent tool

## Shared Core vs Agent-Specific Config

Use this split:

- `SKILL.md`
  - portable, shared skill definition
- `agents/`
  - product-specific config only when one agent needs behavior that the shared `SKILL.md` cannot express cleanly

This keeps the common skill logic in one place while allowing small per-agent adapters.

Example:

```text
my-skill/
├── SKILL.md
└── agents/
    └── openai.yaml
```

## Recommended Directory Model

```text
Agent-Skills/
├── global/
│   ├── coding/
│   │   ├── <skill-name>/
│   │   └── <vendor-or-pack> -> ../forks/<vendor-or-pack>/skills
│   └── local/
├── projects/
│   └── <project>/
└── forks/
    └── <upstream-repo>/
```

Directory roles:

- `global/<category>/<skill-name>/`
  - reusable global skills organized by category
- `global/<category>/<vendor-or-pack>/`
  - exposed install surface for upstream or shared skill bundles within a category
- `global/local/`
  - optional holding area only when a real category is not ready yet
- `projects/<project>/`
  - project-scoped skills that should not become global by default
- `forks/<upstream-repo>/`
  - third-party upstream repositories, usually kept as standalone git clones

## Core Rules

1. Keep exactly one writable source of truth.
2. Use stable install paths. Do not make agents depend on raw temporary paths.
3. Prefer symlink-based installs. Use copy mode only when symlinks are unsupported or broken in a specific environment.
4. Keep project-specific skills separate from global skills.
5. Put third-party upstream sources in a dedicated fork layer instead of mixing them into local authored skills.
6. Install from exposed paths like `global/...` or `projects/...`, not directly from `forks/...`.
7. Keep the shared skill body in `SKILL.md`; add agent-specific config files only when behavior diverges across tools.
8. Organize the global layer by category once the number of skills starts growing.
9. When a new global skill is created, wire it into the shared global runtime path as part of the same change, not as a follow-up task.

## Why `npx skills`

`npx skills` is a good default because it gives you:

- a common install workflow across multiple agent tools
- global and project-scoped install options
- path-based installs for local skill sources
- a cleaner maintenance path than manually linking each runtime directory yourself

This reduces hand-written symlink logic and makes the mechanism easier to reproduce on another machine or in another repo.

## Manual-Only Skills Across Agents

The “manual-only” toggle is not fully standardized across tools.

Recommended pattern:

- shared `SKILL.md`
  - use `disable-model-invocation: true` for Claude Code and Cursor
- Codex-specific `agents/openai.yaml`
  - use:

```yaml
policy:
  allow_implicit_invocation: false
```

This keeps one shared skill body while isolating Codex-specific invocation policy to `agents/openai.yaml`.

Minimal example:

```yaml
# SKILL.md
---
name: my-skill
description: Run only when the user explicitly asks for it.
disable-model-invocation: true
---
```

```yaml
# agents/openai.yaml
policy:
  allow_implicit_invocation: false
```

Use `agents/openai.yaml` only when the Codex behavior must differ or requires an explicit OpenAI-specific policy.

When migrating legacy slash commands into skills, keep the body content unchanged on the first migration pass. Only add the minimum frontmatter and agent-specific config needed for invocation behavior.
Once the command is truly promoted into a normal reusable skill, prefer placing it in the appropriate global category instead of keeping it inside a tool-branded deep subdirectory.

## Standard Workflows

### 1. Install reusable global skills

Install from your local global skill surface:

```bash
npx skills add /path/to/Agent-Skills/global/local -g
```

Install an upstream-exposed global pack:

```bash
npx skills add /path/to/Agent-Skills/global/<vendor-or-pack> -g
```

Target specific agents when needed:

```bash
npx skills add /path/to/Agent-Skills/global/<vendor-or-pack> -g -a codex -a claude-code -a cursor
```

### 2. Install project-scoped skills

Run the install from the target project root:

```bash
cd /path/to/project
npx skills add /path/to/Agent-Skills/projects/<project> -a codex -a claude-code -a cursor
```

This keeps project mappings attached to the project instead of leaking them into the user-global layer.

### 3. Inspect or search skills

List installed skills:

```bash
npx skills list
```

Preview a source before installing:

```bash
npx skills add /path/to/Agent-Skills/global/<vendor-or-pack> --list
```

Search the broader ecosystem:

```bash
npx skills find
npx skills find test
```

### 4. Remove installed mappings

```bash
npx skills remove
```

Use this to clean old mappings or remove bad installs.

## Adding A New Personal Global Skill

1. Create the skill under the right category in `global/` when you already know the category.
2. Use `global/local/` only when the skill still needs a temporary holding area.
3. Add `SKILL.md` and any needed `references/`, `scripts/`, or `assets/`.
4. If Codex needs extra behavior or policy, add `agents/openai.yaml`.
5. Keep the skill self-contained.
6. Map it into the shared global runtime path immediately.
7. Install or refresh the runtime mapping in the same task, for example:

```bash
npx skills add /path/to/Agent-Skills/global/coding/<skill-name> -g
```

If you are managing the runtime path by direct symlink instead of the installer, create or refresh the `~/.agents/skills/<skill-name>` mapping in the same change.

## Migrating Legacy Slash Commands Into Skills

1. Back up the original command files outside the canonical skill repo.
2. Create one skill per command.
3. Preserve the original command body content exactly on the first migration.
4. Add only the minimal wrapper:
   - `SKILL.md` frontmatter
   - `disable-model-invocation: true` when the old command was explicit/manual
   - `agents/openai.yaml` only if Codex needs explicit manual-only policy
5. Place promoted skills in the appropriate global category unless a real namespace collision requires a special grouping layer.
6. Prefer one runtime path per skill name. If the promoted command becomes a shared global skill, map it into one shared runtime layer such as `~/.agents/skills/` instead of duplicating it across per-agent global directories.

## Adding A New Project Skill

1. Create the skill under `projects/<project>/`.
2. Keep project-only assumptions there.
3. Install it from the project root:

```bash
cd /path/to/project
npx skills add /path/to/Agent-Skills/projects/<project> -a codex -a claude-code -a cursor
```

4. If the skill becomes reusable across projects, extract the reusable part into `global/local/`.

## Adding A New Upstream Skill Source

1. Add the upstream repository under `forks/`, usually as a standalone `git clone`.
2. Expose its usable install surface under the right category in `global/` or under `projects/` with a symlink.
3. Document:
   - upstream repository URL
   - tracked branch if applicable
   - update command
   - clean re-clone command if you want a stateless refresh path
   - exposed install path
4. Install from the exposed path, not directly from the raw fork checkout.

Example:

```text
forks/example-pack/
global/example-pack -> ../forks/example-pack/skills
```

## Update Workflow

When a skill source changes:

1. update the source-of-truth content first
2. if the source is third-party, update the upstream checkout in `forks/`
3. if the skill uses agent-specific config such as `agents/openai.yaml`, update that config alongside the shared `SKILL.md`
4. re-run `npx skills add ...` against the same exposed path if agent mappings need refresh
5. keep the path stable whenever possible

When the third-party source is a normal branch-tracking clone, a periodic update can be as simple as:

```bash
git -C /path/to/Agent-Skills/forks/<upstream-repo> pull --ff-only
```

If you prefer a stateless refresh workflow, re-clone instead of pulling:

```bash
rm -rf /path/to/Agent-Skills/forks/<upstream-repo>
git clone --branch <branch> <repo-url> /path/to/Agent-Skills/forks/<upstream-repo>
```

## Verification Checklist

After any structural change, verify:

1. the canonical source directory still contains the expected skill files
2. exposed paths under `global/` or `projects/` resolve correctly
3. `npx skills add ... --list` sees the expected bundle
4. agent installs work without copied duplicates
5. there is still only one writable source of truth
6. the installer's claimed target locations match the real runtime directories
7. no agent can see the same skill name from two different global locations
8. if a skill is meant to be manual-only, its shared and agent-specific invocation flags are aligned

## Anti-Patterns

Avoid these:

- manually copying one skill into multiple runtime directories
- editing installed runtime copies and forgetting the real source
- installing directly from the raw `forks/` layer
- mixing local authored skills and third-party upstream content in the same writable directory
- using copy mode by default
- creating multiple canonical skill repositories on the same machine
- trusting installer output without inspecting the real runtime mapping
- exposing one skill name through multiple global runtime directories for the same agent
- treating parent-repo git tracking and third-party fork tracking as the same problem

## Adaptation Checklist

When duplicating this mechanism into a new repo or machine:

1. choose the canonical `Agent-Skills/` location
2. create `global/`, `projects/`, and `forks/`
3. migrate personal reusable skills into `global/local/`
4. add upstream packs into `forks/`
5. expose upstream packs through stable symlinked paths in `global/` or `projects/`
6. install with `npx skills`
7. document the local instantiation in the nearest `AGENTS.md` and `README.md`
