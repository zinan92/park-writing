# AGENTS.md — park-writing

- 这是 Park 写作框架的唯一一份。2026-10-13 从 park-operating-system 的 `skills/park-writing/` 搬出来（历史保留）；别处不抄写，本机 `~/.claude/skills/park-writing` 软链接到这里。
- 一件事一个 PR 进 `main`，分支 `feat/…` / `fix/…`；提交标题用中文，说清对 Park 有什么变化。
- 提 PR 前：`git diff --check`、`python3 -m pytest -q`。
- 工作台（content-studio）线上服务实时读这里：`module.yaml` 指到的标题（`文件#标题开头`）改名或删掉，工作台那一步会拒绝运行；改这些段落等于改工作台行为。
- 以后要开源：方法层公开，Park 自己的口气、数据留私有（2026-10-13 定，见 `decision-log.md`）。
