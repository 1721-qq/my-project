# Todo CLI —— Vibe-Coding 实战项目

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

一个基于 Python 标准库的命令行待办事项管理工具，支持增删改查、优先级和完成标记。  
本项目是 **Vibe-Coding（氛围编程）** 的实战产物——通过与 AI Agent 协作完成代码开发，我在理解代码的基础上进行了多轮审查、调试与优化。

🔗 **项目地址**：[GitHub - 你的用户名/仓库名](https://github.com/你的用户名/仓库名)

---

## ✨ 功能特性

- ✅ **添加 (add)** – 添加新事项，支持高/中/低三级优先级（默认中）
- ✅ **删除 (delete)** – 根据 ID 删除事项
- ✅ **修改 (update)** – 修改事项内容、优先级或状态
- ✅ **查看 (list)** – 列出所有事项，支持按 `--done` / `--pending` / `--priority` 筛选
- ✅ **完成标记 (done / undone)** – 快速切换完成状态
- ✅ **数据持久化** – 自动存储在本地 `todos.json` 文件中

---

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/你的用户名/仓库名.git
cd 仓库名
