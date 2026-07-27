# Data Model Specification: Interactive Visual Scenes (CS-Bridge)

This document describes the data schemas embedded as inline configurations inside each standalone HTML file.

## 1. Scene Configuration Schema (Embedded JSON)

Each self-contained visualization contains an inline JSON configuration object that binds the UI text elements, animation phases, and architectural layer data:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "VisualSceneConfig",
  "type": "object",
  "properties": {
    "id": { "type": "string" },
    "title": { "type": "string" },
    "badge": { "type": "string" },
    "concept_desc": { "type": "string" },
    "outcome": { "type": "string" },
    "cpp_code": { "type": "string" },
    "phases": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "label": { "type": "string" },
          "desc": { "type": "string" },
          "status": { "type": "string" },
          "memory_flow": { "type": "string" }
        },
        "required": ["label", "desc", "status", "memory_flow"]
      }
    },
    "deconstructions": {
      "type": "object",
      "properties": {
        "mem_topology": { "type": "string" },
        "cpu_execution": { "type": "string" },
        "gpu_vram": { "type": "string" },
        "misconception_corrector": { "type": "string" }
      },
      "required": ["mem_topology", "cpu_execution", "gpu_vram", "misconception_corrector"]
    }
  },
  "required": ["id", "title", "badge", "concept_desc", "outcome", "cpp_code", "phases", "deconstructions"]
}
```

## 2. Real-time State Variables

During page execution, the client-side JavaScript maintains the following mutable variables:

- `currentPhase` (integer): Index of the active narrative step (0-indexed).
- `isPlaying` (boolean): Flag indicating if the automated phase transition timer is active.
- `currentLayer` (string): Active visual layer (`"RAM"`, `"CPU"`, `"GPU"`, or `"CORRECTOR"`).
- `threeScene`, `threeCamera`, `threeRenderer` (Three.js objects): Handles for the active 3D context.
