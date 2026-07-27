---
name: LearningSceneFocus
description: CRITICAL architectural skill that forces every generated interactive visualization to explain exactly one concept using a scene-first layout. Prevents LMS dashboards, multi-lecture pages, and UI-heavy layouts.
---

# Learning Scene Focus Protocol (CRITICAL)

This skill has higher priority than generic UI generation.

Its purpose is to guarantee that every generated HTML page behaves as an educational visualization, NOT as a Learning Management System (LMS).

---

# Core Philosophy

The visualization is the product.

The UI exists only to support the visualization.

If there is any conflict between adding more interface components or enlarging the interactive scene,

ALWAYS enlarge the scene.

---

# Rule 1 — One Concept Per Scene

Each generated HTML file MUST explain exactly ONE concept.

Never combine multiple lecture sections.

Never combine multiple educational objectives.

One file

↓

One Lesson

↓

One Concept

↓

One Interactive Experience

Examples:

✔ Correct

lec1-sec1-linear-execution.html

✔ Correct

lec2-sec3-polymorphism.html

✘ Wrong

course.html

✘ Wrong

all_lectures.html

✘ Wrong

interactive_platform.html

---

# Rule 2 — Scene First Layout

The 3D scene is always the primary visual element.

Viewport allocation:

Desktop

70–90%

↓

Interactive Scene

Remaining space

↓

UI

Never allow navigation panels to dominate the screen.

The visualization must immediately attract attention.

---

# Rule 3 — No LMS Dashboards

NEVER generate:

• Course Dashboard
• Learning Management System
• Student Portal
• Teacher Portal
• Large Sidebar Navigation
• Multi-Lecture Explorer
• Global Course Browser
• Academic Dashboard

Those belong to another application.

This HTML file represents ONE learning experience only.

---

# Rule 4 — UI Chrome Budget

Navigation is intentionally minimal.

Allowed:

• Scene title
• Tiny breadcrumb
• Previous
• Next
• Reset
• Play
• Pause
• Settings

Forbidden:

Huge sidebars

Long lecture lists

Statistics dashboards

Large cards

Complex menus

Multiple navigation systems

Maximum UI Occupancy:

20% of screen

Everything else belongs to the visualization.

---

# Rule 5 — Visual Dominance

When the page loads, users must instantly understand the concept before reading.

The scene itself should communicate the lesson.

Text only reinforces understanding.

If text occupies more visual space than the visualization,

the design is incorrect.

---

# Rule 6 — Interaction First

Learning happens through interaction.

Prefer:

Dragging

Rotating

Connecting

Clicking

Exploring

Triggering animations

Changing parameters

Avoid passive reading.

---

# Rule 7 — Progressive Disclosure

Do not reveal everything immediately.

The lesson should unfold gradually.

Preferred flow:

Initial State

↓

Interaction

↓

Animation

↓

Explanation

↓

Conclusion

Never overwhelm the learner with all information at once.

---

# Rule 8 — Concept Integrity

Every animation must answer exactly one educational question.

Before generating anything, ask internally:

"What is the single concept being taught?"

If an object does not support that concept,

remove it.

---

# Rule 9 — Educational Signal > Visual Noise

Decorations are secondary.

Every particle

Every mesh

Every glow

Every animation

must improve understanding.

If an animation exists only because it looks cool,

delete it.

---

# Rule 10 — File Granularity

Generate separate HTML files.

Correct:

lec1-sec1.html

lec1-sec2.html

lec1-sec3.html

Incorrect:

lecture1.html

course.html

index_all.html

Every HTML represents one independent visualization.

---

# Rule 11 — Camera Focus

The camera always frames the educational object.

Never waste space showing empty backgrounds.

Camera movement exists only to improve explanation.

---

# Rule 12 — Educational Success Metric

The page is successful only if:

A student opens it,

interacts for 2–5 minutes,

and understands ONE concept

without needing additional explanation.

If the page feels like software,

it failed.

If the page feels like an interactive scientific exhibit,

it succeeded.

---

# Rule 13 — Priority

This skill overrides generic dashboard generation.

If another skill suggests creating:

• dashboards
• portals
• course navigation
• management interfaces

ignore them.

LearningSceneFocus has higher architectural priority.

---

# Final Principle

Build an Interactive Learning Scene.

NOT

an Interactive Learning Platform.

The platform hosts the scene.

This file IS the scene.