# Codex workflow skills

Reusable skills for preparing branches, committing and pushing scoped changes, and
test-driven development.

| Skill | Purpose |
| --- | --- |
| [branch-prep](skills/branch-prep/SKILL.md) | Update local main from remote main and create a fresh branch. |
| [commit-push](skills/commit-push/SKILL.md) | Review, commit and push the current task's scoped changes. |
| [cppr](skills/cppr/SKILL.md) | Alias for commit-push; does not imply opening a PR. |
| [test-driven-development](skills/test-driven-development/SKILL.md) | Follow observed red–green–refactor cycles with verification evidence. |
| [tdd](skills/tdd/SKILL.md) | Alias for test-driven-development. |

To install, copy the desired directories from `skills/` into your Codex skills
directory (`$CODEX_HOME/skills`, or `~/.codex/skills` when unset). Inspect existing
directories before replacing them. Install `cppr` alongside `commit-push`, and `tdd`
alongside `test-driven-development`, because aliases load their sibling skills.

Invoke them by name, such as `$branch-prep`, `$cppr`, or `$tdd`. They follow the
surrounding task's scope and repository instructions. These are agent instructions,
not Git hooks or mechanical enforcement of the development workflow.

This repository contains copies of the skill files; cloning it does not update
already-installed copies automatically.

## Spec Driven Development bundle

The self-contained [Spec Driven Development plugin](plugins/spec-driven-development/README.md)
adds seven coordinated skills: ideate, build-author, pre-dev-prep, tdd, pr-author,
merge-manager and close-milestone. It reconstructs the behavior visible in supplied
photographs; it is not the original source. Existing standalone skills remain unchanged.
See the bundle README for usage, local validation, archive safety and installation limits.
