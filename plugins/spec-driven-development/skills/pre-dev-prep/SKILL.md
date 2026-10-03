---
name: pre-dev-prep
description: Check repository state and prepare or reuse the recorded branch and worktree without disturbing existing work. Use before a planned implementation phase.
---

# Pre Dev Prep

Read the [shared contract](../../references/contract.md) before using this workflow.

Read the specification, phase and context record. Inventory with
`python3 <plugin-root>/scripts/inspect_branch.py --repo <repository-root>`.
This helper is read-only; its output does not prove worktree ownership or remote freshness.
Inspect dirty files and worktrees, identify who owns them, and retain unrelated changes.
Do not silently stash, reset, discard or reuse another task's branch.

For continuing milestone work, verify the recorded worktree, branch and scope and reuse
them. Do not fetch/rebase/switch just to start the next phase. For a new standalone branch,
fetch the intended remote main, compare histories and fast-forward local main only in a
clean, unused checkout. Divergence needs a scoped resolution, never a reset. Create a
new non-tracking branch from that exact main and record starting SHA and worktree path.

Verify dependencies and the agreed commands in the actual environment. Separate missing
credentials/environment from product failures. Confirm the acceptance route: full build,
review of completed implementation, or documentation-only work. An acceptance-only
route still requires independent evidence and current merge gates; it cannot bypass them.
Update context with ownership, branch/base, authorization, tests and next action.
