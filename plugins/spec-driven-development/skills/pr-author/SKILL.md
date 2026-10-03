---
name: pr-author
description: Create or update the authorized draft pull request with final scope, acceptance criteria and actual verification evidence.
---

# Pr Author

Read the [shared contract](../../references/contract.md) before using this workflow.

Inspect the intended remote, branch, full diff and commit history. Follow existing
commit/push authority and repository conventions. Stage only this task's changes and
never publish secrets, private screenshots or unrelated staged work. A PR request does
not grant direct-to-main pushes, forced history changes, merge or deployment authority.

Use one existing milestone PR where recorded. Lead with the concrete problem and
resulting behavior, then acceptance, verification commands/results, failure cases and
limitations. Rewrite descriptions when scope changes instead of appending obsolete plans.
Record red/green evidence and distinguish implementation checks from independent reviews.

For UI work attach inspected desktop/mobile images of the actual branch, with revision,
viewport/state and reproducible steps, before review. For non-UI work state why screenshots
are not applicable. Use the approved GitHub connector or authenticated CLI; preserve
newlines through structured arguments or body files. Verify returned URL, head and draft
state. If publication fails, retain local work and report the exact boundary.

Keep the PR draft until merge-manager has both final-head sign-offs, passing required
checks and completed release evidence. Publishing or marking ready never implies merge.
