---
name: close-milestone
description: Preview and archive explicitly completed milestone records, preserving active directories and supported Markdown links after main records completion.
---

# Close Milestone

Read the [shared contract](../../references/contract.md) before using this workflow.

Read the [archive contract](../../references/archive.md) and the actual completion
record. Confirm main has recorded completion, required evidence is available and current,
and archival is authorized by this task or existing bounded authority. Product completion,
archival, and publication of housekeeping are separate events. Never infer completion from
an agent's last message, a merged PR alone, or the helper's digest.

Preview with `python3 <plugin-root>/scripts/close_milestone.py --repo <repository-root>`.
Inspect every move and link edit, ownership and repository quietness. The helper refuses
unsupported or ambiguous cases; adapt the scoped records with review rather than bypass
guards. It does not supply authorization, validate remote reviews, or merge anything.

When authorized, apply with the exact returned digest and a recorded reason:
`python3 <plugin-root>/scripts/close_milestone.py --repo <repository-root> --apply <digest> --reason <authorization-reference>`.
A stale preview requires a new preview and inspection. Check the resulting diff, links,
record status and preservation of active directories. Caught failures trigger best-effort
rollback; process crashes and concurrent writers are not transactionally protected.

Publish the housekeeping diff only under applicable commit/push/PR authority and the
repository's review requirements. Verify the outcome; do not install skills or modify
global configuration as a side effect of closing a milestone.
