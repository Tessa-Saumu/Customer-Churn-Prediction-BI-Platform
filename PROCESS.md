
Project Process & Collaboration

This document describes how the team worked during the sprint: Git workflow, pull request conventions, definition of done, and the review process. It was split out of README.md during the final documentation pass (Issue #18) so the README could stay focused on running and understanding the project, with process/collaboration detail kept here instead.

## Git Workflow

**No direct pushes to `main`. Ever.** Every change — no matter how small — follows this sequence:

```
Issue → Branch → Development → Pull Request → Code Review → Final Review (Michael) → Merge
```

### Branch naming

Use the format `<your-name>/<short-description>`, all lowercase, words separated by hyphens:

```bash
git checkout -b mercy/etl-schema
git checkout -b praise/fastapi-scaffold
```

### Making changes

```bash
# Make sure main is up to date before branching
git checkout main
git pull origin main

# Create your branch
git checkout -b <your-name>/<short-description>

# ... make your changes ...

# Stage and commit
git add <files>
git commit -m "type: short description of what changed"

# Push your branch
git push origin <your-name>/<short-description>
```

### Commit message convention

Prefix commits with a type, followed by a short, present-tense description:

- `feat:` — a new feature (e.g. `feat: add customer repository layer`)
- `fix:` — a bug fix
- `chore:` — setup, tooling, or non-feature changes
- `docs:` — documentation-only changes
- `test:` — adding or updating tests

### Opening a Pull Request

1. Push your branch to GitHub.
2. Open a Pull Request targeting `main`.
3. Use the [PR template](#pull-request-template) below — copy it in full, don't skip sections.
4. Link the PR to its issue using `Closes #<issue-number>` in the "Related Issue" section.
5. Request review.
6. Once your PR is open, post a completion comment on the linked issue:

   ```markdown
   PR opened to address this issue: #<PR-number>.
   <Short summary of what was completed — 1 sentence>
   All changes have been implemented and verified locally.
   ```

**If what you actually built differs at all from the issue's original scope** — a renamed function, a different library, an extra endpoint you thought was needed — call this out explicitly under "Notes" in the PR description and flag it for confirmation. Do not silently ship a deviation, even one you believe is an improvement.

---

## Pull Request Template

Copy this in full into every PR description:

```markdown
## Summary
Briefly describe what this PR does and why it exists.
(1–2 sentences, outcome-focused)

## Scope
What is included in this PR:
- 
- 
- 

## Implementation Details
Key technical work completed:
- 
- 
- 

## Validation / Testing
How you verified this works:
- 
- 
- 

## Configuration / Setup Changes (if applicable)
- Environment variables:
- New dependencies:
- Migrations / schema updates:

## Notes
Anything reviewers should be aware of:
- 
- 

## Related Issue
Closes #<issue-number>

## How to Run (if relevant)
Steps to reproduce or run locally:
​```bash
# example
python -m scripts.init_db
​```
```

---


## Definition of Done

A task is complete only if:

- Code works
- Tests added
- Type hints included (Python's `typing` module / built-in generics — no untyped function signatures)
- Logging included (`logging` module — no `print()` statements)
- Documentation updated
- PR approved by Theresia (first-pass review)
- Signed off by Michael (final review — required on **every** PR before merge)
- Merged into `main`

---


## Review Process

Every PR follows a two-step gate:

1. **First-pass review** — Theresia reviews for correctness, adherence to the Definition of Done, and scope alignment.
2. **Final sign-off** — Michael reviews and signs off on **every individual PR** before it can merge. This is a hard, per-PR gate, not a milestone-level check.

Given the compressed timeline, keep PRs small and scoped to a single issue — this keeps both review passes fast.

---
## Sprint Board (Click on the Projects Tab)

GitHub Projects board with these columns, in order:

**Backlog → To Do → In Progress → In Review → Changes Requested → Final Review (Michael) → Done**

- **Backlog:** everything identified as needed for the project, including work not yet unblocked.
- **To Do:** the subset of Backlog that's unblocked and ready to be picked up right now.
- **In Review:** open PR, awaiting Theresia's pass.
- **Changes Requested:** sent back after review; move back to In Review once addressed.
- **Final Review (Michael):** passed first review, awaiting Michael's sign-off.
- **Done:** merged into `main`.

---

## Milestones

The sprint is tracked against GitHub milestones M0 through M7, each covering a distinct phase of the project (Sprint Kickoff, Data Foundation, API Scaffold, Model Training, Real Integration, Dashboard, Docs/Testing/Presentation, and optional Stretch Goals respectively). See README.md's "Milestones" section for what each one covers.

## Notes on This Document

This document reflects how the team actually worked during the sprint, consolidated from the project brief and the working conventions established across Issues #1–#19. It is not a new set of rules — it's a written-down version of practices that were already in effect throughout the sprint, moved here from the README during the final documentation and integration pass (Issues #18/#20) to keep the README itself focused on running and understanding the project rather than on internal process.