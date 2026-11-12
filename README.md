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
