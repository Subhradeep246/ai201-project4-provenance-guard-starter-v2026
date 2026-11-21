# Run and test Provenance Guard for the capstone

Provenance Guard is a local Flask API. It measures text predictability with
GPT-2 and writing patterns with stylometry, combines the scores, and returns
`human`, `ai`, or `unsure`. It logs decisions and accepts appeals. The scores
are heuristics, not probabilities or proof of authorship. Appeals record review
requests; a reviewer interface and completed review are not implemented.

Each tester runs their own copy on their device at http://127.0.0.1:5000.
There is no website interface or API key. Use two terminals in the project folder:
Terminal 1 runs the server; Terminal 2 sends requests and runs evaluations.

## 1. Requirements and project download (all platforms)

- Python **3.11, 3.12, or 3.13**, not 3.14.
- Git for cloning, or download and extract the repository ZIP from
  [GitHub](https://github.com/Subhradeep246/ai201-project4-provenance-guard-starter-v2026).
- Internet for dependency installation and the initial GPT-2 download (about
  550 MB), plus disk space for Python dependencies and model files.
- Available RAM for PyTorch and GPT-2. The measured Python process used about
  **857 MB after loading GPT-2** on the development laptop; other devices can
  differ. This is **Path B: local, with logs**, rather than a 512 MB host.

If you already have the project, skip cloning and open its folder in your terminal.
Complete the model download before presenting.

## 2. Windows setup (PowerShell)

```powershell
git clone https://github.com/Subhradeep246/ai201-project4-provenance-guard-starter-v2026.git
cd ai201-project4-provenance-guard-starter-v2026
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe detector.py
```

If `python` is unavailable but the Python launcher is installed, use `py -3.13`
for the version and virtual-environment commands. Install a supported Python
version if neither command exists. Direct interpreter paths avoid needing
PowerShell activation or execution-policy changes.

Start the server in **Terminal 1**:

```powershell
$env:HOST = "127.0.0.1"
$env:PORT = "5000"
$env:AI201_DEBUG = "0"
$env:AI201_RATE_LIMITS = "1"
.\.venv\Scripts\python.exe app.py
```

Leave it running. Its development-server warning is expected for this local
capstone demonstration. Use `Ctrl+C` to stop it. Use Flask via `app.py` on
Windows: Gunicorn requires Unix and fails on Windows because `fcntl` is absent.

## 3. macOS and Linux setup (bash or zsh)

Both platforms use the commands below. On macOS, install a supported Python 3
if necessary. On Linux, your distribution may require its Python venv/pip
packages before `python3 -m venv` works. Check that `python3 --version` reports
3.11, 3.12, or 3.13; use a versioned executable such as `python3.13` if needed.

```bash
git clone https://github.com/Subhradeep246/ai201-project4-provenance-guard-starter-v2026.git
cd ai201-project4-provenance-guard-starter-v2026
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python detector.py
```

Start the server in **Terminal 1**:

```bash
HOST=127.0.0.1 PORT=5000 AI201_DEBUG=0 AI201_RATE_LIMITS=1 .venv/bin/python app.py
```

Leave it running. The local development-server warning is expected. Use `Ctrl+C`
to stop it. Virtual-environment activation is unnecessary with these paths.

## 4. Check the service and run the demo samples

Open **Terminal 2 in the project folder**. Wait for Terminal 1 to report that
it is running at http://127.0.0.1:5000.

### Windows PowerShell

Use `curl.exe`, since `curl` can be a PowerShell alias. File-based JSON avoids
Windows quoting problems. Keep each curl command on one line.

```powershell
$base = "http://127.0.0.1:5000"
curl.exe -sS "$base/ping" -H "Content-Type: application/json" --data-binary "@ping.json" | ConvertFrom-Json | ConvertTo-Json
curl.exe -sS "$base/health" | ConvertFrom-Json | ConvertTo-Json
curl.exe -sS "$base/submit" -H "Content-Type: application/json" --data-binary "@submit_human.json" | ConvertFrom-Json | ConvertTo-Json
curl.exe -sS "$base/submit" -H "Content-Type: application/json" --data-binary "@submit_plain.json" | ConvertFrom-Json | ConvertTo-Json
curl.exe -sS "$base/submit" -H "Content-Type: application/json" --data-binary "@submit_ai.json" | ConvertFrom-Json | ConvertTo-Json
```

### macOS / Linux

```bash
base=http://127.0.0.1:5000
curl -sS "$base/ping" -H 'Content-Type: application/json' --data-binary '@ping.json'
curl -sS "$base/health"
curl -sS "$base/submit" -H 'Content-Type: application/json' --data-binary '@submit_human.json'
curl -sS "$base/submit" -H 'Content-Type: application/json' --data-binary '@submit_plain.json'
curl -sS "$base/submit" -H 'Content-Type: application/json' --data-binary '@submit_ai.json'
```

Expected checks and reference results:

- `/ping`: `ok: true` and `you_sent: "hello"`.
- `/health`: `ok: true`, `rate_limiting: true`. `detector_loaded` can be false
  before the server's first scored submit. Running `detector.py` downloads the
  cached model but does not load it into the separate Flask process.
- Bus/rain paragraph (`submit_human.json`): recorded `human`, **0.2787**.
- Store paragraph (`submit_plain.json`): recorded `unsure`, **0.6700**.
- Repetitive paragraph (`submit_ai.json`): recorded `ai`, **0.8680**.

Compare your own output with these recorded values. Responses include
`content_id`, `model_score`, `style_score`, `combined_score`, `confidence`,
`guess`, and `label`. The field named `confidence` repeats the combined
AI-like score; it is not a calibrated probability of correctness.

The current thresholds are human <= **0.30**, AI >= **0.75**, and unsure between
them. Weights are 55% model / 45% style, or an equal average when the signal
gap is at least **0.40**. To see a disagreement, submit `submit_split.json`
using the same command pattern: the recorded combined score was **0.4945**, unsure.

## 5. Test your own writing, appeal it, and inspect the log

Use several sentences, a nonempty creator ID, and no more than 8,000 characters.
Replace the example paragraph below with your own writing.

### Windows PowerShell

This captures the fresh response, appeals its exact ID, and displays both events:

```powershell
$base = "http://127.0.0.1:5000"
$body = @{
    text = "I walked to the store after class. Rain had soaked my notebook, so I kept it inside my jacket. The cashier found a spare bag for me, and I carried the bread home before it got dark."
    creator_id = "capstone_guest"
} | ConvertTo-Json
$result = Invoke-RestMethod -Uri "$base/submit" -Method Post -ContentType "application/json; charset=utf-8" -Body ([System.Text.Encoding]::UTF8.GetBytes($body))
$result | ConvertTo-Json

$appealBody = @{
    content_id = $result.content_id
    reasoning = "I wrote this paragraph myself. Please review the label."
} | ConvertTo-Json
Invoke-RestMethod -Uri "$base/appeal" -Method Post -ContentType "application/json; charset=utf-8" -Body ([System.Text.Encoding]::UTF8.GetBytes($appealBody)) | ConvertTo-Json

$log = Invoke-RestMethod -Uri "$base/log"
$log.entries | Where-Object { $_.content_id -eq $result.content_id } | ConvertTo-Json -Depth 6
```

### macOS / Linux

This Python snippet uses the installed `requests` package to perform the same
steps without needing an extra JSON command-line tool:

```bash
.venv/bin/python - <<'PY'
import json
import requests

base = "http://127.0.0.1:5000"
response = requests.post(f"{base}/submit", json={
    "text": "I walked to the store after class. Rain had soaked my notebook, so I kept it inside my jacket. The cashier found a spare bag for me, and I carried the bread home before it got dark.",
    "creator_id": "capstone_guest",
}, timeout=180)
response.raise_for_status()
result = response.json()
print("Submission:", json.dumps(result, indent=2))

response = requests.post(f"{base}/appeal", json={
    "content_id": result["content_id"],
    "reasoning": "I wrote this paragraph myself. Please review the label.",
}, timeout=30)
response.raise_for_status()
print("Appeal:", json.dumps(response.json(), indent=2))

response = requests.get(f"{base}/log", timeout=30)
response.raise_for_status()
entries = [e for e in response.json()["entries"]
           if e.get("content_id") == result["content_id"]]
print("Log:", json.dumps(entries, indent=2))
PY
```

Expected: the appeal returns `under_review`. The log contains the original
`decided` entry and a separate appeal event with the same ID. The application
appends to `logs/audit.jsonl`; an appeal does not overwrite the decision.
Do not reuse the ID stored in the repository's `appeal.json`: it belongs to
an earlier run. Always use an ID from your own successful submission.

## 6. Verify invalid requests

The `-i` option displays HTTP status codes. Run these in Terminal 2.

Windows PowerShell:

```powershell
curl.exe -i http://127.0.0.1:5000/submit -H "Content-Type: application/json" --data-binary "@submit_empty.json"
curl.exe -i http://127.0.0.1:5000/submit -H "Content-Type: application/json" --data-binary "@submit_missing.json"
curl.exe -i http://127.0.0.1:5000/appeal -H "Content-Type: application/json" --data-binary "@appeal_unknown.json"
```

macOS / Linux:

```bash
curl -i http://127.0.0.1:5000/submit -H 'Content-Type: application/json' --data-binary '@submit_empty.json'
curl -i http://127.0.0.1:5000/submit -H 'Content-Type: application/json' --data-binary '@submit_missing.json'
curl -i http://127.0.0.1:5000/appeal -H 'Content-Type: application/json' --data-binary '@appeal_unknown.json'
```

Expected statuses: **400**, **400**, and **404**, plus rejection log entries.
An unknown ID must not create an appeal event. The automated suite also checks
oversized text. Rate-limited submissions can return 429 before validation.

## 7. Run the capstone test suites

Keep Terminal 1 running. Execute these in Terminal 2, waiting for each to finish.

### Windows PowerShell

```powershell
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe run_eval.py --trials 3 --label capstone
.\.venv\Scripts\python.exe eval_appeals.py
.\.venv\Scripts\python.exe run_attacks.py --set attack_set --label capstone
```

### macOS / Linux

```bash
.venv/bin/python test.py
.venv/bin/python run_eval.py --trials 3 --label capstone
.venv/bin/python eval_appeals.py
.venv/bin/python run_attacks.py --set attack_set --label capstone
```

What they do:

- `test.py` checks environment, packages, model availability, and service status.
  It is an environment check, not a detector-accuracy evaluation.
- `run_eval.py` exercises eight human paragraphs, a two-example score
  comparison, six label-coverage inputs, and three invalid bodies, across
  three trials each. Some paragraphs are reused across groups.
- `eval_appeals.py` checks five valid appeals and three unknown IDs, including
  what was recorded in the log.
- `run_attacks.py` sends 36 cases: six false-positive tests, six evasion tests,
  three AI examples, two irregular human examples, seven malformed requests,
  and twelve submissions sharing a creator ID.

Read `results/run_*_capstone.md`, `results/attack_run_*_capstone.md`, and
`results/appeals_eval.json`. Compare actual outcomes against `criteria.md`;
the acceptance evaluator still requires comparison with your targets. Attack
reports now fill every Verdict and Reason automatically for the bundled families.
The acceptance targets:

1. At most **1 of 8** human paragraphs labelled AI.
2. AI example scores at least **0.20** above the human example.
3. All **3 labels** appear in **6 inputs**.
4. **5 valid appeals** are under review; **3 unknown IDs** return 404 without
   appeal events.
5. Missing, empty, and over-**8,000-character** text return 400 plus rejection
   entries, never 500.

Testing appends to the existing audit file. `logs/` and `results/` are tracked
project evidence; preserve earlier runs. `appeals_eval.json` is overwritten on
rerun, and timestamped report names can collide within the same minute.

The saved before/after attack results show the improvement: raising
`config.py::AI_THRESHOLD` from **0.72 to 0.75** changed human example FP02 at
**0.7418** from AI to unsure. AI01 stayed AI at **0.8680**. Chopped AI example
EV03 still scored about **0.234** and was labelled human. These are small,
hand-selected tests, not a general accuracy benchmark.

### Attack verdicts and reports from earlier runs

Every attack row now has a Verdict and a Reason:

- **HELD:** human fixtures returned human/unsure, AI/evasion fixtures returned
  AI, malformed input returned 400, or a flood probe was blocked with 429.
- **BROKE:** a human fixture was accused, an AI fixture avoided the AI label,
  malformed input was accepted, an API/connection failed, or a flood probe
  reached its stated target of HTTP 200.
- **REVIEW:** an unknown family needs an expectation, or a 429 prevented the
  classification/validation being tested. The reason tells you what to check.

These verdicts evaluate the supplied fixtures and attack targets, not general
authorship accuracy. In particular, a flood probe accepted within the normal
allowance is expected. Its BROKE verdict means that individual probe reached
its 200 target, not that the limiter failed. The report separately shows how
many probes were accepted and blocked; inspect timing and quotas before
claiming that the limiter is correct or broken.

To add verdicts to the saved after-run **without running the model or server**:

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe run_attacks.py --set attack_set --rejudge results/attack_run_2026-11-12_1237_after.md --label feedback_after
```

macOS / Linux:

```bash
.venv/bin/python run_attacks.py --set attack_set --rejudge results/attack_run_2026-11-12_1237_after.md --label feedback_after
```

This writes a new timestamped report, records the source report, and preserves
the observed statuses, labels, scores, and content IDs. It does not pretend to
be a new live run or apply current thresholds to old scores. Expectations come
from the family definitions in the selected attack set. Original reports remain
unchanged. Use the same command with a before-run path to compare the results.

Report regression checks (no API/model needed):

```powershell
.\.venv\Scripts\python.exe -m unittest test_attack_reports -v
```

On macOS / Linux, replace the interpreter with `.venv/bin/python`.

## 8. Rate limits and a dedicated flood check

The default is **10 submissions per minute and 80 per day per creator ID**.
The 11th inside one minute is blocked with **429**. Invalid submissions also
count because limiting runs before validation. Changing creator IDs bypasses
this prototype's limit.

Windows PowerShell:

```powershell
$floodCreator = "capstone_flood_" + [guid]::NewGuid().ToString("N")
.\.venv\Scripts\python.exe run_attacks.py --flood 15 --creator $floodCreator
```

macOS / Linux:

```bash
.venv/bin/python run_attacks.py --flood 15 --creator "capstone_flood_$(date +%s)"
```

With a warm model and all requests inside one minute, expect ten 200s then five
429s. If scoring takes longer than a minute, the window can expire during the
run. Repeated suites reuse creator IDs. Wait for the minute window to expire
if you hit 429, or restart your local server for a fresh test session. Counts
are in memory and reset on restart; the audit file remains. Keep limiting
enabled when evaluating rate-limit behavior.

## 9. Troubleshooting and presentation preparation

- **Connection refused:** start Terminal 1 and check its address and port.
- **Port 5000 already in use:** use the existing project server, or stop that
  process in its own terminal before starting another copy.
- **First request is slow:** GPT-2 loads into the Flask process on first use.
  Send one sample before presenting so the model is warm.
- **503 detector unavailable:** check the server output and rerun the platform's
  `detector.py` command to diagnose package or download errors.
- **400 too-short text:** use a paragraph with several sentences.
- **404 on appeal:** use the ID from a successful submission on your copy.
- **Unexpected 429:** earlier submissions used the same creator ID; account
  for the minute/day limits before interpreting the result.
- **PowerShell JSON quoting errors:** use `curl.exe --data-binary "@file.json"`
  or the `Invoke-RestMethod` example above.

For a three-minute capstone presentation, have the model ready, show one live
submission, read one or two criteria with their numbers, show saved before/after
results, and explain the threshold change and remaining chopped-text failure.
