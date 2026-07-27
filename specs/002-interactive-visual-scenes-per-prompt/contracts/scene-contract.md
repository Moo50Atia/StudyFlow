# Scene File Contract: Interactive Visual Scenes Per Prompt

**Date**: 2026-07-09
**Feature**: [spec.md](file:///D:/projects/laravel_projects/college_project/specs/002-interactive-visual-scenes-per-prompt/spec.md)

## Overview

Each scene HTML file exposes a consistent interface to the user. This contract defines what every file MUST provide.

---

## File Contract: Scene HTML File

### Structure

Every scene file MUST follow this HTML structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Meta: charset, viewport, title, description -->
  <!-- CDN: Three.js, KaTeX CSS, KaTeX JS, auto-render, Google Fonts (Inter) -->
  <!-- Inline: <style> with all CSS -->
</head>
<body>
  <!-- Header bar (glassmorphism): title, prev/next, menu toggle -->
  <!-- Canvas container: full-viewport Three.js canvas -->
  <!-- Tab bar (glassmorphism): 5 layer buttons -->
  <!-- Details panel (glassmorphism, collapsible): layer description + KaTeX -->
  <!-- Controls panel (glassmorphism): scene-specific interactive controls -->
  <!-- Inline: <script> with all JavaScript -->
</body>
</html>
```

### CDN Dependencies (exact versions)

| Library | URL |
|---------|-----|
| Three.js | `https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js` |
| OrbitControls | `https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js` |
| KaTeX CSS | `https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css` |
| KaTeX JS | `https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js` |
| KaTeX auto-render | `https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js` |
| Inter font | `https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap` |

### CSS Design Tokens (consistent across all files)

```css
:root {
  /* Typography */
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-size-body: 16px;
  --font-size-caption: 14px;
  --font-size-heading: 28px;
  --font-size-title: 36px;
  --line-height-body: 1.6;
  --line-height-heading: 1.2;

  /* Spacing Scale */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;

  /* Border Radius */
  --radius-button: 14px;
  --radius-card: 20px;
  --radius-dialog: 24px;
  --radius-badge: 999px;

  /* Glassmorphism */
  --glass-bg: rgba(15, 15, 25, 0.12);
  --glass-border: rgba(255, 255, 255, 0.15);
  --glass-blur: 20px;
  --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);

  /* Semantic Colors */
  --color-learning: #3b82f6;     /* Blue — knowledge */
  --color-success: #22c55e;      /* Green — correct */
  --color-attention: #f59e0b;    /* Orange — thinking */
  --color-creative: #a855f7;     /* Purple — visualization */
  --color-danger: #ef4444;       /* Red — error/warning */
  --color-focus: #eab308;        /* Yellow — hints */
  --color-programming: #06b6d4;  /* Cyan — programming subject */

  /* Layer-Specific Colors */
  --layer-software: #3b82f6;     /* Blue */
  --layer-ram: #a855f7;          /* Purple */
  --layer-cpu: #06b6d4;          /* Cyan */
  --layer-gpu: #22c55e;          /* Green */
  --layer-corrector: #ef4444;    /* Red */

  /* Animation */
  --duration-micro: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 400ms;
  --duration-scene: 600ms;
  --easing-default: cubic-bezier(0.4, 0, 0.2, 1);
  --easing-spring: cubic-bezier(0.34, 1.56, 0.64, 1);

  /* Z-Index Layers */
  --z-canvas: 0;
  --z-interactive: 5;
  --z-panel: 10;
  --z-dialog: 20;
  --z-alert: 30;
  --z-tooltip: 40;
}
```

### JavaScript Manager Classes (required in every file)

| Class | Responsibility |
|-------|---------------|
| `SceneManager` | Canvas creation, renderer setup (ACES Filmic, pixelRatio capped at 2), animation loop, disposal |
| `CameraManager` | PerspectiveCamera, OrbitControls, Lerp/Slerp transitions, preset positions |
| `LightingManager` | Standard rig: AmbientLight + DirectionalLight (key) + DirectionalLight (fill) + PointLight (rim) |
| `AnimationManager` | Central animation queue, choreography (one major animation at a time), easing functions |
| `InteractionManager` | Control handlers, raycasting for 3D hover/click, keyboard bindings, state tracking |
| `MaterialManager` | Material cache, color interpolation helper, dispose tracking |
| `UIBridge` | Tab switching, panel content updates, KaTeX re-rendering, staggered entrance |
| `[Scene]Generator` | (Unique per file) Builds scene-specific 3D objects, animations, and interactions |

### Interaction Contract

Every interactive element MUST:
1. Have a visible hover state (scale 1.02, glow)
2. Have a click/activation ripple effect
3. Have a visible focus ring (`:focus-visible`)
4. Have an `aria-label` attribute
5. Respond to both mouse and keyboard events

### Tab Switch Contract

When a tab button is clicked:
1. Active tab button gets `aria-selected="true"` and highlighted border
2. `UIBridge.switchTab(index)` is called
3. `generator.transitionLayer(index)` morphs 3D materials smoothly (duration: 600ms, easing: ease-in-out)
4. Description panel content updates with layer-specific text
5. `renderMathInElement()` re-runs on the updated panel for KaTeX
6. No WebGL objects are destroyed/recreated — only material properties change

### Disposal Contract

On `window.beforeunload`:
1. Cancel `requestAnimationFrame` loop
2. Call `generator.dispose()` — iterates all meshes, materials, geometries and calls `.dispose()`
3. Call `renderer.dispose()`
4. Remove all event listeners
5. Set `renderer.domElement` to `null`

---

## File Contract: Index HTML File (`index.html`)

### Structure

The index page lists all 38 scenes as clickable cards grouped by lecture.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Meta, Google Fonts (Inter), inline CSS -->
</head>
<body>
  <!-- Hero header: "C++ OOP Visual Simulator" -->
  <!-- Lecture groups: cards arranged in a responsive grid -->
  <!-- Each card: scene title, visual outcome preview, link to scene file -->
</body>
</html>
```

### Card Contract

Each card MUST:
- Show lecture + section number
- Show the visual learning outcome (1 line)
- Link to the corresponding `lec{N}-sec{M}.html` file
- Have glassmorphism styling
- Have hover animation (scale 1.02, glow)
- Have keyboard focus support
