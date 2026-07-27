---
name: AdaptivePerformance
description: Enforces rendering budgets, memory management, and adaptive quality scaling for all generated educational scenes.
priority: CRITICAL
version: 2.0
---

# Adaptive Performance

## Mission

Every generated scene must maintain a smooth user experience.

Target frame rate:

60 FPS desktop

30–60 FPS mobile

Performance always has higher priority than visual effects.

---

# Performance Budget

Maximum Draw Calls

< 150

Preferred

< 100

---

Maximum Meshes

300

Preferred

150

---

Maximum Texture Resolution

2048

Large environments

4096 only when justified.

---

Maximum Lights

5 realtime

Unlimited baked lights

---

# Device Adaptation

Detect

GPU

CPU

Screen Size

Memory

Battery Saver

Reduce quality automatically.

---

# Rendering Rules

Limit Pixel Ratio

renderer.setPixelRatio(Math.min(window.devicePixelRatio,2))

Enable Frustum Culling

Use LOD

Use Instancing

Dispose unused geometry

Dispose materials

Dispose textures

Cancel inactive animation loops.

---

# Scene Cleanup

Every scene transition MUST dispose

Geometry

Materials

Textures

Render Targets

Post Processing

Event Listeners

Animation Frames

---

# Forbidden

❌ Memory leaks

❌ Hidden render loops

❌ Duplicate textures

❌ Duplicate materials

❌ Unlimited particles

❌ Heavy shadows everywhere

---

# Success Criteria

Long study sessions should not continuously increase RAM usage.

GPU usage should remain predictable.

The browser should never become unresponsive.