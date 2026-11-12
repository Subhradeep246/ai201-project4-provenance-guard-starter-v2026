"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. Criterion 4
(appeals) cannot be expressed as POST /submit bodies, so it is run by
`eval_appeals.py` instead of this file.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": [
            "The 7:42 bus was already full when I got to the stop. Rain on the vinyl seats. A kid in a yellow coat kept kicking the pole, not mean, just bored, and nobody said a thing until the driver yelled at the back door. I stood the whole way and counted the grocery bags people were hugging like they might leak.",
            "Lab was supposed to end at five. It did not. The printer jammed on page three of the handout, someone had unplugged the switch to charge a phone, and I still had to screenshot the error before I could leave. I wrote the bug down on the back of a MetroCard because my notebook was in the other bag.",
            "My roommate left a note on the fridge that just said 'eggs gone, sorry, payday Friday.' I ate cereal with water. It tasted like nothing, which was honest of it. I put the empty carton in the recycling anyway so the next person would not open it hoping.",
            "I called home and talked around the grade. Ma asked if I was eating. I said yes. She asked if the coat was warm enough. I said the wind in this city comes up from the river and goes straight through whatever you wear. She laughed like that was a complaint she had heard from someone else first.",
            "The library fifth floor smells like old heat and highlighter. I sat next to a window that does not open and copied the same integral three times because I did not trust the first two. A guy two tables over was watching a lecture at full volume with no headphones. I moved. He did not notice.",
            "I missed the G train by twenty seconds and watched it leave. The next one was twelve minutes. I sat on the metal bench and read the ad for a personal-injury lawyer until I could recite the phone number. When the train came it was packed and I held the pole with two fingers because someone else's coffee was occupying the rest of the grip.",
            "Office hours were in a room with one whiteboard and a dying marker. I asked about the recurrence. The TA wrote T(n) = 2T(n/2) + n and then stopped, waiting to see if I would finish it. I did, slowly, and the marker squeaked on the last n. I thanked them and walked out still not sure I could do the next one alone.",
            "Saturday I walked to the laundromat on 14th because the one in the building eats quarters. A woman was folding tiny socks into a pile that kept falling. I gave her the top of the dryer as a shelf. She said thanks in a way that meant she had been there an hour. I watched my jeans tumble and thought about the problem set I had not started.",
        ],
    },
    {
        "name": "score spread",
        "criterion": 2,
        "texts": [
            "The results are good. The results are clear. The results are useful. The system provides good results. The system provides clear results. The system provides useful results for users.",
            "The 7:42 bus was already full when I got to the stop. Rain on the vinyl seats. A kid in a yellow coat kept kicking the pole, not mean, just bored, and nobody said a thing until the driver yelled at the back door. I stood the whole way and counted the grocery bags people were hugging like they might leak.",
        ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            "The 7:42 bus was already full when I got to the stop. Rain on the vinyl seats. A kid in a yellow coat kept kicking the pole, not mean, just bored, and nobody said a thing until the driver yelled at the back door. I stood the whole way and counted the grocery bags people were hugging like they might leak.",
            "Lab was supposed to end at five. It did not. The printer jammed on page three of the handout, someone had unplugged the switch to charge a phone, and I still had to screenshot the error before I could leave. I wrote the bug down on the back of a MetroCard because my notebook was in the other bag.",
            "I went to the store after class. The rain was light and I forgot my bag. I bought bread and milk and stood in line. The person in front of me paid with coins. I walked home and put the food away.",
            "In conclusion, it is important to note that this approach offers several benefits. Furthermore, it is worth mentioning that the overall process is simple. Additionally, users can easily understand the system. Overall, the solution works well.",
            "The results are good. The results are clear. The results are useful. The system provides good results. The system provides clear results. The system provides useful results for users.",
            "The system works well. It handles most cases correctly and provides good results. Users generally find it easy to use and understand. The overall process is simple and effective for a wide variety of different inputs.",
        ],
    },
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_bad_missing"},
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
