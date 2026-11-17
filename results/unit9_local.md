# Unit 9 — Path B local run

Produced on this Windows laptop, 17 Nov 2026.

## Why not a free host

Measured by `_unit9_budget.py` after `detector.warm_up()`:

```
pid 52132
RSS before model load: 14 MB
gpt2 loaded and ready.
RSS after gpt2 load:   857 MB
A typical free tier:   512 MB
Over budget:           345 MB
```

That is the process working set with gpt2 in memory, before Flask even answers a request. A 512 MB free tier is 345 MB short. The 550 MB weights also have to live on disk; a free host with no persistent disk would download them again after every idle spin-down.

## gunicorn on this machine

`gunicorn` is in `requirements.txt` and is the start command a Linux host would use (`Procfile`). On Windows it fails before it binds, because it needs `fcntl`:

```
python -m gunicorn app:app --bind 127.0.0.1:5000
ModuleNotFoundError: No module named 'fcntl'
```

So Path B here is Flask on loopback, debug off. The Linux command stays in the Procfile for a host that could actually hold the model — which a 512 MB free tier still could not.

## Local process

```
$env:AI201_DEBUG='0'; python app.py
```

Startup (debug off; Flask itself still warns it is not a production server):

```
Provenance Guard on http://127.0.0.1:5000
  detector model:  gpt2
  rate limiting:   ON
  audit log:       ...\logs\audit.jsonl

 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
```

## Live routes

`GET /health` after a scored submit:

```json
{"detector_loaded":true,"detector_model":"gpt2","log_entries":174,"ok":true,"rate_limiting":true}
```

`POST /submit` with `@submit_human.json` (HTTP 200):

```json
{"combined_score":0.2787,"confidence":0.2787,"content_id":"05e6acc8af054d5480a24d50ef5a3165","guess":"human","label":"We think a person wrote this.","model_score":0.3015,"style_score":0.2508}
```
