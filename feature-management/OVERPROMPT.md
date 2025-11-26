# SREcodex Feature Management Workflow

**Version**: 1.0.0
**Target Runtime**: OpenAI Codex

---

## How to Use This Document

When you (the agent) are asked to "process features" or "work on the backlog," read this document and execute the phases in order. This is a self-contained workflow — no external tools required beyond standard file operations.

---

## Phase 1: Assess the Backlog

**Goal**: Identify the highest-priority unprocessed item.

**Steps**:
1. Read `features/features.md` to see all tracked items
2. Filter for `status: new` items
3. Sort by priority (P0 > P1 > P2 > P3)
4. Select the top item
5. If no items remain, report "Backlog empty" and stop

**Output**: The feature ID to process (e.g., `FEAT-001`)

---

## Phase 2: Load the Work Item

**Goal**: Understand what needs to be done.

**Steps**:
1. Navigate to `features/FEAT-XXX-slug/`
2. Read `feature_request.json` for metadata
3. Read `PROMPT.md` for implementation instructions
4. If `PLAN.md` or `TASKS.md` exist, read those too

**Output**: Full understanding of the feature scope and acceptance criteria

---

## Phase 3: Update Status to In-Progress

**Goal**: Signal that work has begun.

**Steps**:
1. Edit `feature_request.json`:
   - Set `"status": "in_progress"`
   - Set `"started_date": "YYYY-MM-DD"` (today)
   - Update `"updated_date": "YYYY-MM-DD"` (today)
2. Update `features/features.md` index to reflect new status

**Output**: Status updated, work officially started

---

## Phase 4: Execute Implementation

**Goal**: Complete the work defined in PROMPT.md.

**Steps**:
1. Follow the implementation steps in `PROMPT.md`
2. Check off acceptance criteria as completed
3. If blocked, create a note in `comments.md` and continue to next item
4. Commit changes incrementally with descriptive messages

**Output**: Feature implemented, acceptance criteria met

---

## Phase 5: Validate Completion

**Goal**: Ensure all acceptance criteria are satisfied.

**Steps**:
1. Review all acceptance criteria in `PROMPT.md`
2. Verify each checkbox is legitimately complete
3. If any criteria unmet, return to Phase 4
4. Run any relevant tests or validation scripts

**Output**: Confirmation that feature is complete

---

## Phase 6: Archive and Update Status

**Goal**: Close out the feature.

**Steps**:
1. Edit `feature_request.json`:
   - Set `"status": "resolved"`
   - Set `"completed_date": "YYYY-MM-DD"` (today)
   - Update `"updated_date": "YYYY-MM-DD"` (today)
2. Move the entire feature directory to `completed/`:
   ```
   mv features/FEAT-XXX-slug/ completed/
   ```
3. Update `features/features.md` to remove or mark as completed
4. Log the completion in `UPDATE_LOG.md`

**Output**: Feature archived, indexes updated

---

## Phase 7: Report Summary

**Goal**: Provide visibility into what was accomplished.

**Steps**:
1. Summarize:
   - Feature ID and title
   - What was implemented
   - Any issues encountered
   - Time from started_date to completed_date
2. Output summary to the user

**Output**: Human-readable completion report

---

## Handling Edge Cases

### Blocked Features
If a feature cannot be completed:
1. Document the blocker in `comments.md`
2. Keep status as `in_progress`
3. Add tag `blocked` to feature_request.json
4. Move to next priority item

### Dependencies
If a feature depends on another:
1. Check if dependency is `resolved`
2. If not, skip to next non-blocked item
3. Document skip reason in UPDATE_LOG.md

### Multiple Features
To process multiple features in one session:
1. Complete Phases 1-7 for first feature
2. Return to Phase 1
3. Repeat until backlog empty or session limit reached

---

## Quick Reference

| Phase | Action | Key File |
|-------|--------|----------|
| 1 | Find next item | `features/features.md` |
| 2 | Load details | `FEAT-XXX/PROMPT.md` |
| 3 | Mark in-progress | `FEAT-XXX/feature_request.json` |
| 4 | Do the work | (varies) |
| 5 | Validate | `FEAT-XXX/PROMPT.md` criteria |
| 6 | Archive | Move to `completed/` |
| 7 | Report | Output to user |
