# Research: Interactive Visual Scenes Per Prompt

**Date**: 2026-07-09
**Feature**: [spec.md](file:///D:/projects/laravel_projects/college_project/specs/002-interactive-visual-scenes-per-prompt/spec.md)

## Research Summary

No NEEDS CLARIFICATION markers existed in the spec or technical context. All decisions below were pre-resolved via loaded skill constraints and reasonable defaults.

---

## Decision 1: Three.js Version & Loading Strategy

**Decision**: Three.js r128 loaded via CDN (`jsdelivr.net`), with OrbitControls as a CDN addon module.

**Rationale**: r128 is the version explicitly referenced in MyFirstSkill. CDN loading ensures zero local dependencies per FR-002. Using `importmap` or classic `<script>` tags avoids build tooling.

**Alternatives Considered**:
- Three.js r170+ (latest): Higher API surface but spec/skills reference r128 conventions. Risk of breaking changes in material APIs.
- Local bundled copy: Violates self-contained CDN-only constraint. Increases file size beyond 500KB budget.
- React Three Fiber: Framework dependency violates single-file self-contained constraint.

---

## Decision 2: CSS Framework

**Decision**: Vanilla CSS with custom properties (CSS variables) — no framework.

**Rationale**: Glassmorphism skill mandates `backdrop-filter`, custom border-radius tokens (14/20/24/999px), and specific opacity ranges. These are straightforward in vanilla CSS. UIConsistency spacing scale (4/8/12/16/24/32/48/64) maps directly to CSS custom properties. No build step needed.

**Alternatives Considered**:
- Tailwind CSS: Referenced by MyFirstSkill but would require CDN Play mode (runtime overhead, 400KB+). Vanilla CSS is lighter and gives full control over glassmorphism layering.
- CSS Modules: Requires bundler — violates self-contained constraint.

---

## Decision 3: Scene Architecture Pattern (Single File)

**Decision**: Each HTML file contains logically separated JavaScript classes — `SceneManager`, `CameraManager`, `LightingManager`, `AnimationManager`, `InteractionManager`, `MaterialManager`, `UIBridge` — all within a single `<script>` tag.

**Rationale**: ThreeJSArchitecture mandates manager separation. MyFirstSkill mandates single self-contained files. The conflict resolution (from spec) says: "each scene is ONE file but with logical manager separation inside it." This means class-based organization within one file, not file-based separation.

**Alternatives Considered**:
- ES Module imports across files: Violates FR-002 (no local file dependencies).
- Single monolithic function: Violates ThreeJSArchitecture (no logical separation).
- Web Components: Unnecessary complexity for single-page scenes.

---

## Decision 4: Font Loading Strategy

**Decision**: Google Fonts CDN for Inter (primary) with system fallback stack: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`.

**Rationale**: TypographySystem mandates Inter as first preference. CDN loading keeps files self-contained. System fallback prevents FOUT on slow connections.

**Alternatives Considered**:
- Self-hosted font files: Violates self-contained constraint.
- Geist (second preference): Less availability on Google Fonts CDN; Inter is universally supported.

---

## Decision 5: KaTeX Integration

**Decision**: KaTeX CSS + JS + auto-render loaded via CDN. Delimiters: `$...$` for inline, `$$...$$` for display math. Rendering triggered after each tab switch via `renderMathInElement()`.

**Rationale**: MyFirstSkill explicitly mandates KaTeX with `$` and `$$` delimiters. Auto-render extension handles post-DOM-update rendering seamlessly.

**Alternatives Considered**:
- MathJax: Heavier runtime (~500KB vs ~200KB for KaTeX). Slower rendering.
- Pre-rendered SVG: Would require build-time processing — violates self-contained constraint.

---

## Decision 6: Tab-Switch WebGL Memory Management

**Decision**: On each tab switch, the active generator's `transitionLayer(tabIndex)` method morphs existing meshes (color, wireframe, opacity) rather than destroying and recreating them. Full disposal occurs only on page unload via `window.addEventListener('beforeunload', ...)`.

**Rationale**: The 5 layers modify visual appearance of the SAME conceptual objects (e.g., a stack frame is shown as solid blue in Software Layer, wireframe purple in RAM Layer, cyan highlight in CPU Layer). Morphing is cheaper than destroy/recreate and provides smooth transitions per MotionSystem. Full disposal on unload satisfies AdaptivePerformance.

**Alternatives Considered**:
- Full destroy/recreate per tab: Causes visible flicker, heavier GC pressure, violates MotionSystem "never teleport" rule.
- No disposal: Memory leaks — explicitly forbidden by AdaptivePerformance.

---

## Decision 7: Responsive Strategy

**Decision**: CSS media queries at breakpoints 768px (tablet) and 1366px (laptop). The 3D canvas is always 100% viewport with `position: fixed`. Glass panels float absolutely with responsive sizing. On mobile (<768px), panels stack below the scene with a toggle button.

**Rationale**: LearningSceneFocus mandates 70-90% viewport for the scene. On mobile, the full viewport is the scene; panels become togglable overlays. FR-015 specifies the three target viewports.

**Alternatives Considered**:
- Fixed layout (no responsiveness): Violates FR-015 and EnterprisePolish.
- CSS Grid-based layout: Violates LearningSceneFocus's floating panel architecture.

---

## Decision 8: Accessibility Implementation

**Decision**: All interactive buttons get `tabindex="0"`, `role="button"`, `aria-label`. Canvas gets `role="img"` with `aria-label` describing the concept. Focus-visible outlines use `:focus-visible` with a 2px cyan outline. `prefers-reduced-motion` media query disables all CSS transitions and sets a JS flag to skip Three.js animations.

**Rationale**: AccessibilityFirst mandates keyboard-only operation, visible focus rings, WCAG AA contrast, and reduced-motion respect. Canvas cannot be made fully interactive to screen readers, but `aria-label` provides a description.

**Alternatives Considered**:
- Full canvas accessibility via ARIA live regions: Extremely complex for 3D scenes; `aria-label` on canvas + accessible UI controls is the pragmatic standard.

---

## Decision 9: Navigation Between Scenes

**Decision**: Each scene includes a minimal glassmorphism header bar with: scene title, "← Previous" button, "Next →" button, and a "☰ All Scenes" toggle that opens a compact scene list overlay. The index page provides the full navigation grid.

**Rationale**: LearningSceneFocus allows: scene title, tiny breadcrumb, Previous/Next. NarrativeFlow requires scenes to naturally lead to the next. This provides linear progression + random access without violating the 20% UI budget.

**Alternatives Considered**:
- No inter-scene navigation: Violates NarrativeFlow's scene progression principle.
- Full sidebar: Violates LearningSceneFocus's "no large sidebar navigation" rule.

---

## Decision 10: Scene-Specific 3D Content Strategy

**Decision**: Each of the 38 scenes gets a unique `SceneGenerator` class implementing the specific 3D visualization described in its prompt. Generators share a common base pattern (lighting rig, camera setup, tab switching) but each implements custom mesh creation, animation, and interaction logic tailored to its educational concept.

**Rationale**: FR-003 mandates unique visualizations per prompt. The base pattern ensures consistency (UIConsistency, LightingDirector) while custom generators deliver the distinct educational content that was missing in the previous attempt.

**Alternatives Considered**:
- Generic parameterized generator: Cannot express the diversity of 38 unique concepts (execution tracks, data spheres, conveyor belts, vault shields, etc.).
- Template-based generation: Violates MyFirstSkill's "absolute ban on automation scripts."
