# Tasks: Interactive Visual Scenes Refactor (CS-Bridge)

**Input**: Design documents from `specs/001-interactive-visual-scenes/`

**Prerequisites**: plan.md (required), spec.md (required)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- All paths are relative to the repository root.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project directory setup and initial resources

- [X] T001 Create Results output folder at Interactive-Seens-Material/D.Mahde/Results/
- [X] T002 Configure local CDN offline cache references or fallbacks in Interactive-Seens-Material/D.Mahde/Results/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core JavaScript boilerplate architecture for Three.js control and memory management

- [X] T003 Design dynamic tabbed switching UI and narrative controller layout in Interactive-Seens-Material/D.Mahde/Results/
- [X] T004 Implement strict WebGL memory cleanup loops (geometry, material, texture disposals) to prevent memory leaks during layer switches in Interactive-Seens-Material/D.Mahde/Results/

---

## Phase 3: User Story 1 - Dynamic Visual Simulation of OOP Concepts (Priority: P1) 🎯 MVP

**Goal**: Generate 39 independent visual scene HTML files containing C++ code contexts, outcomes, controls, and dynamic memory state flows.

**Independent Test**: Double-click any of the 39 generated HTML files in a browser, trigger the controls, and verify they load and run at 60 FPS.

- [X] T005 [P] [US1] Build self-contained HTML scene for Lec1_Sec1 in Interactive-Seens-Material/D.Mahde/Results/Lec1_Sec1.html
- [X] T006 [P] [US1] Build self-contained HTML scene for Lec1_Sec2 in Interactive-Seens-Material/D.Mahde/Results/Lec1_Sec2.html
- [X] T007 [P] [US1] Build self-contained HTML scene for Lec2_Sec1 in Interactive-Seens-Material/D.Mahde/Results/Lec2_Sec1.html
- [X] T008 [P] [US1] Build self-contained HTML scene for Lec2_Sec2 in Interactive-Seens-Material/D.Mahde/Results/Lec2_Sec2.html
- [X] T009 [P] [US1] Build self-contained HTML scene for Lec2_Sec3 in Interactive-Seens-Material/D.Mahde/Results/Lec2_Sec3.html
- [X] T010 [P] [US1] Build self-contained HTML scene for Lec3_Sec1 in Interactive-Seens-Material/D.Mahde/Results/Lec3_Sec1.html
- [X] T011 [P] [US1] Build self-contained HTML scene for Lec3_Sec2 in Interactive-Seens-Material/D.Mahde/Results/Lec3_Sec2.html
- [X] T012 [P] [US1] Build self-contained HTML scene for Lec3_Sec3 in Interactive-Seens-Material/D.Mahde/Results/Lec3_Sec3.html
- [X] T013 [P] [US1] Build self-contained HTML scene for Lec4_Sec1 in Interactive-Seens-Material/D.Mahde/Results/Lec4_Sec1.html
- [X] T014 [P] [US1] Build self-contained HTML scene for Lec4_Sec2 in Interactive-Seens-Material/D.Mahde/Results/Lec4_Sec2.html
- [X] T015 [P] [US1] Build self-contained HTML scene for Lec5_Sec1 in Interactive-Seens-Material/D.Mahde/Results/Lec5_Sec1.html
- [X] T016 [P] [US1] Build self-contained HTML scene for Lec5_Sec2 in Interactive-Seens-Material/D.Mahde/Results/Lec5_Sec2.html
- [X] T017 [P] [US1] Build self-contained HTML scene for Lec6_Sec1 in Interactive-Seens-Material/D.Mahde/Results/Lec6_Sec1.html
- [X] T018 [P] [US1] Build self-contained HTML scene for Lec6_Sec2 in Interactive-Seens-Material/D.Mahde/Results/Lec6_Sec2.html
- [X] T019 [P] [US1] Build self-contained HTML scene for Lec6_Sec3 in Interactive-Seens-Material/D.Mahde/Results/Lec6_Sec3.html
- [X] T020 [P] [US1] Build self-contained HTML scene for Lec7_Sec1 in Interactive-Seens-Material/D.Mahde/Results/Lec7_Sec1.html
- [X] T021 [P] [US1] Build self-contained HTML scene for Lec7_Sec2 in Interactive-Seens-Material/D.Mahde/Results/Lec7_Sec2.html
- [X] T022 [P] [US1] Build self-contained HTML scene for Lec7_Sec3 in Interactive-Seens-Material/D.Mahde/Results/Lec7_Sec3.html
- [X] T023 [P] [US1] Build self-contained HTML scene for Lec8_Sec1 in Interactive-Seens-Material/D.Mahde/Results/Lec8_Sec1.html
- [X] T024 [P] [US1] Build self-contained HTML scene for Lec8_Sec2 in Interactive-Seens-Material/D.Mahde/Results/Lec8_Sec2.html
- [X] T025 [P] [US1] Build self-contained HTML scene for Lec8_Sec3 in Interactive-Seens-Material/D.Mahde/Results/Lec8_Sec3.html
- [X] T026 [P] [US1] Build self-contained HTML scene for Lec8_Sec4 in Interactive-Seens-Material/D.Mahde/Results/Lec8_Sec4.html
- [X] T027 [P] [US1] Build self-contained HTML scene for Lec9_Sec1 in Interactive-Seens-Material/D.Mahde/Results/Lec9_Sec1.html
- [X] T028 [P] [US1] Build self-contained HTML scene for Lec9_Sec2 in Interactive-Seens-Material/D.Mahde/Results/Lec9_Sec2.html
- [X] T029 [P] [US1] Build self-contained HTML scene for Lec10_Sec1 in Interactive-Seens-Material/D.Mahde/Results/Lec10_Sec1.html
- [X] T030 [P] [US1] Build self-contained HTML scene for Lec10_Sec2 in Interactive-Seens-Material/D.Mahde/Results/Lec10_Sec2.html
- [X] T031 [P] [US1] Build self-contained HTML scene for Lec11_Sec1 in Interactive-Seens-Material/D.Mahde/Results/Lec11_Sec1.html
- [X] T032 [P] [US1] Build self-contained HTML scene for Lec11_Sec2 in Interactive-Seens-Material/D.Mahde/Results/Lec11_Sec2.html
- [X] T033 [P] [US1] Build self-contained HTML scene for Lec12_Sec1 in Interactive-Seens-Material/D.Mahde/Results/Lec12_Sec1.html
- [X] T034 [P] [US1] Build self-contained HTML scene for Lec12_Sec2 in Interactive-Seens-Material/D.Mahde/Results/Lec12_Sec2.html
- [X] T035 [P] [US1] Build self-contained HTML scene for Lec13_Sec1 in Interactive-Seens-Material/D.Mahde/Results/Lec13_Sec1.html
- [X] T036 [P] [US1] Build self-contained HTML scene for Lec13_Sec2 in Interactive-Seens-Material/D.Mahde/Results/Lec13_Sec2.html
- [X] T037 [P] [US1] Build self-contained HTML scene for Lec13_Sec3 in Interactive-Seens-Material/D.Mahde/Results/Lec13_Sec3.html
- [X] T038 [P] [US1] Build self-contained HTML scene for Lec15_Sec1 in Interactive-Seens-Material/D.Mahde/Results/Lec15_Sec1.html
- [X] T039 [P] [US1] Build self-contained HTML scene for Lec15_Sec2 in Interactive-Seens-Material/D.Mahde/Results/Lec15_Sec2.html
- [X] T040 [P] [US1] Build self-contained HTML scene for Lec15_Sec3 in Interactive-Seens-Material/D.Mahde/Results/Lec15_Sec3.html
- [X] T041 [P] [US1] Build self-contained HTML scene for Lec15_Sec4 in Interactive-Seens-Material/D.Mahde/Results/Lec15_Sec4.html
- [X] T042 [P] [US1] Build self-contained HTML scene for Lec15_Sec5 in Interactive-Seens-Material/D.Mahde/Results/Lec15_Sec5.html
- [X] T043 [P] [US1] Build self-contained HTML scene for Lec15_Sec6 in Interactive-Seens-Material/D.Mahde/Results/Lec15_Sec6.html

**Checkpoint**: User Story 1 (39 basic visualizations) is testable and complete.

---

## Phase 4: User Story 2 - Dynamic Architectural Layer Switching (Priority: P1)

**Goal**: Implement the 4 dynamic animation loops (RAM, CPU, GPU, Corrector) for each of the 39 scenes.

**Independent Test**: Select any tab (e.g. RAM, GPU, CPU) in a scene browser window, and verify the active visual loop matches that target system layer.

- [X] T044 [US2] Implement RAM Topology 3D animation loop (animating Stack/Heap boundaries and operations) across all files in Interactive-Seens-Material/D.Mahde/Results/
- [X] T045 [US2] Implement CPU & Execution Flow loop (animating Instruction Pointer and Bus routes) across all files in Interactive-Seens-Material/D.Mahde/Results/
- [X] T046 [US2] Implement GPU & VRAM render loop (animating shader core packets and frame buffers) across all files in Interactive-Seens-Material/D.Mahde/Results/
- [X] T047 [US2] Implement Under-the-Hood Corrector visual overlays across all files in Interactive-Seens-Material/D.Mahde/Results/

**Checkpoint**: User Story 2 is testable and complete.

---

## Phase 5: User Story 3 - LaTeX Equation & Offset Rendering (Priority: P2)

**Goal**: Integrate client-side KaTeX rendering for math and address offset formulas inside description cards and deconstruction grids.

**Independent Test**: Verify that the formulas are properly rendered without syntax warnings on load.

- [X] T048 [P] [US3] Integrate KaTeX automatic renderer onto narrative text cards and deconstruction paragraphs across all files under Interactive-Seens-Material/D.Mahde/Results/
- [X] T049 [P] [US3] Format all mathematical equations using LaTeX delimiters inside description structures under Interactive-Seens-Material/D.Mahde/Results/

**Checkpoint**: All mathematical equations render cleanly.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Optimization and final validations

- [X] T050 [P] Verify responsive layout parameters for mobile, tablet, and desktop viewports in Interactive-Seens-Material/D.Mahde/Results/
- [X] T051 Run full walkthrough and verification against quickstart.md guidelines in Interactive-Seens-Material/D.Mahde/Results/

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Phase 1 completion.
- **User Story 1 (Phase 3)**: Depends on Phase 2 completion. Individual scenes can be developed in parallel.
- **User Story 2 (Phase 4)**: Depends on Phase 3 completion.
- **User Story 3 (Phase 5)**: Depends on Phase 3/4 completion.
- **Polish (Phase N)**: Depends on all stories being complete.

### Parallel Opportunities
- All 39 HTML file creation tasks (`T005` to `T043`) in Phase 3 can run in parallel.
- KaTeX integration and equation formatting tasks (`T048`, `T049`) can run in parallel once HTML files are established.

---

## Parallel Example: User Story 1
```bash
# Developers A, B, and C can create separate HTML files simultaneously:
Task: "Build self-contained HTML scene for Lec1_Sec1 in Interactive-Seens-Material/D.Mahde/Results/Lec1_Sec1.html"
Task: "Build self-contained HTML scene for Lec1_Sec2 in Interactive-Seens-Material/D.Mahde/Results/Lec1_Sec2.html"
Task: "Build self-contained HTML scene for Lec2_Sec1 in Interactive-Seens-Material/D.Mahde/Results/Lec2_Sec1.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1 (Setup) and Phase 2 (Boilerplate framework).
2. Complete Phase 3 (39 HTML scene files creation).
3. Validate each page loads basic layouts, narrative, and C++ code contexts properly.

### Incremental Delivery
1. Set up basic scenes (US1).
2. Add dynamic Three.js rendering loops for RAM, CPU, GPU, and Corrector tabs (US2).
3. Apply KaTeX typesetting parser on all text boxes (US3).
4. Run final layout polish.
