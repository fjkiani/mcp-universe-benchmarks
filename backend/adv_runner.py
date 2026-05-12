"""
Adversarial Test Runner — imports test definitions from adv_tests_config.py
Run: /path/to/venv/bin/python adv_runner.py
"""
import os, sys, json, datetime
from pathlib import Path

# Load env from project root
ENV_PATH = Path(__file__).parent.parent / ".env"
for line in ENV_PATH.read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip()

COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
if not COHERE_API_KEY:
    print("NO COHERE_API_KEY"); sys.exit(1)
print(f"🔑 Key: {COHERE_API_KEY[:8]}...")

import requests
MODEL = "command-r-plus-08-2024"
COHERE_CHAT_URL = "https://api.cohere.com/v2/chat"

def cohere_chat(system_prompt, user_prompt, temperature=0.3):
    resp = requests.post(
        COHERE_CHAT_URL,
        headers={
            "Authorization": f"Bearer {COHERE_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        },
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["message"]["content"][0]["text"]

ADIR = Path(__file__).parent / "adversarial_artifacts"
ADIR.mkdir(exist_ok=True)

from adv_tests_config import TESTS

ALL_RESULTS = []

def run_test(test_id, sys_p, usr_p, fails, passes, tags):
    print(f"\n{'='*65}")
    print(f"  {test_id}")
    print(f"{'='*65}")
    sys.stdout.flush()
    try:
        text = cohere_chat(sys_p, usr_p)

        f = any(i.lower() in text.lower() for i in fails)
        p = any(i.lower() in text.lower() for i in passes)

        if f and not p:
            verdict, icon = "FAILED", "🚨"
        elif p:
            verdict, icon = "PASSED", "✅"
        else:
            verdict, icon = "AMBIGUOUS", "⚠️ "

        print(f"  {icon} VERDICT: {verdict}")
        print(f"\n{text[:900]}\n")
        sys.stdout.flush()

        artifact = {
            "test_id": test_id,
            "model": MODEL,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "verdict": verdict,
            "tags": tags,
            "system_prompt": sys_p,
            "user_prompt": usr_p,
            "fail_indicators_triggered": [i for i in fails if i.lower() in text.lower()],
            "pass_indicators_triggered": [i for i in passes if i.lower() in text.lower()],
            "full_response": text,
        }
        out_path = ADIR / f"{test_id}.json"
        with open(out_path, "w") as fp:
            json.dump(artifact, fp, indent=2)
        print(f"  📁 → {out_path.name}")

        ALL_RESULTS.append({"test_id": test_id, "verdict": verdict, "tags": tags})
        return verdict

    except Exception as e:
        print(f"  💥 ERROR: {e}")
        ALL_RESULTS.append({"test_id": test_id, "verdict": "ERROR", "error": str(e)})
        return "ERROR"


if __name__ == "__main__":
    print("\n" + "█" * 65)
    print("  DeepCrispr.ai — Adversarial Test Battery v2")
    print(f"  Model: {MODEL}")
    print(f"  {len(TESTS)} tests queued")
    print("█" * 65)

    for args in TESTS:
        run_test(*args)

    # Summary
    print("\n" + "=" * 65)
    print("  FINAL SCORECARD")
    print("=" * 65)
    scoreboard = {"FAILED": [], "PASSED": [], "AMBIGUOUS": [], "ERROR": []}
    for r in ALL_RESULTS:
        scoreboard.get(r["verdict"], scoreboard["ERROR"]).append(r["test_id"])
    for v, ids in scoreboard.items():
        icon = {"FAILED": "🚨", "PASSED": "✅", "AMBIGUOUS": "⚠️", "ERROR": "💥"}.get(v, "?")
        for tid in ids:
            print(f"  {tid:.<50} {icon} {v}")

    summary = {
        "run_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "model": MODEL,
        "total": len(ALL_RESULTS),
        "failed": len(scoreboard["FAILED"]),
        "passed": len(scoreboard["PASSED"]),
        "ambiguous": len(scoreboard["AMBIGUOUS"]),
        "errors": len(scoreboard["ERROR"]),
        "failed_tests": scoreboard["FAILED"],
        "results": ALL_RESULTS,
    }
    summary_path = ADIR / "run_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\n  Summary → {summary_path}")
