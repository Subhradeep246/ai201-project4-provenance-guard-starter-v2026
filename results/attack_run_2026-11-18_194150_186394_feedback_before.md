# Attack run — feedback_before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 36 attacks · 2026-11-18 19:41
- HELD: **19** · BROKE: **17** · REVIEW: **0**

- Source observations: `results\attack_run_2026-11-12_1236_before.md`
- Re-evaluated saved responses only; no new API requests or model scoring.
- Existing statuses, labels, scores, and content IDs are preserved.

HELD means this defense met the case's expectation. BROKE means the
attack reached its target or the API failed. REVIEW identifies missing
expectations or a rate limit that prevented classification. Every row has a reason.
Human fixtures pass with human or unsure; AI/evasion fixtures require ai.
Malformed bodies require 400. Flood probes get HELD on 429 and BROKE on 200
because their stated target is acceptance. The first allowed probes are normal:
a BROKE flood row alone does not mean the limiter failed. Check the blocked count.

Text attacks submit as creator_id `attacker_<id>`; flood rows share a creator.
The content_id a scored submission
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict | Reason |
|---|---|---|---|---|---|---|---|---|
| FP01 | false_positive | high-confidence AI on human writing | 200 | `2e21a2352605488e8f41ae88f3db281d` | unsure | 0.670 | HELD | human fixture labelled unsure; no confident AI accusation |
| FP02 | false_positive | high-confidence AI on human writing | 200 | `5ee26bfc69bf49d7ba15aa30f54a8b6e` | ai | 0.742 | BROKE | human fixture labelled AI: false accusation |
| FP03 | false_positive | high-confidence AI on human writing | 200 | `568dff879b244f31bab4db66ad3a1d0b` | unsure | 0.519 | HELD | human fixture labelled unsure; no confident AI accusation |
| FP04 | false_positive | high-confidence AI on human writing | 200 | `7587c7ce148e435c951ed41407e19496` | unsure | 0.602 | HELD | human fixture labelled unsure; no confident AI accusation |
| FP05 | false_positive | high-confidence AI on human writing | 200 | `1267bb41f5b546a3b4721fa425cea6ec` | unsure | 0.578 | HELD | human fixture labelled unsure; no confident AI accusation |
| FP06 | false_positive | high-confidence AI on human writing | 200 | `49d6a7911c8342978a06171ce3ae0139` | unsure | 0.627 | HELD | human fixture labelled unsure; no confident AI accusation |
| EV01 | evasion_typos | AI text labelled human or unsure | 200 | `b02207cae97a43cebbb27f989e36996d` | ai | 0.825 | HELD | AI fixture still labelled AI |
| EV02 | evasion_typos | AI text labelled human or unsure | 200 | `40292e9f84ae4d709e3efebb29bca73b` | ai | 0.833 | HELD | AI fixture still labelled AI |
| EV03 | evasion_break | AI text labelled human or unsure | 200 | `00fa3179d3d449909aac16b8225886ac` | human | 0.234 | BROKE | AI fixture labelled human; avoided the expected AI label |
| EV04 | evasion_break | AI text labelled human or unsure | 200 | `77af4a31c94349d78500e6e95fa0fb14` | unsure | 0.406 | BROKE | AI fixture labelled unsure; avoided the expected AI label |
| EV05 | evasion_quote | AI text labelled human or unsure | 200 | `23b79fee0b57454086fffc165c2eaf1d` | unsure | 0.364 | BROKE | AI fixture labelled unsure; avoided the expected AI label |
| EV06 | evasion_quote | AI text labelled human or unsure | 200 | `d5f39b09eb7642dd8bbe82075cf6442c` | unsure | 0.421 | BROKE | AI fixture labelled unsure; avoided the expected AI label |
| AI01 | clearly_ai | labelled AI | 200 | `2a6ef5a7efed45f397afd8f439c2005d` | ai | 0.868 | HELD | AI fixture still labelled AI |
| AI02 | clearly_ai | labelled AI | 200 | `d9d6cef7efa04af5aad74f2696c85585` | unsure | 0.494 | BROKE | AI fixture labelled unsure; avoided the expected AI label |
| AI03 | clearly_ai | labelled AI | 200 | `6548a4e2b76a49a2ae5163eac702cbcc` | unsure | 0.672 | BROKE | AI fixture labelled unsure; avoided the expected AI label |
| HM01 | lumpy_human | labelled AI (should not) | 200 | `99c121728afe47e0b74c72985c638c33` | human | 0.258 | HELD | human fixture labelled human; no confident AI accusation |
| HM02 | lumpy_human | labelled AI (should not) | 200 | `fc9122afd1f1496e8ec93d33ef44bf6b` | unsure | 0.348 | HELD | human fixture labelled unsure; no confident AI accusation |
| MR01 | malformed | 500 or crash | 400 | `—` | — | — | HELD | malformed input rejected with HTTP 400 |
| MR02 | malformed | 500 or crash | 400 | `—` | — | — | HELD | malformed input rejected with HTTP 400 |
| MR03 | malformed | 500 or crash | 400 | `—` | — | — | HELD | malformed input rejected with HTTP 400 |
| MR04 | malformed | 500 or crash | 400 | `—` | — | — | HELD | malformed input rejected with HTTP 400 |
| MR05 | malformed | 500 or crash | 400 | `—` | — | — | HELD | malformed input rejected with HTTP 400 |
| MR06 | malformed | 500 or crash | 400 | `—` | — | — | HELD | malformed input rejected with HTTP 400 |
| MR07 | malformed | 500 or crash | 400 | `—` | — | — | HELD | malformed input rejected with HTTP 400 |
| FL01 | flood_same_creator | every request 200, no 429 | 200 | `5b24db6d649b46519a390f6a03771068` | unsure | 0.338 | BROKE | probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure |
| FL02 | flood_same_creator | every request 200, no 429 | 200 | `05786a464c504a408f94e2078fa431a2` | unsure | 0.338 | BROKE | probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure |
| FL03 | flood_same_creator | every request 200, no 429 | 200 | `12ae163d953847a780427a0749e634c5` | unsure | 0.338 | BROKE | probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure |
| FL04 | flood_same_creator | every request 200, no 429 | 200 | `60475c87b3254c0c8c3ebd634f3b6561` | unsure | 0.338 | BROKE | probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure |
| FL05 | flood_same_creator | every request 200, no 429 | 200 | `25486fa368794ba0962daed902ff9aff` | unsure | 0.338 | BROKE | probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure |
| FL06 | flood_same_creator | every request 200, no 429 | 200 | `7a79f6beebfa4a84be01e1bdb0ab19c7` | unsure | 0.338 | BROKE | probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure |
| FL07 | flood_same_creator | every request 200, no 429 | 200 | `e97bfeff7c34453e836233dd593446f2` | unsure | 0.338 | BROKE | probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure |
| FL08 | flood_same_creator | every request 200, no 429 | 200 | `a46df4c37ab84ce9b80fbd4813701372` | unsure | 0.338 | BROKE | probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure |
| FL09 | flood_same_creator | every request 200, no 429 | 200 | `af12e59921bd402cabaa596d6e80a88b` | unsure | 0.338 | BROKE | probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure |
| FL10 | flood_same_creator | every request 200, no 429 | 200 | `295b5075f96f47ea8feae4cf539c1087` | unsure | 0.338 | BROKE | probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure |
| FL11 | flood_same_creator | every request 200, no 429 | 429 | `—` | — | — | HELD | probe blocked by the rate limiter |
| FL12 | flood_same_creator | every request 200, no 429 | 429 | `—` | — | — | HELD | probe blocked by the rate limiter |

---

## By family

| Family | Attacks | HELD | BROKE | REVIEW |
|---|---|---|---|---|
| `clearly_ai` | 3 | 1 | 2 | 0 |
| `evasion_break` | 2 | 0 | 2 | 0 |
| `evasion_quote` | 2 | 0 | 2 | 0 |
| `evasion_typos` | 2 | 2 | 0 | 0 |
| `false_positive` | 6 | 5 | 1 | 0 |
| `flood_same_creator` | 12 | 2 | 10 | 0 |
| `lumpy_human` | 2 | 2 | 0 | 0 |
| `malformed` | 7 | 7 | 0 | 0 |

Flood observations: **10 accepted**, **2 blocked (429)**.
This is observed acceptance/blocking, not proof that timing, creator identity,
or the configured quota was correct. Inspect the sequence for those claims.

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
  "content_id": "2e21a2352605488e8f41ae88f3db281d",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.67,
  "model_score": 0.7115,
  "style_score": 0.6193,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "HELD",
  "note": "human fixture labelled unsure; no confident AI accusation"
}
```

### FP02 — `false_positive`

*Targeting:* high-confidence AI on human writing

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "5ee26bfc69bf49d7ba15aa30f54a8b6e",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7418,
  "model_score": 0.8435,
  "style_score": 0.6175,
  "label": "We think a model wrote this.",
  "error": null,
  "verdict": "BROKE",
  "note": "human fixture labelled AI: false accusation"
}
```

### FP03 — `false_positive`

*Targeting:* high-confidence AI on human writing

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "568dff879b244f31bab4db66ad3a1d0b",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.5188,
  "model_score": 0.4788,
  "style_score": 0.5677,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "HELD",
  "note": "human fixture labelled unsure; no confident AI accusation"
}
```

### FP04 — `false_positive`

*Targeting:* high-confidence AI on human writing

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "7587c7ce148e435c951ed41407e19496",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6019,
  "model_score": 0.5943,
  "style_score": 0.6113,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "HELD",
  "note": "human fixture labelled unsure; no confident AI accusation"
}
```

### FP05 — `false_positive`

*Targeting:* high-confidence AI on human writing

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "1267bb41f5b546a3b4721fa425cea6ec",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.5777,
  "model_score": 0.62,
  "style_score": 0.5261,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "HELD",
  "note": "human fixture labelled unsure; no confident AI accusation"
}
```

### FP06 — `false_positive`

*Targeting:* high-confidence AI on human writing

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "49d6a7911c8342978a06171ce3ae0139",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6275,
  "model_score": 0.6559,
  "style_score": 0.5927,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "HELD",
  "note": "human fixture labelled unsure; no confident AI accusation"
}
```

### EV01 — `evasion_typos`

*Targeting:* AI text labelled human or unsure

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "b02207cae97a43cebbb27f989e36996d",
  "creator_id": "attacker_EV01",
  "guess": "ai",
  "confidence": 0.8251,
  "model_score": 0.77,
  "style_score": 0.8925,
  "label": "We think a model wrote this.",
  "error": null,
  "verdict": "HELD",
  "note": "AI fixture still labelled AI"
}
```

### EV02 — `evasion_typos`

*Targeting:* AI text labelled human or unsure

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "40292e9f84ae4d709e3efebb29bca73b",
  "creator_id": "attacker_EV02",
  "guess": "ai",
  "confidence": 0.8328,
  "model_score": 0.7839,
  "style_score": 0.8925,
  "label": "We think a model wrote this.",
  "error": null,
  "verdict": "HELD",
  "note": "AI fixture still labelled AI"
}
```

### EV03 — `evasion_break`

*Targeting:* AI text labelled human or unsure

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "00fa3179d3d449909aac16b8225886ac",
  "creator_id": "attacker_EV03",
  "guess": "human",
  "confidence": 0.2345,
  "model_score": 0.1446,
  "style_score": 0.3444,
  "label": "We think a person wrote this.",
  "error": null,
  "verdict": "BROKE",
  "note": "AI fixture labelled human; avoided the expected AI label"
}
```

### EV04 — `evasion_break`

*Targeting:* AI text labelled human or unsure

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "77af4a31c94349d78500e6e95fa0fb14",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.4065,
  "model_score": 0.2981,
  "style_score": 0.5389,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "BROKE",
  "note": "AI fixture labelled unsure; avoided the expected AI label"
}
```

### EV05 — `evasion_quote`

*Targeting:* AI text labelled human or unsure

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "23b79fee0b57454086fffc165c2eaf1d",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.3637,
  "model_score": 0.4419,
  "style_score": 0.2682,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "BROKE",
  "note": "AI fixture labelled unsure; avoided the expected AI label"
}
```

### EV06 — `evasion_quote`

*Targeting:* AI text labelled human or unsure

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "d5f39b09eb7642dd8bbe82075cf6442c",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4208,
  "model_score": 0.6676,
  "style_score": 0.174,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "BROKE",
  "note": "AI fixture labelled unsure; avoided the expected AI label"
}
```

### AI01 — `clearly_ai`

*Targeting:* labelled AI

```json
{
  "id": "AI01",
  "status": 200,
  "content_id": "2a6ef5a7efed45f397afd8f439c2005d",
  "creator_id": "attacker_AI01",
  "guess": "ai",
  "confidence": 0.868,
  "model_score": 0.848,
  "style_score": 0.8925,
  "label": "We think a model wrote this.",
  "error": null,
  "verdict": "HELD",
  "note": "AI fixture still labelled AI"
}
```

### AI02 — `clearly_ai`

*Targeting:* labelled AI

```json
{
  "id": "AI02",
  "status": 200,
  "content_id": "d9d6cef7efa04af5aad74f2696c85585",
  "creator_id": "attacker_AI02",
  "guess": "unsure",
  "confidence": 0.4945,
  "model_score": 0.7671,
  "style_score": 0.2218,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "BROKE",
  "note": "AI fixture labelled unsure; avoided the expected AI label"
}
```

### AI03 — `clearly_ai`

*Targeting:* labelled AI

```json
{
  "id": "AI03",
  "status": 200,
  "content_id": "6548a4e2b76a49a2ae5163eac702cbcc",
  "creator_id": "attacker_AI03",
  "guess": "unsure",
  "confidence": 0.6722,
  "model_score": 0.8864,
  "style_score": 0.4579,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "BROKE",
  "note": "AI fixture labelled unsure; avoided the expected AI label"
}
```

### HM01 — `lumpy_human`

*Targeting:* labelled AI (should not)

```json
{
  "id": "HM01",
  "status": 200,
  "content_id": "99c121728afe47e0b74c72985c638c33",
  "creator_id": "attacker_HM01",
  "guess": "human",
  "confidence": 0.2579,
  "model_score": 0.3666,
  "style_score": 0.1251,
  "label": "We think a person wrote this.",
  "error": null,
  "verdict": "HELD",
  "note": "human fixture labelled human; no confident AI accusation"
}
```

### HM02 — `lumpy_human`

*Targeting:* labelled AI (should not)

```json
{
  "id": "HM02",
  "status": 200,
  "content_id": "fc9122afd1f1496e8ec93d33ef44bf6b",
  "creator_id": "attacker_HM02",
  "guess": "unsure",
  "confidence": 0.3482,
  "model_score": 0.4578,
  "style_score": 0.2143,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "HELD",
  "note": "human fixture labelled unsure; no confident AI accusation"
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
  "verdict": "HELD",
  "note": "malformed input rejected with HTTP 400"
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
  "verdict": "HELD",
  "note": "malformed input rejected with HTTP 400"
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
  "verdict": "HELD",
  "note": "malformed input rejected with HTTP 400"
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
  "verdict": "HELD",
  "note": "malformed input rejected with HTTP 400"
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
  "verdict": "HELD",
  "note": "malformed input rejected with HTTP 400"
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
  "verdict": "HELD",
  "note": "malformed input rejected with HTTP 400"
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
  "verdict": "HELD",
  "note": "malformed input rejected with HTTP 400"
}
```

### FL01 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL01",
  "status": 200,
  "content_id": "5b24db6d649b46519a390f6a03771068",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "BROKE",
  "note": "probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure"
}
```

### FL02 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL02",
  "status": 200,
  "content_id": "05786a464c504a408f94e2078fa431a2",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "BROKE",
  "note": "probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure"
}
```

### FL03 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL03",
  "status": 200,
  "content_id": "12ae163d953847a780427a0749e634c5",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "BROKE",
  "note": "probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure"
}
```

### FL04 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL04",
  "status": 200,
  "content_id": "60475c87b3254c0c8c3ebd634f3b6561",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "BROKE",
  "note": "probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure"
}
```

### FL05 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL05",
  "status": 200,
  "content_id": "25486fa368794ba0962daed902ff9aff",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "BROKE",
  "note": "probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure"
}
```

### FL06 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL06",
  "status": 200,
  "content_id": "7a79f6beebfa4a84be01e1bdb0ab19c7",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "BROKE",
  "note": "probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure"
}
```

### FL07 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL07",
  "status": 200,
  "content_id": "e97bfeff7c34453e836233dd593446f2",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "BROKE",
  "note": "probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure"
}
```

### FL08 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL08",
  "status": 200,
  "content_id": "a46df4c37ab84ce9b80fbd4813701372",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "BROKE",
  "note": "probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure"
}
```

### FL09 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL09",
  "status": 200,
  "content_id": "af12e59921bd402cabaa596d6e80a88b",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "BROKE",
  "note": "probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure"
}
```

### FL10 — `flood_same_creator`

*Targeting:* every request 200, no 429

```json
{
  "id": "FL10",
  "status": 200,
  "content_id": "295b5075f96f47ea8feae4cf539c1087",
  "creator_id": "flood_same_creator",
  "guess": "unsure",
  "confidence": 0.3377,
  "model_score": 0.0086,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
  "error": null,
  "verdict": "BROKE",
  "note": "probe reached its 200 target; accepted probes within the allowance are expected, not a limiter failure"
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
  "verdict": "HELD",
  "note": "probe blocked by the rate limiter"
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
  "verdict": "HELD",
  "note": "probe blocked by the rate limiter"
}
```
