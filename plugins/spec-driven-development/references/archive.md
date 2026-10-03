# Archive format and limits

The helper reads a tracked `harness/milestone.json` at the Git repository root. Existing
projects using another format need an explicit scoped adaptation; never silently migrate
or replace their workflow. Files must be tracked `.md`, `.json` or `.txt` records beneath
`harness/active/<id>/`. Only declared files move to matching `harness/archive/<id>/` paths.
Active directories and undeclared files remain. No executable implementation is archived.

Main records completion after verifying actual source evidence. Commit all product and
milestone evidence first and obtain both independent reviews on that implementation SHA.
Then commit **only** `harness/milestone.json` to record completion; any other difference
from the reviewed head is rejected. That completion/housekeeping commit still follows
applicable PR review rules. The helper's current HEAD and full preview digest must match
at apply; the reviewed SHA must be an ancestor with no other tree changes. Evidence URLs
and names are assertions to verify, not cryptographic proof or authorization.

Example shape (replace the illustrative values with verified records):

```json
{
  "id": "demo",
  "status": "completed",
  "recorded_by": "main-agent",
  "reviewed_head": "40-lowercase-hex-characters",
  "required_checks": ["acceptance"],
  "checks": [{"name": "acceptance", "status": "passed", "head": "same-reviewed-sha"}],
  "reviews": [
    {"role": "code", "reviewer": "independent-a", "verdict": "sign-off", "head": "same-reviewed-sha", "evidence": "https://example.invalid/code"},
    {"role": "e2e", "reviewer": "independent-b", "verdict": "sign-off", "head": "same-reviewed-sha", "evidence": "https://example.invalid/e2e"}
  ],
  "files": ["harness/active/demo/phase.md", "harness/active/demo/review.md"]
}
```

Preview prints HEAD, moves, edited file paths and digest, without full document contents.
Apply requires the identical digest plus a nonempty reason identifying existing authority.
A clean working tree/index including untracked files and a named branch are required.
Symlinks in selected paths, path traversal, collisions, stale checks/reviews, missing or
non-independent reviewers and uncompleted records fail closed. Apply updates the record
status to archived and records moves, source HEAD, digest and reason. It does not commit.

Simple relative inline Markdown links and images, including percent-encoded paths and
fragments, are rewritten in tracked Markdown files. Relative links inside moved Markdown
are rebased; external URLs and fragment-only links remain. Titles, spaces/escapes in inline
URLs are unsupported. Affected reference-definition and HTML links are rejected. This is
not a complete Markdown parser: nested/escaped link syntax and inline-link examples in
code spans/fences are conservatively rejected across scanned Markdown. Affected autolinks
are also rejected. use the documented simple-link subset for records and
inbound references, and inspect every proposed/resulting diff. Markdown files over 2 MiB
and more than 1,000 selected records are refused.

Use a quiet repository with no concurrent editors or Git processes. The helper attempts
rollback on caught filesystem errors, but is **not crash-safe or protected against
concurrent writers**. It cannot prove ownership, remote evidence truth, network freshness,
permission or final human acceptance. If interrupted, inspect actual files and Git diff
before retrying; do not clear work or automatically reset. Back up important data first
where the repository's operating procedure requires it.
