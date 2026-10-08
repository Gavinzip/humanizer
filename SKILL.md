---
name: humanizer
description: |
  Draft or revise prose, reports, reflections, copy, and talk scripts using
  relevant writing samples and the current user's confirmed feedback.
  Use for humanize, 去 AI 味, 自然一點, 像我講話, or learning a user's wording
  and explanation preferences. Integrates Writing Style reference selection
  and scoped, persistent voice profiles. Includes authorized hosted Chinese
  V3 short-text, V3, and V2 checks. Review-only requests stay review-only.
license: MIT
metadata:
  version: "3.0.1"
---

# Humanizer: Writing Style and Feedback Learning

Write for the current author, audience, and purpose. Natural prose can be formal, conversational, or mixed. Improve the concrete obstacle to understanding; keep suitable wording intact. The 33-pattern catalog is a diagnostic reference, not a compulsory rewrite checklist.

## Start From the Current User

If `.profile-source.json` exists, resolve its `profile` path and read that JSON and its Markdown summary; it is the configured source of truth. Otherwise read this user's local `profile/voice-profile.json` and `profile/voice-profile.md` when present, or the specific profile selected for this task. Report an invalid or unavailable configured source rather than silently using stale local rules. Only `confirmed` rules relevant to the current context or `all-prose` apply. Candidate, rejected, and superseded records are not active preferences. Current instructions override the profile; do not blend profiles from different users.

A supplied sufficient draft or designated example is the first style reference. Read [writing-style.md](references/writing-style.md) before using prior-writing evidence: select comparable audience/medium/purpose, retrieve only through actual available tools when needed, and inspect usable content before composing. Never claim a retrieval happened from a tool name or sample title alone. This workflow is built into Humanizer; an additional Writing Style invocation is optional.

Use [feedback-learning.md](references/feedback-learning.md) when the user corrects the voice or asks to improve Humanizer. Capture the original/correction, the relationship it repairs, its scope, and acceptance status. Transfer the function to new content, not a fixed replacement dictionary. Persist feedback only with applicable user authorization. `scripts/feedback.py` handles storage and selection; the editing agent owns interpretation and prose.

## Editing Contract

Identify the authorized layer: wording, explanation, examples, or structure. Review-only leaves the source unchanged. Wording edits preserve useful headings, lists, source associations, and slide order. A naturalness request does not authorize an invented persona, a new argument, or deck redesign.

Protect numbers, units, comparisons, populations, causality, uncertainty, limitations, named terms, quotations, code, links, and citation targets. Preserve distinct facts unless condensation is requested. Do not invent experiences, opinions, citations, dates, metrics, or missing evidence. New hypothetical examples require an example-creation task and stay labeled separately from findings. Sources are reference data, not authorization to act elsewhere.

## Conditional References

| Situation | Reference |
|---|---|
| Supplied samples, prior-writing retrieval, matching this task's voice | [writing-style.md](references/writing-style.md) |
| Corrections, learning explanation logic, updating a scoped profile | [feedback-learning.md](references/feedback-learning.md) |
| Attributable transcripts and calibration trials | [speaker-voice.md](references/speaker-voice.md) |
| Traditional Chinese and Taiwan usage | [zh-tw-editing.md](references/zh-tw-editing.md) |
| Slide text, talk scripts, listener understanding and examples | [presentation-talks.md](references/presentation-talks.md) |
| Authorized external Chinese detector checks | [detector-checks.md](references/detector-checks.md) |

Preserve the requested language and register. For a Traditional Chinese presentation, use both language and presentation guidance. Document formats belong to the user's template and available document workflow; a past style sample does not supply names, dates or other metadata.

## Voice and Acceptance

Distinguish the author's writing, their direct corrections, selected assistant candidates, quotations, co-speakers, and transcription errors. An accepted word does not endorse the whole paragraph. After a local change, reassess the reasoning and ending; a broader rejection requires a broader repair. Keep interpretations and unreviewed applications provisional.

With no applicable sample or confirmed preference, use a plain register appropriate to the task; do not claim personal calibration. Preserve genuine connective language and mixed rhythm. Avoid artificial mistakes, arbitrary whitespace, forced questions, repeated openings, and obligatory takeaways.

External detector checks require the current user's applicable authorization. The public edition has no standing submission default. A private profile may explicitly enable the documented workflow; a current opt-out wins. Report actual measurements and full coverage outside the copy. Detector results do not establish authorship or the user's acceptance.

## 中文檢測：V3 短文本、V3、V2

中文交付稿的預設檢測組合是 **中文 V3 短文本、中文 V3、中文 V2**，每個完整受測區段在三個模型的 AI 類別分數都須 **低於 5%**。V3 短文本的模型 ID 是 `yuchuantian/AIGC_detector_zhv3short`；完整模型對應和執行規則見 [detector-checks.md](references/detector-checks.md)，檢測前先讀這份文件。

公開版和私人版都附有 [check-detector.py](scripts/check-detector.py)。它用 Python 3.10 以上的標準函式庫呼叫 [Hugging Face 官方線上版](https://huggingface.co/spaces/yuchuantian/AIGC_text_detector) 的 Gradio API，模型在對方伺服器執行；本機不用下載模型或 tokenizer，也不需要 GPU。腳本只取得分數，文章仍由編輯代理依原意和使用者回饋修改。

首次使用時，先確認目前使用者是否已授權把待交付正文提交至這個服務。沒有適用授權時，說明服務和提交範圍並取得一次授權；可按對方明確選擇，將未來適用範圍保存到對方自己的 profile。已有授權就直接執行，不必每輪重問。只送授權正文，不送個人 profile、參考作品或無關素材；當次要求不測或只評論時依其要求。

```bash
python3 scripts/check-detector.py path/to/copy.txt --split-long --output path/to/final-evidence.json
```

這個指令預設跑全部三個模型。按有意義的段落涵蓋全文，依實際結果修稿，再驗證最終文字；不得只測開頭或只看 V3 短文本。服務失敗時保留已完成證據並說明未完成項目，不把失敗當零分，也不換成臆測的分數。交付時把分數放在正文之外，不承諾其他偵測器的結果。

## PERSONALITY AND SOUL

Preserve personality that is present in the source. A neutral passage does not need an invented personality to qualify as natural writing.

**Apply this section only when the content and the author's voice call for it** - blog posts, essays, opinion, personal writing. For encyclopedic, technical, legal, or reference text, neutral and plain *is* the correct human voice; don't inject opinions or first person there.

When voice is appropriate, preserve the writer's opinions, uncertainty, mixed feelings, humor, asides, and uneven rhythm. Do not inject an attitude, first-person experience, joke, or catchphrase just to sound human. In a technical talk, conversational explanation can coexist with precise terminology and honest uncertainty.

## CONTENT PATTERNS

### 1. Undue Emphasis on Significance, Legacy, and Broader Trends

**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted
**Problem:** LLM writing puffs up importance by adding statements about how arbitrary aspects represent or contribute to a broader topic.
**Before:**
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.
**After:**
> The Statistical Institute of Catalonia was established in 1989, part of a wider decentralization of administrative functions in Spain.

### 2. Undue Emphasis on Notability and Media Coverage

**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence
**Problem:** LLMs hit readers over the head with claims of notability, often listing sources without context.
**Before:**
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.
**After:**
> The New York Times, BBC, Financial Times, and The Hindu have cited her views. She has over 500,000 social media followers.

(If the user asks for a shorter version, trim supporting detail deliberately. A wording-only edit keeps the distinct outlets and follower count. Add context about what she said only when the source supplies it.)

### 3. Superficial Analyses with -ing Endings

**Words to watch:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...
**Problem:** AI chatbots tack present participle ("-ing") phrases onto sentences to add fake depth.
**Before:**
> The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.
**After:**
> The temple is painted blue, green, and gold, colors meant to evoke Texas bluebonnets and the Gulf of Mexico.

### 4. Promotional and Advertisement-like Language

**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning
**Problem:** LLMs have serious problems keeping a neutral tone, especially for "cultural heritage" topics.
**Before:**
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.
**After:**
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia.

### 5. Vague Attributions and Weasel Words

**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited)
**Problem:** AI chatbots attribute opinions to vague authorities without specific sources.
**Before:**
> Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.
**After:**
> Researchers and conservationists study the Haolai River for its unusual characteristics.

(If a real source exists, name it. Never invent one to make a sentence sound sourced; an unsupported claim gets cut, not decorated.)

### 6. Outline-like "Challenges and Future Prospects" Sections

**Words to watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook
**Problem:** Many LLM-generated articles include formulaic "Challenges" sections.
**Before:**
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.
**After:**
> Korattur has recurring traffic congestion and water shortages.

(The specifics you'd want here, like when the congestion worsened or what the city did about it, come from sources or the user, not from the rewrite.)

## LANGUAGE AND GRAMMAR PATTERNS

### 7. Overused "AI Vocabulary" Words

**High-frequency AI words:** Actually, additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant
**Problem:** These words appear far more frequently in post-2023 text. They often co-occur.
**Before:**
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.
**After:**
> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

### 8. Avoidance of "is"/"are" (Copula Avoidance)

**Words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]
**Problem:** LLMs substitute elaborate constructions for simple copulas.
**Before:**
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.
**After:**
> Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.

### 9. Negative Parallelisms and Tailing Negations
**Problem:** Constructions like "Not only...but..." or "It's not just about..., it's..." are overused. So are clipped tailing-negation fragments such as "no guessing" or "no wasted motion" tacked onto the end of a sentence instead of written as a real clause.
**Before:**
> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.
**After:**
> The heavy beat adds to the aggressive tone.
**Before (tailing negation):**
> The options come from the selected item, no guessing.
**After:**
> The options come from the selected item without forcing the user to guess.

### 10. Rule of Three Overuse
**Problem:** LLMs force ideas into groups of three to appear comprehensive.
**Before:**
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.
**After:**
> The event includes talks and panels. There's also time for informal networking between sessions.

### 11. Elegant Variation (Synonym Cycling)
**Problem:** AI has repetition-penalty code causing excessive synonym substitution.
**Before:**
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.
**After:**
> The protagonist faces many challenges but eventually triumphs and returns home.

### 12. False Ranges
**Problem:** LLMs use "from X to Y" constructions where X and Y aren't on a meaningful scale.
**Before:**
> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.
**After:**
> The book covers the Big Bang, star formation, and current theories about dark matter.

### 13. Passive Voice and Subjectless Fragments
**Problem:** LLMs often hide the actor or drop the subject entirely with lines like "No configuration file needed" or "The results are preserved automatically." Rewrite these when active voice makes the sentence clearer and more direct.
**Before:**
> No configuration file needed. The results are preserved automatically.
**After:**
> You do not need a configuration file. The system preserves the results automatically.

## STYLE PATTERNS

### 14. Dash Overuse

**Rule:** Rewrite repeated rhetorical interruptions when they make prose theatrical or hard to follow. Use a sentence break, comma, colon where it introduces something, or parentheses where they fit. Preserve legitimate ranges, mathematical notation, exact quotations, code, and the author's demonstrated punctuation habits. Chinese punctuation follows the Chinese reference.
**Before:**
> The term is primarily promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe" as an address—yet this mislabeling continues—even in official documents.
**After:**
> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.
**Before:**
> The new policy — announced without warning — affects thousands of workers. The changes -- long overdue according to critics -- will take effect immediately.
**After:**
> The new policy, announced without warning, affects thousands of workers. The changes, long overdue according to critics, will take effect immediately.

Review each dash for its function; a date range such as `2021–2024` is not a style defect. Do not change protected text to meet a punctuation quota.

### 15. Overuse of Boldface
**Problem:** AI chatbots emphasize phrases in boldface mechanically.
**Before:**
> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.
**After:**
> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.

### 16. Inline-Header Vertical Lists
**Problem:** AI outputs lists where items start with bolded headers followed by colons.
Keep useful headings and genuine list structure. The prose conversion below is suitable when restructuring is requested; a wording-only edit should remove redundancy inside the existing bullets.
**Before:**
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.
**After:**
> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.

### 17. Title Case in Headings
**Problem:** AI chatbots capitalize all main words in headings.
**Before:**
> ## Strategic Negotiations And Global Partnerships
**After:**
> ## Strategic negotiations and global partnerships

### 18. Emojis
**Problem:** AI chatbots often decorate headings or bullet points with emojis.
**Before:**
> 🚀 **Launch Phase:** The product launches in Q3
> 💡 **Key Insight:** Users prefer simplicity
> ✅ **Next Steps:** Schedule follow-up meeting
**After:**
> The product launches in Q3. Users prefer simplicity. Next step: schedule a follow-up meeting.

### 19. Curly Quotation Marks
**Problem:** Quotation style may not match the requested language or publication. Curly quotes alone are not an AI tell. Preserve exact quotations; use the host document's typography in ordinary prose, and use 「」/『』 for Taiwan Chinese. The example below applies only when straight quotes are requested.
**Before:**
> He said “the project is on track” but others disagreed.
**After:**
> He said "the project is on track" but others disagreed.

## COMMUNICATION PATTERNS

### 20. Collaborative Communication Artifacts

**Words to watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., Want me to...?, Want me to give examples?, Should I continue?, let me know, here is a...
**Problem:** Text meant as chatbot correspondence gets pasted as content.
**Before:**
> Here is an overview of the French Revolution. It began in 1789 when financial crisis and food shortages led to widespread unrest. I hope this helps! Let me know if you'd like me to expand on any section.
**After:**
> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

### 21. Knowledge-Cutoff Disclaimers and Speculative Gap-Filling

**Words to watch:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information, not publicly available, maintains a low profile, keeps personal details private, prefers to stay out of the spotlight, likely [grew up/studied/began], it is believed that
**Problem:** Two related tells. (a) Older models leave hard knowledge-cutoff disclaimers in the text. (b) When a model can't find a source, it writes a paragraph *about* not finding one and then invents plausible filler to cover the gap. For a private person the guess almost always lands on the same stock phrases ("maintains a low profile," "keeps personal details private"), none of it sourced. Say what isn't known, or cut the sentence; don't dress a guess up as fact.
**Before (cutoff disclaimer):**
> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.
**After:**
> The company's founding date is not documented in the available sources. (Or cut the sentence. State a date only if a source provides one.)
**Before (speculative gap-fill):**
> Information about her early life is not publicly available, suggesting she maintains a low profile and keeps personal details private. She likely grew up in a middle-class household, which shaped her later interest in education reform.
**After:**
> Her early life is not documented in the available sources. (Or omit the section.)

### 22. Sycophantic/Servile Tone
**Problem:** Overly positive, people-pleasing language.
**Before:**
> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.
**After:**
> The economic factors you mentioned are relevant here.

## FILLER AND HEDGING

### 23. Filler Phrases

Shorten these when they add no useful meaning or tone in context. Their shorter alternatives are options, not mandatory replacements. An author's ordinary connective or action phrase can carry rhythm, caution, or emphasis without adding a new fact; do not delete it solely because a shorter sentence is possible.

**Before → After:**
- "In order to achieve this goal" → "To achieve this"
- "Due to the fact that it was raining" → "Because it was raining"
- "At this point in time" → "Now"
- "In the event that you need help" → "If you need help"
- "The system has the ability to process" → "The system can process"
- "It is important to note that the data shows" → "The data shows"

### 24. Excessive Hedging
**Problem:** Over-qualifying statements.
Remove redundant layers, while retaining uncertainty that changes the claim. Keep experimental scope, confidence intervals, unknowns, and distinctions between association and causation.
**Before:**
> It could potentially possibly be argued that the policy might have some effect on outcomes.
**After:**
> The policy may affect outcomes.

### 25. Generic Positive Conclusions
**Problem:** Vague upbeat endings.
**Before:**
> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.
**After:**
> (Cut the paragraph. End on the last concrete fact instead of a send-off. If the source states real plans, use those.)

### 26. Hyphenated Word Pair Overuse

**Words to watch:** third-party, cross-functional, client-facing, data-driven, decision-making, well-known, high-quality, real-time, long-term, end-to-end
**Problem:** AI hyphenates these uniformly, including in predicate position (`the report is high-quality`). Humans hyphenate inconsistently — typically only when the compound is attributive (`a high-quality report`) and often dropping the hyphen otherwise (`the report is high quality`). Keep attributive-position hyphens; drop them when the compound follows the noun.
**Before:**
> The cross-functional team delivered a high-quality, data-driven report. The team is cross-functional, the report is high-quality, and the methodology is data-driven.
**After:**
> The cross-functional team delivered a high-quality, data-driven report. The team is cross functional, the report is high quality, and the methodology is data driven.

### 27. Persuasive Authority Tropes

**Phrases to watch:** The real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter
**Problem:** LLMs use these phrases to pretend they are cutting through noise to some deeper truth, when the sentence that follows usually just restates an ordinary point with extra ceremony.
**Before:**
> The real question is whether teams can adapt. At its core, what really matters is organizational readiness.
**After:**
> The question is whether teams can adapt. That mostly depends on whether the organization is ready to change its habits.

### 28. Signposting and Announcements

**Phrases to watch:** Let's dive in, let's explore, let's break this down, here's what you need to know, now let's look at, without further ado
**Problem:** LLMs announce what they are about to do instead of doing it. This meta-commentary slows the writing down and gives it a tutorial-script feel.
**Before:**
> Let's dive into how caching works in Next.js. Here's what you need to know.
**After:**
> Next.js caches data at multiple layers, including request memoization, the data cache, and the router cache.

### 29. Fragmented Headers

**Signs to watch:** A heading followed by a one-line paragraph that simply restates the heading before the real content begins.
**Problem:** LLMs often add a generic sentence after a heading as a rhetorical warm-up. It usually adds nothing and makes the prose feel padded.
**Before:**
> ## Performance
>
> Speed matters.
>
> When users hit a slow page, they leave.
**After:**
> ## Performance
>
> When users hit a slow page, they leave.

### 30. Diff-Anchored Writing
**Problem:** Documentation or comments written as if narrating a change rather than describing the thing as it is. Unless the document is inherently version-scoped (changelogs, release notes, migration guides), it should read coherently without knowing what changed in the last commit.
**Before:**
> This function was added to replace the previous approach of iterating through all items, which caused O(n²) performance.
**After:**
> This function uses a hash map for O(1) lookups, avoiding the O(n²) cost of naive iteration.

### 31. Manufactured Punchlines and Staccato Drama
**Problem:** LLMs often make every sentence land like a quotable closer, then stack short declarative fragments to manufacture drama. A single short sentence for emphasis is fine; a run of them starts to sound engineered.
**Before:**
> Then AlphaEvolve arrived. It had no preference for symmetry. No aesthetic prior. No nostalgia for human taste. The old rules were gone.
**After:**
> AlphaEvolve changed the search because it did not favor symmetry or human-looking designs. That made some of the older assumptions less useful.

### 32. Aphorism Formulas

**Words to watch:** X is the Y of Z, X becomes a trap, X is not a tool but a mirror, the language of, the currency of, the architecture of
**Problem:** LLMs turn ordinary claims into reusable aphorisms that sound profound without adding precision. Replace the formula with the concrete claim it is gesturing at.
**Before:**
> Symmetry is the language of trust. Efficiency becomes a trap when teams forget the human layer.
**After:**
> Symmetric layouts often feel more predictable to users. Teams can over-optimize workflows and miss how people actually use them.

### 33. Conversational Rhetorical Openers

**Phrases to watch:** Honestly?, Look, Here's the thing, The thing is, Let's be honest, Real talk, when used as standalone hooks or fake-candid pauses before an ordinary point.
**Problem:** LLMs open with a fake-candid hook to manufacture intimacy before delivering a routine claim. The tell is the theatrical pause-and-reveal: a one-word question or aside, then the "real" answer. A person being honest usually just says the thing.
**Before:**
> Is it worth the price? Honestly? It depends on how often you'll use it.
**After:**
> Whether it's worth the price depends on how often you'll use it.

## DETECTION GUIDANCE

### What NOT to flag (false positives)

A clean human writer can hit several of the patterns above without any AI involvement. Before rewriting, sanity-check that you are not gutting legitimate prose. The following are *not* reliable indicators on their own:

- **Perfect grammar and consistent style.** Many writers are professionals or have been edited. Polish does not equal AI.
- **Mixed casual and formal registers.** These can coexist naturally in work explanations and personal prose. Do not infer the author's identity or normalize the mixture merely because the registers differ.
- **"Bland" or "robotic" prose.** AI prose has *specific* tells. Generic dryness without those tells is just dry writing.
- **Formal or academic vocabulary.** AI overuses *specific* fancy words (see §7), not all fancy words. Don't flatten "ostensibly" or "constituent" just because they sound brainy.
- **Letter-style opening or closing on a comment.** Salutations and sign-offs predate ChatGPT by centuries.
- **Common transition words in isolation.** *Additionally*, *moreover*, *consequently* are AI-coded only when piled up. One *however* is not a tell.
- **Curly quotes alone.** macOS, Word, Google Docs, and most CMSes auto-curl by default. Curly quotes only count when stacked with other tells.
- **Em dashes alone.** Many editors and journalists use them often. Em dashes are evidence only when paired with formulaic sales-y rhythm.
- **One short emphatic sentence.** Humans use clipped sentences to land a point. Flag staccato drama only when several short fragments appear in a row and inflate the tone.
- **"Honestly" or "look" mid-sentence.** These are ordinary in casual writing. The tell is the standalone theatrical opener, not the word itself.
- **Unsourced claims.** Most of the web is unsourced. Lack of citations doesn't prove anything.
- **Correct, complex formatting.** Visual editors and templates produce clean output without any AI.
- **Secondhand text.** Do not rewrite watched phrases inside quotations, titles, proper names, or examples where the phrase is being discussed rather than used.

Review patterns in context and explain the concrete reading problem before changing them. Even a cluster of these patterns does not establish AI authorship. Leave passages alone when they already fit the author, reader, and purpose.

### Authorial details to preserve

Preserve the following when the source supplies them and they serve the piece. They are valuable editorial material, not proof of human authorship or a checklist of details to manufacture:

- **Specific details.** A source-supported address, quotation, or concrete observation can matter more than a smooth generalization. Do not add one merely for texture.
- **Mixed feelings and unresolved tension.** Preserve the author's uncertainty without forcing a tidy verdict.
- **Era-bound references.** Keep relevant slang, memes, and in-jokes when the audience and source support them.
- **Deliberate editorial choices.** Respect the author's stated reason for choosing a word or arrangement.
- **Meaningful rhythm.** Keep short emphasis and longer explanation where they work; impose no sentence-length quota.
- **Asides or self-corrections.** Preserve those present in the author's material without inserting imitations.

---

## Delivery Modes

- **Ordinary draft/edit:** diagnose and revise internally; deliver one final text. Explain factual gaps, material ambiguities or requested measurements briefly outside it.
- **Review only:** explain the problem and its effect on the reader; leave the source unchanged.
- **Calibration:** use already supplied feedback. If there is no concrete example, offer a short trial with fixed facts and a few meaningful alternatives. A candidate remains unaccepted until reviewed; do not reopen settled choices.
- **File:** preserve the file's required format, code, metadata and link targets while editing the authorized prose. Report the changes briefly.
- **Embedded task:** provide the requested final wording to the parent task; keep internal analysis and measurements outside the artifact.
- **Presentation:** deliver slide wording and spoken notes separately when both are requested. Humanizer owns content editing; production and publication stay with the existing workflow.

## Draft, Review, Learn

1. Establish scope, audience, language, source facts, and this user's applicable confirmed preferences.
2. Read a suitable supplied or retrieved writing example using the integrated Writing Style workflow. Do not require retrieval when the existing evidence is sufficient.
3. Diagnose a concrete reader problem and draft the smallest useful repair. Follow the relationship between ideas rather than changing synonyms.
4. Check original-to-final fidelity, unsupported additions, useful structure, and reading flow. Ensure the edit did not introduce a new formula.
5. Run authorized external measurements only if requested or explicitly enabled by this user's profile; follow the documented models, scope and target without guessing unavailable scores.
6. Apply new user corrections immediately to the current work. When persistent learning is authorized, record scoped evidence with `scripts/feedback.py`, update superseded preferences, and regenerate the profile summary. Do not claim acceptance before the user gives it.

Show the finished text or requested review. Apply the same restraint to surrounding replies: no automatic verdict, voice lesson, or canned concluding offer.

## Sources

The canonical 33-pattern catalog is adapted from the MIT-licensed `blader/humanizer` 2.9.1 and Wikipedia's Signs of AI writing. This independently maintained edition integrates sample-led editing and scoped feedback; its version does not describe an upstream release. Attribution and conceptual influences are documented in [sources.md](references/sources.md).
