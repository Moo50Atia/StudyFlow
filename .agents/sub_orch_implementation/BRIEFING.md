# BRIEFING — 2026-07-12T12:15:00+03:00

## Mission
Expand the Funding Intelligence Database to 150+ high-quality verified entities with strict schema compliance and E2E verification.

## 🔒 My Identity
- Archetype: Sub-Orchestrator
- Roles: orchestrator, user_liaison, human_reporter, successor
- Working directory: d:\projects\laravel_projects\college_project\.agents\sub_orch_implementation
- Original parent: parent orchestrator
- Original parent conversation ID: 4633414d-a806-4057-8b1f-51ecc6b03c03

## 🔒 My Workflow
- **Pattern**: Project
- **Scope document**: d:\projects\laravel_projects\college_project\.agents\sub_orch_implementation\SCOPE.md
1. **Decompose**: We follow the 4 milestones defined in SCOPE.md:
   - Milestone 1: Data Collection (Egypt & MENA)
   - Milestone 2: Data Collection (Global)
   - Milestone 3: JSON Merging & QA
   - Milestone 4: Final Verification
2. **Dispatch & Execute**:
   - **Direct (iteration loop)**: For each milestone, we spawn Explorer/Worker/Reviewer agents to perform data collection, validation, and JSON generation.
3. **On failure** (in this order):
   - Retry: nudge stuck agent or re-send task
   - Replace: spawn fresh agent with partial progress
   - Skip: proceed without (only if non-critical)
   - Redistribute: split stuck agent's remaining work
   - Redesign: re-partition decomposition
   - Escalate: report to parent (sub-orchestrators only, last resort)
4. **Succession**: Self-succeed at 16 spawns, write handoff.md, spawn successor.
- **Work items**:
  1. Data Collection (Egypt & MENA) [pending]
  2. Data Collection (Global) [pending]
  3. JSON Merging & QA [pending]
  4. Final Verification [pending]
- **Current phase**: 1
- **Current focus**: Milestone 1: Data Collection (Egypt & MENA)

## 🔒 Key Constraints
- Build a database of at least 150+ high-quality verified entities.
- Follow schemas exactly (Government vs Standard).
- Egypt and MENA priority, then Europe and North America.
- No placeholder values, fake emails, or dummy websites.
- Ensure E2E tests pass via `python verify_funding_db.py` when `TEST_READY.md` is available.
- Never reuse a subagent after it has delivered its handoff — always spawn fresh.

## Current Parent
- Conversation ID: 4633414d-a806-4057-8b1f-51ecc6b03c03
- Updated: not yet

## Key Decisions Made
- Initial plan: Run search tasks in parallel for M1 and M2, then combine, merge duplicates, and run verification.

## Team Roster
| Agent | Type | Work Item | Status | Conv ID |
|-------|------|-----------|--------|---------|
| worker_m1 | teamwork_preview_worker | Data Collection (Egypt & MENA) | completed | 3911bccc-0ee8-4cf2-b0b0-5d5eaeb52cab |
| worker_m2 | teamwork_preview_worker | Data Collection (Global) | completed | ae22199f-9f8d-4907-bc2d-9fe9e96eeec3 |
| worker_m3 | teamwork_preview_worker | JSON Merging & QA | failed | 5e2e1196-f9d8-4b6b-841a-775fb7adfcec |
| worker_m3_gen2 | teamwork_preview_worker | JSON Merging & QA Gen 2 | in-progress | 41836dff-c8fa-4204-ad0f-e64c4a924605 |

## Succession Status
- Succession required: no
- Spawn count: 4 / 16
- Pending subagents: 41836dff-c8fa-4204-ad0f-e64c4a924605
- Predecessor: none
- Successor: not yet spawned

## Active Timers
- Heartbeat cron: ba3f0004-7f51-4d22-ae7e-d5d0f55f64aa/task-15
- Safety timer: none
- On succession: kill all timers before spawning successor
- On context truncation: run `manage_task(Action="list")` — re-create if missing

## Artifact Index
- d:\projects\laravel_projects\college_project\.agents\sub_orch_implementation\progress.md — heartbeat and checkpoint file
- d:\projects\laravel_projects\college_project\.agents\sub_orch_implementation\ORIGINAL_REQUEST.md — user request record
