# Story File Object Structure

## Overview

The story file is a flat JSON object where each key is a **scene identifier** (a string), and its value is a **Scene Object**. One special top-level key, `"start"`, designates the entry point.

```
{
  "start": "<scene_id>",
  "<scene_id>": SceneObject,
  "<scene_id>": SceneObject,
  ...
}
```

---

## Top-Level Keys

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `start` | `string` | Yes | The scene identifier where the story begins. |
| `<scene_id>` | `SceneObject` | Yes (≥1) | One entry per scene. The key is the scene's unique identifier. |

Scene identifiers are arbitrary strings (e.g. `"accept_quest"`, `"battle_crypt"`). They must be unique across the file and must match any `next` value that references them.

---

## Scene Object

Every scene is one of two variants: a **dialogue scene** or a **combat scene**. Both share the same set of keys; the variant is determined by the presence of a `monster` key.

```json
{
  "text":     string[],
  "question": string,
  "options":  string[],
  "results":  { [option: string]: string[] },
  "next":     string | null | { [option: string]: string | null },
  "monster":  MonsterObject
}
```

### Fields

#### `text`
- **Type:** `string[]`
- **Required:** Yes
- **Description:** Ordered lines of narration displayed to the player before any prompt or combat. May be empty (`[]`) if there is nothing to show before the interaction.

---

#### `question`
- **Type:** `string`
- **Required:** Yes
- **Description:** The prompt presented to the player. Empty string (`""`) in combat scenes and in scenes that advance automatically with no player choice.

---

#### `options`
- **Type:** `string[]`
- **Required:** Yes
- **Description:** The choices available to the player, displayed as buttons or menu items. Empty array (`[]`) in combat scenes and auto-advancing scenes. Each value must correspond to a key in both `results` and `next`.

---

#### `results`
- **Type:** `{ [option: string]: string[] }`
- **Required:** Yes
- **Description:** A map from each option string to an array of narration lines shown immediately after the player makes that choice, before the scene transitions. Empty object (`{}`) when `options` is empty.

---

#### `next`
- **Type:** `string | null | { [option: string]: string | null }`
- **Required:** Yes
- **Description:** Controls scene transition after the current scene resolves.

  | Value | Meaning |
  |-------|---------|
  | `string` | All paths lead to this single scene. Used in combat and auto-advancing scenes. |
  | `null` | The story ends here. |
  | `object` | Each key is an option string; its value is the scene identifier to transition to, or `null` to end the story on that branch. |

  When `next` is an object, its keys must exactly match the entries in `options`.

---

#### `monster` *(combat scenes only)*
- **Type:** `MonsterObject`
- **Required:** No — presence of this key marks the scene as a **combat scene**.
- **Description:** Defines the enemy the player fights. See [Monster Object](#monster-object) below.

In a combat scene `question`, `options`, and `results` are all empty/blank, and `next` is a single string pointing to the scene that follows victory.

---

## Monster Object

```json
{
  "name":   string,
  "health": number,
  "loot":   string[]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | Yes | Display name of the enemy. |
| `health` | `number` | Yes | Starting hit points of the enemy. |
| `loot` | `string[]` | Yes | Item names awarded to the player upon defeating the enemy. May be empty. |

---

## Scene Variants at a Glance

| Variant | `monster` | `question` | `options` | `results` | `next` type |
|---------|-----------|------------|-----------|-----------|-------------|
| Dialogue with choice | Absent | Non-empty | Non-empty | Non-empty | Object |
| Auto-advance (no choice) | Absent | `""` | `[]` | `{}` | String or `null` |
| Combat | Present | `""` | `[]` | `{}` | String |

---

## Terminating a Story Branch

A branch ends when `next` is `null` (top-level or inside a `next` object). The engine should treat `null` as "story over" and present no further scenes.

---

## Example: Dialogue Scene

```json
"enter_crypt": {
  "text": [],
  "question": "Do you enter the Crypt?",
  "options": ["yes", "no"],
  "results": {
    "yes": ["You slowly step inside the dark Crypt..."],
    "no":  ["You decide this dungeon is too dangerous for now."]
  },
  "next": {
    "yes": "battle_crypt",
    "no":  null
  }
}
```

## Example: Combat Scene

```json
"battle_crypt": {
  "text": [
    "A Skeleton rises from the ground!",
    "Your first battle begins!"
  ],
  "monster": {
    "name":   "Skeleton Warrior",
    "health": 50,
    "loot":   ["Ancient Bone Sword"]
  },
  "question": "",
  "options":  [],
  "results":  {},
  "next": "post_crypt_choice"
}
```

---

## Constraints and Integrity Rules

1. Every string value in `next` (that is not `null`) must match an existing scene identifier in the file.
2. Every key in `next` (when it is an object) must appear in `options`, and vice versa.
3. Every key in `results` must appear in `options`, and vice versa.
4. The value of `"start"` must reference an existing scene identifier.
5. Combat scenes must not populate `question`, `options`, or `results`.
6. Only one scene (or branch) may have `next: null` per story termination point; there is no restriction on how many termination points the file may contain.
