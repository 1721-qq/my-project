# vibe-coding todolist

一个简单易用的命令行待办事项管理工具，使用 Python 开发，数据存储在本地 JSON 文件中（默认 ~/.vibe-todo.json）。

## 功能特性

- ✨ 添加、删除、修改待办事项
- 🏷️ 支持高、中、低三种优先级设置
- ✅ 标记任务为完成/未完成状态
- 🔍 按优先级和状态筛选任务
- 💾 数据持久化存储

## 安装与使用

### 前提条件

- Python 3.7+

### 使用方法

将 `todo.py` 下载到本地，然后通过以下命令使用：

```bash
python todo.py [命令] [参数]
```

## 命令说明

### 添加任务

```bash
# 添加普通任务
python todo.py add "购买 groceries"

# 添加带优先级的任务
python todo.py add "完成报告" -p high
```

### 列出任务

```bash
# 列出所有任务
python todo.py list

# 列出未完成的任务
python todo.py list --undone

# 列出已完成的任务
python todo.py list --done

# 按优先级筛选
python todo.py list -p high
```

### 更新任务

```bash
# 更新任务标题
python todo.py update 1 -t "新标题"

# 更新任务优先级
python todo.py update 1 -p low

# 同时更新标题和优先级
python todo.py update 1 -t "新标题" -p low
```

### 标记任务状态

```bash
# 标记任务为完成
python todo.py done 1

# 标记任务为未完成
python todo.py undone 1
```

### 删除任务

```bash
# 删除任务
python todo.py delete 1
```

## 快捷命令

- `add` 可简写为 `a`
- `delete` 可简写为 `d` 或 `rm`
- `update` 可简写为 `u`
- `done` 可简写为 `do`
- `undone` 可简写为 `undo`
- `list` 可简写为 `ls` 或 `l`

## 任务状态与优先级

- 状态：未完成（⬜）/ 已完成（✅）
- 优先级：
  - 高（🔴 高）
  - 中（🟡 中）
  - 低（🟢 低）

## 数据存储

所有任务数据都保存在 `~/.vibe-todo.json` 文件中，格式如下：

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "任务标题",
      "priority": "high",
      "done": false,
      "created_at": "2023-01-01T12:00:00",
      "updated_at": "2023-01-01T12:00:00"
    }
  ]
}
```

## 贡献者

- github用户: 1721-qq

## 审查与修改记录

| 日期 | 版本 | 修改内容 | 修改人 | 备注 |
|------|------|----------|--------|------|
| 2026-06-30 | v1.0.0 | 初始化项目文档，添加基本功能说明 | 1721-qq | 创建README文档 |
| 2026-06-30 | v1.0.0 | 添加命令使用说明和示例 | 1721-qq | 补充使用文档 |
| 2026-06-30 | v1.0.0 | 添加数据存储格式说明 | 1721-qq | 完善技术细节 |

## 许可证

MIT License