---
name: build-author
description: Break an agreed specification into coherent build phases, verification contracts and reviewer assignments. Use to prepare a standalone build or named milestone.
---

# Build Author

Read the [shared contract](../../references/contract.md) before using this workflow.

Read the agreed specification, repository instructions and existing execution records.
Assess complexity, dependencies and concrete risks. Create phases that each deliver a
verifiable user outcome; avoid phases that merely scatter layers across separate PRs.
Use [phase](../../templates/phase.md), [context](../../templates/context.md) and
[review](../../templates/review.md) templates. Record commands, fixtures, expected red,
success/failure scenarios, UI evidence and reviewer capability requirements before work.

A bounded milestone uses one recorded branch/worktree and PR across covered phases.
Standalone independently deliverable phases may each have one recorded branch/PR.
Reuse existing authorization for covered phases and reviews; explain actual scope changes
before requesting new authority. Record what is authorized and the source of that authority.

Separate main implementation duties from independent code and E2E reviewers. Default
reviewers inherit runtime/model policy. Preserve explicitly required reviewer models;
if unavailable, report the gap. Bundled [reviewer instructions](../../references/reviewers.md)
can be passed verbatim to real independent agents when named roles are unavailable.
Templates do not register agents or supply missing review capability.

Record a resumption point and next phase. Do not begin implementation from a plan-only request.
