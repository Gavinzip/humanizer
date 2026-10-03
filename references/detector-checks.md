# Optional External Detector Checks

The public skill does not automatically submit writing to external services. Use this workflow only when the current user explicitly requests it or their own profile contains applicable standing authorization. Confirm the service and submitted material once if authorization is missing; a score target alone does not authorize disclosure. Never send retrieved writing samples, personal-profile records, account details, or unrelated source documents.

The private edition can carry its owner's standing authorization. A current request to skip checks, reproduce exact text, or only review overrides that default. Skill maintenance and surrounding conversation do not trigger submissions. Do not buy subscriptions or spend paid credits without separate authorization.

For an authorized Chinese three-model workflow, the following procedure uses V3 short-text, V3, and V2 and a strict less-than-5% target on each checked section. Other requested model sets or thresholds must be stated explicitly; do not imply the default target was met by a one-model check. A service failure is an unresolved check, never a zero score.

## Draft, Measure, Revise, Verify

1. Identify the purpose, audience, language, source facts, protected claims, and applicable user corrections. For a reflection, follow the user's requested focus and source material; do not invent a personal experience.
2. Preserve a comparison baseline. Use the user's original when editing, or the first complete source-grounded draft when writing new prose. Label assistant drafts correctly. Establish actual baseline results on all three models; an already verified result may be reused only for the exact text, model, and section scope.
3. Build a brief from the functions of the user's corrections, using [feedback-learning.md](feedback-learning.md). Diagnose a specific reading problem: a missing action/object, condition/choice, reason/result, example link, or repetitive ending. Adding ordinary words and connectors is appropriate when it repairs that relationship. Do not translate the feedback into a find-and-replace dictionary.
4. Measure the same coherent content sections with **V3 short-text, V3, and V2**. If any AI-class probability is **5% or higher**, revise the unresolved content and measure again. Do not stop at a human label, a low short-text score, an average below 5%, or an arbitrary small number of rounds. A 4.99% result meets the strict score target; 5.00% does not.
5. Recheck source fidelity and reading flow after every substantive revision. Retain distinct facts, numbers, terms, uncertainty, and useful content. Do not lower scores through fabricated experiences, added typos, arbitrary whitespace, gibberish, unrelated padding, or removing the point of the task. A more conversational draft is appropriate only if the requested register supports it.
6. Check the exact completed wording on all three models for every section. Any subsequent wording change invalidates those results for the altered sections. Changed segmentation also requires verification of the new windows. Do not ask for permission between already authorized editing rounds.
7. Deliver one readable final draft with a compact score/coverage report outside the copy. Record whether the technical score target is met separately from whether the user has accepted the voice. Integrate his next confirmed correction into the existing references; an assistant revision is not accepted personal style until he reviews it.

Completion requires the full requested content to be covered and every required model/section result to be strictly below 0.05, followed by fidelity and reading checks. No measurement guarantees what another detector or a person will think. Do not claim unmeasured improvements. If the service is unavailable, a request has an unresolved accepted event, or further changes would require invented facts or damage the requested content, diagnose the real blocker, continue independent authorized work, and explicitly report the unmet measurement instead of calling the task complete. There is no substitute score or silent fallback.

## Three Selected Hosted Models

The [official demo](https://huggingface.co/spaces/yuchuantian/AIGC_text_detector) exposes these mappings:

| CLI key | Demo tab | Model | API name |
|---|---|---|---|
| `v3short` | 中文-V3-短文本 | `yuchuantian/AIGC_detector_zhv3short` | `predict_zh4` |
| `v3` | 中文-V3 | `yuchuantian/AIGC_detector_zhv3` | `predict_zh` |
| `v2` | 中文-V2 | `yuchuantian/AIGC_detector_zhv2` | `predict_zh6` |

POST to `https://yuchuantian-aigc-text-detector.hf.space/gradio_api/call/<API_NAME>` returns an event ID; GET on that same event retrieves its result. The demo's **Use via API** and [hosted app source](https://huggingface.co/spaces/yuchuantian/AIGC_text_detector/blob/main/app.py) are the source of truth. These three models share `BertTokenizer` from the Chinese V3 repository and truncate inputs at 512 tokens. Verify current mappings/configuration if behavior changes; identify the actual model in the evidence.

These selected models are for Chinese. Apply the editorial and feedback workflow to other languages, but do not claim a language-appropriate three-model target from Chinese models or translate a deliverable merely to change its score. Use verified appropriate variants when supported by the requested workflow and clearly report any measurement limitation.

The returned probability belongs to the winning label. For `AI`, it is the AI-class probability. For `人类` / Human, the AI-class probability is `1 - winning_probability`. Human 62.66% therefore means AI 37.34%, not a 62.66% AI score. This is the model's binary class score, not the percentage of words actually authored by AI. Keep third-party category proportions, such as Decopy's mixed-text share, separate.

## Reusable Measurement Helper

The shipped [check-detector.py](../scripts/check-detector.py) uses Python's standard library and the hosted service. It downloads no local models or tokenizers and does not generate prose; the editing agent owns the revision and reasoning review.

```bash
python3 scripts/check-detector.py path/to/copy.txt --split-long --output path/to/final-evidence.json
```

Default: all three models, strict 5% target. With no file or `-`, it reads exact UTF-8 text from stdin. Use quoted heredocs or structured stdin, not text interpolated into shell code. Optional `--model v3short`, `--model v3`, or `--model v2` supports diagnosis/resuming one event, but a one-model result does not complete the three-model workflow.

The JSON includes the document digest, exact section text and offsets, section digests, model names/endpoints, event IDs, UTC measurement times, winning labels/probabilities, normalized AI probabilities, and a complete/target status. Require `three_model_target_met: true` for the default workflow; `target_met` alone can describe a single-model diagnostic. `max_verified_ai_probability` is the **worst measured section/model result**, not a document probability. Exit codes: `0` means every requested result met the target, `2` means complete measurements with an unmet target, `1` means an incomplete/error result. Successful results must be retained even if another request fails. `--output` checkpoints each accepted event and result so partial evidence is recoverable.

## Coverage and Comparable Sections

Never report a truncated prefix as a full-document result. The helper limits sections to 480 characters and a conservative 512-token upper bound, including special tokens, based on the verified lowercase/NFD/strip-accent BERT configuration. It labels the bound honestly; it is not an exact token count. Paragraph boundaries are preferred, then sentence boundaries. The original characters and separators are retained without gaps.

Use corresponding coherent content sections for baseline and revision. If length changes move automatic boundaries, document the mapping and remeasure the actual final sections. Do not cherry-pick friendly sentences, append filler, or change segmentation merely to hide a high result. Short pieces use a single full-text check; long pieces have separate section results and **no invented overall probability**. Check every paragraph's content, including the last one. If the score report is embedded in a document task, keep it outside the finished document.

## Pending Requests and Evidence

The helper logs accepted event IDs before waiting and persists them when `--output` is used. Gradio consumes completed event streams; a completed result is not assumed replayable. Resume an accepted pending event using the exact short input and explicitly selected model:

```bash
python3 scripts/check-detector.py path/to/section.txt --model v3 --event-id ACCEPTED_EVENT_ID
```

Do not queue duplicates because a wait timed out. Diagnose the accepted event and retain all already completed results. A model/error result is not a valid threshold result; it must not be treated as zero or hidden by the other models. Final evidence must match the delivered text digest.

Keep trial text and temporary checks in stdin or memory where practical. If temporary test files were created, list the exact agent-created files before deleting them, following the user's cleanup instructions. Preserve the delivered final text, requested score evidence, reusable runtime helper, pre-existing materials, and user photos.

## Score Target and Voice Acceptance

A detector result describes that tool's classification of the measured text. It does not establish authorship, guarantee another tool's result, or confirm that the user likes the wording. Continue to apply confirmed voice feedback even when the technical target is met. Do not convert measured success into an accepted personal-style rule.
