#!/usr/bin/env python3
"""Validate Humanizer's portable package surfaces without external dependencies."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import voice_profile


ROOT = Path(__file__).resolve().parent.parent
SKILL = (ROOT / "SKILL.md").read_text()
README = (ROOT / "README.md").read_text()
PLUGIN = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())


def require(match: re.Match[str] | None, message: str) -> re.Match[str]:
    if match is None:
        raise SystemExit(message)
    return match


frontmatter = require(
    re.match(r"\A---\n(.*?)\n---\n", SKILL, re.DOTALL),
    "SKILL.md must start with YAML frontmatter",
).group(1)

for nonportable_key in ("compatibility:", "allowed-tools:"):
    if re.search(rf"(?m)^{re.escape(nonportable_key)}", frontmatter):
        raise SystemExit(f"Remove nonportable frontmatter key: {nonportable_key[:-1]}")

skill_version = require(
    re.search(r'(?m)^\s+version:\s*["\']([^"\']+)["\']\s*$', frontmatter),
    "SKILL.md metadata.version is missing",
).group(1)
readme_version = require(
    re.search(r"(?m)^- \*\*([0-9]+\.[0-9]+\.[0-9]+)\*\*", README),
    "README version history is missing",
).group(1)

versions = {skill_version, readme_version, str(PLUGIN.get("version", ""))}
if len(versions) != 1:
    raise SystemExit(f"Version mismatch: {sorted(versions)}")

pattern_numbers = [
    int(number)
    for number in re.findall(r"(?m)^### ([0-9]+)\. ", SKILL)
]
if pattern_numbers != list(range(1, 34)):
    raise SystemExit(f"Expected patterns 1-33, found {pattern_numbers}")

readme_numbers = {
    int(number) for number in re.findall(r"(?m)^\| ([0-9]+) \|", README)
}
if readme_numbers != set(range(1, 34)):
    raise SystemExit("README pattern table must contain patterns 1-33")

if len(SKILL.splitlines()) > 500:
    raise SystemExit("SKILL.md exceeds the 500-line portability budget")

distribution = json.loads((ROOT / 'distribution.json').read_text())
edition = distribution.get('edition')
if edition not in {'public', 'private'}:
    raise SystemExit('Unknown distribution edition')
if distribution.get('core_version') != skill_version:
    raise SystemExit('Distribution version does not match the skill')
if distribution.get('personal_profile_included') is not (edition == 'private'):
    raise SystemExit('Profile inclusion does not match distribution edition')
if edition == 'private':
    profile = voice_profile.load(ROOT / 'profile/voice-profile.json')
    if (ROOT / 'profile/voice-profile.md').read_text() != voice_profile.render(profile):
        raise SystemExit('Private profile Markdown is stale; regenerate it from JSON')
else:
    repo_root = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
    if repo_root.returncode == 0 and Path(repo_root.stdout.strip()).resolve() == ROOT:
        tracked = subprocess.run(['git', '-C', str(ROOT), 'ls-files', '--', 'profile', '.profile-source.json'], check=True, capture_output=True, text=True)
        if tracked.stdout:
            raise SystemExit('Public package tracks personal profile files')

for path in [ROOT / 'SKILL.md', ROOT / 'README.md', *sorted((ROOT / 'references').glob('*.md'))]:
    for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if link.startswith(('http://', 'https://', '#', 'mailto:')):
            continue
        if not (path.parent / link.split('#')[0]).exists():
            raise SystemExit(f'Broken local reference in {path.name}: {link}')

print(f"Humanizer package v{skill_version} is valid")
