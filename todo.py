#!/usr/bin/env python3
"""
vibe-coding todolist — 简单易用的命令行待办事项管理工具
数据存储在本地 JSON 文件中（默认 ~/.vibe-todo.json）
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
DATA_FILE = Path.home() / ".vibe-todo.json"

# ── 优先级常量 ────────────────────────────────────────
PRIORITY_HIGH = "high"
PRIORITY_MEDIUM = "medium"
PRIORITY_LOW = "low"
PRIORITIES = {PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW}
PRIORITY_LABELS = {PRIORITY_HIGH: "🔴 高", PRIORITY_MEDIUM: "🟡 中", PRIORITY_LOW: "🟢 低"}

# ════════════════════════════════════════════════════════
#  步骤 1: 数据模型
# ════════════════════════════════════════════════════════
#
#  每一条任务是一个 dict，字段如下：
#    id         int       自增主键，唯一标识一条任务
#    title      str       待办事项内容
#    priority   str       优先级，取值为 "high" / "medium" / "low"
#    done       bool      是否已完成，默认 False
#    created_at str       创建时间（ISO 格式字符串）
#    updated_at str       最后修改时间（ISO 格式字符串）
#
#  整个 JSON 文件的结构:
#    { "tasks": [ ... ] }

# ════════════════════════════════════════════════════════
#  步骤 2: 数据持久化层
# ════════════════════════════════════════════════════════

def load_tasks() -> list[dict]:
    """从 JSON 文件加载所有任务。文件不存在或损坏时返回空列表。"""
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("tasks", [])
    except (json.JSONDecodeError, KeyError):
        return []


def save_tasks(tasks: list[dict]) -> None:
    """将任务列表写入 JSON 文件（自动创建父目录）。"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"tasks": tasks}, f, ensure_ascii=False, indent=2)


def next_id(tasks: list[dict]) -> int:
    """返回下一个可用的任务 ID（当前最大 ID + 1，空列表返回 1）。"""
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


def now_iso() -> str:
    """返回当前时间的 ISO 格式字符串，精确到秒。"""
    return datetime.now().isoformat(timespec="seconds")


# ════════════════════════════════════════════════════════
#  步骤 3-6: 业务逻辑（增删改查 + 完成标记）
# ════════════════════════════════════════════════════════

def add_task(title: str, priority: str = PRIORITY_MEDIUM) -> dict:
    """步骤 3 — 添加新任务，返回创建的任务。"""
    tasks = load_tasks()
    now = now_iso()
    task = {
        "id": next_id(tasks),
        "title": title,
        "priority": priority,
        "done": False,
        "created_at": now,
        "updated_at": now,
    }
    tasks.append(task)
    save_tasks(tasks)
    return task


def delete_task(task_id: int) -> dict | None:
    """步骤 4 — 按 ID 删除任务。返回被删除的任务，不存在则返回 None。"""
    tasks = load_tasks()
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            deleted = tasks.pop(i)
            save_tasks(tasks)
            return deleted
    return None


def update_task(
    task_id: int,
    title: str | None = None,
    priority: str | None = None,
) -> dict | None:
    """步骤 5 — 修改标题或优先级。返回更新后的任务，不存在则返回 None。"""
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            if title is not None:
                t["title"] = title
            if priority is not None:
                t["priority"] = priority
            t["updated_at"] = now_iso()
            save_tasks(tasks)
            return t
    return None


def mark_done(task_id: int) -> dict | None:
    """步骤 6 — 标记任务为已完成。"""
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            t["updated_at"] = now_iso()
            save_tasks(tasks)
            return t
    return None


def mark_undone(task_id: int) -> dict | None:
    """步骤 6 — 标记任务为未完成。"""
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = False
            t["updated_at"] = now_iso()
            save_tasks(tasks)
            return t
    return None


def list_tasks(
    priority: str | None = None,
    status: str | None = None,
) -> list[dict]:
    """步骤 7 — 列出任务，支持按优先级和状态筛选。"""
    tasks = load_tasks()

    if priority:
        tasks = [t for t in tasks if t["priority"] == priority]
    if status == "done":
        tasks = [t for t in tasks if t["done"]]
    elif status == "undone":
        tasks = [t for t in tasks if not t["done"]]

    # 排序：未完成优先 → 高优先级优先 → 旧的在前
    pri_order = {PRIORITY_HIGH: 0, PRIORITY_MEDIUM: 1, PRIORITY_LOW: 2}
    tasks.sort(key=lambda t: (t["done"], pri_order.get(t["priority"], 1), t["created_at"]))
    return tasks


# ════════════════════════════════════════════════════════
#  步骤 8: 格式化输出
# ════════════════════════════════════════════════════════

def fmt_task(task: dict) -> str:
    """格式化单个任务为一行可读字符串。"""
    status = "✅" if task["done"] else "⬜"
    label = PRIORITY_LABELS.get(task["priority"], task["priority"])
    title = task["title"]
    if task["done"]:
        title = f"\033[2m\033[3m{title}\033[0m"  # 灰色斜体
    return f"  {status}  [{task['id']:>3d}]  {label}  {title}"


def print_task_list(tasks: list[dict]) -> None:
    """打印任务列表，含统计信息。"""
    if not tasks:
        print("  📭 暂无待办事项\n")
        return
    total = len(tasks)
    done_count = sum(1 for t in tasks if t["done"])
    print(f"  📋 共 {total} 项，已完成 {done_count} 项，待办 {total - done_count} 项\n")
    for t in tasks:
        print(fmt_task(t))
    print()


# ════════════════════════════════════════════════════════
#  步骤 9: CLI 入口
# ════════════════════════════════════════════════════════

def die(msg: str) -> None:
    """打印错误并退出。"""
    print(f"  ❌ {msg}", file=sys.stderr)
    sys.exit(1)


def cmd_add(args):
    task = add_task(args.title, priority=args.priority)
    print(f"\n  ✨ 已添加任务 #{task['id']}:")
    print(fmt_task(task))


def cmd_delete(args):
    task = delete_task(args.id)
    if task is None:
        die(f"任务 #{args.id} 不存在")
    print(f"\n  🗑️  已删除任务 #{args.id}:")
    print(fmt_task(task))


def cmd_update(args):
    if args.title is None and args.priority is None:
        die("请至少指定一项修改：--title 或 --priority")
    task = update_task(args.id, title=args.title, priority=args.priority)
    if task is None:
        die(f"任务 #{args.id} 不存在")
    print(f"\n  ✏️  已更新任务 #{args.id}:")
    print(fmt_task(task))


def cmd_done(args):
    task = mark_done(args.id)
    if task is None:
        die(f"任务 #{args.id} 不存在")
    print(f"\n  🎉 任务 #{args.id} 已完成:")
    print(fmt_task(task))


def cmd_undone(args):
    task = mark_undone(args.id)
    if task is None:
        die(f"任务 #{args.id} 不存在")
    print(f"\n  🔄 任务 #{args.id} 已恢复为未完成:")
    print(fmt_task(task))


def cmd_list(args):
    status = "done" if args.done else ("undone" if args.undone else None)
    tasks = list_tasks(priority=args.priority, status=status)

    # 拼标题
    parts = []
    if args.priority:
        parts.append(PRIORITY_LABELS.get(args.priority, args.priority))
    if status == "done":
        parts.append("已完成")
    elif status == "undone":
        parts.append("未完成")
    label = " · ".join(parts) if parts else "全部"

    print(f"\n  📌 {label}任务:\n")
    print_task_list(tasks)


def main():
    parser = argparse.ArgumentParser(
        prog="todo",
        description="vibe-coding todolist — 简单易用的待办事项管理",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # add
    p = sub.add_parser("add", aliases=["a"], help="添加新待办事项")
    p.add_argument("title", help="待办事项内容")
    p.add_argument("-p", "--priority", choices=list(PRIORITIES), default=PRIORITY_MEDIUM,
                   help="优先级（默认 medium）")
    p.set_defaults(func=cmd_add)

    # delete
    p = sub.add_parser("delete", aliases=["d", "rm"], help="删除待办事项")
    p.add_argument("id", type=int, help="要删除的任务 ID")
    p.set_defaults(func=cmd_delete)

    # update
    p = sub.add_parser("update", aliases=["u"], help="修改待办事项的标题或优先级")
    p.add_argument("id", type=int, help="要修改的任务 ID")
    p.add_argument("-t", "--title", help="新的标题内容")
    p.add_argument("-p", "--priority", choices=list(PRIORITIES), help="新的优先级")
    p.set_defaults(func=cmd_update)

    # done
    p = sub.add_parser("done", aliases=["do"], help="标记任务为已完成")
    p.add_argument("id", type=int, help="要完成的任务 ID")
    p.set_defaults(func=cmd_done)

    # undone
    p = sub.add_parser("undone", aliases=["undo"], help="标记任务为未完成")
    p.add_argument("id", type=int, help="要恢复的任务 ID")
    p.set_defaults(func=cmd_undone)

    # list
    p = sub.add_parser("list", aliases=["ls", "l"], help="列出待办事项")
    p.add_argument("-p", "--priority", choices=list(PRIORITIES), help="按优先级筛选")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--done", action="store_true", help="只显示已完成的")
    g.add_argument("--undone", action="store_true", help="只显示未完成的")
    p.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
