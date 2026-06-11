# BCTR v4 Canon — Frozen

**Stable objects survive questioning. Questioning generates tails. Tails reveal debt. Packets pay debt. Return verifies ownership. The tail becomes the next core. Wrong answers are coordinates.**

## Version

v4 — frozen as of June 2026

## Change Policy

Any change to the invariant requires incrementing the major version (v5). The invariant cannot change within a major version.

## The Invariant in Code

```json
{
  "success_criteria": "do + explain + rebuild + return",
  "debt_types": ["entry", "continuity", "transformation", "reconstruction", "return"],
  "packet_steps_min": 3,
  "packet_steps_max": 5
}

---

### 3. `schema/bctr.v4.schema.json` — Machine-Readable Contract

```json
{
  "$schema": "https://json-schema.org/draft/07/schema",
  "$id": "https://bctr.dev/v4/crossing.schema.json",
  "title": "BCTR Crossing Request",
  "version": "4.0",
  "type": "object",
  "properties": {
    "object": { "type": "string" },
    "observed_input": { "type": "string" },
    "agent_type": { "type": "string", "enum": ["human", "ai", "group", "organization"] }
  },
  "required": ["object", "observed_input"],
  "definitions": {
    "debt_type": {
      "type": "string",
      "enum": ["entry", "continuity", "transformation", "reconstruction", "return", "mixed"]
    },
    "packet": {
      "type": "object",
      "properties": {
        "packet_id": { "type": "string" },
        "debt_type": { "$ref": "#/definitions/debt_type" },
        "steps": { "type": "array", "items": { "type": "string" }, "minItems": 3, "maxItems": 5 },
        "retest": { "type": "string" },
        "success_criteria": { "type": "string", "const": "do + explain + rebuild + return" }
      }
    }
  }
}
