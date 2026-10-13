# park-writing

Park 的写作框架：把他自己的内容（口述、转写、笔记）变成一条视频或一篇文章。

- `SKILL.md`：入口。三条硬规矩、每种形态走哪几步、第 4 步整理（11 点）。
- `references/`：每一步的细则。拍视频先看 `视频框架.md`。
- `module.yaml` / `MODULE.md`：工作台（content-studio）读的模块清单。

## 装

```bash
git clone https://github.com/zinan92/park-writing.git ~/work/park-writing
ln -sfn ~/work/park-writing ~/.claude/skills/park-writing
```

工作台按 `~/.claude/skills`、`~/.codex/skills`、`~/.agents/skills` 的顺序找 `park-writing`，也可以用环境变量 `CONTENT_STUDIO_WRITING_SKILL` 指定。

## 改

一件事一个 PR 进 `main`；`python3 -m pytest -q` 要过。持久的决定记进 `decision-log.md`。
