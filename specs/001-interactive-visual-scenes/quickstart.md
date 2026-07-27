# Quickstart Validation Guide: Interactive Visual Scenes (CS-Bridge)

This guide documents the procedures for opening, running, and validating the generated visual scene files.

## 1. Prerequisites
- A modern desktop web browser (e.g. Google Chrome 110+, Mozilla Firefox 105+, Apple Safari 16+, Microsoft Edge 110+).
- Hardware acceleration enabled in browser settings (required for Three.js WebGL performance).
- Stable internet connection (for loading Tailwind, Three.js, and KaTeX CDNs on initial load, though cached loading is supported).

---

## 2. Validation Scenarios

### Scenario A: Standalone File Execution
- **Step 1**: Locate any generated scene in the `Results/` folder (e.g. [Lec1_Sec1.html](file:///D:/projects/laravel_projects/college_project/Interactive-Seens-Material/D.Mahde/Results/Lec1_Sec1.html)).
- **Step 2**: Double-click the file to open it directly from the local file system (`file://` protocol).
- **Expected Outcome**:
  - The page loads in under 1.5 seconds.
  - The dark-mode layout displays headers, sidebar, code panel, and visual canvas.
  - Mathematical formulas in description cards render correctly using KaTeX fonts.

### Scenario B: Dynamic Layer State Transition
- **Step 1**: Open a scene file (e.g. [Lec15_Sec5.html](file:///D:/projects/laravel_projects/college_project/Interactive-Seens-Material/D.Mahde/Results/Lec15_Sec5.html)).
- **Step 2**: Click on the **RAM Topology** tab. Observe the canvas animation (displays stack pushes/pops).
- **Step 3**: Click on the **GPU Layer** tab.
- **Expected Outcome**:
  - The active 3D animation loop switches within 150ms.
  - The canvas rendering updates to illustrate graphics primitive uploads to VRAM and shader processing, without freezing or throwing console errors.

### Scenario C: Narrative and Phase Alignment
- **Step 1**: Click the **Auto-Play** button or toggle the phase selectors.
- **Step 2**: Verify the active narrative card text.
- **Expected Outcome**:
  - The narrative updates text description per step.
  - The **Memory Flow** block updates dynamically, showing register updates or `Memory is static now`.
  - The traveling indicator/progress bar in the visual canvas matches the active phase.
