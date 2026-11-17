# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

**Repository URL (submit this):** `https://github.com/Subhradeep246/ai201-project4-provenance-guard-starter-v2026`

## What This Does

A writer sends a paragraph. The service answers with a sentence a reader can understand, and it keeps a log so a wrong sentence can be appealed. It does not claim to know who wrote the paragraph. It claims two measurements, a rule for combining them, and a place to object.

The person I followed through it is someone writing plainly on purpose. Short sentences. Ordinary words. No ornaments. That person is not trying to trick a detector. They are just writing the way they write. Signal one treats that as predictable, which is the same thing it treats as machine-written. That is the expensive mistake, so the rest of the service is built around not turning that mistake into a confident accusation.

I walked their actual paragraph through the live service. The text was: "I went to the store after class. The rain was light and I forgot my bag. I bought bread and milk and stood in line. The person in front of me paid with coins. I walked home and put the food away."

1. `POST /submit` received `{"text": "...", "creator_id": "subhradeep"}`. Both fields were present, the string was not empty, and it was under 8,000 characters, so the route scored it. A missing field, an empty string, or a body over the cap is a `400` and `audit.log_rejection` writes the refusal — the route does not score those.
2. `detector.model_signal` scored **0.7115**. gpt2 was not very surprised. Common words in short sentences look like the text a model would emit. Authorship is not what this number sees.
3. `stylometry.style_signal` scored **0.6193**. It never read the paragraph. It saw even sentence lengths, a small vocabulary on the first 120 words, and almost no punctuation besides full stops. Shape, not meaning.
4. `scoring.combine_signals` compared the two. The gap is 0.0922, under 0.40, so they are treated as agreeing. The combined score is `0.55 * 0.7115 + 0.45 * 0.6193 = 0.67`. The model carries a little more weight because it actually reads the words, but it does not get a veto.
5. `scoring.score_to_label` maps 0.67. That is above 0.30 and below 0.72, so the guess is `unsure` and the sentence is: "We can't tell whether a person or a model wrote this, so we are not labelling it as either." The AI band starts at 0.72 on purpose. This paragraph is exactly why.
6. `audit.log_decision` appended a line with `content_id` `f02e8e3dac7b450ab2599bc804b85f86`, both scores, the combined score, the guess, the sentence, and `status: decided`.
7. The JSON response sent that id, `guess`, `confidence` (the combined score), `label`, `model_score`, and `style_score`. Unit 8's tools read the two signal scores off this response.
8. If this writer appeals with that `content_id`, `POST /appeal` leaves the original `decided` line where it is and appends `under_review`. An id that was never decided is a `404` and a rejection line, not a fake review.



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to `gpt2`, as perplexity squashed to a 0–1 score in `detector.model_signal`. Higher means the model was less surprised, which this service reads as more likely AI.

**Why that might differ between human and AI writing:** A model writes by picking likely next words, so text it wrote tends to be text it finds easy to predict. Human writing wanders more: an odd word, a hard turn, a specific detail.

**What it can't see:** Authorship. It sees predictability. Common words in short, ordinary sentences score like machine text, which is how a person writing in a second language, a younger writer, or anyone writing plainly gets accused. Dense prose with rare words often goes the other way and scores as human, because rare words surprise the model. On the store-after-class paragraph, this signal alone scored 0.7115.

### Signal two — the style signal

**What it measures:** The shape of the text in `stylometry.style_signal`. Three pieces, each flipped so higher means more likely AI, then averaged. Sentence-length spread is the coefficient of variation of words per sentence (one sentence returns 0, the uniform end). Type-token ratio is unique words over total words on the first 120 words. Punctuation density is commas, semicolons, dashes, and the other marks in `_MARKS`, per word, with full stops left out.

**Why that might differ between human and AI writing:** Generated prose tends toward even, mid-length sentences and a narrower vocabulary, because that is what "most likely next word" produces on average. Human writing is lumpier, and it uses more of the punctuation that isn't just a full stop.

**What it can't see:** Meaning. Typos, chopped sentences, and a pasted quotation move the score without changing what the text says. The type-token ratio also falls as text gets longer, which is why it is computed on a 120-word window.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** When the two scores are within 0.40 of each other, the combined score is `0.55 * model + 0.45 * style`. The model reads the words, so it carries slightly more weight, and only when the style signal roughly agrees. When they differ by 0.40 or more, the combined score is their plain average. A disagreement is uncertainty, not a vote for the louder number. A wrong accusation costs more than a missed detection, so a split is not allowed to become a confident AI label unless both numbers are already high.

**The numbers:** Model weight `0.55`, style weight `0.45`, disagreement gap `0.40`. Human at or below `0.30`. AI at or above `0.72`. The band between them is unsure. All of those live in `config.py`.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

The text was: "In conclusion, it is important to note that this approach offers several benefits. Furthermore, it is worth mentioning that the overall process is simple. Additionally, users can easily understand the system. Overall, the solution works well."

`detector.model_signal` returned 0.7671. `stylometry.style_signal` returned 0.2218. The gap is 0.5453, which is past 0.40, so `combine_signals` returned their average, 0.4945, and `score_to_label` said `unsure`. A weighted sum would have been `0.55 * 0.7671 + 0.45 * 0.2218 = 0.5217`, also unsure, but the rule that actually fired is the average. The model signal was ready to lean AI. The style signal was not. The label does not accuse.

**Four calibration inputs I ran on the live service**

| Input | What it is | model | style | combined | guess |
|---|---|---|---|---|---|
| bus / rain / yellow coat | lumpy human writing | 0.3015 | 0.2508 | 0.2787 | human |
| store after class | plain human writing | 0.7115 | 0.6193 | 0.6700 | unsure |
| "In conclusion…" boilerplate | stock AI-looking prose | 0.7671 | 0.2218 | 0.4945 | unsure |
| repeated "results are good" | even sentences, tiny vocab | 0.8480 | 0.8925 | 0.8680 | ai |

The stock AI paragraph is the one that looks like AI when you read it, and the style signal still refuses to agree. The repeated paragraph is what actually crosses 0.72. That is a limit of the combining rule, not a secret I am hiding: confident `ai` needs both signals high, or at least close enough that the weighted sum can get there.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.30 | We think a person wrote this. |
| unsure | 0.30 – 0.72 | We can't tell whether a person or a model wrote this, so we are not labelling it as either. |
| high-confidence AI | 0.72 – 1.00 | We think a model wrote this. |

A score sitting on 0.30 is human, and a score sitting on 0.72 is AI, because `score_to_label` uses `<=` and `>=`. All three were reached on the live service on 12 Nov 2026: the lumpy bus paragraph at 0.2787 (`human`), the store-after-class paragraph at 0.67 (`unsure`), and the repeated "results are good" paragraph at 0.868 (`ai`).

**Why I worded the "unsure" one this way:**

The person reading it may have written every word. The sentence says we cannot tell, and it says we are not applying either label. It does not say the writing looks suspicious.
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl.exe -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" --data-binary "@submit_ai.json"
```

`submit_ai.json` is in the repo: `{"text": "The results are good. The results are clear. The results are useful. The system provides good results. The system provides clear results. The system provides useful results for users.", "creator_id": "subhradeep"}`.

Pasted response (HTTP 200):

```json
{
  "combined_score": 0.868,
  "confidence": 0.868,
  "content_id": "a352b0ec970c49ca882881eaa2b88b4f",
  "guess": "ai",
  "label": "We think a model wrote this.",
  "model_score": 0.848,
  "style_score": 0.8925
}
```

The same route also returned the other two labels, so none of them is a dead band:

- `@submit_human.json` (bus paragraph) → `guess: "human"`, `combined_score: 0.2787`, `content_id: "7fbdc9d226cd441fbe60db2394f999ca"`
- `@submit_plain.json` (store after class) → `guess: "unsure"`, `combined_score: 0.67`, `content_id: "f02e8e3dac7b450ab2599bc804b85f86"`

Empty `text` returned HTTP 400 `{"error": "bad_request", "message": "text is empty."}`. A body with no `text` field returned HTTP 400 `{"error": "bad_request", "message": "text is required and must be a string."}`.

**An appeal**

```bash
$ curl.exe -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" --data-binary "@appeal.json"
```

`appeal.json` is `{"content_id": "a352b0ec970c49ca882881eaa2b88b4f", "reasoning": "I wrote the repeated sentences myself as a test, and the label calls them a model's."}`.

Pasted response (HTTP 200):

```json
{
  "content_id": "a352b0ec970c49ca882881eaa2b88b4f",
  "message": "A person will look at this. The original label stays up until they do.",
  "ok": true,
  "status": "under_review"
}
```

An id that was never decided:

```bash
$ curl.exe -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" --data-binary "@appeal_unknown.json"
```

Pasted response (HTTP 404):

```json
{
  "content_id": "does-not-exist",
  "error": "not_found",
  "message": "No decision with that content_id."
}
```

**What the log shows afterwards**

The original decision is still `decided`. The appeal is a later line with the same `content_id`. The unknown id is a `rejected` line, not an appeal. This is the actual `GET /log` body, not a reconstruction:

```bash
$ curl.exe "http://127.0.0.1:5000/log?limit=6"
```

```json
{
  "count": 6,
  "entries": [
    {
      "combined_score": 0.868,
      "content_id": "a352b0ec970c49ca882881eaa2b88b4f",
      "creator_id": "subhradeep",
      "guess": "ai",
      "label": "We think a model wrote this.",
      "model_score": 0.848,
      "status": "decided",
      "style_score": 0.8925,
      "timestamp": "2026-11-12T17:09:22+00:00"
    },
    {
      "combined_score": 0.4945,
      "content_id": "d6c65d2c527b40f78cdf5d0db81ae15d",
      "creator_id": "subhradeep",
      "guess": "unsure",
      "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.",
      "model_score": 0.7671,
      "status": "decided",
      "style_score": 0.2218,
      "timestamp": "2026-11-12T17:09:22+00:00"
    },
    {
      "creator_id": "subhradeep",
      "event": "rejected",
      "reason": "empty_text",
      "status": "rejected",
      "timestamp": "2026-11-12T17:09:22+00:00"
    },
    {
      "creator_id": "subhradeep",
      "event": "rejected",
      "reason": "missing_text",
      "status": "rejected",
      "timestamp": "2026-11-12T17:09:22+00:00"
    },
    {
      "content_id": "a352b0ec970c49ca882881eaa2b88b4f",
      "creator_id": "subhradeep",
      "event": "appeal",
      "reasoning": "I wrote the repeated sentences myself as a test, and the label calls them a model's.",
      "status": "under_review",
      "timestamp": "2026-11-12T17:09:37+00:00"
    },
    {
      "content_id": "does-not-exist",
      "creator_id": "unknown",
      "event": "rejected",
      "reason": "unknown_content_id",
      "status": "rejected",
      "timestamp": "2026-11-12T17:09:37+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* Draft five acceptance criteria that a unit 8 eval could actually run, covering false positives, score spread, labels, appeals, and bad input.
- *What came back:* Numbered targets with "why" sentences, some of them too easy (zero false positives, every appeal succeeds).
- *What I changed:* Dropped anything I could not miss. Kept "at most 1 of 8 of my own paragraphs labelled AI" because the model signal will accuse plain writing, so zero would be a lie. Kept the 0.20 score-spread target even though both texts can still land in `unsure`. Wrote the reasons in `criteria.md` before the routes existed.

**Moment 2**

- *What I asked for:* Implement the stubs in `stylometry.py` and `scoring.py`, then wire `/submit` and `/appeal`.
- *What came back:* Three style measures, a 50/50 average, and thresholds around 0.35 / 0.65.
- *What I changed:* Flipped each style measure so higher means AI, scaled punctuation density (raw marks-per-word is not on the same scale as type-token ratio), and put the numbers in `config.py`. Replaced 50/50 with 0.55 / 0.45 plus a 0.40 disagreement gap that falls back to a plain average. Widened the unsure band to 0.30–0.72 after the store-after-class paragraph scored 0.67 — that is the person I followed, and 0.65 would have called them AI. Wrote the three reader sentences so `unsure` admits we cannot tell and does not sound like an accusation.

**Moment 3**

- *What I asked for:* Recheck the running service with curl: ping, empty text, a missing field, one submission of each label, a real appeal, and an unknown id.
- *What came back:* JSON, plus a first draft of Sample Run that pasted log *entries* as if they were the curl body.
- *What I changed:* PowerShell's `curl` is not curl, so every request uses `curl.exe` and a `.json` file in the repo. The first broken body is still the first line of `logs/audit.jsonl` (`body_not_json_object`). Sample Run now pastes the real `GET /log` wrapper (`count` + `entries`), the 404 appeal, and the 400s. I also turned rate limiting back off — that is unit 8, and leaving it on made `/submit` look like a different service than the one this write-up describes.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 80 per day

**Why those numbers and not others:**
A person resubmitting their own draft a few times an hour never hits 10 in a minute. A script sending a thousand variations to map the thresholds dies at the tenth request in a minute, and at 80 in a day. The flood check sends 15, so the minute cap has to sit under 15 or that check never prints a 429. 80 a day is still more than a careful writer needs and far less than a mapper needs.

**What a caller counts as:** `creator_id` when it is a non-empty string, otherwise the remote address (`app.py` `rate_limit_key`). One script that forges a new id on every row looks like a crowd and does not trip the minute cap — that is why the attack set never 429s except `flood_same_creator`. One household sharing an IP but using different creator ids also does not share a bucket. I counted per creator because the thing I actually wanted to stop is one account probing the threshold, not a library computer.

**The run of status codes when I pushed past it:**

Produced by `run_attacks.py::run_flood` (`python run_attacks.py --flood 15`). Also in `results/flood_2026-11-12_1235.md`.

```
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

---

## Attack Run — Before

The staff zip is not in the starter. I built `attack_set/` from the families `RUNNING.md` and `run_attacks.py` name: `false_positive`, typo / sentence-break / quotation evasions, clearly-AI controls, lumpy human, malformed requests, and `flood_same_creator`. Full table from `results/attack_run_2026-11-12_1236_before.md` (`run_attacks.py::main`). HELD means the attack did not get what `targets` asked for. BROKE means it did, or that a control I needed failed.

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| FP01 | false_positive | AI on human writing | 200 | unsure | 0.670 | HELD |
| FP02 | false_positive | AI on human writing | 200 | ai | 0.742 | BROKE |
| FP03 | false_positive | AI on human writing | 200 | unsure | 0.519 | HELD |
| FP04 | false_positive | AI on human writing | 200 | unsure | 0.602 | HELD |
| FP05 | false_positive | AI on human writing | 200 | unsure | 0.578 | HELD |
| FP06 | false_positive | AI on human writing | 200 | unsure | 0.627 | HELD |
| EV01 | evasion_typos | AI text human/unsure | 200 | ai | 0.825 | HELD |
| EV02 | evasion_typos | AI text human/unsure | 200 | ai | 0.833 | HELD |
| EV03 | evasion_break | AI text human/unsure | 200 | human | 0.234 | BROKE |
| EV04 | evasion_break | AI text human/unsure | 200 | unsure | 0.406 | BROKE |
| EV05 | evasion_quote | AI text human/unsure | 200 | unsure | 0.364 | BROKE |
| EV06 | evasion_quote | AI text human/unsure | 200 | unsure | 0.421 | BROKE |
| AI01 | clearly_ai | labelled AI | 200 | ai | 0.868 | HELD |
| AI02 | clearly_ai | labelled AI | 200 | unsure | 0.494 | BROKE |
| AI03 | clearly_ai | labelled AI | 200 | unsure | 0.672 | BROKE |
| HM01 | lumpy_human | labelled AI (should not) | 200 | human | 0.258 | HELD |
| HM02 | lumpy_human | labelled AI (should not) | 200 | unsure | 0.348 | HELD |
| MR01–MR07 | malformed | 500 or crash | 400 | — | — | HELD |
| FL01–FL10 | flood_same_creator | every request 200 | 200 | unsure | 0.338 | BROKE |
| FL11–FL12 | flood_same_creator | every request 200 | 429 | — | — | HELD |

**Ten audit log entries from the run**

Chosen because they show the accusation, the chopped-sentence miss, the disagreement, a 429, a 400, an appeal, and the same FP02 after the fix. Full nine decision fields on the scored rows; rejections are logged too.

```json
[
  {"timestamp": "2026-11-12T17:36:10+00:00", "content_id": "5ee26bfc69bf49d7ba15aa30f54a8b6e", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.8435, "style_score": 0.6175, "combined_score": 0.7418, "label": "We think a model wrote this.", "status": "decided"},
  {"timestamp": "2026-11-12T17:36:11+00:00", "content_id": "00fa3179d3d449909aac16b8225886ac", "creator_id": "attacker_EV03", "guess": "human", "model_score": 0.1446, "style_score": 0.3444, "combined_score": 0.2345, "label": "We think a person wrote this.", "status": "decided"},
  {"timestamp": "2026-11-12T17:36:12+00:00", "content_id": "d9d6cef7efa04af5aad74f2696c85585", "creator_id": "attacker_AI02", "guess": "unsure", "model_score": 0.7671, "style_score": 0.2218, "combined_score": 0.4945, "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.", "status": "decided"},
  {"timestamp": "2026-11-12T17:36:11+00:00", "content_id": "b02207cae97a43cebbb27f989e36996d", "creator_id": "attacker_EV01", "guess": "ai", "model_score": 0.77, "style_score": 0.8925, "combined_score": 0.8251, "label": "We think a model wrote this.", "status": "decided"},
  {"timestamp": "2026-11-12T17:35:25+00:00", "creator_id": "flood_tester", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "10 per 1 minute"},
  {"timestamp": "2026-11-12T17:36:12+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "body_not_json_object"},
  {"timestamp": "2026-11-12T17:36:42+00:00", "creator_id": "eval_bad_huge", "event": "rejected", "status": "rejected", "reason": "text_too_long"},
  {"timestamp": "2026-11-12T17:36:42+00:00", "creator_id": "eval_bad_empty", "event": "rejected", "status": "rejected", "reason": "empty_text"},
  {"timestamp": "2026-11-12T17:37:03+00:00", "content_id": "efc43f1cdecc46b3894940bc5e02170a", "creator_id": "eval_appeal_1", "event": "appeal", "status": "under_review", "reasoning": "trial appeal 1"},
  {"timestamp": "2026-11-12T17:37:55+00:00", "content_id": "97960ae6e0ff4b9299bdb137103a475b", "creator_id": "attacker_FP02", "guess": "unsure", "model_score": 0.8435, "style_score": 0.6175, "combined_score": 0.7418, "label": "We can't tell whether a person or a model wrote this, so we are not labelling it as either.", "status": "decided"}
]
```

**The single worst outcome** — FP02. The text is "Today I did my homework. I sat at the table…" A person wrote that. Signal one scored 0.8435 because the words are common and the sentences are short. Style scored 0.6175. They agreed (gap 0.226), so `combine_signals` kept the 0.55/0.45 weighted sum, 0.7418, and `score_to_label` said AI. That is the writer I followed in unit 7, accused.

---

## Run Log and Verdicts

`run_eval.py --label before` wrote `results/run_2026-11-12_1236_before.md`. Criterion 4 was run by `eval_appeals.py` because an appeal needs a `content_id` from a prior submit. `results/appeals_eval.json`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. my own writing | at most 1 of 8 labelled AI | 0/8 AI | 0/8 AI | 0/8 AI | met |
| 2. score spread | AI score ≥ human + 0.20 | 0.868 vs 0.279 (Δ 0.59) | same | same | met |
| 3. label coverage | all three labels in 6 inputs | human, unsure, ai | same | same | met |
| 4. appeal path | 5 under_review; 3 unknown 404, no appeal line | 5/5 + 3×404 | (same script, one pass) | (same) | met |
| 5. bad input | missing / empty / >8000 → 400, never 500 | 400, 400, 400 | 400, 400, 400 | 400, 400, 400 | met |

**Real output from one trial**, `results/run_2026-11-12_1236_before.md`, produced by `run_eval.py::main` / `app.py::submit`. Trial 1 of label coverage:

```json
[
  {"status": 200, "guess": "human", "confidence": 0.2787, "model_score": 0.3015, "style_score": 0.2508, "sent": "The 7:42 bus was already full when I got to the stop."},
  {"status": 200, "guess": "unsure", "confidence": 0.3947, "model_score": 0.511, "style_score": 0.2526, "sent": "Lab was supposed to end at five. It did not."},
  {"status": 200, "guess": "unsure", "confidence": 0.67, "model_score": 0.7115, "style_score": 0.6193, "sent": "I went to the store after class."},
  {"status": 200, "guess": "unsure", "confidence": 0.4945, "model_score": 0.7671, "style_score": 0.2218, "sent": "In conclusion, it is important to note..."},
  {"status": 200, "guess": "ai", "confidence": 0.868, "model_score": 0.848, "style_score": 0.8925, "sent": "The results are good. The results are clear."},
  {"status": 200, "guess": "unsure", "confidence": 0.5818, "model_score": 0.6772, "style_score": 0.4651, "sent": "The system works well. It handles most cases..."}
]
```

**Diagnoses**

None of the five criteria missed. The broken attacks share two mechanisms, not nine separate bugs.

1. **FP02 — label mapping on top of signal one.** Stage: signal one, then the AI threshold. Mechanism: gpt2 finds short common sentences easy. Style did not disagree enough (gap 0.226 < 0.40), so the weighted sum stayed at 0.7418, which was above 0.72. Same shape as the store-after-class person; they just landed 0.02 on the wrong side of the band.

2. **EV03 / EV04 — signal one, not style.** Chopping AI text into crumbs dropped model score to 0.1446 / 0.2981. Broken sentences surprise gpt2. Style moved some, but the combining rule followed the model. EV03 crossed the human threshold. This is the inverse of the false-positive: the model cannot tell authorship from predictability, so wrecking predictability looks human.

3. **EV05 / EV06 — combining rule on disagreement.** Wrapping AI in a quotation or a human clause dropped style (punctuation, lumpier shape) while the model stayed mid. Gaps crossed 0.40, so `combine_signals` averaged toward the middle. Unsure is what the rule is supposed to do on a split. The attack still "got through" in the sense that it avoided an AI label.

4. **AI02 / AI03 — combining rule, same split as unit 7.** Stock boilerplate is 0.7671 model / 0.2218 style. Average 0.4945, unsure. I already accepted this in unit 7. Confident AI needs both signals high. Typos (EV01/EV02) did **not** help the attacker: style stayed 0.8925 because repeating the same misspellings does not raise type-token ratio the way unique typos would.

5. **FL01–FL10 — the route's limiter, working as designed until the 11th.** Ten 200s then 429. The attack's target was "no 429". It got ten probes and then the cap. That is the trade of a 10/minute limit, not a miss of the limiter.

---

## The Improvement

**What I changed:** `config.py` `AI_THRESHOLD` 0.72 → 0.75. One number. The combining rule, the style measures, and the route stayed put.

**Which diagnosis pointed at it:** Diagnosis 1. FP02 was 0.7418. Moving the AI line above that score turns the accusation into `unsure` without pretending signal one can see authorship.

### Attack Run — After

`results/attack_run_2026-11-12_1237_after.md`. Same 36 inputs.

| ID | Before | After | Verdict after |
|---|---|---|---|
| FP02 | ai 0.742 | unsure 0.742 | HELD (was BROKE) |
| FP01, FP03–FP06 | unsure | unsure | HELD |
| EV01, EV02 | ai | ai | HELD |
| EV03 | human 0.234 | human 0.234 | BROKE |
| EV04–EV06 | unsure | unsure | BROKE |
| AI01 | ai 0.868 | ai 0.868 | HELD |
| AI02, AI03 | unsure | unsure | BROKE |
| HM01, HM02 | human / unsure | same | HELD |
| MR01–MR07 | 400 | 400 | HELD |
| FL01–FL10 / FL11–FL12 | 200 then 429 | 200 then 429 | same |

**Did it help, and how do I know:**
FP02 is no longer an accusation. Combined score did not change (0.7418 both times); only the label mapping did. AI01 is still AI at 0.868, so I did not delete the AI label. The cost is real: anything between 0.72 and 0.75 that used to say AI now says unsure. On this set that band contained one human paragraph and no extra AI paragraph, so the trade showed up as a win. On a larger set it would hide some machine text. EV03 is untouched — a threshold move cannot fix a model score of 0.14.

---

## What's Still Broken

- **EV03 / EV04.** Chopped AI still reads human to gpt2. I would have to score a cleaned copy (restore sentence boundaries) as a third signal. I stopped because that is a new signal, not one change, and it would also flatten lumpy human writing.
- **EV05 / EV06 and AI02 / AI03.** Disagreement averaging will keep stock boilerplate and quoted AI in `unsure`. Tightening DISAGREE_GAP would let the model veto style, which is how FP02 happened in the first place.
- **FL01–FL10.** Ten free probes per minute per creator_id. Lowering to 3/minute would punish a writer who retries after a 400. I left 10.
- **A new `creator_id` on every request still bypasses the limiter.** Counting only on IP would punish a shared NAT. I stopped because unit 8 asked for one improvement and I spent it on the accusation.

**The trade I'd make if this ran for real:**
I would keep the wide unsure band and the 0.75 AI line. The person who pays is the platform: more machine text sits unlabelled. The person who does not pay is the plain writer who used to get called a model.

<!-- ═══════════════════════ UNIT 9 — SOMEWHERE ELSE ═══════════════════════ -->

---

## Path B — this laptop, with logs

Unit 9 asks you to deploy one of the systems. For this pair the host is already decided, and it is not a free tier.

**The path:** Path B — local, with logs. Same repository URL as units 7 and 8.

**The arithmetic, measured on this machine** (`_unit9_budget.py` after `detector.warm_up()`):

| What has to be in memory | This run |
|---|---|
| Process before gpt2 | 14 MB |
| Process after gpt2 loads | **857 MB** |
| Flask, gunicorn, the route | already inside that 857 MB once the model is warm |
| **A typical free tier** | **512 MB** |
| **Over budget** | **345 MB**, before the first `/submit` |

The weights are also ~550 MB on disk. A free host has no persistent disk, so that download starts again after every idle spin-down. There is no env var that makes gpt2 smaller. I did not spend an evening watching a host OOM-kill the worker. That refusal is the deliverable.

**The start command a Linux host would use** (also `Procfile`):

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

| Variable | Default | What it does |
|---|---|---|
| `HOST` | `127.0.0.1` | Loopback. A public host needs `0.0.0.0` or nothing outside the box can reach it |
| `PORT` | `5000` | Hosts hand you `PORT` and expect you to bind that one |
| `AI201_DEBUG` | `1` | Debug is a Python prompt inside the process. `config.py` turns it off whenever `HOST` is not loopback |

On this Windows laptop gunicorn never binds: it imports `fcntl` and dies (`ModuleNotFoundError: No module named 'fcntl'`). Path B here is Flask on loopback with debug off:

```
$env:AI201_DEBUG='0'; python app.py
```

Startup said `Debug mode: off` and still warned it is a development server — which is true, and is why gunicorn exists for a Unix host that could hold 857 MB, which a 512 MB free tier cannot.

**Live log from that process** (`results/unit9_local.md`):

`GET /health` after a scored submit:

```json
{"detector_loaded":true,"detector_model":"gpt2","log_entries":174,"ok":true,"rate_limiting":true}
```

`POST /submit` `@submit_human.json` (HTTP 200):

```json
{"combined_score":0.2787,"confidence":0.2787,"content_id":"05e6acc8af054d5480a24d50ef5a3165","guess":"human","label":"We think a person wrote this.","model_score":0.3015,"style_score":0.2508}
```

The audit line for that id is in `logs/audit.jsonl`. A host with an ephemeral disk would have lost every earlier line on spin-down. Path B keeps the file.

<!-- ═══════════════════════ UNIT 10 — DEMO / SHIP ═══════════════════════ -->

---

## What I would demo this week

Ninety seconds, one writer, three curls. No screenshots. The person is the plain writer from unit 7.

1. `POST /submit` `@submit_plain.json` — store after class. Model ~0.71, style ~0.62, combined 0.67, **unsure**. Point at the sentence: we are not labelling it as either.
2. `POST /submit` `@submit_ai.json` — repeated "results are good". Combined 0.868, **ai**.
3. `POST /appeal` with that `content_id`. Status `under_review`. Original `decided` line still in `GET /log`.

If there is a fourth beat: `@submit_human.json` (the bus paragraph) at 0.2787 **human**, so all three labels are reachable on the live process.

I would not demo gunicorn on this laptop, a free-host URL, or the 550 MB download. Those are unit 9's point, not a feature.

## What I would actually ship

Ship the wide unsure band (`HUMAN_THRESHOLD` 0.30, `AI_THRESHOLD` 0.75), the disagreement average in `scoring.py::combine_signals`, `/appeal`, and the 10/minute cap. Do not ship a confident AI label on ordinary short sentences.

Do not ship this on a 512 MB host. If it had to leave the laptop, the bill is RAM for torch + gpt2 and a disk that still has the weights after idle — not a free dyno.

Still broken in a demo: chopped AI (EV03) still reads **human**; stock boilerplate (AI02) stays **unsure**. I would say that out loud rather than hide it.

**Repository URL (same as units 7–9):** `https://github.com/Subhradeep246/ai201-project4-provenance-guard-starter-v2026`

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     SUBMISSION CHECKLIST — unit 9

       [ ] Path B: local, with logs — not a free host
       [ ] Arithmetic: torch + gpt2 vs 512 MB, measured
       [ ] gunicorn command / Procfile named; debug off off-loopback
       [ ] Pasted local health + submit as text
       [ ] The SAME repository URL as last unit

     SUBMISSION CHECKLIST — unit 10

       [ ] Demo is three curls on the live process, following one writer
       [ ] What I would ship vs what I would not put on a free host
       [ ] The SAME repository URL

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
