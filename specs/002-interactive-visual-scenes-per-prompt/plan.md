# Implementation Plan: Interactive Visual Scenes Per Prompt

**Branch**: `002-interactive-visual-scenes-per-prompt` | **Date**: 2026-07-09 | **Spec**: [spec.md](file:///D:/projects/laravel_projects/college_project/specs/002-interactive-visual-scenes-per-prompt/spec.md)

**Input**: Feature specification from `specs/002-interactive-visual-scenes-per-prompt/spec.md`

## Summary

Generate 38 standalone, self-contained HTML files — one per prompt section from `Prompts.txt` — each delivering a unique interactive 3D educational visualization of a C++ OOP concept using Three.js. Each file implements 5 switchable content layers (Software, RAM, CPU, GPU, Corrector) with scene-specific interactive controls, glassmorphism UI, enterprise polish, and full compliance with 23 loaded skill constraints. A 39th file (`index.html`) serves as a navigation hub linking all scenes.

## Technical Context

**Language/Version**: HTML5 + ES6+ JavaScript (inline, no build step)

**Primary Dependencies**:
- Three.js r128+ (CDN: `https://cdn.jsdelivr.net/npm/three@0.128.0/`)
- Three.js OrbitControls (CDN addon)
- KaTeX 0.16.8+ (CDN: `https://cdn.jsdelivr.net/npm/katex@0.16.8/`)
- KaTeX auto-render extension (CDN)
- Google Fonts: Inter (CDN)

**Storage**: N/A — static HTML files, no database

**Testing**: Manual browser testing + headless browser validation (mcp-nodriver)

**Target Platform**: Modern browsers (Chrome 90+, Firefox 88+, Edge 90+, Safari 15+) with WebGL 2.0

**Project Type**: Static educational web application — collection of standalone HTML visualizations

**Performance Goals**: 60 FPS desktop, 30+ FPS mobile, <150 draw calls, <300 meshes per scene

**Constraints**: Each file <500KB inline code, 100% self-contained (no local dependencies), WCAG AA compliant, `prefers-reduced-motion` respected

**Scale/Scope**: 38 scene files + 1 index file = 39 HTML files total

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The project constitution (`.specify/memory/constitution.md`) contains only template placeholders — no project-specific governance rules are defined. Therefore:

- **Gate Result**: ✅ PASS — no constitution violations possible
- **Post-Phase-1 Re-check**: Will verify that generated artifacts don't violate any skill constraints (which serve as the de facto constitution for this project)

## Project Structure

### Documentation (this feature)

```text
specs/002-interactive-visual-scenes-per-prompt/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── scene-contract.md
└── tasks.md             # Phase 2 output (created by /speckit-tasks)
```

### Source Code (repository root)

```text
Interactive-Seens-Material/TestSkillsApility/scenes/
├── index.html               # Navigation hub — links to all 38 scenes
├── lec1-sec1.html           # Lec1 Sec1: Linear execution path
├── lec1-sec2.html           # Lec1 Sec2: Global data node
├── lec2-sec1.html           # Lec2 Sec1: Autonomous communicating entities
├── lec2-sec2.html           # Lec2 Sec2: Identity, state, behavior
├── lec2-sec3.html           # Lec2 Sec3: Encapsulation barrier
├── lec3-sec1.html           # Lec3 Sec1: State as physical data
├── lec3-sec2.html           # Lec3 Sec2: Behavior as functional capability
├── lec3-sec3.html           # Lec3 Sec3: Class vs Object (template/instances)
├── lec4-sec1.html           # Lec4 Sec1: UML class box
├── lec4-sec2.html           # Lec4 Sec2: Access symbols / static notation
├── lec5-sec1.html           # Lec5 Sec1: Class semicolon seal
├── lec5-sec2.html           # Lec5 Sec2: Default private barrier
├── lec6-sec1.html           # Lec6 Sec1: Public gateways vs private walls
├── lec6-sec2.html           # Lec6 Sec2: Default private lock
├── lec6-sec3.html           # Lec6 Sec3: Public data corruption
├── lec7-sec1.html           # Lec7 Sec1: Inline function in class
├── lec7-sec2.html           # Lec7 Sec2: External definition via ::
├── lec7-sec3.html           # Lec7 Sec3: Inline keyword at call site
├── lec8-sec1.html           # Lec8 Sec1: Data linked to out-of-order methods
├── lec8-sec2.html           # Lec8 Sec2: Local variable lifetime
├── lec8-sec3.html           # Lec8 Sec3: Variable shadowing
├── lec8-sec4.html           # Lec8 Sec4: Explicit scoping (this->, ::)
├── lec9-sec1.html           # Lec9 Sec1: PascalCase naming
├── lec9-sec2.html           # Lec9 Sec2: Standard vs custom type naming
├── lec10-sec1.html          # Lec10 Sec1: Object assignment (data copy)
├── lec10-sec2.html          # Lec10 Sec2: Equality comparison not default
├── lec11-sec1.html          # Lec11 Sec1: Abstraction (interface hides impl)
├── lec11-sec2.html          # Lec11 Sec2: Encapsulation (data barrier)
├── lec12-sec1.html          # Lec12 Sec1: Data corruption without barrier
├── lec12-sec2.html          # Lec12 Sec2: Fragile architecture / tight coupling
├── lec13-sec1.html          # Lec13 Sec1: Getter/setter architecture
├── lec13-sec2.html          # Lec13 Sec2: Const getter (non-destructive read)
├── lec13-sec3.html          # Lec13 Sec3: Setter validation gate
├── lec15-sec1.html          # Lec15 Sec1: Constructor initialization
├── lec15-sec2.html          # Lec15 Sec2: Destructor cleanup
├── lec15-sec3.html          # Lec15 Sec3: Initializer list
├── lec15-sec4.html          # Lec15 Sec4: Constructor delegation
├── lec15-sec5.html          # Lec15 Sec5: Pass-by-reference efficiency
└── lec15-sec6.html          # Lec15 Sec6: Array of objects construction
```

**Structure Decision**: Flat directory of standalone HTML files under `Interactive-Seens-Material/TestSkillsApility/scenes/`. No build system, no bundler, no framework. Each file is 100% self-contained with inline CSS/JS and CDN-loaded libraries. This matches MyFirstSkill's "absolute ban on automation scripts" and LearningSceneFocus's "file granularity" requirements.

## Complexity Tracking

No constitution violations to justify — the constitution is unpopulated. All constraints come from loaded skills, which are fully integrated into the spec.
