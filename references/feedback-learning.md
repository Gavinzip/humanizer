# 從使用者回饋學習

這份流程處理持久偏好，不修改模型權重。寫作前讀目前使用者的 profile；同一原則要依用途選用，不能把心得的寫法套到每種文案。

## 記錄什麼

收到「這裡改成……」「這句太生硬」「之後都這樣寫」時，保留修改的證據與範圍，再判斷它處理的關係：動作／對象、情境／選擇、原因／結果、一般想法／例子、程度／範圍或重複收尾。原則說明要回答這次修改幫讀者理解了什麼，不只寫「更自然」。

記錄欄位見 [voice-profile.example.json](../assets/voice-profile.example.json)：`id`、`scope`、`status`、`principle`、`applies_when`、`does_not_apply`、`evidence`、`rationale`、`rationale_status`、`supersedes`。證據中的原文與修正只存使用者直接提供的必要片段，不複製檢索全文或不相關私人資料。

- `confirmed`：使用者明確要求、直接修改，或明確認可的偏好。
- `candidate`：代理推測或新寫的候選；不得當成已確認習慣套用。
- `rejected`：使用者拒絕的做法，保留脈絡以免再誤用。
- `superseded`：被較新的明確回饋取代；不再作為現行偏好。

`rationale_status` 分開標記原因是使用者明說的 `explicit`，或代理解讀的 `interpretation`。直接修改可以確認局部選擇，但不能把推測原因、整段或所有用途一併升級成確認。

## 應用與更新

1. 先讀使用者已給的修改，不重新詢問同一個選擇。範圍不明時保持當次用途；只有會影響工作時才釐清。
2. 在新內容中重用該關係，而非原詞。例如需要先交代情境時補條件，需要讓動作清楚時指出對象；不固定撒同一個連接詞。
3. 檢查整段意思、事實與收尾。局部接受不代表整段已驗收，分數通過也不代表本人認可。
4. 當次明確要求保存，或 profile 的 `defaults.feedback_persistence_authorized` 有適用授權時，用 `scripts/feedback.py` 更新 profile；沒有時先完成當次修改，在要持久保存前取得一次授權。拒絕保存不妨礙當次編輯。
5. 明確取代舊偏好時使用 `supersedes`，保留歷史。局部情境的修正不能停用其他情境仍有效的廣泛偏好；需要時拆成不同範圍的紀錄。新候選要到使用者認可才轉 `confirmed`，附上確認證據。

## 操作

每位使用者使用各自的 profile 路徑與 `owner_id`，不讀取另一位使用者的檔案。預設的 `profile/` 不進公開 Git。第一次經授權初始化：

```bash
python3 scripts/feedback.py init --owner-id my-writing-profile
python3 scripts/feedback.py add /path/to/user-correction.json
python3 scripts/feedback.py show --context lecture-reflection
python3 scripts/feedback.py confirm preference-id --evidence '使用者這次明確接受的回覆'
```

`add` 的 JSON 必須包含相同 `owner_id` 與一個 `preference` 物件。初始化範例沒有預先填入任何人的偏好。工具保存並產生 `voice-profile.md`；它不推測語意，也不替使用者宣布接受。編輯代理負責解讀回饋、選適用情境與檢查新稿。

`--profile` 可選定這次使用者自己的 JSON；同目錄的 Markdown 是該 JSON 的可讀摘要。若安裝有 `.profile-source.json`，工具預設寫入該來源，並同步同一使用者的本機摘要副本；來源壞掉時報錯，不改用過期檔案。起草時只用同用途的 `confirmed` 規則與當次指示，保留其適用界線；不能把候選當成已學會的聲音。
