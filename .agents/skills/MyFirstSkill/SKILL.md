---
name: MyFirstSkill
description: General-purpose framework for generating high-fidelity interactive 3D visual scenes across multi-disciplinary domains, enforcing manual generation, and preventing memory leaks.
---

# Generative Visual Scene Design & Multi-Disciplinary Framework

This skill guides the preparation, validation, and manual generation of 3D interactive visual scenes for any academic discipline. It ensures rigid quality control, enforces an interactive prompt refinement loop, and bans automation scripts.

---

## 1. Historical Architecture Comparison

To ensure maximum visual quality and technical accuracy, all generated scenes must avoid the characteristics of the **Refused Views** and strictly conform to the **Accepted Views**.

| Category | Refused Views (DO NOT USE) | Accepted Views (MANDATORY) |
| :--- | :--- | :--- |
| **Automation & Creation** | **Using Python, Node.js, or any background automation scripts to generate files.** | **100% Manual Generation by the Agent.** The Agent must output the full, complete HTML/JS code directly in the workspace. |
| **Domain Scope** | Rigid low-level Computer Science terminology only, confusing non-CS students. | **Multi-Disciplinary Adaptability.** Uses metaphorical mapping to adapt technical layers to any subject (Medicine, Physics, Business, etc.). |
| **Visual Fidelity** | Simple 2D canvas drawings, static/flat diagrams, or basic shapes. | Premium 3D visualizations using **Three.js** (r128) with dynamic particle effects, orbit controls, and rich gradients. |
| **Styling & Layout** | Browser default fonts, unstyled layouts, lack of padding/gaps. | Modern dark-mode styling with **Tailwind CSS**, glassmorphism panels, glowing interactive markers, and fluid viewports. |
| **Resource Disposal** | Re-creating canvases without cleaning WebGL buffers, causing severe memory leaks. | Strict garbage collection: Explicitly calling `.dispose()` on geometries, materials, and textures, and canceling active `requestAnimationFrame` loops on tab switching. |
| **Mathematical Rendering**| Plain text formulas or code comments explaining math rules. | Clear mathematical formulas rendered on-screen using **KaTeX** with configured `$` and `$$` delimiters. |

---

## 2. Universal 5-Layer Metaphorical Mapping

To maintain a unified 5-Tab interface across all academic fields, the Agent must map any non-CS domain into the 5 core presentation layers using logical analogies:

1. **The Software Layer (The Interface):** The interactive UI controls, buttons, and sliders the student plays with.
2. **The Infrastructure Layer (Formerly RAM):** The internal containment or storage matrix (e.g., Blood vessels in medicine, Warehouses in logistics, Chemical bonds in chemistry).
3. **The Dynamics & Flow Layer (Formerly CPU):** The logical execution, formulas, movement, and functional operations of the concept (e.g., Valve contraction, Price fluctuations, Acceleration vectors).
4. **The Visual FX Layer (Formerly GPU):** The cinematic particle systems, glowing fields, heat-maps, and micro-animations that represent energy or data flow.
5. **The Under-The-Hood Corrector:** Ground-truth scientific analysis that explicitly shatters the core student misconception of that specific topic.

---

## 3. Interactive Development Workflow

Every time this skill is activated, the Agent **MUST** execute this two-step process:

### Step 1: Prompt Refinement & Approval Loop
1. Read the section specifications and expand them into a highly descriptive technical plan based on the **Universal 5-Layer Mapping**.
2. Present the expanded prompt specification to the user.
3. **HALT AND WAIT FOR APPROVAL.** Do NOT generate any file or code until the user explicitly reviews the plan and types: **"Generate"**. If modifications are requested, regenerate the prompt blueprint and repeat this loop.

### Step 2: Code Generation Execution
Once and only once the user says "Generate", output the production code following these constraints:
* **Absolute Ban on Scripts:** Write the entire HTML file yourself. Do not provide a python/node script to execute or build it.
* **100% Self-Contained:** Everything (HTML, Tailwind CSS configurations, Three.js logic, KaTeX configs) must live inside a single standalone file.
* **Flawless State Switching:** When a student clicks between the 5 view tabs, the JavaScript controller must fully purge the WebGL memory of the previous view before spawning the new animation loop to avoid memory leaks.