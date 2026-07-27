# Data Model: Interactive Visual Scenes Per Prompt

**Date**: 2026-07-09
**Feature**: [spec.md](file:///D:/projects/laravel_projects/college_project/specs/002-interactive-visual-scenes-per-prompt/spec.md)

## Overview

This feature produces static HTML files. There is no database, no API, and no persistent storage. The "data model" describes the **in-memory JavaScript object structures** that power each scene at runtime.

---

## Entity: SceneConfig

The static configuration object embedded in each HTML file that defines the scene's content.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Scene identifier, e.g., `"lec1-sec1"` |
| `lecture` | `number` | Lecture number (1–15) |
| `section` | `number` | Section number within lecture |
| `title` | `string` | Human-readable scene title |
| `visualOutcome` | `string` | The visual learning outcome statement |
| `misconception` | `string` | The misconception this scene corrects |
| `layers` | `Layer[5]` | Array of exactly 5 layer definitions |
| `controls` | `ControlDef[]` | Scene-specific interactive controls |
| `navigation` | `NavigationDef` | Previous/Next scene links |

**Identity/Uniqueness**: `id` field — unique per file, derived from `lec{N}-sec{M}` pattern.

**Lifecycle**: Created once at page load, immutable thereafter. No state transitions.

---

## Entity: Layer

One of the 5 educational perspectives on the concept.

| Field | Type | Description |
|-------|------|-------------|
| `index` | `number` | 0–4 (Software=0, RAM=1, CPU=2, GPU=3, Corrector=4) |
| `name` | `string` | Display name (e.g., "THE SOFTWARE LAYER") |
| `icon` | `string` | Tab icon identifier |
| `description` | `string` | Full layer description text (may contain KaTeX `$...$` / `$$...$$`) |
| `visualConfig` | `LayerVisualConfig` | 3D appearance settings for this layer |

---

## Entity: LayerVisualConfig

Defines how the 3D scene morphs when this layer is active.

| Field | Type | Description |
|-------|------|-------------|
| `primaryColor` | `string` | Hex color for primary meshes (e.g., `"#00bcd4"`) |
| `secondaryColor` | `string` | Hex color for secondary meshes |
| `wireframe` | `boolean` | Whether meshes display as wireframe |
| `opacity` | `number` | Material opacity (0.0–1.0) |
| `emissiveIntensity` | `number` | Glow intensity (0.0–2.0) |
| `particleConfig` | `ParticleConfig | null` | Optional particle system settings |
| `cameraPreset` | `string` | Camera position preset: `"overview"`, `"focus"`, `"detail"` |

---

## Entity: ControlDef

Defines a scene-specific interactive control.

| Field | Type | Description |
|-------|------|-------------|
| `type` | `string` | Control type: `"slider"`, `"button"`, `"toggle"`, `"drag"` |
| `label` | `string` | Display label (e.g., "Radius") |
| `ariaLabel` | `string` | Accessibility label |
| `min` | `number | null` | Minimum value (for sliders) |
| `max` | `number | null` | Maximum value (for sliders) |
| `defaultValue` | `any` | Initial value |
| `onChange` | `string` | Name of handler method in SceneGenerator |

---

## Entity: NavigationDef

Links to adjacent scenes.

| Field | Type | Description |
|-------|------|-------------|
| `previous` | `{ id: string, title: string, href: string } | null` | Previous scene link |
| `next` | `{ id: string, title: string, href: string } | null` | Next scene link |
| `indexHref` | `string` | Link to index.html |

---

## Entity: SceneManager (Runtime)

The central runtime object managing the Three.js lifecycle.

| Field | Type | Description |
|-------|------|-------------|
| `renderer` | `THREE.WebGLRenderer` | WebGL renderer instance |
| `scene` | `THREE.Scene` | Three.js scene graph |
| `camera` | `THREE.PerspectiveCamera` | Active camera |
| `controls` | `OrbitControls` | User orbit controls |
| `animationId` | `number | null` | Active `requestAnimationFrame` ID |
| `activeLayer` | `number` | Currently active layer index (0–4) |
| `generator` | `BaseGenerator` | Scene-specific 3D content generator |
| `clock` | `THREE.Clock` | Animation timing clock |

**Lifecycle**: Created → Initialized → Running → Disposed (on page unload)

**State Transitions**:
```
Created → init() → Running
Running → switchLayer(n) → Running (mesh morphing)
Running → dispose() → Disposed
```

---

## Entity: BaseGenerator (Abstract)

Base class for scene-specific 3D content generators.

| Field | Type | Description |
|-------|------|-------------|
| `scene` | `THREE.Scene` | Reference to parent scene |
| `meshes` | `THREE.Object3D[]` | All created meshes |
| `materials` | `THREE.Material[]` | All created materials (for disposal) |
| `geometries` | `THREE.BufferGeometry[]` | All created geometries (for disposal) |

**Methods**:
| Method | Description |
|--------|-------------|
| `create()` | Build all 3D objects for the scene |
| `update(delta)` | Per-frame animation update |
| `transitionLayer(tabIndex)` | Morph meshes to match new layer appearance |
| `handleInteraction(controlId, value)` | Respond to user control input |
| `dispose()` | Clean up all GPU resources |

**Subclasses**: 38 unique implementations, one per scene (e.g., `LinearExecutionGenerator`, `GlobalDataGenerator`, `EncapsulationBarrierGenerator`, etc.)

---

## Relationships

```
SceneConfig 1──5 Layer
SceneConfig 1──* ControlDef
SceneConfig 1──1 NavigationDef
SceneManager 1──1 BaseGenerator (subclass)
SceneManager 1──1 SceneConfig
BaseGenerator 1──* THREE.Object3D (meshes)
Layer 1──1 LayerVisualConfig
```
