# Tasks: Interactive Visual Scenes Per Prompt

**Input**: Design documents from `/specs/002-interactive-visual-scenes-per-prompt/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/scene-contract.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Exact file paths are provided in the descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and base assets

- [x] T001 Initialize directories and verify environment paths under `Interactive-Seens-Material/TestSkillsApility/scenes/`
- [x] T002 Create design asset baseline and verify CDN availability for Three.js, OrbitControls, and KaTeX

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core JavaScript managers and style layouts. No user stories can begin until the base manager templates are drafted.

- [x] T003 Create base HTML/CSS template containing the CSS variables, layout blocks, and glassmorphism styling in `Interactive-Seens-Material/TestSkillsApility/scenes/template.html`
- [x] T004 Create base Javascript manager classes (`SceneManager`, `CameraManager`, `LightingManager`, `AnimationManager`, `InteractionManager`, `MaterialManager`, `UIBridge`) in `Interactive-Seens-Material/TestSkillsApility/scenes/template.html`

**Checkpoint**: Foundational template ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Standalone Scene Files (Priority: P1) 🎯 MVP

**Goal**: Create all 38 standalone scene HTML files, each displaying the basic 3D canvas and initial Software Layer visual outcome.

**Independent Test**: Open any individual scene HTML file directly. Verify the 3D scene loads and renders the Software Layer.

### Implementation for User Story 1

- [x] T005 [P] [US1] Create `lec1-sec1.html` with basic track canvas and floating glass blocks
- [x] T006 [P] [US1] Create `lec1-sec2.html` with global data sphere and floating function nodes
- [x] T007 [P] [US1] Create `lec2-sec1.html` with autonomous communicating sphere nodes
- [x] T008 [P] [US1] Create `lec2-sec2.html` with 3-tier object box (identity, state, behavior)
- [x] T009 [P] [US1] Create `lec2-sec3.html` with private central core and defensive shield barrier
- [x] T010 [P] [US1] Create `lec3-sec1.html` with radius-controlled circle sphere
- [x] T011 [P] [US1] Create `lec3-sec2.html` with behavioral logic rotating gears
- [x] T012 [P] [US1] Create `lec3-sec3.html` with constructor conveyor belt spawning cubes
- [x] T013 [P] [US1] Create `lec4-sec1.html` with 3D UML card and attributes/methods tiers
- [x] T014 [P] [US1] Create `lec4-sec2.html` with access symbol gates and static member platform
- [x] T015 [P] [US1] Create `lec5-sec1.html` with wireframe class declaration container and semicolon socket
- [x] T016 [P] [US1] Create `lec5-sec2.html` with locked private default variables vault
- [x] T017 [P] [US1] Create `lec6-sec1.html` with public gates and private wall barriers
- [x] T018 [P] [US1] Create `lec6-sec2.html` with variables padlock status panel
- [x] T019 [P] [US1] Create `lec6-sec3.html` with negative input value slider and stability meter
- [x] T020 [P] [US1] Create `lec7-sec1.html` with inline execution track highlighting caller sites
- [x] T021 [P] [US1] Create `lec7-sec2.html` with class declaration and definition linked by a :: bridge
- [x] T022 [P] [US1] Create `lec7-sec3.html` with timeline track displaying inlined code injections
- [x] T023 [P] [US1] Create `lec8-sec1.html` with central data cylinder and out-of-order method rings
- [x] T024 [P] [US1] Create `lec8-sec2.html` with local stack frame variables dissolving on exit
- [x] T025 [P] [US1] Create `lec8-sec3.html` with foreground local stack variable masking member variable
- [x] T026 [P] [US1] Create `lec8-sec4.html` with explicit target pointer beams (this->, ::)
- [x] T027 [P] [US1] Create `lec9-sec1.html` with PascalCase character text plates
- [x] T028 [P] [US1] Create `lec9-sec2.html` with lowercase library and PascalCase user namespaces folders
- [x] T029 [P] [US1] Create `lec10-sec1.html` with side-by-side object copy containers
- [x] T030 [P] [US1] Create `lec10-sec2.html` with comparison operator check gate
- [x] T031 [P] [US1] Create `lec11-sec1.html` with sliding cover plate shielding implementation circuits
- [x] T032 [P] [US1] Create `lec11-sec2.html` with private data core locked in gear wheels
- [x] T033 [P] [US1] Create `lec12-sec1.html` with negative value direct-mutation input box
- [x] T034 [P] [US1] Create `lec12-sec2.html` with central layout offset modification warning flags
- [x] T035 [P] [US1] Create `lec13-sec1.html` with getter/setter bridge channels
- [x] T036 [P] [US1] Create `lec13-sec2.html` with const filter barrier passing copies
- [x] T037 [P] [US1] Create `lec13-sec3.html` with validation range gate filter
- [x] T038 [P] [US1] Create `lec15-sec1.html` with constructor stamping wireframe molds into solid models
- [x] T039 [P] [US1] Create `lec15-sec2.html` with active scope zone dissolving models exiting boundaries
- [x] T040 [P] [US1] Create `lec15-sec3.html` with initializer list slot routing inputs past constructor body
- [x] T041 [P] [US1] Create `lec15-sec4.html` with delegated signal arrows connecting constructor blocks
- [x] T042 [P] [US1] Create `lec15-sec5.html` with value duplicate vs reference pointer cost lanes
- [x] T043 [P] [US1] Create `lec15-sec6.html` with loop index counter constructor array stamper

**Checkpoint**: At this point, all 38 files exist and load their default 3D visualizations.

---

## Phase 4: User Story 2 - Switch Between 5 Educational Layers (Priority: P1)

**Goal**: Implement the 5-layer tab switching (Software, RAM Map, CPU Dynamics, GPU FX, Corrector) in all 38 files.

**Independent Test**: Click each layer tab in any scene file. Verify 3D meshes transition, text panel updates, and LaTeX renders correctly.

### Implementation for User Story 2

- [x] T044 [US2] Implement layer tabs HTML bar and collapsible details panel layout in `template.html`
- [x] T045 [US2] Implement KaTeX auto-render parsing callback logic in `UIBridge.switchTab()` in `template.html`
- [x] T046 [US2] Define standard RAM Map translucent wireframe styling, CPU RIP highlights, GPU particle effects, and Corrector crimson alert colors inside `MaterialManager`
- [x] T047 [US2] Implement `transitionLayer(tabIndex)` morphing logic in all 38 generators (`lec1-sec1.html` through `lec15-sec6.html`)
- [x] T048 [US2] Add the 5 layers description text and LaTeX equations to all 38 configuration objects in each file

**Checkpoint**: Layer switching, visual morphing, text updates, and math rendering are functional across all scenes.

---

## Phase 5: User Story 3 - Interact with Scene-Specific Controls (Priority: P2)

**Goal**: Add interactive controls (sliders, buttons, toggles) to all files and map them to Three.js modifications.

**Independent Test**: Modify controls in a scene (e.g. radius slider in `lec3-sec1.html`) and verify real-time updates.

### Implementation for User Story 3

- [x] T049 [US3] Implement dynamic controls panel template and state listeners in `InteractionManager` and `UIBridge`
- [x] T050 [US3] Connect sliders, toggles, buttons to corresponding `handleInteraction()` handlers in generators:
  - Sliders for play speed, radius, values (`lec1-sec1.html`, `lec3-sec1.html`, `lec3-sec3.html`, `lec6-sec3.html`, `lec12-sec1.html`, `lec13-sec3.html`)
  - Toggles and button clicks for calling functions and unlocking slots (`lec1-sec2.html`, `lec2-sec3.html`, `lec3-sec2.html`, `lec5-sec1.html`, `lec6-sec1.html`, `lec6-sec2.html`, `lec11-sec1.html`, `lec11-sec2.html`, `lec13-sec2.html`, `lec15-sec1.html`, `lec15-sec3.html`, `lec15-sec6.html`)

**Checkpoint**: Users can interact with 3D scenes via controls and get responsive visual updates.

---

## Phase 6: User Story 4 - Navigation Index Page (Priority: P3)

**Goal**: Create the master index page linking all scenes.

**Independent Test**: Open `index.html`, verify the cards layout, and click cards to open scenes.

### Implementation for User Story 4

- [x] T051 [US4] Create responsive glassmorphism grid layout in `Interactive-Seens-Material/TestSkillsApility/scenes/index.html`
- [x] T052 [US4] Generate 38 visual cards grouped by lectures (Lec1 to Lec15) in `Interactive-Seens-Material/TestSkillsApility/scenes/index.html`
- [x] T053 [US4] Add inline transition animations and hover effects on grid cards

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Verify performance, accessibility, WebGL garbage collection, and responsive constraints across all files.

- [x] T054 Verify WebGL resource disposal logic in `SceneManager.dispose()` in all 38 files to prevent memory leaks
- [x] T055 [P] Audit WCAG AA color contrast on text panels and verify visible focus outlines (`:focus-visible`)
- [x] T056 [P] Add keyboard listeners for tabs selection and drawer toggling to ensure mouse independence
- [x] T057 Add `prefers-reduced-motion` media checks to disable particle velocities and CSS transitions
- [x] T058 Run all 10 scenarios in `quickstart.md` using the nodriver browser tool and document results

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion. Blocks all user stories.
- **User Stories (Phases 3–6)**: All depend on Foundational phase completion.
  - US1 (Standalone files) must complete first.
  - US2 (Layers) and US3 (Controls) can then be implemented incrementally per file.
  - US4 (Index page) can run in parallel with US3.
- **Polish (Phase 7)**: Depends on all user stories being complete.

### Parallel Opportunities

- All US1 file creation tasks (`T005` to `T043`) can run in parallel.
- Accessibility audit (`T055`) and keyboard controls (`T056`) can run in parallel.

---

## Parallel Example: User Story 1

```bash
# Launch multiple scene file creations concurrently:
Task: "Create lec1-sec1.html with basic track canvas and floating glass blocks"
Task: "Create lec1-sec2.html with global data sphere and floating function nodes"
Task: "Create lec2-sec1.html with autonomous communicating sphere nodes"
```

---

## Implementation Strategy

### MVP First (User Story 1 & 2 for Lecture 1)

1. Complete Phase 1 (Setup) and Phase 2 (Foundational managers).
2. Implement User Story 1 and User Story 2 for `lec1-sec1.html` and `lec1-sec2.html` (the MVP).
3. **STOP and VALIDATE**: Verify that the files load independently, tabs switch smoothly, and colors morph correctly.

### Incremental Delivery

1. Once the MVP is validated, roll out the generator layouts to all 38 files.
2. Layer switching and controls are integrated incrementally, section by section.
3. Finally, the navigation index page links the completed collection.
