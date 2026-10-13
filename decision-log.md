# decision-log

格式：面对什么 / 定了什么 / 为什么 / 怎么验证 / 踩了什么坑。更早的决定在 park-operating-system 的 `decision-log.md`（10/5–10/12）。

## 2026-10-13 — park-writing 搬成单独的仓库

- 面对什么：Park 要的是 park-writing 本身（一套能开源的写作框架），不是 park-OS；park-OS 不开源。
- 定了什么：`skills/park-writing/` 连历史（`git subtree split`，11 次提交）搬到私有仓库 `zinan92/park-writing`，本机 clone 在 `~/work/park-writing`，`~/.claude/skills/park-writing` 改指到这里；park-OS 删掉那份。开源时把这个仓库改公开，不复制。
- 为什么：复制出去的公开版会停在复制那天；只留一份。
- 怎么验证：搬之前 `diff -r` 和 park-OS 那份逐字一样；工作台 `writing_rules.skill_dir()` 解析到新路径，`write_module.load()` 不报错。
- 踩了什么坑：工作台按软链接找 skill（`~/.claude/skills` → `.resolve()`），所以换链接就够，工作台代码不用动。
