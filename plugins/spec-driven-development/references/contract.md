# Shared workflow contract

Use repository instructions and the user's actual scope. These seven entrypoints share
one context record; they are not seven human approval interruptions. An explicit bounded
milestone authorization covers the recorded implementation phases and reviews. Reuse it
until scope, target, risk or required authority changes. Explain the concrete uncovered
action when asking for authority. Plan-only means no implementation.

Record repository, specification, phase route, milestone, branch/worktree ownership,
base/head observations, PR, verification, reviewers, authorized actions and their source,
remaining decisions and resumption point in the project's existing convention. The
[context template](../templates/context.md) is a starting point, not a second ledger.
Standalone independently deliverable phases may use separate branches. Covered milestone
phases keep their recorded branch/worktree/PR unless the owner changes that plan.

Main owns implementation, scope decisions, finding triage and completion. Real distinct
independent agents assess code and subsequent E2E acceptance. Each posts its exact reviewed
SHA, actual checks, findings or sign-off. If posting is unavailable, main may relay the
report verbatim with attribution under applicable authority. Missing reviewers, explicitly
required models, credentials, environments or evidence block readiness. A model assessment
is not human acceptance or a branch-protection override. Reviewer templates inherit
runtime/model policy; they do not install or register roles.

All new commits need both reviewers' final-head revalidation. Code changes go through code
review before E2E. UI changes require actual-branch desktop/mobile images using synthetic
content, relevant interaction states, visual inspection and durable PR links before review.
The E2E reviewer must inspect the images and exercise the workflows. Notes-only changes may
use documentary revalidation. Report non-UI screenshot evidence as not applicable.

Create/update the draft PR using actual implementation and evidence. Mark it non-draft only
after reviews, required checks and release evidence pass; verify remote state before saying
ready. Merge, production deployment and final human acceptance remain separate gates. Use
existing explicit authority where applicable; a skill name never grants missing authority.

Helpers are local filesystem/Git tools, not hosted services or background agents. They have
no model endpoint, credentials, telemetry or GitHub client. The hosting Codex runtime has
its own inference/data handling. GitHub publication uses only the user's approved interface
and scoped destination. No helper fabricates approval or proves the truth of supplied
review records; the caller verifies source evidence and authority.
