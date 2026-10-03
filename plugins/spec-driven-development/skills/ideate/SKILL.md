---
name: ideate
description: Plan an idea as a focused product specification with scope and acceptance scenarios. Use before implementation or when refining an unclear feature.
---

# Ideate

Read the [shared contract](../../references/contract.md) before using this workflow.

Turn the user's idea into the smallest useful outcome. Default to planning-only unless
implementation is already authorized. Identify the user, problem, deployment/runtime,
constraints, non-goals and observable acceptance scenarios, including relevant failures.
Respect the existing repository stack; for a new backend, consider the user's Python
and database preferences without imposing them on unrelated repositories.

Inspect existing plans before adding a parallel specification. Use the
[specification template](../../templates/specification.md), adapting its size to the task.
State whether this is a standalone build or a named milestone. Surface only decisions
that change scope, security, architecture or acceptance; settle routine choices directly.

Record the chosen outcome and open decisions. Hand the specification to build-author
when phase planning is requested. A specification does not authorize implementation,
merge, deployment or final human acceptance.
