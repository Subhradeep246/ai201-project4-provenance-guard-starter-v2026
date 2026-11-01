# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. Of 8 paragraphs I wrote myself, at most 1 is labelled high-confidence AI

**Why this target:** A wrong accusation costs the writer more than a missed
detection costs the site. One in eight is already a lot of false accusations
to live with, and I am not writing zero: the model signal treats plain,
ordinary sentences as predictable, so a promise of zero is a promise this
signal cannot keep. Unit 8 has to hold the same count on all three trials.

---

## 2. A clearly AI paragraph scores at least 0.20 higher than a clearly human one

**Why this target:** The two pieces are ones I can tell apart by reading them.
If their combined scores land within 0.20, the thresholds are sitting on noise
and the labels are not measuring the difference I think they are. 0.20 is
tighter than the unsure band, so this can fail even when both texts are
labelled unsure.

---

## 3. Each of the three labels appears at least once in a set of 6 inputs

**Why this target:** Two inputs I expect to read as human, two as AI, two as
borderline. A label that none of those six can reach is not a label I can
show a reader. Six is enough to cover three labels without pretending the
detector is accurate.

---

## 4. 5 real appeals move to `under_review` in the log; 3 unknown ids return 404 and add no appeal line

**Why this target:** The appeal is the only way off a wrong accusation, so
every real `content_id` has to change status and leave both the original
decision and the appeal in the log. A typo has to fail in the open: 404, and
no appeal line, or a bad id looks like a successful review.

---

## 5. Missing text, empty text, and text over 8,000 characters each return 400 and a rejection log line, never 500

**Why this target:** Those three are the bodies a public route actually
receives when a client is broken or hostile. A 500 means the service fell
over. A 400 with no log line is a refusal I cannot see next unit. 8,000
characters is the cap in `config.py`.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
