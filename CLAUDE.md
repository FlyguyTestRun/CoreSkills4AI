# Claude AI – Global Operating Contract

This file defines mandatory behavioral rules for Claude Code in this repository.
It is a contract, not documentation.

Claude MUST follow these rules in all sessions.

---

## 1. Core Operating Rules (Non-Negotiable)

1. **THINK** – Read only what is necessary before acting
2. **PLAN** – Produce a written plan before any execution
3. **APPROVAL** – Wait for explicit user approval before building
4. **EXECUTE** – Implement incrementally; no large jumps
5. **SIMPLICITY** – Minimal, direct changes only
6. **REVIEW** – Security and correctness checks are mandatory
7. **DOCUMENT** – Outcomes and lessons must be recorded

**Never skip planning. Never infer approval.**

---

## 2. Mode-Based Execution System

Claude operates in explicit modes.
Modes control autonomy, scope, and memory loading.

| Mode   | Purpose            | Autonomy | Commits | Agent File |
|--------|-------------------|----------|---------|------------|
| SCOPE  | Requirements & plan | Low      | None    | `.claude/agents/agent.scope.md` |
| BUILD  | Implementation     | High     | Every step | `.claude/agents/agent.build.md` |
| SECURE | Security review    | Medium   | After fixes | `.claude/agents/agent.secure.md` |
| TEST   | Automated testing  | High     | After suite | `.claude/agents/agent.test.md` |
| FIX    | Debugging          | Medium   | Per fix | `.claude/agents/agent.fix.md` |
| DEPLOY | Production actions | Low      | After validation | `.claude/agents/agent.deploy.md` |

**Mode Activation:**
- Auto-detect from context, then ask for approval OR
- Obey explicit instruction: `"Enter [MODE] mode"`

**When a mode is activated, load its agent file ONLY.**
Agent files contain mode-specific instructions.

---

## 3. Planning & Approval Gate

Before BUILD, TEST, FIX, or DEPLOY:

- A written plan MUST exist
- The plan MUST be approved by the user
- No files may be modified before approval

Planning artifacts use the format defined in:
`.claude/procedures/task_format.md`

---

## 4. Incremental Commit Discipline

- Every successful step requires a commit
- Commits must be small, reversible, and scoped
- No secrets or credentials may ever be committed

Commit rules are defined in:
`.claude/procedures/commit_policy.md`

---

## 5. Security Is Mandatory

Before declaring work "complete":

- Perform a security review
- Validate inputs, auth boundaries, and secret handling

Security criteria are defined in:
`.claude/procedures/security_checklist.md`

---

## 6. Token & Context Discipline

Claude must actively minimize context usage:

- Do not reread files unnecessarily
- Do not load procedural files unless required
- Prefer diffs and summaries over full file reads
- Avoid verbose explanations unless explicitly requested
- **Use `/clear` after completing ANY feature**

**Context Clearing:**
```
/clear
```

**When to clear:**
- ✅ Feature complete + committed
- ✅ Before unrelated work
- ✅ When switching projects
- ❌ During active development

This repository prioritizes **precision over verbosity**.

---

## 7. Explicit Prohibitions

Claude MUST NOT:

- Add features not explicitly requested
- Over-engineer solutions
- Execute untrusted code without approval
- Make breaking changes without discussion
- Modify memory or rules implicitly
- Commit secrets or credentials

---

## 8. Learning & Memory Hygiene

Important lessons, constraints, or discoveries:
- MUST be appended to `.claude/logs/lessons.md`
- MUST NOT bloat this root file

Lessons are referenced, not auto-loaded.

---

## 9. Project Structure

### Directories

- **`.claude/agents/`** - Mode-specific instruction agents (load on demand)
- **`.claude/procedures/`** - Reusable procedures (reference when needed)
- **`.claude/logs/`** - Append-only learning log
- **`.claude/tooling/`** - Optional tool integrations

### Projects

- **`projects/`** - Git-enabled, auto-commits happen here
- **`agent-system/`** - Reference implementation (do not modify)
- **`shared/`** - Templates, configs, utilities

---

## 10. Authority Hierarchy

If a conflict exists:

1. **User instruction wins**
2. **This file wins over all others**
3. **Mode agent instructions override procedures**
4. **Procedures override tooling notes**

---

## 11. Environment Constraints

**Required:**
- Python 3.12.x
- Windows 10 + WSL2
- Docker

**Principles:**
- Simplicity | Security | Clarity | Solo project

---

**END OF CONTRACT**

*For mode-specific instructions, see `.claude/agents/`*
*For procedures and checklists, see `.claude/procedures/`*
