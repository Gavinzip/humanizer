"""Validate, select, and persist scoped writing preferences. No network access."""
from __future__ import annotations

import copy
import json
import os
import re
import tempfile
from pathlib import Path

STATUSES = {"confirmed", "candidate", "rejected", "superseded"}
KINDS = {"user-instruction", "user-correction", "user-accepted-candidate", "editorial-hypothesis"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(profile: dict) -> dict:
    require(isinstance(profile, dict) and profile.get("schema_version") == 1, "Unsupported profile schema")
    require(isinstance(profile.get("owner_id"), str) and bool(profile["owner_id"].strip()), "owner_id is required")
    require(type(profile.get("revision")) is int and profile["revision"] >= 0, "Invalid revision")
    defaults = profile.get("defaults")
    require(isinstance(defaults, dict), "defaults must be an object")
    require(isinstance(defaults.get("language"), str), "defaults.language must be a string")
    require(type(defaults.get("feedback_persistence_authorized")) is bool, "Feedback persistence authorization must be explicit")
    detector = defaults.get("detector_checks")
    require(isinstance(detector, dict) and type(detector.get("enabled")) is bool, "Invalid detector setting")
    require(detector.get("authorization") in {"none", "standing-deliverable"}, "Invalid detector authorization")
    require(not detector["enabled"] or detector["authorization"] == "standing-deliverable", "Enabled checks need standing authorization")
    require(detector.get("models") == ["v3short", "v3", "v2"], "Profile supports the documented three-model set")
    require(type(detector.get("target_ai_probability")) in {int, float} and 0 < detector["target_ai_probability"] < 1, "Invalid target probability")
    records = profile.get("preferences")
    require(isinstance(records, list), "preferences must be an array")
    ids = set()
    for record in records:
        require(isinstance(record, dict), "Preference must be an object")
        key = record.get("id")
        require(isinstance(key, str) and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", key) is not None, "Invalid preference id")
        require(key not in ids, f"Duplicate preference id: {key}")
        ids.add(key)
        require(record.get("status") in STATUSES, f"Invalid status: {key}")
        scopes = record.get("scope")
        require(isinstance(scopes, list) and len(scopes) > 0 and all(isinstance(s, str) and s.strip() for s in scopes), f"Invalid scope: {key}")
        require(len(set(scopes)) == len(scopes), f"Duplicate scopes: {key}")
        for field in ("principle", "applies_when", "does_not_apply", "rationale"):
            require(isinstance(record.get(field), str) and bool(record[field].strip()), f"Missing {field}: {key}")
        require(record.get("rationale_status") in {"explicit", "interpretation"}, f"Invalid rationale status: {key}")
        evidence = record.get("evidence")
        require(isinstance(evidence, dict) and evidence.get("kind") in KINDS, f"Invalid evidence: {key}")
        for field in ("context", "before", "after", "statement"):
            require(isinstance(evidence.get(field), str), f"Missing evidence.{field}: {key}")
        require(bool(evidence["context"].strip()), f"Evidence context required: {key}")
        require(isinstance(record.get("confirmation", ""), str), f"Invalid confirmation evidence: {key}")
        if record["status"] == "confirmed":
            require(evidence["kind"] != "editorial-hypothesis" or bool(record.get("confirmation", "").strip()), f"Hypothesis needs explicit confirmation: {key}")
            require(bool(evidence["after"].strip() or evidence["statement"].strip() or record.get("confirmation", "").strip()), f"Confirmed preference needs user evidence: {key}")
        supersedes = record.get("supersedes")
        require(isinstance(supersedes, list) and all(isinstance(x, str) for x in supersedes), f"Invalid supersedes: {key}")
        require(len(set(supersedes)) == len(supersedes) and key not in supersedes, f"Invalid supersession: {key}")
    for record in records:
        require(set(record["supersedes"]).issubset(ids), f"Unknown superseded preference: {record['id']}")
    return profile


def load(path: Path) -> dict:
    return validate(json.loads(path.read_text(encoding="utf-8")))


def selected(profile: dict, context: str | None = None) -> list[dict]:
    return [r for r in profile["preferences"] if r["status"] == "confirmed" and
            (context is None or context in r["scope"] or "all-prose" in r["scope"])]


def retire_superseded(profile: dict, record: dict) -> None:
    if record["status"] != "confirmed":
        require(not record["supersedes"], "Only confirmed feedback can supersede existing preferences")
        return
    by_id = {r["id"]: r for r in profile["preferences"]}
    for key in record["supersedes"]:
        require(key in by_id and key != record["id"], f"Unknown superseded preference: {key}")
        old = by_id[key]
        covers_old = "all-prose" in record["scope"] or set(old["scope"]).issubset(record["scope"])
        require(covers_old, "Partial scope changes need separate scoped records; do not retire a broader preference")
        require(old["status"] in {"confirmed", "candidate", "rejected"}, "Preference already superseded")
        old["status"] = "superseded"


def add(profile: dict, incoming: dict) -> dict:
    require(isinstance(incoming, dict) and incoming.get("owner_id") == profile["owner_id"], "Profile owner mismatch")
    record = incoming.get("preference")
    require(isinstance(record, dict), "preference must be an object")
    updated = copy.deepcopy(profile)
    require(record.get("id") not in {r["id"] for r in updated["preferences"]}, "Existing ids cannot be overwritten; use a new superseding record")
    updated["preferences"].append(copy.deepcopy(record))
    validate(updated)
    retire_superseded(updated, updated["preferences"][-1])
    updated["revision"] += 1
    return validate(updated)


def confirm(profile: dict, key: str, evidence: str) -> dict:
    require(bool(evidence.strip()), "User confirmation evidence is required")
    updated = copy.deepcopy(profile)
    matches = [r for r in updated["preferences"] if r["id"] == key]
    require(len(matches) == 1 and matches[0]["status"] == "candidate", "Only a known candidate can be confirmed")
    matches[0]["status"] = "confirmed"
    matches[0]["confirmation"] = evidence
    retire_superseded(updated, matches[0])
    updated["revision"] += 1
    return validate(updated)


def render(profile: dict, context: str | None = None) -> str:
    lines = ["# Current Writing Preferences", "", f"Profile: `{profile['owner_id']}`; revision: {profile['revision']}.", "",
             "Current instructions take precedence. Only confirmed, relevant preferences apply. Interpretations are not user-stated reasons.", "",
             "Defaults: " + json.dumps(profile["defaults"], ensure_ascii=False), ""]
    for record in selected(profile, context):
        lines.extend([f"## {record['id']}", "", f"Scope: {', '.join(record['scope'])}", "",
                      record["principle"], "", "Use when: " + record["applies_when"],
                      "Boundary: " + record["does_not_apply"],
                      f"Reason ({record['rationale_status']}): {record['rationale']}", ""])
    if not selected(profile, context):
        lines.extend(["No confirmed preferences for this context. Use the supplied draft and current brief.", ""])
    return "\n".join(lines)


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".profile-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def save(path: Path, profile: dict) -> None:
    validate(profile)
    atomic_write(path, json.dumps(profile, ensure_ascii=False, indent=2) + "\n")
    atomic_write(path.with_suffix(".md"), render(profile))
