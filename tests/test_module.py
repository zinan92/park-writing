"""park-writing 的清单要自洽：工作台读它，写错了会拒绝运行，所以先在这里挡住。"""
from __future__ import annotations

import unittest
from pathlib import Path

import yaml

SKILL = Path(__file__).resolve().parents[1]
GROUPS = {"写", "风格", "查"}
STATUS = {"split", "whole", "planned"}
OUTPUT = {"article", "report", "verdict", "changes"}  # changes = 第一轮的修改清单（#132）
ON_FAIL = {"warn", "swap", "block", "swap-if-ending-unfinished"}
CONSTRAINTS = {"max-change-pct", "keep-order", "original-words", "no-new-facts"}
# 和工作台读清单时的校验一致（content-studio extras/xline/write_module.py）：#132 起每步多了 round（第几轮调用）和 fix（直接改 / 只评论）
STEP_KEYS = {"title", "group", "round", "status", "prompt", "does", "output", "fix", "ask", "only", "may-move", "may-add", "may-delete", "on-fail"}
ROUNDS = {1, 2}
FIX = {"edit", "comment"}
FORMS = {"长文", "长帖", "短帖"}


def section(text: str, anchor: str) -> str | None:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("#") and line.lstrip("#").strip().startswith(anchor):
            level = len(line) - len(line.lstrip("#"))
            end = next((j for j in range(i + 1, len(lines)) if lines[j].startswith("#") and len(lines[j]) - len(lines[j].lstrip("#")) <= level), len(lines))
            return "\n".join(lines[i:end])
    return None


class ModuleManifest(unittest.TestCase):
    def setUp(self) -> None:
        self.m = yaml.safe_load((SKILL / "module.yaml").read_text(encoding="utf-8"))

    def test_flows_use_only_known_steps_without_repeats(self) -> None:
        self.assertTrue(self.m["flows"])
        for name, ids in self.m["flows"].items():
            self.assertEqual(len(ids), len(set(ids)), name)
            self.assertFalse(set(ids) - set(self.m["steps"]), name)

    def test_constraints_are_known_gates(self) -> None:
        self.assertFalse(set(self.m["constraints"]) - CONSTRAINTS)
        self.assertLessEqual(self.m["constraints"]["max-change-pct"], 50)
        self.assertIs(self.m["constraints"]["keep-order"], True)

    def test_every_step_is_well_formed_and_its_prompt_section_exists(self) -> None:
        for sid, step in self.m["steps"].items():
            self.assertFalse(set(step) - STEP_KEYS, sid)
            self.assertIn(step["group"], GROUPS, sid)
            self.assertIn(step["status"], STATUS, sid)
            self.assertIn(step["output"], OUTPUT, sid)
            self.assertIn(step["on-fail"], ON_FAIL, sid)
            self.assertIn(step.get("round"), ROUNDS, sid)
            self.assertIn(step.get("fix", "edit"), FIX, sid)
            self.assertTrue(step["title"] and step["does"], sid)
            self.assertFalse(set(step.get("only", [])) - FORMS, sid)
            if step["status"] == "planned":
                self.assertIsNone(step["prompt"], sid)
                continue
            path, _, anchor = step["prompt"].partition("#")
            file = SKILL / path
            self.assertTrue(file.is_file(), f"{sid}: 找不到 {path}")
            if anchor:
                self.assertIsNotNone(section(file.read_text(encoding="utf-8"), anchor), f"{sid}: {path} 里没有以「{anchor}」开头的标题")

    def test_only_style_may_delete_and_density_may_add(self) -> None:
        deleters = [sid for sid, s in self.m["steps"].items() if s.get("may-delete")]
        self.assertEqual(deleters, ["style"])
        self.assertEqual(self.m["steps"]["density"].get("may-add"), "bridge-sentence")
        self.assertNotIn("may-delete", self.m["steps"]["check-pain"])

    def test_only_the_opening_may_move_text(self) -> None:
        movers = [sid for sid, s in self.m["steps"].items() if s.get("may-move")]
        self.assertEqual(movers, ["opening"])

    def test_review_items_point_at_real_steps_and_every_step_is_reviewed_once(self) -> None:
        items = self.m["review"]
        self.assertEqual([i["id"] for i in items], ["retain", "pain", "density", "benefit", "scarcity", "egg", "tone", "complete", "typo"])
        self.assertEqual(len({i["title"] for i in items}), len(items))
        used = [sid for i in items for sid in i["from"]]
        self.assertEqual(len(used), len(set(used)))  # 一步只算进一项
        self.assertFalse(set(used) - set(self.m["steps"]))
        self.assertEqual(set(used), set(self.m["steps"]))  # 每一步都在 9 项里有去处

    def test_post_shoot_reads_the_review_section_of_the_video_frame(self) -> None:
        shoot = self.m["post-shoot"]
        path, _, anchor = shoot["prompt"].partition("#")
        self.assertIsNotNone(section((SKILL / path).read_text(encoding="utf-8"), anchor))
        self.assertTrue(shoot["title"] and shoot["does"])

    def test_groups_run_in_order_write_style_check(self) -> None:
        for name, ids in self.m["flows"].items():
            order = [["写", "风格", "查"].index(self.m["steps"][i]["group"]) for i in ids]
            self.assertEqual(order, sorted(order), name)


if __name__ == "__main__":
    unittest.main()
