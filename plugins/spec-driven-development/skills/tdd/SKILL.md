---
name: tdd
description: Implement one coherent authorized phase through observed failing tests, working code, refactoring and independent staff review.
---

# Tdd

Read the [shared contract](../../references/contract.md) before using this workflow.

This is the bundle's complete test-driven-development entrypoint, not an alias or a
second skill dependency. Read the phase and context before touching implementation.

Write a test of the next observable behavior, run it and retain command, exit and
assertion evidence. Missing modules, syntax errors and broken environments are not useful
red results. For new helpers, start from an executable minimal interface and demonstrate
its missing behavior. Do not deliberately break completed code to manufacture history.

Implement the smallest in-scope fix. Run the same test to green, then relevant regressions.
Assess whether a behavior-preserving refactor improves clarity; do not invent one.
Document any limitations honestly. Pure documentation uses structural/workflow checks,
not artificial failing application tests. Repeat for remaining acceptance criteria.

Record evidence with the change and keep the main agent responsible for fixes and scope.
Prepare/update the draft PR using pr-author so reviewers have a durable target, then
request an independent staff/code review of every new commit and combined diff. Use
[reviewer instructions](../../references/reviewers.md); a missing independent agent is a
review gap, not permission for self-sign-off. Triage findings, fix valid ones, publish
evidence and obtain updated code sign-off. E2E follows code sign-off via merge-manager.

For UI changes, capture and inspect actual-branch synthetic desktop/mobile screenshots
and affected states before review. Attach durable links to the PR, refresh after UI fixes,
and retain current drafts/conversations during interaction tests. Follow repository sizes.
Update context and phase records with results and next action; do not merge or deploy.
