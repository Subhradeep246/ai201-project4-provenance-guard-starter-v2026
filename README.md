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

## What This Does

A submission is a piece of writing from a creator. The service answers with a label a reader can understand, and keeps a log so a wrong label can be appealed.

The person I followed through it is someone writing plainly on purpose: short sentences, ordinary words, no ornaments. Signal one treats that as predictable, which is the same thing it treats as machine-written. If both signals agree, the label can accuse them. If they split, the score is pulled to the middle and the label says we can't tell.

1. `POST /submit` receives JSON with `text` and `creator_id`.
2. A missing field, an empty string, or more than 8,000 characters is a `400`, and `audit.log_rejection` writes the refusal. The route does not score it.
3. `detector.model_signal` scores how predictable the text is to gpt2. Higher means more likely AI.
4. `stylometry.style_signal` scores the shape of the text, without reading it. Higher means more likely AI.
5. `scoring.combine_signals` turns the two numbers into one. A gap of 0.40 or more is a disagreement, and the score becomes their average.
6. `scoring.score_to_label` turns that number into `human`, `unsure`, or `ai`, plus a sentence.
7. `audit.log_decision` appends the decision, including a `content_id`.
8. The response sends that id, both signal scores, the combined score, the guess, and the sentence.
9. `POST /appeal` with that `content_id` leaves the original decision where it is and appends a line with status `under_review`. An id that was never decided is a `404`.



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to `gpt2`, as perplexity squashed to a 0–1 score in `detector.model_signal`. Higher means the model was less surprised, which this service reads as more likely AI.

**Why that might differ between human and AI writing:** A model writes by picking likely next words, so text it wrote tends to be text it finds easy to predict. Human writing wanders more: an odd word, a hard turn, a specific detail.

**What it can't see:** Authorship. It sees predictability. Common words in short, ordinary sentences score like machine text, which is how a person writing in a second language, a younger writer, or anyone writing plainly gets accused. Dense prose with rare words often goes the other way and scores as human, because rare words surprise the model. On the plain paragraph below, this signal alone scored 0.7092.

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

`detector.model_signal` returned 0.7671. `stylometry.style_signal` returned 0.2218. The gap is 0.545, which is past 0.40, so `combine_signals` returned their average, 0.4945, and `score_to_label` said `unsure`. A weighted sum would have been `0.55 * 0.7671 + 0.45 * 0.2218 = 0.5217`, also unsure, but the rule that actually fired is the average. The model signal was ready to lean AI. The style signal was not. The label does not accuse.



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

A score sitting on 0.30 is human, and a score sitting on 0.72 is AI, because `score_to_label` uses `<=` and `>=`. All three were reached on the live service: the lumpy bus paragraph at 0.1802 (`human`), the store-and-rain paragraph at 0.5564 (`unsure`), and the repeated "results are good" paragraph at 0.868 (`ai`).

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
$ curl.exe -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" --data-binary "@submit.json"
```

`submit.json` was `{"text": "The results are good. The results are clear. The results are useful. The system provides good results. The system provides clear results. The system provides useful results for users.", "creator_id": "subhradeep"}`.

```json
{
  "combined_score": 0.868,
  "confidence": 0.868,
  "content_id": "d35186e0feaf45e28ef68f1803a0dda7",
  "guess": "ai",
  "label": "We think a model wrote this.",
  "model_score": 0.848,
  "style_score": 0.8925
}
```

**An appeal**

```bash
$ curl.exe -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" --data-binary "@appeal.json"
```

```json
{
  "content_id": "d35186e0feaf45e28ef68f1803a0dda7",
  "message": "A person will look at this. The original label stays up until they do.",
  "ok": true,
  "status": "under_review"
}
```

**What the log shows afterwards**

The decision is still `decided`. The appeal is a later line. An unknown id returned 404 and a rejection, not an appeal.

```bash
$ curl.exe "http://127.0.0.1:5000/log?limit=8"
```

```json
{
  "combined_score": 0.868,
  "content_id": "d35186e0feaf45e28ef68f1803a0dda7",
  "creator_id": "subhradeep",
  "guess": "ai",
  "label": "We think a model wrote this.",
  "model_score": 0.848,
  "status": "decided",
  "style_score": 0.8925,
  "timestamp": "2026-11-01T20:59:35+00:00"
}
```

```json
{
  "content_id": "d35186e0feaf45e28ef68f1803a0dda7",
  "creator_id": "subhradeep",
  "event": "appeal",
  "reasoning": "I wrote the repeated sentences myself as a test, and the label calls them a model's.",
  "status": "under_review",
  "timestamp": "2026-11-01T21:00:09+00:00"
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* Build unit 7 of Provenance Guard from the starter: criteria first, then the style signal, the combining rule, `/submit`, and `/appeal`.
- *What came back:* An implementation of the stubs in `stylometry.py`, `scoring.py`, and `app.py`, plus a first pass at the thresholds.
- *What I changed:* Kept the disagreement rule after calibration. The stock AI-looking paragraph scored 0.8864 on the model and 0.4579 on style, and the average landed at 0.6722, which is unsure rather than AI. I left that in place. A repeated paragraph was what actually crossed 0.72, which is a real limit of the rule and it is written above.

**Moment 2**

- *What I asked for:* Recheck the running service with curl: ping, empty text, a missing field, one submission of each label, a real appeal, and an unknown id.
- *What came back:* The JSON pasted in Sample Run, plus `human` at 0.1802 and `unsure` at 0.5564.
- *What I changed:* The first curl attempt from PowerShell sent a body the route correctly rejected as not JSON. That rejection is the first line of `logs/audit.jsonl`. The later requests used files so the JSON arrived intact.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
