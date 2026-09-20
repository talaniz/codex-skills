---
name: commit-push
description: Review and commit the current task's changes, then push the intended branch to its remote. Also invoked through the cppr alias. Use for commit-and-push requests, not branch preparation alone.
---

# Commit and Push

`cppr` is an alias for this workflow. Invocation authorizes creating the scoped commit and pushing it; use standing session authorization and repository instructions without redundant confirmation. Enforced execution controls still apply.

1. Identify the repository, current branch, remote destination and applicable AGENTS.md. Inspect staged, unstaged and untracked changes, and existing unpushed commits. Follow the current task's scope; do not sweep unrelated user work into the commit or publish unrelated history. Do not switch branches as a side effect. If HEAD is detached or the destination is ambiguous, resolve it from context or ask for the missing detail before publication.
2. Review the actual diff and run the checks required for these changes, reusing still-valid results from the current task. Resolve in-scope failures; disclose unavailable checks. Do not call unrun checks passed or bypass commit/push hooks. Check for credentials and private runtime artifacts without printing their contents.
3. Stage only the intended paths or hunks and inspect the complete staged diff before committing. Preserve unrelated staged work; do not commit it accidentally. If safely isolating mixed work is not possible, stop and identify the scope conflict. Choose a concise message describing the change, with any repository-required trailers. Preserve required commit boundaries; do not amend or rewrite published commits unless explicitly requested.
4. Create the commit. If no scoped changes remain, do not create an empty commit; push already-authorized pending commits if needed, or report that everything is already committed and pushed. A failed commit stops publication of the intended change.
5. Push with an explicit remote and branch destination so Git defaults cannot send work to the wrong branch. For a first push, establish the matching upstream (for example, git push -u origin HEAD:refs/heads/BRANCH). Prefer the verified existing destination when intentional. Do not push directly to main when the task/repository requires a feature-branch PR. Never force-push or bypass protection. On non-fast-forward rejection, fetch and inspect the difference; reconcile only within the task's authorization, then rerun affected checks, or report the blocker rather than retrying blindly.
6. Verify the remote branch points to the intended commit, and report the commit SHA, destination, check results and any remaining local changes. If the commit succeeds but push fails, distinguish those outcomes and leave the local commit intact.

This skill does not add PR creation, merging or deployment to the request. Continue any PR/review work already required by the surrounding task and repository workflow. Calling the alias does not change this scope.
