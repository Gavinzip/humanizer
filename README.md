# Humanizer — Writing Style 與回饋學習

Humanizer 是一個能依你的回饋調整寫作風格的技能。寫報告、心得、文案或講稿時，你都可以直接告訴它哪裡不像自己，也可以貼上你會怎麼改。它會先修好這次的內容；你同意保存後，再把確認的偏好整理成你自己的寫作設定，之後寫同類內容時接著沿用。

回饋可以是用詞、語氣、句子怎麼接，也可以是「這篇應該多寫學到什麼」這種內容方向。它會理解修改背後的表達邏輯，累積你認可的寫法，讓後續稿件逐步更貼近你的風格。每位使用者都有各自的設定，心得、工作訊息和講稿也能分別調整。

此版由 MIT 授權的 `blader/humanizer` 2.9.1 與本機 2.15.0 擴充版整理而來，保留原始授權及 33 項模式。本專案獨立維護版本，沒有重新訓練模型，也不保證外部偵測器的結果。

## 安裝與使用

發佈後可用 `npx skills add Gavinzip/humanizer` 安裝；本機驗證可使用 `npx skills add . --list`。複製安裝時保留 `SKILL.md`、`references/`、`scripts/`、`assets/` 和 `agents/`。

```text
用 $humanizer 修這段話，保留事實，參考我提供的同類文章。
用 $humanizer 學習我這次的修改邏輯，之後同類心得沿用。
用 $humanizer 檢查哪裡難懂，只提意見，先不要改檔案。
```

## 直接回饋，逐步建立自己的風格

你不用一次把風格描述完整。可以邊寫邊回饋，例如：

```text
這句太正式，我會這樣寫：……
這裡要先交代原因，後面的例子才接得上。
這篇給同事看，語氣直接一點，先寫接下來要做什麼。
這次修改我喜歡，之後同類文案沿用這種語氣。
```

如果希望以後也記得，可以先說：「記住我的寫作偏好，之後同類內容沿用。」授權後，直接修改或明確認可的偏好會保存到你自己的本機 profile；後續可繼續回饋、調整或取消舊做法。代理推測出的習慣會先保留為候選，等你認可才套用。

保存的是可重用的寫作選擇與適用情境。你的個人設定不會提交到這個公開 repo，也不會套用到其他使用者。要讓下一次接續使用，請保留自己的 `profile/` 資料夾；單次稿件的事實、引用內容和帳號資訊不會當成寫作偏好。

## 中文三模型檢測：V3 短文本、V3、V2

分享版已包含檢測流程和 [check-detector.py](scripts/check-detector.py)，主技能的「中文檢測」一節也直接列出三個模型。完整對應與規則在 [detector-checks.md](references/detector-checks.md)。分享時保留整個技能資料夾，不能只複製 `SKILL.md`。

目前透過 Python 腳本呼叫 [Hugging Face 官方線上版](https://huggingface.co/spaces/yuchuantian/AIGC_text_detector) 的 API，模型在對方伺服器執行。使用者端需要 Python 3.10 以上和網路；不用下載模型、安裝 PyTorch 或準備 GPU。腳本測分數，使用技能的編輯代理負責修稿。

可直接這樣呼叫，這段指令同時授權提交本次正文：

```text
用 $humanizer 修改這篇中文文章，保留原意。
我同意把這篇待交付正文送到 Hugging Face 官方 AIGC_text_detector，
用中文 V3 短文本、V3、V2 檢測並反覆修改，
直到每個完整區段在三個模型的 AI 類別分數都低於 5%。
```

第一次尚未取得提交授權時，技能會先說明服務與提交範圍。若對方選擇未來也沿用，可保存到對方自己的 profile；不沿用其他人的授權或個人語氣。服務不可用時明確記錄未完成，分數達標也不保證其他工具的結果。

已授權的正文可用以下指令實測；預設測全部三個模型，長文章按區段完整涵蓋：

```bash
python3 scripts/check-detector.py path/to/copy.txt --split-long --output path/to/final-evidence.json
```

## 怎麼學習

- Writing Style 流程已內建：使用已提供的合適樣本；需要時透過實際可用的 search/retrieve 讀同類作品。沒有工具就說明限制，不假裝讀過。
- 保存原句、使用者版本、適用情境與接受狀態，判斷修改改善的是哪個讀者關係。
- 只有相關的 `confirmed` 規則會進寫作摘要；候選、拒絕與被取代的版本保留歷史，不作現行習慣。
- 以目前使用者的 profile 寫作，當次要求優先。心得、客戶訊息和技術審查可有各自規則，不混成固定人格。

取得保存授權後，用 `python3 scripts/feedback.py init --owner-id my-writing-profile` 初始化。回饋 JSON 的格式、狀態與操作見 [feedback-learning.md](references/feedback-learning.md) 和 [空白 profile 範例](assets/voice-profile.example.json)。`python3 scripts/feedback.py show --context lecture-reflection` 可查看這次用途會套用的規則。

`profile/` 預設被 Git 忽略，個人檔案留在使用者端；不蒐集他人的回饋上傳到這個公開 repo，不保存檢索全文。使用者若要求持久偏好，可依其記憶規則同步確認過的原則。

## 結構與檢測

`SKILL.md` 是入口與通用模式；Writing Style、回饋、繁中、講稿與外部檢測在各自 `references/`。`scripts/voice_profile.py` 管 profile 的驗證、範圍選擇與保存；`scripts/feedback.py` 提供操作介面。格式由使用者模板與文件工具負責。

外部偵測須有目前使用者的授權。公開版預設不提交文章；私人版可以保存明確的提交範圍和服務授權。既有中文三模型 helper 保留完整區段與實際分數證據；技術目標與使用者語氣認可分開，服務失敗不當作通過。

## 維護驗證

```bash
python3 scripts/validate-package.py
npx skills add . --list
claude plugin validate .
```

維護 Git 上傳前遵守使用者的 Push 同意規則。私人的預填版本以公開核心加 profile 維護，不把私人回饋改進公開程式時一併帶出。

## 33 Patterns Detected (with Before/After Examples)

### Content Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 1 | **Significance inflation** | "marking a pivotal moment in the evolution of..." | "was established in 1989 as part of a wider decentralization" |
| 2 | **Notability name-dropping** | "cited in NYT, BBC, FT, and The Hindu" | State sourced outlets plainly; condense facts only when requested |
| 3 | **Superficial -ing analyses** | "symbolizing... reflecting... showcasing..." | Remove, or keep only what the source supports |
| 4 | **Promotional language** | "nestled within the breathtaking region" | "is a town in the Gonder region" |
| 5 | **Vague attributions** | "Experts believe it plays a crucial role" | Name a real source or cut the claim |
| 6 | **Formulaic challenges** | "Despite challenges... continues to thrive" | Keep the sourced facts; cut the boosterism |

### Language Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 7 | **AI vocabulary** | "Actually... additionally... testament... landscape... showcasing" | "also... remain common" |
| 8 | **Copula avoidance** | "serves as... features... boasts" | "is... has" |
| 9 | **Negative parallelisms / tailing negations** | "It's not just X, it's Y", "..., no guessing" | State the point directly |
| 10 | **Rule of three** | "innovation, inspiration, and insights" | Use natural number of items |
| 11 | **Synonym cycling** | "protagonist... main character... central figure... hero" | "protagonist" (repeat when clearest) |
| 12 | **False ranges** | "from the Big Bang to dark matter" | List topics directly |
| 13 | **Passive voice / subjectless fragments** | "No configuration file needed" | Name the actor when it helps clarity |

### Style Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 14 | **Dash overuse** | "institutions—not the people—yet this continues—" | Repair interruptions; preserve ranges, quotations, and author habits |
| 15 | **Boldface overuse** | "**OKRs**, **KPIs**, **BMC**" | "OKRs, KPIs, BMC" |
| 16 | **Inline-header lists** | "**Performance:** Performance improved" | Remove redundancy; preserve useful structure during wording edits |
| 17 | **Title Case Headings** | "Strategic Negotiations And Partnerships" | "Strategic negotiations and partnerships" |
| 18 | **Emojis** | "🚀 Launch Phase: 💡 Key Insight:" | Remove emojis |
| 19 | **Quotation style** | Mismatched quotation typography | Follow the language and document; protect exact quotations |
| 26 | **Hyphenated word pairs** | “cross-functional, data-driven, client-facing” | Drop hyphens on common word pairs |
| 27 | **Persuasive authority tropes** | "At its core, what matters is..." | State the point directly |
| 28 | **Signposting announcements** | "Let's dive in", "Here's what you need to know" | Start with the content |
| 29 | **Fragmented headers** | "## Performance" + "Speed matters." | Let the heading do the work |
| 30 | **Diff-anchored writing** | "This function was added to replace..." | Describe what it does, not what changed |
| 31 | **Manufactured punchlines / staccato drama** | "It had no preference. No prior. No nostalgia." | Use varied sentence lengths and concrete claims |
| 32 | **Aphorism formulas** | "Symmetry is the language of trust" | Replace the formula with the actual claim |
| 33 | **Conversational rhetorical openers** | "Honestly? It depends..." | Remove the fake-candid setup |

### Communication Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 20 | **Chatbot artifacts** | "I hope this helps! Let me know if..." | Remove entirely |
| 21 | **Cutoff disclaimers** | "While details are limited in available sources..." | Find sources or remove |
| 22 | **Sycophantic tone** | "Great question! You're absolutely right!" | Respond directly |

### Filler and Hedging

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 23 | **Filler phrases** | "In order to", "Due to the fact that" | "To", "Because" |
| 24 | **Excessive hedging** | "could potentially possibly" | "may"; retain meaningful uncertainty and study limits |
| 25 | **Generic conclusions** | "The future looks bright" | Specific plans or facts |

## Version History

- **3.0.2** - Clarified how users give feedback, authorize persistent preferences, and build their own scoped writing style; made this workflow visible in the introduction and skill entrypoint. Existing storage and detector code remain unchanged.
- **3.0.1** - Made the hosted Chinese V3 short-text, V3 and V2 workflow visible in the skill entrypoint and sharing instructions; documented Python requirements, full-package sharing and per-user submission authorization. Measurement code and existing voice profiles remain unchanged.
- **3.0.0** - Integrated Writing Style reference selection and inspect-before-compose workflow; added scoped persistent profiles, explicit feedback states, owner isolation, and deterministic save/render helpers. Public package starts with no personal profile and requires authorization for external checks. Retains the canonical 33-pattern catalog.

## Attribution and License

See [LICENSE](LICENSE) and [sources.md](references/sources.md) for the original MIT notices and conceptual sources. Writing Style service access is conditional on the actual tools available in the user's environment.
