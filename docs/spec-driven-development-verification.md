# Reconstruction verification

The four photos provided a README and skill summaries, not source files. The new bundle
implements those visible behaviors; its schema/helpers are original reconstruction choices.
No photos, private screen content, installed skills or global settings were published.

Before implementation, the acceptance contract was committed and published in draft
[PR1](https://github.com/talaniz/codex-skills/pull/1). Existing standalone skills are unchanged.
The bundle uses stdlib Python 3.11+ for local helpers and a repo-local marketplace entry.
It is not installed on this Pi by this change.

## Observed test-first evidence

- Initial executable preview interface produced an empty move plan. Running
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s plugins/spec-driven-development/tests -p test_workflow.py -k test_preview_and_apply -v`
  failed with `0 != 2`, exit1, before archive implementation. After implementation the same
  behavior passed, including moves, retained active directory and link preservation.
- Added negative cases for affected autolinks, nested link syntax and link code examples.
  Each focused test failed with `ValueError not raised`, exit1, before guard implementation.
  The guards now reject these ambiguous forms rather than silently corrupt references.
- `python3 scripts/check_spec_driven.py`: package metadata/reference/Python checks and
  20 isolated tests passed. Fixtures use real temporary Git repositories, synthetic review
  records and injected caught-write failure. They cover preview/apply, reason, source drift,
  stale digest, dirty/detached repository, review independence/completeness, failed/stale
  evidence, unsafe paths/symlinks, collisions, link forms and rollback.
- Bundled system plugin validator passed; all seven system skill validators passed.
  `git diff --check` passed. No UI changes; screenshot evidence is not applicable.

## Limits and review

Helpers cannot verify remote evidence truth or ownership. They never contact GitHub, merge,
deploy or supply authorization. Archival supports a conservative documented Markdown subset
and requires an explicit completion-record format; caught-error rollback is best effort,
not crash-safe or safe against concurrent writers. A complete live project/adoption trial,
plugin installation/discovery and real GitHub merging are not claimed by fixture tests.

Independent code review and subsequent distinct workflow E2E/forward-testing reports will
be attached to PR1 with exact reviewed SHAs. They are required before readiness.

## Independent code review corrections

[First code review](https://github.com/talaniz/codex-skills/pull/1#issuecomment-5974249326)
found two valid P2 gaps: unsupported relative references inside moved records could point
at retained siblings and silently break, and an ignored untracked completion record was
accepted. Both require fail-closed behavior before filesystem mutation.

Before fixes, focused `-k moved_reference` and `-k ignored_completion` fixture tests each
failed with `ValueError not raised` (exit1). The record must now be tracked by Git; relative
reference/HTML/autolinks in moved documents are rejected whether or not their target moves.
Additional HTML/autolink-to-retained-sibling cases exercise the shared condition. The full
master check passes 23 tests plus package/reference/syntax validation. Original records and
existing standalone skills remain untouched. Re-review is required on the fix head.

The [second review](https://github.com/talaniz/codex-skills/pull/1#issuecomment-5974293148)
identified valid HTML attribute forms bypassing the guard. The focused
`-k html_attribute_variants` test failed in 11 subcases before the fix (exit1), covering
whitespace, case, unquoted values and character references, both in moved records and
in retained files linking to moved records. Stdlib `HTMLParser` now extracts normalized
`href`/`src` attributes before the existing affected-link guard. All 24 tests and package
checks pass; every rejected preview leaves the fixture repository unchanged.

## Completed independent verification

On implementation revision `a80928e1485342f042b996d66e986cad1421f6ee`:

- [Independent code sign-off](https://github.com/talaniz/codex-skills/pull/1#issuecomment-5974314082)
  confirms all findings addressed, 24 passing tests, package validation, whitespace and
  independent HTML regression probes.
- [Distinct E2E and instruction forward-test sign-off](https://github.com/talaniz/codex-skills/pull/1#issuecomment-5974359882)
  records actual CLI preview/apply, link preservation, declared-file-only movement,
  retained active directory, and seven refusal cases without content changes. The reviewer
  also produced and inspected planning artifacts, resumed a bounded milestone fixture with
  unrelated dirty work, and evaluated a merge-readiness fixture with incomplete reviews
  and no merge authority. The linked report contains self-contained evidence and limits.

These are isolated synthetic workflow trials, not plugin installation/discovery or a full
live project adoption trial. Final documentation-only revisions require both reviewers'
documentary revalidation on the PR before its draft-to-ready transition.
