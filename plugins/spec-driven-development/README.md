# Spec Driven Development

Seven Codex skills for turning a specification into a bounded, independently reviewed
outcome. This version 0.1.0 is reconstructed from the owner's four photographs of a README
and skill summary, not copied from the original source. Original helper internals, schemas
and historical tests were unavailable; this bundle defines and tests its own conservative
archive format. No original-source or original-author endorsement is claimed.

## First prompt

Start a fresh task in the target repository:

> Use $ideate from the spec-driven-development plugin to plan the smallest useful outcome
> for my idea. Keep this planning-only; identify runtime, scope, acceptance scenarios and
> whether this is a standalone build or named milestone.

Without installation, provide the actual local path to `skills/ideate/SKILL.md`. Reading a
skill by path can test its instructions but does not prove plugin installation/discovery.
All entrypoints link bundled resources by relative path.

| Skill | Use |
| --- | --- |
| [ideate](skills/ideate/SKILL.md) | Focus the product specification and acceptance scenarios. |
| [build-author](skills/build-author/SKILL.md) | Define phases, risks, context, verification and reviewers. |
| [pre-dev-prep](skills/pre-dev-prep/SKILL.md) | Prepare or reuse the recorded branch and worktree. |
| [tdd](skills/tdd/SKILL.md) | Observed red, green, refactor and independent staff review. |
| [pr-author](skills/pr-author/SKILL.md) | Create/update the authorized draft PR with evidence. |
| [merge-manager](skills/merge-manager/SKILL.md) | Independent acceptance and current merge gates. |
| [close-milestone](skills/close-milestone/SKILL.md) | Archive only after main records completion. |

`tdd` is this plugin's complete short entrypoint, not a runtime alias. It does not replace
the repository's pre-existing standalone `tdd` alias. Select this plugin explicitly when
both are installed. Seven skills do not require seven confirmations: covered milestone
phases reuse recorded authority and branch. Merge, deployment and final human acceptance
remain distinct gates.

## Prerequisites and use

Python 3.11+ and Git are needed for helpers; no Python packages or network are required.
Real independent agents are needed for the specified reviews. Templates inherit runtime
policy and do not register agents. Pass the supplied role instructions to independent
agents if named roles are unavailable, preserving any explicitly required reviewer model.
See the [shared contract](references/contract.md) and [archive format](references/archive.md).

The repository includes a marketplace entry. Publication does not install or activate the
plugin or alter global configuration. To install, use the target runtime's supported plugin
interface to add this GitHub repository as a marketplace and select Spec Driven Development.
Verify the chosen revision and loaded skill entrypoints in a fresh task. This release's
validation does not claim that installation or a complete real-project adoption trial passed.

## Helpers and verification

From this plugin directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_package.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 scripts/inspect_branch.py --repo /path/to/project
python3 scripts/close_milestone.py --repo /path/to/project
# After inspecting the preview and confirming applicable archival authority:
python3 scripts/close_milestone.py --repo /path/to/project --apply EXACT_DIGEST --reason "Authority reference"
```

From repository root, `python3 scripts/check_spec_driven.py` runs the same validation/tests.
Tests use temporary real Git repositories and synthetic review evidence. They do not
contact GitHub, merge a real PR or prove live agent behavior. Independent workflow reviews
and their limits are recorded in the repository's verification document and PR.

Helpers use local files/Git and add no hosted service, background timer, model endpoint,
authentication store or credentials. The hosting runtime has its own inference/data handling.
GitHub publication uses only the user's approved interface and scoped destination. Keep
secrets and private images out of records and publications. Archival is preview-first with
best-effort rollback on caught errors; it is not crash-safe or concurrent-writer safe.

For community distribution, copy the complete plugin directory, adapt repository metadata,
register it using that repository's marketplace conventions and retain the validation/test
command. Follow its license, review and publication requirements. Avoid divergent copies.
