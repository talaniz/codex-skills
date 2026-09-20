---
name: test-driven-development
description: Use red-green-refactor cycles when implementing or changing executable behavior or fixing bugs. Also invoked as tdd. Apply repository-specific test and evidence requirements; do not invent failing tests for documentation-only changes.
---

# Test-driven development

Use small, observable red–green–refactor cycles within the authorized change scope.
The `tdd` skill is an alias for this workflow.

## Establish the contract

Read applicable repository instructions and identify the behavior, acceptance criteria,
relevant failure cases, and existing test commands. Use the project's test framework
and fixtures. Run the relevant baseline when available so existing failures are not
misattributed to the change. Define the next small behavioral increment before coding.

## Red

Write a focused test that expresses the intended observable behavior before changing
production code for that increment. For a bug, reproduce it with a regression test.
Run the test and inspect the actual failure; record the command, exit status and
failing assertion or diagnostic, and explain why it demonstrates missing behavior.

An unrelated import/syntax error, unavailable dependency, missing credentials or
broken environment is not red evidence. Fix the test setup or report the blocker.
If the test already passes, investigate whether the behavior exists or the test misses
the requirement; do not force a failure or change production code just to obtain red.
Do not proceed with dependent implementation until meaningful red is established.

## Green

Implement the smallest in-scope change that satisfies the behavioral contract.
Run the same test to prove it now passes, then the relevant regression checks.
Do not weaken assertions, skip tests, or over-mock the behavior to manufacture green.
Use deterministic fixtures and mock external boundaries where appropriate, while
retaining required integration or end-to-end checks for behavior they alone can prove.

## Refactor

With tests passing, assess whether the new code or tests need clearer structure or
less duplication. Make only justified, behavior-preserving improvements; refactoring
is an assessment step, not a requirement to create extra changes. Re-run affected
tests after refactoring. New behavior starts another red cycle rather than entering
as an untested refactor. If no refactor is needed, record that briefly.

## Completion and evidence

Repeat for the remaining acceptance criteria and relevant failure cases. Run required
repository checks against the final implementation and report actual results and gaps.
Retain concise red, green and post-refactor evidence in the repository's prescribed
log or PR; otherwise include it in the task summary. Never reconstruct unobserved red
results or claim that skipped checks passed. If required verification is blocked,
report the concrete blocker and do not call that increment complete.

For a pure behavior-preserving refactor, establish passing characterization coverage
first, refactor, and rerun it; do not deliberately break working behavior to fake red.
For documentation-only or other changes without executable behavior, use appropriate
structural/manual checks and state why red–green does not apply. Preserve existing
user changes; do not delete or revert implementation merely to stage a test-first story.

Follow the repository's commit and review workflow. Red–green–refactor cycles do not
require separate commits, replace independent reviews, or authorize commits, pushes,
merges or deployments beyond the surrounding task's authorization.
