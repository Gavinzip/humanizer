#!/usr/bin/env python3
"""Measure every section of Chinese copy on three hosted detectors."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request


BASE_URL = "https://yuchuantian-aigc-text-detector.hf.space/gradio_api/call"
MODELS = {
    "v3short": ("yuchuantian/AIGC_detector_zhv3short", "predict_zh4"),
    "v3": ("yuchuantian/AIGC_detector_zhv3", "predict_zh"),
    "v2": ("yuchuantian/AIGC_detector_zhv2", "predict_zh6"),
}
MODEL = MODELS["v3short"][0]
ENDPOINT = f"{BASE_URL}/{MODELS['v3short'][1]}"
MAX_CHARACTERS = 480
MAX_TOKENS = 512
TIMEOUT = 45
HUMAN_LABELS = {"Human", "human", "\u4eba\u7c7b", "\u4eba\u985e"}


def token_upper_bound(text: str) -> int:
    """Bound the verified shared BERT tokenizer; this is not an exact count.

    Its lowercase/NFD/strip-accent configuration leaves at most one WordPiece
    per remaining non-whitespace character. Include CLS and SEP. No local
    tokenizer or model is required.
    """
    normalized = unicodedata.normalize("NFD", text.lower())
    return 2 + sum(1 for char in normalized
                   if not char.isspace() and unicodedata.category(char) != "Mn")


def fits_window(text: str) -> bool:
    return len(text) <= MAX_CHARACTERS and token_upper_bound(text) <= MAX_TOKENS


def split_text(text: str) -> list[str]:
    chunks = []
    position = 0
    while position < len(text):
        end = min(position + MAX_CHARACTERS, len(text))
        while end > position and not fits_window(text[position:end]):
            end -= 1
        if end == position:
            raise ValueError("Cannot fit a character in the verified model window")
        if end < len(text):
            window = text[position:end]
            minimum = len(window) // 2
            paragraphs = [m.end() for m in re.finditer(r"\n\s*\n", window) if m.end() >= minimum]
            sentences = [m.end() for m in re.finditer(r"[。！？!?]\s*", window) if m.end() >= minimum]
            useful = paragraphs or sentences
            if useful:
                end = position + useful[-1]
        chunks.append(text[position:end])
        position = end
    if "".join(chunks) != text or not all(fits_window(chunk) for chunk in chunks):
        raise RuntimeError("Segmentation changed the input or exceeded the model window")
    return chunks


def normalize_result(data: object) -> dict:
    if not isinstance(data, list) or len(data) != 2:
        raise ValueError("Unexpected detector response shape")
    label, probability = data
    probability = float(probability)
    if not 0 <= probability <= 1:
        raise ValueError("Invalid detector probability")
    if label == "AI":
        ai_probability = probability
    elif label in HUMAN_LABELS:
        ai_probability = 1 - probability
    else:
        raise ValueError(f"Unexpected detector label: {label!r}")
    return {
        "label": label,
        "winning_probability": probability,
        "ai_probability": ai_probability,
    }


def read_event(event_id: str, endpoint: str = ENDPOINT) -> dict:
    if not re.fullmatch(r"[A-Za-z0-9_-]+", event_id):
        raise ValueError("Invalid event ID")
    started = time.monotonic()
    event = None
    with urllib.request.urlopen(f"{endpoint}/{event_id}", timeout=TIMEOUT) as response:
        for raw_line in response:
            if time.monotonic() - started > TIMEOUT:
                raise TimeoutError(f"No verified result received for event {event_id}; completed streams cannot be replayed")
            line = raw_line.decode("utf-8").strip()
            if line.startswith("event: "):
                event = line[7:]
            elif line.startswith("data: ") and event == "complete":
                return normalize_result(json.loads(line[6:]))
            elif line.startswith("data: ") and event == "error":
                raise RuntimeError(f"Detector event {event_id} failed: {line[6:]}")
    raise RuntimeError(f"Stream ended without a verified result for event {event_id}")


def measure(text: str, event_id: str | None = None, model_key: str = "v3short", on_accepted=None) -> dict:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    model, api_name = MODELS[model_key]
    endpoint = f"{BASE_URL}/{api_name}"
    if event_id is None:
        request = urllib.request.Request(
            endpoint,
            data=json.dumps({"data": [text]}, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            event_id = json.load(response)["event_id"]
    accepted = {"model_key": model_key, "model": model, "endpoint": endpoint,
                "event_id": event_id, "sha256": digest}
    if on_accepted:
        on_accepted(accepted)
    print(json.dumps(accepted), file=sys.stderr, flush=True)
    result = read_event(event_id, endpoint)
    return {
        **accepted,
        "characters": len(text),
        "token_upper_bound": token_upper_bound(text),
        "measured_at_utc": datetime.now(timezone.utc).isoformat(),
        **result,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text_file", nargs="?", help="UTF-8 copy file; omitted or - reads stdin")
    parser.add_argument("--model", choices=["all", *MODELS], default="all", help="Default checks all three models")
    parser.add_argument("--max-ai-percent", type=float, default=5.0, help="Strict upper target")
    parser.add_argument("--output", help="Save evidence after each accepted request and result")
    parser.add_argument("--split-long", action="store_true", help="Report each segment separately")
    parser.add_argument("--event-id", help="Read an accepted pending event for this same short input; completed streams cannot be replayed")
    args = parser.parse_args()
    raw_text = sys.stdin.buffer.read() if args.text_file in (None, "-") else Path(args.text_file).read_bytes()
    text = raw_text.decode("utf-8")
    if not text.strip():
        parser.error("Copy is empty")
    if not 0 < args.max_ai_percent <= 100:
        parser.error("--max-ai-percent must be greater than 0 and at most 100")
    if not fits_window(text) and not args.split_long:
        parser.error("Input exceeds the verified window guard; map sections or use --split-long")
    chunks = split_text(text)
    if args.event_id and (len(chunks) != 1 or args.model == "all"):
        parser.error("Resume the exact short input with an explicit --model v3short, v3, or v2")
    keys = list(MODELS) if args.model == "all" else [args.model]
    report = {
        "models": {key: MODELS[key][0] for key in keys},
        "scope": "full_text" if len(chunks) == 1 else "segments_not_document_probability",
        "characters": len(text),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "target_ai_probability": args.max_ai_percent / 100,
        "sections": [],
        "results": [],
    }
    offset = 0
    for index, chunk in enumerate(chunks, start=1):
        report["sections"].append({"segment": index, "start_character": offset,
                                   "end_character": offset + len(chunk), "text": chunk,
                                   "token_upper_bound": token_upper_bound(chunk),
                                   "sha256": hashlib.sha256(chunk.encode("utf-8")).hexdigest()})
        offset += len(chunk)

    def checkpoint() -> None:
        completed = [row for row in report["results"] if row.get("state") == "complete"]
        report["complete"] = len(completed) == len(chunks) * len(keys)
        worst = max((row["ai_probability"] for row in completed), default=None)
        report["max_verified_ai_probability"] = worst
        report["target_met"] = (report["complete"] and worst is not None
                                and worst < report["target_ai_probability"])
        report["three_model_target_met"] = report["target_met"] and set(keys) == set(MODELS)
        if args.output:
            Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    checkpoint()
    for index, chunk in enumerate(chunks, start=1):
        for key in keys:
            row = {"segment": index, "model_key": key, "state": "pending"}
            report["results"].append(row)

            def accepted(data: dict) -> None:
                row.update(data)
                checkpoint()

            try:
                row.update(measure(chunk, args.event_id, key, accepted))
                row["state"] = "complete"
            except (OSError, ValueError, RuntimeError, KeyError, TypeError) as error:
                row["state"] = "error"
                row["error"] = str(error)
                print(json.dumps(row, ensure_ascii=False), file=sys.stderr, flush=True)
            checkpoint()
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["target_met"] else (2 if report["complete"] else 1)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        raise SystemExit(1)
