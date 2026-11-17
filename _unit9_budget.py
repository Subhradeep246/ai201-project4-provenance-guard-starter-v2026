"""Print working-set RAM after gpt2 loads. Unit 9 Path B evidence."""

import os
import subprocess

import detector


def rss_mb() -> float:
    raw = subprocess.check_output(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"(Get-Process -Id {os.getpid()}).WorkingSet64",
        ],
        text=True,
    ).strip()
    return int(raw) / (1024**2)


print(f"pid {os.getpid()}")
print(f"RSS before model load: {rss_mb():.0f} MB")
print(detector.warm_up())
after = rss_mb()
print(f"RSS after gpt2 load:   {after:.0f} MB")
print("A typical free tier:   512 MB")
print(f"Over budget:           {after - 512:.0f} MB")
