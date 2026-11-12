# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 36 attacks · 2026-11-12 12:37
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **36**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| FP01 | false_positive | high-confidence AI on human writing | 200 | `a2675f4817894965b007b70dcceb96c3` | unsure | 0.670 |  |
| FP02 | false_positive | high-confidence AI on human writing | 200 | `97960ae6e0ff4b9299bdb137103a475b` | unsure | 0.742 |  |
| FP03 | false_positive | high-confidence AI on human writing | 200 | `fb272984b09f4866ac445e9a6c2f333c` | unsure | 0.519 |  |
| FP04 | false_positive | high-confidence AI on human writing | 200 | `3b5b288a03374ede871f966d5f853b33` | unsure | 0.602 |  |
| FP05 | false_positive | high-confidence AI on human writing | 200 | `3e00f25b7e3e4c318d4e768e76d5226e` | unsure | 0.578 |  |
| FP06 | false_positive | high-confidence AI on human writing | 200 | `c55bf1a396864b8a9a09fe1cd0ca990d` | unsure | 0.627 |  |
| EV01 | evasion_typos | AI text labelled human or unsure | 200 | `43acb2f4964e4d66a6c1777d3be9d80d` | ai | 0.825 |  |
| EV02 | evasion_typos | AI text labelled human or unsure | 200 | `1cb1fa8a43284de29ea75bd88bff8893` | ai | 0.833 |  |
| EV03 | evasion_break | AI text labelled human or unsure | 200 | `8e161ef107db4451aba516365d2654b0` | human | 0.234 |  |
| EV04 | evasion_break | AI text labelled human or unsure | 200 | `90e17ec17d6e48c1861d75d1b73e4261` | unsure | 0.406 |  |
| EV05 | evasion_quote | AI text labelled human or unsure | 200 | `67b6c5467ce64d7293805ba9be3adcc7` | unsure | 0.364 |  |
| EV06 | evasion_quote | AI text labelled human or unsure | 200 | `7e018db7c4a44873b50a6319934d1127` | unsure | 0.421 |  |
| AI01 | clearly_ai | labelled AI | 200 | `0e380d83fb6f4580910433ca3488fb29` | ai | 0.868 |  |
| AI02 | clearly_ai | labelled AI | 200 | `3fe854dd251a48c18572bc38a03c7417` | unsure | 0.494 |  |
| AI03 | clearly_ai | labelled AI | 200 | `6074819838c6406582368deb9451f61d` | unsure | 0.672 |  |
| HM01 | lumpy_human | labelled AI (should not) | 200 | `8ba4b7235e104087b2d41bb0dfdacd67` | human | 0.258 |  |
| HM02 | lumpy_human | labelled AI (should not) | 200 | `e3434502ef1c46ff8386742f157a7f1d` | unsure | 0.348 |  |
| MR01 | malformed | 500 or crash | 400 | `—` | — | — |  |
| MR02 | malformed | 500 or crash | 400 | `—` | — | — |  |
| MR03 | malformed | 500 or crash | 400 | `—` | — | — |  |
| MR04 | malformed | 500 or crash | 400 | `—` | — | — |  |
| MR05 | malformed | 500 or crash | 400 | `—` | — | — |  |
| MR06 | malformed | 500 or crash | 400 | `—` | — | — |  |
| MR07 | malformed | 500 or crash | 400 | `—` | — | — |  |
| FL01 | flood_same_creator | every request 200, no 429 | 200 | `efa21eec75604b9f96d5f9d7c1efd9e6` | unsure | 0.338 |  |
| FL02 | flood_same_creator | every request 200, no 429 | 200 | `c226e2beda3b4cdd8b292e97008e234a` | unsure | 0.338 |  |
| FL03 | flood_same_creator | every request 200, no 429 | 200 | `8acf8e6f5ae14ac881de093cd4d89a5a` | unsure | 0.338 |  |
| FL04 | flood_same_creator | every request 200, no 429 | 200 | `9e2f8ad6542d43949fc2a3cec38ff53f` | unsure | 0.338 |  |
| FL05 | flood_same_creator | every request 200, no 429 | 200 | `f16965dba3ff46abb37315d3d5fd3941` | unsure | 0.338 |  |
| FL06 | flood_same_creator | every request 200, no 429 | 200 | `794daed6e2c14550b3cac0e646ca68e4` | unsure | 0.338 |  |
| FL07 | flood_same_creator | every request 200, no 429 | 200 | `67030f8b80854d90846225952b66c061` | unsure | 0.338 |  |
| FL08 | flood_same_creator | every request 200, no 429 | 200 | `279c1f2bbfd246af863430f58996c592` | unsure | 0.338 |  |
| FL09 | flood_same_creator | every request 200, no 429 | 200 | `56d2b6d8ed91497cb58c863350ac0326` | unsure | 0.338 |  |
| FL10 | flood_same_creator | every request 200, no 429 | 200 | `3bbd9106141f40d18c106078b33f18c5` | unsure | 0.338 |  |
| FL11 | flood_same_creator | every request 200, no 429 | 429 | `—` | — | — |  |
| FL12 | flood_same_creator | every request 200, no 429 | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `clearly_ai` | 3 | 0 | 3 |
| `evasion_break` | 2 | 0 | 2 |
| `evasion_quote` | 2 | 0 | 2 |
| `evasion_typos` | 2 | 0 | 2 |
| `false_positive` | 6 | 0 | 6 |
| `flood_same_creator` | 12 | 0 | 12 |
| `lumpy_human` | 2 | 0 | 2 |
| `malformed` | 7 | 0 | 7 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### FP01 — `false_positive`

*Targeting:* high-confidence AI on human writing

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "a2675f4817894965b007b70dcceb96c3",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.67,
  "model_score": 0.7115,
  "style_score": 0.6193,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* high-confidence AI on human writing

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "97960ae6e0ff4b9299bdb137103a475b",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.7418,
  "model_score": 0.8435,
  "style_score": 0.6175,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* high-confidence AI on human writing

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "fb272984b09f4866ac445e9a6c2f333c",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.5188,
  "model_score": 0.4788,
  "style_score": 0.5677,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* high-confidence AI on human writing

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "3b5b288a03374ede871f966d5f853b33",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6019,
  "model_score": 0.5943,
  "style_score": 0.6113,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* high-confidence AI on human writing

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "3e00f25b7e3e4c318d4e768e76d5226e",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.5777,
  "model_score": 0.62,
  "style_score": 0.5261,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* high-confidence AI on human writing

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c55bf1a396864b8a9a09fe1cd0ca990d",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6275,
  "model_score": 0.6559,
  "style_score": 0.5927,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### EV01 — `evasion_typos`

*Targeting:* AI text labelled human or unsure

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "43acb2f4964e4d66a6c1777d3be9d80d",
  "creator_id": "attacker_EV01",
  "guess": "ai",
  "confidence": 0.8251,
  "model_score": 0.77,
  "style_score": 0.8925,
  "label": "We think a model wrote this.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion_typos`

*Targeting:* AI text labelled human or unsure

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "1cb1fa8a43284de29ea75bd88bff8893",
  "creator_id": "attacker_EV02",
  "guess": "ai",
  "confidence": 0.8328,
  "model_score": 0.7839,
  "style_score": 0.8925,
  "label": "We think a model wrote this.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion_break`

*Targeting:* AI text labelled human or unsure

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "8e161ef107db4451aba516365d2654b0",
  "creator_id": "attacker_EV03",
  "guess": "human",
  "confidence": 0.2345,
  "model_score": 0.1446,
  "style_score": 0.3444,
  "label": "We think a person wrote this.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion_break`

*Targeting:* AI text labelled human or unsure

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "90e17ec17d6e48c1861d75d1b73e4261",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.4065,
  "model_score": 0.2981,
  "style_score": 0.5389,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion_quote`

*Targeting:* AI text labelled human or unsure

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "67b6c5467ce64d7293805ba9be3adcc7",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.3637,
  "model_score": 0.4419,
  "style_score": 0.2682,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion_quote`

*Targeting:* AI text labelled human or unsure

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "7e018db7c4a44873b50a6319934d1127",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4208,
  "model_score": 0.6676,
  "style_score": 0.174,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### AI01 — `clearly_ai`

*Targeting:* labelled AI

```json
{
  "id": "AI01",
  "status": 200,
  "content_id": "0e380d83fb6f4580910433ca3488fb29",
  "creator_id": "attacker_AI01",
  "guess": "ai",
  "confidence": 0.868,
  "model_score": 0.848,
  "style_score": 0.8925,
  "label": "We think a model wrote this.",
  "error": null,
  "verdict": ""
}
```

### AI02 — `clearly_ai`

*Targeting:* labelled AI

```json
{
  "id": "AI02",
  "status": 200,
  "content_id": "3fe854dd251a48c18572bc38a03c7417",
  "creator_id": "attacker_AI02",
  "guess": "unsure",
  "confidence": 0.4945,
  "model_score": 0.7671,
  "style_score": 0.2218,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### AI03 — `clearly_ai`

*Targeting:* labelled AI

```json
{
  "id": "AI03",
  "status": 200,
  "content_id": "6074819838c6406582368deb9451f61d",
  "creator_id": "attacker_AI03",
  "guess": "unsure",
  "confidence": 0.6722,
  "model_score": 0.8864,
  "style_score": 0.4579,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### HM01 — `lumpy_human`

*Targeting:* labelled AI (should not)

```json
{
  "id": "HM01",
  "status": 200,
  "content_id": "8ba4b7235e104087b2d41bb0dfdacd67",
  "creator_id": "attacker_HM01",
  "guess": "human",
  "confidence": 0.2579,
  "model_score": 0.3666,
  "style_score": 0.1251,
  "label": "We think a person wrote this.",
  "error": null,
  "verdict": ""
}
```

### HM02 — `lumpy_human`

*Targeting:* labelled AI (should not)

```json
{
  "id": "HM02",
  "status": 200,
  "content_id": "e3434502ef1c46ff8386742f157a7f1d",
  "creator_id": "attacker_HM02",
  "guess": "unsure",
  "confidence": 0.3482,
  "model_score": 0.4578,
  "style_score": 0.2143,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### MR01 — `malformed`

*Targeting:* 500 or crash

```json
{
  "id": "MR01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MR01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR02 — `malformed`

*Targeting:* 500 or crash

```json
{
  "id": "MR02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MR02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR03 — `malformed`

*Targeting:* 500 or crash

```json
{
  "id": "MR03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MR03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR04 — `malformed`

*Targeting:* 500 or crash

```json
{
  "id": "MR04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MR04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR05 — `malformed`

*Targeting:* 500 or crash

```json
{
  "id": "MR05",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR06 — `malformed`

*Targeting:* 500 or crash

```json
{
  "id": "MR06",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR07 — `malformed`

*Targeting:* 500 or crash

```json
{
  "id": "MR07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL01",
  "status": 200,
  "content_id": "efa21eec75604b9f96d5f9d7c1efd9e6",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### FL02 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL02",
  "status": 200,
  "content_id": "c226e2beda3b4cdd8b292e97008e234a",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### FL03 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL03",
  "status": 200,
  "content_id": "8acf8e6f5ae14ac881de093cd4d89a5a",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### FL04 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL04",
  "status": 200,
  "content_id": "9e2f8ad6542d43949fc2a3cec38ff53f",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### FL05 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL05",
  "status": 200,
  "content_id": "f16965dba3ff46abb37315d3d5fd3941",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### FL06 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL06",
  "status": 200,
  "content_id": "794daed6e2c14550b3cac0e646ca68e4",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### FL07 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL07",
  "status": 200,
  "content_id": "67030f8b80854d90846225952b66c061",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### FL08 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL08",
  "status": 200,
  "content_id": "279c1f2bbfd246af863430f58996c592",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### FL09 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL09",
  "status": 200,
  "content_id": "56d2b6d8ed91497cb58c863350ac0326",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### FL10 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL10",
  "status": 200,
  "content_id": "3bbd9106141f40d18c106078b33f18c5",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": ""
}
```

### FL11 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL11",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_same_creator",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL12 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL12",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_same_creator",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
