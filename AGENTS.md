# Humanizer 維護規則

- `SKILL.md` 保留 33 項模式與原始授權；版本須同步 README 第一筆版本紀錄和 `.claude-plugin/plugin.json`。
- 共通編輯、Writing Style、回饋與個人 profile 分開維護，不把一位使用者的偏好塞進公開核心。
- 公開 repo 不追蹤 `profile/`、回饋全文、交付文件、帳號資料或外部作品全文。私人版只以明確指定的私人 profile 覆蓋核心。
- 新回饋分清確認、候選、拒絕與被取代，不把代理解讀視為使用者接受。維持每位使用者的 profile 隔離。
- 上傳使用 Git `push`，先取得使用者同意。不可用 GitHub contents API 繞過。
- 發佈前執行 `python3 scripts/validate-package.py`、profile 功能驗證、`npx skills add . --list` 與 `claude plugin validate .`，並檢查 stage 的檔案清單。測試暫存刪除前先告知，不刪使用者資料。
