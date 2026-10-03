#!/usr/bin/env python3
"""Maintain a user's writing profile from explicitly attributable feedback."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import voice_profile

ROOT = Path(__file__).resolve().parent.parent


def default_profile() -> Path:
    pointer = ROOT / '.profile-source.json'
    if pointer.exists():
        data = json.loads(pointer.read_text())
        voice_profile.require(isinstance(data.get('profile'), str) and bool(data['profile']), 'Invalid profile-source pointer')
        return Path(data['profile']).expanduser().resolve()
    return ROOT / 'profile' / 'voice-profile.json'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    try:
        primary = default_profile()
    except (ValueError, OSError) as exc:
        parser.exit(2, f'Profile source failed: {exc}\n')
    parser.add_argument("--profile", type=Path, default=primary)
    commands = parser.add_subparsers(dest="command", required=True)
    initialize = commands.add_parser("init")
    initialize.add_argument("--owner-id", required=True)
    append = commands.add_parser("add")
    append.add_argument("record", type=Path)
    confirm = commands.add_parser("confirm")
    confirm.add_argument("id")
    confirm.add_argument("--evidence", required=True)
    show = commands.add_parser("show")
    show.add_argument("--context")
    commands.add_parser("validate")
    args = parser.parse_args()
    try:
        mirror = ROOT / 'profile' / 'voice-profile.json'
        linked = (ROOT / '.profile-source.json').exists() and args.profile.resolve() == primary and mirror.resolve() != primary
        if args.command == "init":
            voice_profile.require(not args.profile.exists() and not args.profile.with_suffix('.md').exists(), "Profile already exists; initialization would overwrite it")
            profile = json.loads((ROOT / "assets" / "voice-profile.example.json").read_text())
            profile["owner_id"] = args.owner_id
            voice_profile.save(args.profile, profile)
        else:
            profile = voice_profile.load(args.profile)
            if linked and mirror.exists():
                voice_profile.require(voice_profile.load(mirror)['owner_id'] == profile['owner_id'], 'Installed profile owner mismatch')
            if args.command == "show":
                print(voice_profile.render(profile, args.context), end="")
                return 0
            if args.command == "validate":
                print(f"Profile valid: revision {profile['revision']}; {len(profile['preferences'])} records")
                return 0
            if args.command == "add":
                profile = voice_profile.add(profile, json.loads(args.record.read_text()))
            elif args.command == "confirm":
                profile = voice_profile.confirm(profile, args.id, args.evidence)
            voice_profile.save(args.profile, profile)
        if linked:
            voice_profile.save(mirror, profile)
        print(f"Saved revision {profile['revision']} to {args.profile}")
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f"Profile update failed: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
