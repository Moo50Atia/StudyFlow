# Quickstart Validation Guide: Interactive Visual Scenes Per Prompt

**Date**: 2026-07-09
**Feature**: [spec.md](file:///D:/projects/laravel_projects/college_project/specs/002-interactive-visual-scenes-per-prompt/spec.md)

## Prerequisites

- Modern browser: Chrome 90+, Firefox 88+, Edge 90+, or Safari 15+
- WebGL 2.0 support (check via `chrome://gpu`)
- Internet connection (for CDN-hosted libraries)
- File system access to `Interactive-Seens-Material/TestSkillsApility/scenes/`

## Setup

No build step required. All files are standalone HTML.

```bash
# Navigate to the scenes directory
cd Interactive-Seens-Material/TestSkillsApility/scenes/
```

Optionally serve via a local static server (recommended over `file://` for CORS):

```bash
# Using Python
python -m http.server 8080

# Using Node.js
npx serve .
```

Then open `http://localhost:8080/index.html` in browser.

---

## Validation Scenarios

### Scenario 1: Index Page Loads (FR-009)

**Steps**:
1. Open `index.html` in browser
2. Verify page title displays "C++ OOP Visual Simulator"
3. Verify 38 scene cards are visible, grouped by lecture (Lec1–Lec15)
4. Verify each card shows lecture/section number and visual learning outcome

**Expected**: All 38 cards rendered with glassmorphism styling, grouped by lecture. No blank cards.

---

### Scenario 2: Scene File Loads Independently (FR-001, FR-002)

**Steps**:
1. Open `lec1-sec1.html` directly (not via index)
2. Verify Three.js canvas renders with a 3D visualization
3. Verify no console errors in DevTools
4. Open browser Network tab — verify no requests to local files (only CDN)

**Expected**: Full-screen 3D scene with glowing execution track, floating instruction blocks, interactive slider. Zero local file requests.

---

### Scenario 3: 5-Layer Tab Switching (FR-004, FR-005)

**Steps**:
1. Open any scene file (e.g., `lec2-sec3.html`)
2. Click each tab in order: Software → RAM Map → CPU/RIP → GPU/VRAM → Corrector
3. For each tab, verify:
   - 3D meshes change appearance (color, wireframe, opacity)
   - Description panel text updates
   - No console errors

**Expected**: Smooth material transitions (~600ms), unique text per layer, KaTeX formulas render where applicable.

---

### Scenario 4: Interactive Controls (FR-006, FR-007)

**Steps**:
1. Open `lec3-sec1.html` (State as Physical Data)
2. Locate the radius slider control
3. Drag the slider from min to max
4. Verify the 3D sphere scales proportionally in real time

**Expected**: Sphere scales smoothly as slider moves. No lag or frame drops.

---

### Scenario 5: KaTeX Math Rendering (FR-008)

**Steps**:
1. Open `lec1-sec1.html`
2. Switch to the CPU/RIP tab (tab index 2)
3. Look for the formula `$$\Delta RIP = +4$$` in the description panel
4. Verify it renders as a formatted equation (not raw LaTeX text)

**Expected**: Properly formatted mathematical expression with Delta symbol, subscript, and equals sign.

---

### Scenario 6: Keyboard Navigation (FR-011)

**Steps**:
1. Open any scene file
2. Press `Tab` key repeatedly
3. Verify visible focus rings appear on: tab buttons, interactive controls, navigation buttons
4. Press `Enter` or `Space` on a focused tab button
5. Verify it activates the tab

**Expected**: All interactive elements reachable via keyboard. Focus rings visible (cyan outline, 2px). Tab switch triggers on Enter/Space.

---

### Scenario 7: Responsive Layout (FR-015)

**Steps**:
1. Open any scene file
2. Resize browser to 1920×1080 — verify full desktop layout
3. Resize to 1366×768 — verify laptop layout (panels may be smaller)
4. Resize to 768×1024 — verify tablet layout (panels may stack/toggle)
5. Verify 3D canvas fills available space at all sizes

**Expected**: No layout breaks, no horizontal scrollbars, canvas always fills viewport.

---

### Scenario 8: WebGL Disposal (FR-012)

**Steps**:
1. Open `lec1-sec1.html`
2. Open browser DevTools → Performance → Memory tab
3. Note initial GPU memory
4. Navigate to `lec2-sec1.html`
5. Navigate back to `lec1-sec1.html`
6. Check GPU memory — should not continuously increase

**Expected**: GPU memory returns to baseline after page navigation. No leaks across page loads.

---

### Scenario 9: Reduced Motion (FR-013)

**Steps**:
1. Enable `prefers-reduced-motion: reduce` in OS/browser settings
2. Open any scene file
3. Verify: no CSS transitions, no entrance animations, no particle effects
4. Verify: 3D scene still renders (static pose), tabs still switch (instant, no animation)

**Expected**: All non-essential animations disabled. Scene remains functional.

---

### Scenario 10: Performance (FR-014)

**Steps**:
1. Open any scene file
2. Open DevTools → Performance → FPS meter
3. Interact with the scene: rotate camera, switch tabs, use controls
4. Monitor FPS throughout

**Expected**: ≥30 FPS at all times on mid-range hardware. ≥60 FPS on desktop.

---

## Pass Criteria

All 10 scenarios must pass for the feature to be considered complete. See [scene-contract.md](contracts/scene-contract.md) for detailed implementation specifications.
