"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    Coefficient of variation of sentence lengths, in words.

    Higher means lumpier writing, which I treat as more human. A single
    sentence has no spread, so it returns 0.0 — the uniform, more AI-like end.
    `stdev` needs two lengths, and this returns before calling it.
    """
    lengths = [len(words(sentence)) for sentence in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    if mean == 0:
        return 0.0
    return statistics.stdev(lengths) / mean


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words, on the first 120 words only.

    Higher means a more varied vocabulary, which I treat as more human.
    The window is there because this ratio falls as a text gets longer even
    when the writer doesn't change. Two texts past 120 words are compared on
    the same slice. Empty text returns 0.0.
    """
    tokens = words(text)[:120]
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


# Full stops are left out. Almost every sentence has one, so they don't
# separate writers. Commas, semicolons, dashes, and the rest do.
_MARKS = set(",;:!?()\"'`—–-")


def punctuation_density(text: str) -> float:
    """
    Distinctive punctuation marks per word. Higher means more of them.

    I treat a higher density as more human. The count is marks from `_MARKS`
    divided by the word count, so a long text is not punished for being long.
    Empty text returns 0.0.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    marks = sum(1 for ch in text if ch in _MARKS)
    return marks / len(tokens)


# ── Combining them ───────────────────────────────────────────────────────────

def _unit(value: float) -> float:
    """Clamp to the 0–1 range the other signal already uses."""
    return min(max(value, 0.0), 1.0)


def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.** ← TODO

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.
    """
    # Each piece is flipped so that higher means more AI, then clamped to 0–1.
    # Spread of 0.75 (very lumpy) maps to 0. Type-token ratio of 0.70 maps to
    # 0; 0.42 maps to 1. Punctuation density of 0.14 marks per word maps to 0.
    spread = sentence_length_spread(text)
    ratio = type_token_ratio(text)
    density = punctuation_density(text)

    ai_from_spread = _unit(1.0 - spread / 0.75)
    ai_from_vocab = _unit((0.70 - ratio) / 0.28)
    ai_from_punct = _unit(1.0 - density / 0.14)
    return round((ai_from_spread + ai_from_vocab + ai_from_punct) / 3.0, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
