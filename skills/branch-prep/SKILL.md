---
name: branch-prep
description: Update local main from remote main and create a new branch for the next set of changes. Use when preparing a fresh development branch.
---

# Branch Prep

Prepare the intended repository for new work, following its AGENTS.md and the current task's scope. Invocation authorizes this preparation; honor existing session authorization without asking again.

1. Identify the repository, intended remote (normally origin), current branch, working-tree/index state, and linked worktrees. Infer the new branch name from the task and repository conventions unless supplied; ask only when the repository or intended work cannot be determined.
2. Preserve existing work. Do not stash, discard, reset, or carry unrelated changes into the new branch. If local changes obstruct preparation, use an appropriate isolated worktree when context supports it; otherwise explain the concrete blocker. Never overwrite an existing branch or disrupt a worktree used by another active task.
3. Fetch the remote's main branch and verify the fetch succeeded. Compare local main with the freshly fetched remote main. Fast-forward local main only. If main is absent locally, create it from remote main; if absent remotely, report that rather than silently substituting another base. If local main is ahead or diverged, report the commits and stop before creating the new branch unless the user already specified how to handle them. Never reset away local commits or push main to make the comparison pass.
4. Update main in a clean checkout. If main is checked out in another worktree, inspect that worktree before updating it; a locked, dirty, or actively used worktree is a blocker to changing it. Creating a branch directly from remote main does not by itself satisfy the requirement to update local main.
5. Confirm local main equals the fetched remote main, then create and check out the new branch from that exact commit. Use a new branch, not a reused name; if the user supplied an existing name, clarify or follow an already agreed continuation. Set the new branch not to track remote main (for example, git switch --no-track -c BRANCH main); its matching remote branch can be established on push.
6. Verify the checked-out branch, starting SHA and working-tree state. Report the repository/worktree, new branch and base SHA, plus any blocker. Preparation alone does not commit or push changes.
