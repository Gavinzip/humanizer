# Sources and Local Adaptation

This maintained Humanizer derivative extends the installed `blader/humanizer` 2.9.1. The existing 33 numbered patterns remain in `SKILL.md`; the extensions add conditional references for Traditional Chinese, speaker voice, and presentation explanations. This is not a claim that the upstream projects released this local version.

Reviewed on 2026-09-07:

| Source | Revision | Used for |
|---|---|---|
| [nagameTW/humanizer-zh-tw](https://github.com/nagameTW/humanizer-zh-tw/blob/12087742fbad6a971d7c3c65b79e846034018772/SKILL.md) | `12087742fbad6a971d7c3c65b79e846034018772` | Chinese register, punctuation, protected meaning, and sample-led voice editing |
| [Speaker Toolkit README](https://github.com/jbaruch/speaker-toolkit/blob/8456d7eae79191ba50dbedee1f108044f7a435e0/README.md) | `8456d7eae79191ba50dbedee1f108044f7a435e0` | Concept of deriving speaking habits from the speaker's own material |
| [Speaker Toolkit content guidance](https://github.com/jbaruch/speaker-toolkit/blob/8456d7eae79191ba50dbedee1f108044f7a435e0/skills/presentation-creator/references/phase3-content.md) | Same revision | Separation of slide content and script, source-based verbal habits, evidence for pacing |
| [Speaker Toolkit ingress](https://github.com/jbaruch/speaker-toolkit/blob/8456d7eae79191ba50dbedee1f108044f7a435e0/skills/vault-ingress/SKILL.md) | Same revision | Observations tied to source locations and limits of available source types |

The Speaker Toolkit influence is conceptual; no implementation, scripts, vault schema, taxonomy catalog, publishing workflow, or substantial source text is bundled. Its runtime dependencies and phase approval gates are not requirements of this local editor.

The example-selection rubric and small editing examples are locally authored for the requested presentation improvements. Their fictional inputs are not evidence about an actual paper. These references are used locally without fetching upstream content on each invocation.

## Attribution

The base Humanizer retains its original `LICENSE`. The Traditional Chinese adaptation credits `nagameTW/humanizer-zh-tw`; its MIT notice is included below.

MIT License

Copyright (c) 2026 nagameTW

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Writing Style Integration

The style-reference workflow was informed by the installed Writing Style (`write-like-me`, version 0.1.1) instructions: prefer supplied comparable samples; use available search/retrieve actions when needed; read usable content before composing; keep source provenance; do not retain a retrieved corpus. The integration and feedback-storage code here are independently authored. No plugin implementation or complete plugin instruction file is bundled. This package does not imply ownership of or guaranteed access to the Writing Style service.
