#!/usr/bin/env python3
"""Run the baseline and our method on the photos in data/photos and save every answer.

    python run_models.py --split dev            # the photos used to tune the prompts
    python run_models.py --split test           # the held-out photos; allowed only after PROMPTS_FROZEN.txt exists

Answers go to results/outputs/<system>/<photo name>.json. A photo that already has an answer is skipped,
so an interrupted run can simply be started again. Needs GEMINI_API_KEY (a free key from aistudio.google.com).
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

import secondlife as sl

ROOT = Path(__file__).resolve().parent
PHOTOS, OUT = ROOT / "data" / "photos", ROOT / "results" / "outputs"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}

try:                                    # iPhone photos (HEIC) need this optional package
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass


def photo_split() -> dict[str, list[Path]]:
    """Photos sorted by file name; every fourth one (1st, 5th, 9th, ...) is a development photo, the rest are test photos."""
    photos = sorted((p for p in PHOTOS.iterdir() if p.suffix.lower() in EXTENSIONS), key=lambda p: p.name.casefold())
    return {"dev": photos[0::4], "test": [p for i, p in enumerate(photos) if i % 4 != 0], "all": photos}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--split", choices=["dev", "test", "all"], default="dev")
    parser.add_argument("--system", choices=["pipeline", "baseline", "both"], default="both")
    parser.add_argument("--lang", choices=["ru", "en"], default="ru")
    parser.add_argument("--limit", type=int, default=0, help="only the first N photos of the split")
    args = parser.parse_args()
    if args.split in ("test", "all") and not (ROOT / "PROMPTS_FROZEN.txt").exists():
        sys.exit("The test photos are locked: PROMPTS_FROZEN.txt does not exist yet (prompts are still being tuned on the dev photos).")

    photos = photo_split()[args.split]
    photos = photos[:args.limit] if args.limit else photos
    systems = ["baseline", "pipeline"] if args.system == "both" else [args.system]
    done = failed = skipped = 0
    for photo in photos:
        for system in systems:
            target = OUT / system / f"{photo.stem}.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                skipped += 1
                continue
            started = time.time()
            try:
                card = getattr(sl, system)(photo, lang=args.lang)
                card["_meta"].update({"photo": photo.name, "model": sl.MODEL, "lang": args.lang, "seconds": round(time.time() - started, 1)})
                target.write_text(json.dumps(card, ensure_ascii=False, indent=2))
                done += 1
                print(f"ok   {system:8s} {photo.name}: {card['verdict']} | {card['idea_title']}", flush=True)
            except Exception as error:                      # keep going: one bad photo must not stop the run
                failed += 1
                (target.with_suffix(".error.txt")).write_text(f"{type(error).__name__}: {error}")
                print(f"FAIL {system:8s} {photo.name}: {type(error).__name__}: {str(error)[:200]}", flush=True)
    seconds = [c["seconds"] for c in sl.CALL_LOG if c["status"] == 200]
    info = {"split": args.split, "photos": len(photos), "model": sl.MODEL, "answers_written": done, "skipped_existing": skipped, "failed": failed,
            "model_calls": len(sl.CALL_LOG), "calls_not_ok": sum(c["status"] != 200 for c in sl.CALL_LOG),
            "median_seconds_per_call": round(statistics.median(seconds), 1) if seconds else None, "finished": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())}
    (OUT / f"run_info_{args.split}.json").write_text(json.dumps(info, indent=2))
    print(json.dumps(info))


if __name__ == "__main__":
    main()
