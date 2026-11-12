#!/usr/bin/env python3
"""
Criterion 4 cannot be tested by POST /submit alone. Submit five texts, appeal
each content_id, then send three ids that were never decided.

    python eval_appeals.py
"""

import json
import sys

import requests

import config

URL = f"http://{config.HOST}:{config.PORT}"
TEXT = (
    "The 7:42 bus was already full when I got to the stop. Rain on the vinyl "
    "seats. A kid in a yellow coat kept kicking the pole, not mean, just bored."
)


def main() -> int:
    try:
        requests.get(f"{URL}/health", timeout=5)
    except Exception as exc:  # noqa: BLE001
        print(f"Nothing answering at {URL}: {exc}", file=sys.stderr)
        return 1

    results = {"real_appeals": [], "unknown": []}

    for i in range(1, 6):
        submitted = requests.post(
            f"{URL}/submit",
            json={"text": TEXT, "creator_id": f"eval_appeal_{i}"},
            timeout=90,
        )
        body = submitted.json()
        content_id = body.get("content_id")
        appealed = requests.post(
            f"{URL}/appeal",
            json={"content_id": content_id, "reasoning": f"trial appeal {i}"},
            timeout=30,
        )
        log = requests.get(f"{URL}/log?limit=400", timeout=30).json()
        entries = [
            e for e in log.get("entries", [])
            if e.get("content_id") == content_id
        ]
        statuses = [e.get("status") for e in entries]
        results["real_appeals"].append({
            "submit_status": submitted.status_code,
            "appeal_status": appealed.status_code,
            "content_id": content_id,
            "appeal_body": appealed.json(),
            "log_statuses": statuses,
        })
        print(f"  real {i}: submit {submitted.status_code} appeal {appealed.status_code} log {statuses}")

    for bad_id in ("does-not-exist-1", "does-not-exist-2", "does-not-exist-3"):
        appealed = requests.post(
            f"{URL}/appeal",
            json={"content_id": bad_id, "reasoning": "typo"},
            timeout=30,
        )
        log = requests.get(f"{URL}/log?limit=400", timeout=30).json()
        appeal_lines = [
            e for e in log.get("entries", [])
            if e.get("content_id") == bad_id and e.get("event") == "appeal"
        ]
        results["unknown"].append({
            "content_id": bad_id,
            "status": appealed.status_code,
            "body": appealed.json(),
            "appeal_lines": len(appeal_lines),
        })
        print(f"  unknown {bad_id}: {appealed.status_code} appeal_lines={len(appeal_lines)}")

    config.RESULTS_DIR.mkdir(exist_ok=True)
    path = config.RESULTS_DIR / "appeals_eval.json"
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote {path.relative_to(config.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
