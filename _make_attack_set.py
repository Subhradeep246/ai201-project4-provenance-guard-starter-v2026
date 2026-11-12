from pathlib import Path
import csv
import json

root = Path(__file__).parent / "attack_set"
root.mkdir(exist_ok=True)

plain = [
    "I went to the store after class. The rain was light and I forgot my bag. I bought bread and milk and stood in line. The person in front of me paid with coins. I walked home and put the food away.",
    "Today I did my homework. I sat at the table. I wrote the answers. Then I checked them. It took a long time. I think they are correct.",
    "The class was good. The teacher talked. We took notes. After class I went home. I ate food. I will study later.",
    "My friend is kind. We meet after school. We talk about the work. Sometimes we are tired. We still try to finish.",
    "I like the library. It is quiet. I can sit and read. The chairs are not very nice. I stay anyway because I have to.",
    "Please find attached my essay. I wrote it myself this week. I hope it is okay. Thank you for your time and help.",
]
ai = (
    "The results are good. The results are clear. The results are useful. "
    "The system provides good results. The system provides clear results. "
    "The system provides useful results for users."
)
stock = (
    "In conclusion, it is important to note that this approach offers several benefits. "
    "Furthermore, it is worth mentioning that the overall process is simple. "
    "Additionally, users can easily understand the system. Overall, the solution works well."
)
lumpy = (
    "The 7:42 bus was already full when I got to the stop. Rain on the vinyl seats. "
    "A kid in a yellow coat kept kicking the pole, not mean, just bored, and nobody "
    "said a thing until the driver yelled at the back door."
)
typo_ai = (
    "The resullts are goood. The resullts are cleer. The resullts are usefull. "
    "The system provids goood resullts. The system provids cleer resullts. "
    "The system provids usefull resullts for usres."
)
broken_ai = (
    "The results are good it handles most cases. Users find it. Easy. "
    "To use and understand overall. The process is simple. Effective."
)
quoted = (
    "She said, 'the vinyl seats were wet and the driver yelled at the back door,' "
    "and then she added a whole generated paragraph: "
    + ai
)

rows = []
for i, t in enumerate(plain, 1):
    rows.append(
        {
            "id": f"FP{i:02d}",
            "family": "false_positive",
            "targets": "high-confidence AI on human writing",
            "text": t,
        }
    )
rows += [
    {"id": "EV01", "family": "evasion_typos", "targets": "AI text labelled human or unsure", "text": typo_ai},
    {"id": "EV02", "family": "evasion_typos", "targets": "AI text labelled human or unsure", "text": typo_ai.replace("oo", "o")},
    {"id": "EV03", "family": "evasion_break", "targets": "AI text labelled human or unsure", "text": broken_ai},
    {"id": "EV04", "family": "evasion_break", "targets": "AI text labelled human or unsure", "text": "Good. Clear. Useful. The system. Provides. Results. For. Users. Overall. Simple."},
    {"id": "EV05", "family": "evasion_quote", "targets": "AI text labelled human or unsure", "text": quoted},
    {"id": "EV06", "family": "evasion_quote", "targets": "AI text labelled human or unsure", "text": f"As the report notes: '{stock}' That is the whole claim."},
    {"id": "AI01", "family": "clearly_ai", "targets": "labelled AI", "text": ai},
    {"id": "AI02", "family": "clearly_ai", "targets": "labelled AI", "text": stock},
    {
        "id": "AI03",
        "family": "clearly_ai",
        "targets": "labelled AI",
        "text": (
            "The implementation of the proposed framework requires careful consideration of several key factors. "
            "First, it is important to note that the system must be able to handle a wide variety of different inputs. "
            "Additionally, the overall performance of the solution depends on a number of important variables."
        ),
    },
    {"id": "HM01", "family": "lumpy_human", "targets": "labelled AI (should not)", "text": lumpy},
    {
        "id": "HM02",
        "family": "lumpy_human",
        "targets": "labelled AI (should not)",
        "text": (
            "Lab was supposed to end at five. It did not. The printer jammed on page three of the handout, "
            "someone had unplugged the switch to charge a phone, and I still had to screenshot the error before I could leave."
        ),
    },
]

with (root / "attacks.csv").open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "family", "targets", "text"])
    writer.writeheader()
    writer.writerows(rows)

mal = [
    {"id": "MR01", "family": "malformed", "targets": "500 or crash", "raw_body": json.dumps({"text": "", "creator_id": "attacker_MR01"}), "send_as": "json", "content_type": "application/json"},
    {"id": "MR02", "family": "malformed", "targets": "500 or crash", "raw_body": json.dumps({"creator_id": "attacker_MR02"}), "send_as": "json", "content_type": "application/json"},
    {"id": "MR03", "family": "malformed", "targets": "500 or crash", "raw_body": json.dumps({"text": "word " * 2500, "creator_id": "attacker_MR03"}), "send_as": "json", "content_type": "application/json"},
    {"id": "MR04", "family": "malformed", "targets": "500 or crash", "raw_body": json.dumps({"text": None, "creator_id": "attacker_MR04"}), "send_as": "json", "content_type": "application/json"},
    {"id": "MR05", "family": "malformed", "targets": "500 or crash", "raw_body": "{not json at all", "send_as": "raw", "content_type": "application/json"},
    {"id": "MR06", "family": "malformed", "targets": "500 or crash", "raw_body": "", "send_as": "raw", "content_type": "application/json"},
    {"id": "MR07", "family": "malformed", "targets": "500 or crash", "raw_body": json.dumps(["a", "list"]), "send_as": "json", "content_type": "application/json"},
]
flood_body = json.dumps(
    {
        "text": "Ordinary flood probe from the same account looking for the limit.",
        "creator_id": "flood_same_creator",
    }
)
for i in range(1, 13):
    mal.append(
        {
            "id": f"FL{i:02d}",
            "family": "flood_same_creator",
            "targets": "every request 200, no 429",
            "raw_body": flood_body,
            "send_as": "json",
            "content_type": "application/json",
        }
    )

with (root / "attacks_malformed_requests.csv").open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=["id", "family", "targets", "raw_body", "send_as", "content_type"]
    )
    writer.writeheader()
    writer.writerows(mal)

print("attacks", len(rows), "malformed", len(mal))
