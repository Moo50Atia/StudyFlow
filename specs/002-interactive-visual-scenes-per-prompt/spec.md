# Feature Specification: Interactive Visual Scenes Per Prompt

**Feature Branch**: `002-interactive-visual-scenes-per-prompt`

**Created**: 2026-07-09

**Status**: Draft

**Input**: User description: "Design an interactive visual scene for every prompt in Prompts.txt. Each scene is a separate output HTML file. Each file is a standalone, fully interactive 3D educational visualization built with Three.js, glassmorphism UI, motion design, and enterprise-grade polish — complying with all loaded skill constraints."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Browse and Open Individual Scene Files (Priority: P1)

A learner navigates to the output directory and opens any individual scene HTML file (e.g., `lec1-sec1.html`). The file loads as a **standalone, self-contained** web page with no external dependencies beyond CDN-hosted libraries. The learner immediately sees a full-screen interactive 3D visualization that teaches exactly one C++ OOP concept.

**Why this priority**: This is the core deliverable. Without standalone, content-rich scene files, nothing else matters. The previous attempt failed because it produced a single layout shell with no actual scene content.

**Independent Test**: Open any single `.html` file in a browser. It MUST render a working 3D scene with interactive elements, educational content across 5 layers, and smooth animations — without requiring any other file.

**Acceptance Scenarios**:

1. **Given** a learner opens `lec1-sec1.html`, **When** the page loads, **Then** a full-screen Three.js canvas renders a 3D vertical execution track with floating instruction blocks and an interactive playback slider.
2. **Given** a learner opens `lec3-sec3.html`, **When** the page loads, **Then** a 3D conveyor belt spawning independent cubes from a class template mold is rendered with unique colors per instance.
3. **Given** a learner opens any scene file, **When** the page loads, **Then** the 3D visualization occupies ≥80% of the viewport and UI panels (tabs, descriptions) occupy ≤20%.

---

### User Story 2 - Switch Between 5 Educational Layers (Priority: P1)

Within each scene, the learner switches between 5 content layers using tab buttons: (1) Software Layer, (2) RAM/Memory Topology, (3) CPU & Registers, (4) GPU/VRAM, (5) Under-the-Hood Corrector. Each tab dynamically changes both the 3D visualization appearance and the descriptive text panel.

**Why this priority**: The 5-layer architecture is the educational core of the platform — each layer reveals a different depth of understanding of the same concept.

**Independent Test**: Open any scene file, click each of the 5 tabs sequentially. Verify that the 3D scene morphs (colors, wireframes, particles change) and the description panel updates with layer-specific content.

**Acceptance Scenarios**:

1. **Given** a learner is viewing the Software Layer, **When** they click the "RAM Map" tab, **Then** the 3D meshes transition to translucent wireframes with purple/blue tones and the description panel shows memory topology details (addresses, offsets, segment names).
2. **Given** a learner is viewing any layer, **When** they click the "Corrector" tab, **Then** the 3D scene shifts to glowing crimson alert nodes and the panel shows the misconception-shattering explanation.
3. **Given** a learner switches tabs rapidly, **When** transitions overlap, **Then** animations complete gracefully without visual glitches or JavaScript errors.

---

### User Story 3 - Interact with Scene-Specific Controls (Priority: P2)

Each scene contains interactive controls specific to its concept: sliders, buttons, toggles, or drag handles. These controls directly manipulate the 3D visualization to demonstrate the educational concept.

**Why this priority**: Interactivity transforms passive viewing into active learning. Each prompt in the source file specifies unique interactive elements.

**Independent Test**: Open a scene file, locate the interactive control (e.g., radius slider in lec3-sec1), manipulate it, and verify the 3D visualization responds in real time.

**Acceptance Scenarios**:

1. **Given** a learner opens `lec3-sec1.html` (State as Physical Data), **When** they drag the radius slider, **Then** the 3D sphere scales proportionally in real time.
2. **Given** a learner opens `lec1-sec2.html` (Global Data), **When** they toggle function buttons, **Then** particle systems animate signal waves toward the central data sphere.
3. **Given** a learner opens `lec5-sec1.html` (Class Semicolon), **When** they insert the semicolon key into the slot, **Then** the wireframe class container solidifies with a power-up animation.

---

### User Story 4 - Navigate Between Scenes via Index Page (Priority: P3)

A main `index.html` file provides a visual directory of all scenes, grouped by lecture. Clicking any scene card navigates to the corresponding standalone HTML file.

**Why this priority**: Navigation is important for discoverability but each scene file must work independently first.

**Independent Test**: Open `index.html`, verify all scene cards are listed, click any card, verify it opens the correct standalone scene file.

**Acceptance Scenarios**:

1. **Given** a learner opens `index.html`, **When** the page loads, **Then** all 38 scenes are listed as cards grouped by lecture number (Lec1 through Lec15).
2. **Given** a learner clicks a scene card, **When** the link activates, **Then** the corresponding standalone scene HTML file opens.

---

### Edge Cases

- What happens when WebGL is not available? A graceful fallback message is shown instead of a blank screen.
- What happens on mobile devices with limited GPU? Adaptive performance scaling reduces particle counts and disables post-processing effects.
- What happens when KaTeX formulas contain syntax errors? The raw LaTeX source is displayed as fallback text.
- What happens when the browser window is resized? The Three.js canvas and UI panels adapt responsively without layout breaks.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST generate one standalone HTML file per prompt section (38 files total: `lec1-sec1.html` through `lec15-sec6.html`).
- **FR-002**: Each HTML file MUST be fully self-contained — all CSS inline or embedded, all JavaScript inline or loaded from CDNs, no local file dependencies between scenes.
- **FR-003**: Each scene MUST render a unique 3D visualization matching the specific prompt description from `Prompts.txt`, using Three.js for WebGL rendering.
- **FR-004**: Each scene MUST implement exactly 5 switchable content layers: Software, RAM Map, CPU/RIP, GPU/VRAM, and Corrector.
- **FR-005**: Each layer tab MUST dynamically change both the 3D scene appearance (materials, wireframes, colors, particles) and the descriptive text content.
- **FR-006**: Each scene MUST include scene-specific interactive controls as described in the prompt (sliders, buttons, toggles, drag handles).
- **FR-007**: Interactive controls MUST directly manipulate the 3D visualization in real time.
- **FR-008**: All mathematical formulas (LaTeX syntax from prompts) MUST be rendered using KaTeX within the description panels.
- **FR-009**: System MUST generate a navigation index page (`index.html`) listing all 38 scenes grouped by lecture.
- **FR-010**: All UI panels MUST use glassmorphism styling (frosted glass backgrounds, subtle borders, backdrop blur).
- **FR-011**: All scenes MUST support keyboard navigation and include visible focus indicators for interactive elements.
- **FR-012**: All scenes MUST implement proper WebGL resource disposal when the page unloads to prevent memory leaks.
- **FR-013**: All scenes MUST respect `prefers-reduced-motion` media query by disabling non-essential animations.
- **FR-014**: Each scene MUST achieve ≥30 FPS on mid-range hardware during normal interaction.
- **FR-015**: All scenes MUST be fully responsive across desktop (1920×1080), laptop (1366×768), and tablet (768×1024) viewports.

### Key Entities

- **Scene**: A standalone HTML file representing one educational visualization. Identified by lecture number and section number (e.g., Lec1-Sec1). Contains a unique 3D visualization, 5 content layers, interactive controls, and descriptive text.
- **Layer**: One of 5 educational perspectives on the same concept — Software, RAM Map, CPU/Registers, GPU/VRAM, Corrector. Each layer has distinct visual styling and descriptive content.
- **Interactive Control**: A scene-specific UI element (slider, button, toggle, drag handle) that manipulates the 3D visualization to demonstrate the concept.
- **Prompt**: A section from `Prompts.txt` containing the visual learning outcome, misconception correction, and 5-layer content descriptions that define what each scene must show.

## Complete Scene Inventory (38 Scenes)

| # | File Name | Lecture | Section | Visual Learning Outcome |
|---|-----------|---------|---------|------------------------|
| 1 | `lec1-sec1.html` | Lec 1 | Sec 1 | Linear execution path — procedural flow track |
| 2 | `lec1-sec2.html` | Lec 1 | Sec 2 | Central global data node connected to all logic modules |
| 3 | `lec2-sec1.html` | Lec 2 | Sec 1 | Decentralized network of autonomous communicating entities |
| 4 | `lec2-sec2.html` | Lec 2 | Sec 2 | Single unit binding identity, state, and behavior |
| 5 | `lec2-sec3.html` | Lec 2 | Sec 3 | Secured data core behind encapsulation barrier |
| 6 | `lec3-sec1.html` | Lec 3 | Sec 1 | State — data field dictating physical object condition |
| 7 | `lec3-sec2.html` | Lec 3 | Sec 2 | Behavior — entity processing internal data for actions |
| 8 | `lec3-sec3.html` | Lec 3 | Sec 3 | Class vs Object — template spawning distinct instances |
| 9 | `lec4-sec1.html` | Lec 4 | Sec 1 | UML class box with attributes/operations tiers |
| 10 | `lec4-sec2.html` | Lec 4 | Sec 2 | Access symbols and static member notation |
| 11 | `lec5-sec1.html` | Lec 5 | Sec 1 | Class declaration sealed by semicolon |
| 12 | `lec5-sec2.html` | Lec 5 | Sec 2 | Default private access barrier |
| 13 | `lec6-sec1.html` | Lec 6 | Sec 1 | Public gateways vs private walls |
| 14 | `lec6-sec2.html` | Lec 6 | Sec 2 | Default private lock on variables |
| 15 | `lec6-sec3.html` | Lec 6 | Sec 3 | Public data exposure causing state corruption |
| 16 | `lec7-sec1.html` | Lec 7 | Sec 1 | Inline function embedded in class |
| 17 | `lec7-sec2.html` | Lec 7 | Sec 2 | External definition linked via :: operator |
| 18 | `lec7-sec3.html` | Lec 7 | Sec 3 | Inline keyword injecting code at call site |
| 19 | `lec8-sec1.html` | Lec 8 | Sec 1 | Central data linked to out-of-order methods |
| 20 | `lec8-sec2.html` | Lec 8 | Sec 2 | Local variable lifetime within parent frame |
| 21 | `lec8-sec3.html` | Lec 8 | Sec 3 | Variable shadowing — scope masking hierarchy |
| 22 | `lec8-sec4.html` | Lec 8 | Sec 4 | Explicit scoping navigation (this->, ::) |
| 23 | `lec9-sec1.html` | Lec 9 | Sec 1 | PascalCase naming convention for classes |
| 24 | `lec9-sec2.html` | Lec 9 | Sec 2 | Standard vs custom type naming distinction |
| 25 | `lec10-sec1.html` | Lec 10 | Sec 1 | Object assignment creating data duplicates |
| 26 | `lec10-sec2.html` | Lec 10 | Sec 2 | Equality comparison — non-default for objects |
| 27 | `lec11-sec1.html` | Lec 11 | Sec 1 | Abstraction — interface hiding implementation |
| 28 | `lec11-sec2.html` | Lec 11 | Sec 2 | Encapsulation — physical-logical data barrier |
| 29 | `lec12-sec1.html` | Lec 12 | Sec 1 | Data corruption without protective barrier |
| 30 | `lec12-sec2.html` | Lec 12 | Sec 2 | Fragile architecture from tight coupling |
| 31 | `lec13-sec1.html` | Lec 13 | Sec 1 | Secure getter/setter architecture |
| 32 | `lec13-sec2.html` | Lec 13 | Sec 2 | Const getter — non-destructive read operation |
| 33 | `lec13-sec3.html` | Lec 13 | Sec 3 | Setter validation gate rejecting invalid data |
| 34 | `lec15-sec1.html` | Lec 15 | Sec 1 | Constructor initializing object on creation |
| 35 | `lec15-sec2.html` | Lec 15 | Sec 2 | Destructor cleanup on scope exit |
| 36 | `lec15-sec3.html` | Lec 15 | Sec 3 | Initializer list — pre-body field initialization |
| 37 | `lec15-sec4.html` | Lec 15 | Sec 4 | Constructor delegation — reusing init logic |
| 38 | `lec15-sec5.html` | Lec 15 | Sec 5 | Pass-by-reference vs pass-by-value efficiency |
| 39 | `lec15-sec6.html` | Lec 15 | Sec 6 | Array of objects — sequential construction events |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the 38 prompts from `Prompts.txt` are implemented as individual, standalone HTML files — each file opens and runs independently in a browser.
- **SC-002**: Each scene achieves ≥30 FPS during normal interaction on a device with a mid-range GPU.
- **SC-003**: Learners can switch between all 5 layer tabs in under 1 second per transition, with smooth visual morphing and zero console errors.
- **SC-004**: 100% of scene-specific interactive controls (sliders, buttons, toggles) produce visible, real-time changes to the 3D visualization.
- **SC-005**: All mathematical formulas from the prompts render correctly as formatted equations (not raw LaTeX source).
- **SC-006**: All scenes pass WCAG AA contrast requirements for text elements and provide keyboard-navigable interactive controls.
- **SC-007**: All scenes render correctly at desktop (1920×1080), laptop (1366×768), and tablet (768×1024) viewports without layout breaks.
- **SC-008**: No WebGL memory leaks — GPU resources (geometries, materials, textures) are properly disposed when the page unloads.

## Assumptions

- Learners use modern browsers (Chrome 90+, Firefox 88+, Edge 90+, Safari 15+) with WebGL 2.0 support.
- Scene files will be served from a static file server or opened directly via `file://` protocol.
- CDN-hosted libraries (Three.js, KaTeX, Google Fonts) are available at load time; no offline mode is required.
- Each scene file size should remain reasonable (under 500KB of inline HTML/CSS/JS, excluding CDN resources).
- The output directory is `Interactive-Seens-Material/TestSkillsApility/scenes/` within the project root.
- Lectures 14 is intentionally absent from `Prompts.txt` — the system generates only what is specified (38 scenes, not 39).
- The navigation index page is generated at `Interactive-Seens-Material/TestSkillsApility/scenes/index.html`.

## Clarifications

### Session 2026-07-09

- Q: What engineering constraints do the 23 loaded skills impose? → A: All 23 skills are loaded below as mandatory, cumulative design rules. No skill is optional. All conflicts are resolved by priority (CRITICAL > HIGH > MEDIUM).

---

## Mandatory Skill-Derived Engineering Constraints (23 Skills Loaded)

All sections below are **mandatory engineering rules** derived from the 23 skills loaded from `.agents/skills/`. Every scene file MUST comply with ALL constraints simultaneously. Skills are organized by architectural layer. Where two skills conflict, the resolution rule is stated.

---

### Constraint Layer 1 — Constitutional Principles (CRITICAL Priority)

#### C1.1 — Visual Learning Constitution

Source: `VisualLearningConstitution/SKILL.md` (Priority: CRITICAL)

- Every visual element MUST have educational value — if an object does not help explain the concept, it MUST NOT exist
- Each scene MUST teach ONE primary concept — progressive disclosure is mandatory
- Animations MUST guide attention — never animate purely for aesthetics; every movement MUST answer: "What is the learner supposed to notice?"
- Students MUST discover concepts through interaction (dragging, rotating, exploring, simulating, predicting) — not passive reading
- Visual hierarchy MUST follow: Primary Focus → Secondary Context → Supporting Information → Decorative Elements
- Large paragraphs are forbidden — prefer illustrations, animations, diagrams, interactive objects, short explanations
- Relationships MUST be shown visually (Cause→Effect, Input→Process→Output, Network Topology, Memory Layout, Signal Flow)
- Replace text with visualization whenever possible

**Agent Checklist (per scene)**:
- ✓ Does this teach one concept?
- ✓ Is every animation meaningful?
- ✓ Can the student understand without reading everything?
- ✓ Does interaction reinforce learning?
- ✓ Is the UI secondary to the content?

**Forbidden**: Long paragraphs, random icons, decorative animations, flashing colors, information overload, empty whitespace without purpose, duplicate explanations, unnecessary 3D objects

#### C1.2 — Learning Scene Focus Protocol

Source: `LearningSceneFocus/SKILL.md` (Priority: CRITICAL — overrides all other layout skills)

- Each HTML file MUST explain exactly ONE concept — never combine multiple lecture sections
- The 3D scene is ALWAYS the primary visual element:
  - Desktop: 70–90% viewport → Interactive Scene; remaining → UI
  - Maximum UI Occupancy: 20% of screen
- NEVER generate: Course Dashboard, LMS, Student Portal, Teacher Portal, Large Sidebar Navigation, Multi-Lecture Explorer
- Allowed UI chrome: Scene title, tiny breadcrumb, Previous/Next, Reset, Play/Pause, Settings
- When the page loads, users MUST instantly understand the concept before reading — the scene itself communicates the lesson
- File granularity: separate HTML files per section (e.g., `lec1-sec1.html`, `lec1-sec2.html`)
- Camera ALWAYS frames the educational object — never waste space showing empty backgrounds
- Educational success metric: A student opens the page, interacts for 2–5 minutes, and understands ONE concept without needing additional explanation
- If the page feels like software, it failed; if it feels like an interactive scientific exhibit, it succeeded

**Conflict Resolution**: This skill overrides generic dashboard generation. If any other skill suggests creating dashboards, portals, course navigation, or management interfaces — ignore them.

#### C1.3 — Motion System

Source: `MotionSystem/SKILL.md` (Priority: CRITICAL)

- Motion MUST feel: Natural, Predictable, Physical, Elegant, Responsive — never robotic
- Objects have mass, momentum, acceleration, deceleration — objects NEVER teleport
- Preferred motion curves: `ease-out`, `ease-in-out`, `spring`, `cubic-bezier` — avoid `linear`
- Duration guide:
  - Micro Feedback: 100–180ms
  - Buttons: 180–250ms
  - Cards: 250–350ms
  - Panels: 350–500ms
  - Scene Transition: 500–800ms
  - NEVER exceed 1000ms
- Educational motion MUST: Reveal, Explain, Guide, Focus — never distract
- Animation priorities: Focus Movement → Object Relationship → Visual Feedback → Decorative Motion

**Forbidden**: Infinite bouncing, flashing, random movement, linear interpolation, sudden appearance, teleporting UI

#### C1.4 — Adaptive Performance

Source: `AdaptivePerformance/SKILL.md` (Priority: CRITICAL)

- Target frame rate: 60 FPS desktop, 30–60 FPS mobile
- Performance always has HIGHER priority than visual effects
- Performance budget per scene:
  - Maximum Draw Calls: <150 (preferred <100)
  - Maximum Meshes: 300 (preferred 150)
  - Maximum Texture Resolution: 2048 (4096 only when justified)
  - Maximum Realtime Lights: 5 (unlimited baked)
- Device adaptation: Detect GPU, CPU, Screen Size, Memory, Battery Saver — reduce quality automatically
- Rendering rules:
  - Limit pixel ratio: `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))`
  - Enable frustum culling
  - Use LOD (Level of Detail)
  - Use instancing for repeated geometry
  - Dispose unused geometry, materials, textures
  - Cancel inactive animation loops
- Scene cleanup on EVERY transition: Dispose Geometry, Materials, Textures, Render Targets, Post Processing, Event Listeners, Animation Frames

**Forbidden**: Memory leaks, hidden render loops, duplicate textures/materials, unlimited particles, heavy shadows everywhere

#### C1.5 — Three.js Architecture

Source: `ThreeJSArchitecture/SKILL.md` (Priority: CRITICAL)

- Required manager pattern (logical separation within each scene file):
  - Scene Manager, Camera Manager, Lighting Manager, Animation Manager, Interaction Manager, Asset Manager, Material Manager, UI Bridge
- Each educational object MUST have: Own component logic, own animation, own interaction handling
- Materials MUST be reused and cached — avoid duplicates
- Animation logic MUST NOT be placed inside UI components — use centralized animation management
- Loaders: Use GLTFLoader, TextureLoader, DRACOLoader when appropriate

**Forbidden**: Massive monolithic files without logical separation, global variables, repeated loaders, inline object creation, duplicate materials

#### C1.6 — Scene Generation Framework (MyFirstSkill)

Source: `MyFirstSkill/SKILL.md`

- **Absolute ban on automation scripts**: The agent MUST write complete HTML files directly — no Python/Node.js scripts to generate files
- Each file MUST be 100% self-contained: HTML, CSS, Three.js logic, KaTeX configs all in a single standalone file
- Flawless state switching: When a student clicks between the 5 view tabs, JavaScript MUST fully purge WebGL memory of the previous view before spawning the new animation loop
- Universal 5-Layer Metaphorical Mapping MUST be applied:
  1. **Software Layer** (The Interface): Interactive UI controls, buttons, sliders
  2. **Infrastructure Layer** (RAM): Internal containment/storage matrix
  3. **Dynamics & Flow Layer** (CPU): Logical execution, formulas, operations
  4. **Visual FX Layer** (GPU): Cinematic particle systems, glowing fields, micro-animations
  5. **Under-The-Hood Corrector**: Ground-truth analysis shattering the core misconception
- Visual fidelity: Premium 3D visualizations using Three.js with dynamic particle effects, orbit controls, rich gradients
- Mathematical rendering: KaTeX with `$` and `$$` delimiters
- Strict garbage collection: `.dispose()` on geometries, materials, textures; cancel `requestAnimationFrame` on tab switching

---

### Constraint Layer 2 — Visual Design System (HIGH Priority)

#### C2.1 — Glassmorphism Design System

Source: `Glassmorphism/SKILL.md` (Priority: HIGH)

- All floating interfaces MUST feel lightweight, premium, and layered above the educational canvas
- Layer stack: Canvas → Gradient → Glass Panels → Floating Controls → Dialogs
- Panel rules:
  - Use `backdrop-filter: blur(16px–24px)`
  - Semi-transparent surfaces (dark mode: 8–15% opacity; light mode: 50–70%)
  - Rounded corners: Cards 20px, Dialogs 24px, Buttons 14px, Badges 999px
  - Soft borders: `border: 1px solid rgba(255,255,255,0.2)` — never pure white
  - Soft layered shadows — never heavy black shadows
  - NEVER use solid/opaque panels
- Z-index hierarchy: Canvas z-0 → Interactive Objects z-5 → Glass Panels z-10 → Floating Dialogs z-20 → Alerts z-30 → Tooltips z-40
- Target aesthetic: Apple VisionOS, Linear, Raycast, Arc Browser — NOT traditional admin dashboards

**Forbidden**: Opaque panels, sharp corners, heavy borders, flat rectangles, multiple overlapping blurs

#### C2.2 — Color Psychology System

Source: `ColorPsychology/SKILL.md` (Priority: HIGH)

- Color MUST communicate meaning — never use colors randomly
- Semantic color assignments:
  - Blue: Learning, Trust, Knowledge
  - Green: Success, Completion, Correct Answer, Growth
  - Orange: Attention, Thinking, Problem Solving
  - Purple: Creativity, Visualization, AI, Innovation
  - Red: Critical, Danger, Errors, Warnings
  - Yellow: Focus, Hints, Recommendations
- Subject theme: Programming → Cyan
- Minimum contrast ratio: 4.5:1
- Always pair color with Icons, Labels, or Motion — never rely on color alone

**Forbidden**: Random gradients, rainbow palettes, neon overload, low contrast, meaningless color changes

#### C2.3 — AI Visual Hierarchy

Source: `AIVisualHierarchy/SKILL.md`

- Only four heading levels allowed: H1, H2, H3, Body — never invent random font sizes
- Most important element MUST have: Highest contrast, Largest size, Strongest glow
- Never overcrowd interfaces — every major section must breathe
- User eye movement follows Z-Pattern: Top Left → Center → Bottom Right
- Information density: ONE concept per visual block — never explain three concepts together
- Color meaning enforcement: Blue=Information, Green=Success, Yellow=Attention, Red=Error, Purple=AI
- Important concepts MUST appear inside highlighted cards — avoid plain paragraphs

#### C2.4 — Typography System

Source: `TypographySystem/SKILL.md` (Priority: HIGH)

- Font preference order: Inter, Geist, IBM Plex Sans, Noto Sans
- Type hierarchy:
  - Display: 48–64px
  - Heading: 32–40px
  - Section: 24–28px
  - Body: 16–18px
  - Caption: 14px
  - Label: 12px
- Maximum line length: 75 characters
- Alignment: Prefer Left (RTL → Prefer Right) — never justify text
- Line spacing: Heading 1.2, Body 1.6, Lists 1.5
- Maximum 2 font weights per screen

**Forbidden**: Tiny fonts, dense paragraphs, centered paragraphs, decorative fonts, ALL CAPS, italics (except rare emphasis)

#### C2.5 — UI Consistency Standard

Source: `UIConsistency/SKILL.md` (Priority: HIGH)

- Spacing scale (px): 4, 8, 12, 16, 24, 32, 48, 64 — never invent arbitrary spacing
- Border radius: Buttons 14px, Cards 20px, Dialogs 24px, Badges 999px
- Icons: Use ONE icon family only (Lucide preferred) — never mix icon packs
- Button styles: Primary (Filled), Secondary (Outlined), Danger (Red), Ghost (Transparent) — maximum 4 styles
- Cards: One elevation style, one border style, one spacing system
- Inputs: Equal height, equal padding, equal focus behavior
- Animation timing: Fast 150ms, Normal 250ms, Slow 400ms, NEVER exceed 600ms
- Grid: Consistent 12-column layouts with equal gutters

**Forbidden**: Mixed corner radius, mixed shadows, different button sizes, random spacing, random typography

#### C2.6 — Enterprise Polish

Source: `EnterprisePolish/SKILL.md`

- Consistency: Spacing, radius, typography, colors, shadows MUST remain identical across all scenes
- Empty states: NEVER display blank pages — show illustration + explanation + CTA
- Loading: Every async action requires skeleton/progress/status indication
- Errors: Friendly messages only — never expose stack traces
- Success: Always confirm completed operations (e.g., "✓ Scene Loaded", "✓ Layer Switched")
- Responsive: Desktop, Tablet, Mobile MUST all work correctly
- Animations MUST communicate confidence — no flashy effects, no random bouncing
- Every screen MUST feel like premium enterprise software

#### C2.7 — Frontend Design Direction

Source: `frontend-design/SKILL.md`

- Design as a studio lead: Make deliberate, opinionated choices specific to THIS educational platform — not templated defaults
- Ground design in the subject: C++ OOP is the subject — use its world (memory diagrams, register metaphors, compilation pipelines) as design vocabulary
- Typography carries personality: Pair display and body faces deliberately — the type treatment itself should be a memorable part of the design
- Structural devices (numbering, labels, dividers) MUST encode something true about the content, not decorate
- Motion: Choose one orchestrated moment per scene rather than scattered effects
- Restraint: Spend boldness in ONE place (the 3D scene) — keep everything around it quiet and disciplined
- Self-critique: Before finalizing, evaluate if the design could be mistaken for generic AI output — if yes, revise

---

### Constraint Layer 3 — Cinematic & Scene Direction (HIGH Priority)

#### C3.1 — Camera Director

Source: `CameraDirector/SKILL.md` (Priority: HIGH)

- The camera IS the teacher — it MUST direct attention, never left static without reason
- Camera modes: Overview, Focus, Explore, Detail, Presentation
- Camera behavior: ALWAYS animate — never instantly reposition
  - Prefer: Orbit, Dolly, Pan, Zoom, Lerp, Slerp
- Educational focus:
  - When explaining → Move closer
  - When comparing → Move wider
  - When introducing → Use overview
- Camera MUST always focus important objects — never stare into empty space
- Camera speed: Slow (concept explanation), Medium (navigation), Fast (emergency only)

**Forbidden**: Teleporting, camera shaking, fast spinning, sudden zoom, constant movement

#### C3.2 — Lighting Director

Source: `LightingDirector/SKILL.md` (Priority: HIGH)

- Light is part of teaching — good lighting makes concepts easier to understand
- Standard lighting rig per scene: Ambient Light → Key Light → Fill Light → Rim Light → Environment HDRI
- Color temperature mapping:
  - Warm: Instruction/explanation
  - Neutral: General learning
  - Cool: Technology concepts
  - Emergency: Red accent only
- Shadows: Soft shadows, contact shadows — avoid harsh black shadows
- Tone mapping: ACES Filmic, preferred exposure 1.0–1.3
- Bloom: Subtle, educational highlights only — never bloom entire scenes
- Fog: Use only for Scale, Depth, Distance — never decorative fog

**Forbidden**: Completely flat lighting, full white ambient, pitch black shadows, random colored lights, excessive bloom

#### C3.3 — Scene Composition

Source: `SceneComposition/SKILL.md` (Priority: HIGH)

- Scenes MUST explain, not decorate
- Composition layers: Foreground → Primary Object → Supporting Objects → Background
- Layout principles: Rule of Thirds, Golden Ratio, Negative Space, Visual Balance, Eye Flow
- Only ONE dominant object per scene — everything else supports it
- Always visualize relationships: Cause→Effect, Input→Output, Hierarchy, Dependencies, Connections
- Camera framing: Leave breathing room — avoid cropped educational objects
- White space improves understanding — never fill every corner

**Forbidden**: Crowded scenes, floating unrelated objects, random spacing, decorative clutter

---

### Constraint Layer 4 — Interaction & Animation Choreography (HIGH Priority)

#### C4.1 — Interaction Engine

Source: `InteractionEngine/SKILL.md` (Priority: HIGH)

- Learning happens through interaction — every interaction MUST reinforce understanding
- Supported interactions: Hover, Click, Double Click, Drag, Rotate, Zoom, Pan, Keyboard, Touch, Pinch, Long Press
- Every interactive object MUST provide: Visual Feedback, Cursor Feedback, Animation Feedback, Educational Feedback
- Object states: Idle, Hover, Focused, Selected, Dragging, Animating, Completed, Disabled
- Educational interactions MUST: Reveal concepts, Compare ideas, Explore structures, Simulate behavior, Test hypotheses
- Accessibility: Keyboard navigation required, Touch support required, Screen reader labels, Reduced Motion respected

**Forbidden**: Hidden interactions, invisible clickable objects, tiny click areas, interaction without feedback

#### C4.2 — Animation Director

Source: `AnimationDirector/SKILL.md` (Priority: HIGH)

- Animations MUST work together — not compete
- Animation sequence: Introduce → Focus → Interact → Explain → Confirm → Exit
- Choreography: ONE major animation at a time — secondary animations wait — never animate everything simultaneously
- Educational timing: Explain → Pause → Interaction → Feedback
- Animation categories: Entrance, Exit, State Change, Hover, Selection, Progress, Completion, Error
- Related objects move together — independent objects remain independent

**Forbidden**: Animation chaos, simultaneous explosions, endless looping, random delays

#### C4.3 — Micro Interactions

Source: `MicroInteractions/SKILL.md` (Priority: HIGH)

- Every user action MUST receive feedback — immediate, elegant, meaningful
- Interaction feedback specs:
  - Hover: Soft elevation, glow, cursor change, scale(1.02)
  - Click: Ripple, tiny compression, glow pulse, optional particles
  - Success: Green pulse, checkmark animation, smooth confirmation
  - Error: Gentle shake, red outline, helpful message — never punish the user
  - Loading: Skeleton, progress, morph — never spinning forever
  - Drag: Highlight destination, snap preview, magnetic guidance

**Forbidden**: Loud particles, confetti everywhere, excessive scaling, long delays

#### C4.4 — Staggered Entrance

Source: `StaggeredEntrance/SKILL.md` (Priority: MEDIUM)

- Users MUST discover the interface naturally — not all at once
- UI loading order: Background → Layout → Navigation → Titles → Cards → Controls → Interactive Objects → Decorative Elements
- Delay guide: Layout 0ms → Header 80ms → Sidebar 120ms → Cards 180ms → Controls 240ms → Interactive Objects 320ms
- Scene generation order: Environment → Lighting → Primary Objects → Secondary Objects → Effects
- Educational rule: Reveal concepts progressively — never reveal the answer immediately
- Skip staggering when: Reduced Motion detected OR low-end device

**Forbidden**: Massive pop-in, random delays, long waiting times, blocking interaction

---

### Constraint Layer 5 — Learning & Narrative Flow

#### C5.1 — Narrative Flow

Source: `NarrativeFlow/SKILL.md`

- Every scene MUST feel like a guided journey — the learner should never feel lost
- Every interaction MUST answer: "Why am I seeing this now?"
- Learning sequence per scene: Hook → Context → Visualization → Exploration → Experiment → Reflection → Practice → Assessment → Summary
- Progressive disclosure: Never reveal everything immediately — unfold step by step
- Storytelling: Instead of "This is X", prefer "Imagine doing X..." then animate consequences
- Each scene SHOULD naturally lead to the next one via Previous/Next navigation
- Create curiosity moments: "What happens if...", "Try increasing...", "Can you predict..."
- The learner MUST remember the journey, not individual UI components

#### C5.2 — Delight Engineering

Source: `DelightEngineering/SKILL.md`

- Celebrate progress: When learners finish a step → small animation, progress increase, positive message
- Emotional feedback: Instead of "Correct", prefer "Excellent!", "Great reasoning", "You're improving"
- Tiny surprises (only after achievements): Animated icons, smooth confetti, soft particle bursts, dynamic illustrations
- Motivation indicators: Completion %, learning streak, knowledge growth, skill mastery
- Platform personality: Professional, Friendly, Encouraging, Calm, Intelligent
- End goal: The learner should leave feeling "I actually understand this now" — not "I finished another lesson"

**Avoid**: Childish effects, excessive fireworks, gaming overload

---

### Constraint Layer 6 — Accessibility (NON-NEGOTIABLE)

#### C6.1 — Accessibility First

Source: `AccessibilityFirst/SKILL.md`

- Everything MUST work using keyboard only — no mouse dependency
- Visible focus rings are MANDATORY — never remove outline
- Minimum contrast ratio: WCAG AA (4.5:1 for text, 3:1 for large text)
- Every button requires `aria-label`; every image requires `alt` text; every canvas requires description
- Respect `prefers-reduced-motion` — disable animations automatically
- Never use text below 14px — educational content: 16px+
- Never rely on color alone for conveying information — always pair with icons, labels, messages
- Every student MUST be able to learn regardless of physical limitations

---

### Skill Conflict Resolution Matrix

| Conflict | Resolution |
|----------|------------|
| LearningSceneFocus says <20% UI vs UIConsistency says 12-column grid | LearningSceneFocus wins: glass panels float over scene, no full grid layout. Grid applies only within panels. |
| MotionSystem says max 1000ms vs StaggeredEntrance delay guide sums to 320ms | No conflict: stagger delays are sequential entrance offsets, not animation durations. Both apply. |
| ThreeJSArchitecture says "never one giant file" vs MyFirstSkill says "100% self-contained single file" | Resolved: each scene is ONE file but with logical manager separation inside it (SceneManager, CameraManager, etc. as classes/objects within the same file). |
| EnterprisePolish says "premium software feel" vs LearningSceneFocus says "if it feels like software it failed" | Resolved: Enterprise polish applies to UI chrome quality (glass panels, buttons, typography). The SCENE itself must feel like an interactive exhibit. The UI wrapping the scene must feel enterprise-grade. |
| Glassmorphism dark mode 8-15% opacity vs WCAG AA contrast | Resolved: Glass panel text MUST meet 4.5:1 contrast against the blurred background. Increase text brightness or add subtle dark overlay behind text if needed. |
| CameraDirector says "never static" vs SceneComposition says "leave breathing room" | No conflict: Camera animates subtly (slow orbit) while composition maintains spatial balance. |
| AnimationDirector says "one major animation at a time" vs StaggeredEntrance sequential loading | No conflict: Staggered entrance is the INITIAL loading choreography. AnimationDirector governs runtime interactions after load. |

---

### Consolidated Quality Gate (All Skills Combined)

Before any scene file is considered complete, it MUST pass ALL of the following:

- [ ] Teaches exactly ONE concept (VisualLearningConstitution, LearningSceneFocus)
- [ ] 3D scene occupies ≥80% viewport; UI ≤20% (LearningSceneFocus)
- [ ] Every animation has educational purpose (VisualLearningConstitution, MotionSystem)
- [ ] Glassmorphism panels with backdrop-blur, rounded corners, semi-transparent (Glassmorphism)
- [ ] Semantic color usage — no random colors (ColorPsychology)
- [ ] Typography follows hierarchy: Inter/Geist, 16px+ body, max 75 chars/line (TypographySystem)
- [ ] All spacing from scale: 4/8/12/16/24/32/48/64 (UIConsistency)
- [ ] Keyboard navigable, visible focus rings, aria-labels (AccessibilityFirst)
- [ ] `prefers-reduced-motion` respected (AccessibilityFirst, StaggeredEntrance)
- [ ] Draw calls <150, meshes <300, textures ≤2048 (AdaptivePerformance)
- [ ] `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))` (AdaptivePerformance)
- [ ] Full WebGL disposal on page unload and tab switch (AdaptivePerformance, MyFirstSkill)
- [ ] Standard lighting rig: Ambient + Key + Fill + Rim (LightingDirector)
- [ ] ACES Filmic tone mapping, exposure 1.0–1.3 (LightingDirector)
- [ ] Camera animates with Lerp/Slerp — never teleports (CameraDirector)
- [ ] One dominant object per scene (SceneComposition)
- [ ] Staggered entrance: Environment → Lighting → Primary → Secondary → Effects (StaggeredEntrance)
- [ ] Every interactive object provides visual + cursor + educational feedback (InteractionEngine)
- [ ] Micro-interaction feedback on hover (scale 1.02), click (ripple), success (green pulse) (MicroInteractions)
- [ ] Animation choreography: one major animation at a time (AnimationDirector)
- [ ] Motion curves: ease-out/ease-in-out/spring — never linear (MotionSystem)
- [ ] Progressive disclosure narrative flow (NarrativeFlow)
- [ ] 100% self-contained single HTML file per scene (MyFirstSkill)
- [ ] KaTeX math rendering with $ and $$ delimiters (MyFirstSkill)
- [ ] Enterprise-grade UI polish on all chrome elements (EnterprisePolish)
- [ ] Design grounded in C++ OOP subject matter (frontend-design)
