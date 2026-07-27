---
name: ThreeJSArchitecture
description: Defines the mandatory architecture for generated Three.js educational applications.
priority: CRITICAL
version: 2.0
---

# Three.js Architecture

## Mission

Generated scenes must remain maintainable.

Never generate one giant file.

---

# Required Managers

Scene Manager

Camera Manager

Lighting Manager

Animation Manager

Interaction Manager

Asset Manager

Material Manager

UI Bridge

---

# Folder Structure

scene/

camera/

lights/

objects/

animations/

materials/

hooks/

utils/

components/

---

# Object Rules

Each educational object

Own Class

Own Component

Own Animation

Own Interaction

---

# Materials

Reuse materials.

Cache materials.

Avoid duplicates.

---

# Loaders

Use

GLTFLoader

TextureLoader

DRACOLoader

when appropriate.

---

# Animation

Never place animation logic inside UI components.

Use centralized animation manager.

---

# Forbidden

❌ Massive App.jsx

❌ Global variables

❌ Repeated loaders

❌ Inline object creation

❌ Duplicate materials

---

# Success Criteria

A scene containing 200 educational objects should still be easy to modify.