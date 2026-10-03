---
name: merge-manager
description: Coordinate independent acceptance review, verify current PR merge readiness and merge only under explicit applicable authorization.
---

# Merge Manager

Read the [shared contract](../../references/contract.md) before using this workflow.

Verify the intended PR, current head/base, every commit, scope and recorded contract.
Require an independent code-review sign-off on that exact head before requesting a
separate independent E2E reviewer. Use [reviewer instructions](../../references/reviewers.md).
Give requirements and evidence without prescribing a verdict. E2E must exercise actual
success and failure workflows, inspect attached UI images and report missing capabilities.

Main triages findings and supplies fixes/replies; it never approves its own work. Any new
code requires renewed code review before E2E. Every later commit invalidates prior head
sign-offs; documentation-only commits can use proportional documentary revalidation.
Unresolved disagreements and absent evidence remain visible blockers. An acceptance-only
request follows the same gates; prior completion or a cached base/ref is not sufficient.

After both distinct reviewers sign off the final SHA, independently verify current checks,
conflicts, review evidence, release notes and screenshot freshness. Change the GitHub PR
from draft to ready and verify `isDraft=false` before reporting readiness. If blocked,
report the actual draft state and reason. Use the approved GitHub interface; never bypass
branch protection or represent relayed comments as formal GitHub approvals.

Merge only when the user has authorized this concrete merge (or a clearly bounded
applicable set), and recheck head/base/checks immediately before it. Use the expected head
SHA guard when supported. Changed targets require reevaluation; do not force a merge.
Record the actual result. Deployment and final human acceptance remain separate actions.
Main alone records milestone completion once its criteria are satisfied; reviewers report
assessments. Then close-milestone can perform separately authorized housekeeping.
