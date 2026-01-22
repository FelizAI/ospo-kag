# Contributing to OSPO-KAG

首先，感谢你对 OSPO-KAG 项目的关注！🎉

我们非常欢迎任何形式的贡献，无论是修复 Bug、添加新功能，还是完善文档。为了确保协作的顺畅和代码的高质量（以及符合开源的最佳实践），请在提交代码前仔细阅读以下指南。

## 🤝 协作流程 (Workflow)

我们遵循标准的 GitHub 开源协作流程：

1. **提 Issue**：任何代码变动前，请先[创建一个 Issue](https://github.com/FelizAI/ospo-kag/issues)。
* 如果是 Bug，请使用 `Bug Report` 模板。
* 如果是新功能，请使用 `Feature Request` 模板。
* 如果是团队任务，请使用 `Project Task` 模板。


2. **分配 (Assign)**：在 Issue 中认领任务，避免重复劳动。
3. **开发 (Coding)**：从 `main` 分支切出一个新分支进行开发。
4. **提交 (PR)**：开发完成后，提交 Pull Request，并关联对应的 Issue。

---

## 🌳 Git 分支规范 (Branching Strategy)

为了保持提交历史的清晰，请严格遵守以下分支命名规则：

* **主分支**：`main` (时刻保持可部署状态)
* **开发分支命名格式**：`type/short-description`

| 类型 | 示例 | 说明 |
| --- | --- | --- |
| **feat** | `feat/data-pipeline` | 新功能开发 |
| **fix** | `fix/login-error` | Bug 修复 |
| **docs** | `docs/update-readme` | 文档修改 |
| **refactor** | `refactor/api-structure` | 代码重构（无功能变动） |

---

## 📝 Commit 信息规范 (Commit Convention)

我们采用 [Conventional Commits](https://www.conventionalcommits.org/) 规范。这是**必须遵守**的规则，因为清晰的日志能帮助我们快速生成 Changelog。

**格式**：`<type>(<scope>): <subject>`

### 常用 Type：

* `feat`: ✨ 新增功能 (Feature)
* `fix`: 🐛 修复 Bug
* `docs`: 📚 文档变更
* `style`: 💎 代码格式调整 (空格, 格式化, 不影响代码运行)
* `refactor`: ♻️ 代码重构 (即不是新增功能，也不是修改bug的代码变动)
* `perf`: 🚀 性能优化
* `test`: ✅ 增加或修改测试用例
* `chore`: 🔧 构建过程或辅助工具的变动

### 示例：

> ✅ `feat(parser): add support for csv file export`
> ✅ `fix(auth): resolve token expiration issue`
> ❌ `update code` (描述不清，禁止使用)

---

## 🚀 提交 Pull Request (PR)

提交 PR 时，请遵循以下清单：

1. **标题**：使用与 Commit 相同的规范（例如 `feat: add search module`）。
2. **描述**：
* 简要描述修改内容。
* **关键步骤**：在描述中使用 `Closes #IssueID` (例如 `Closes #12`)。这样当 PR 合并时，Issue 会自动关闭，这是开源协作的重要记录！


3. **检查**：
* 确保本地代码能正常运行。
* 如果你添加了新功能，请确保添加了对应的注释或文档。


---

## 🛠 开发环境设置 (Development Setup)

关于详细的项目安装、依赖配置及本地启动指南，请查阅我们独立的开发手册：

👉 **[DEV_MANUAL.md](DEV_MANUAL.md)**

在该手册中，你可以找到：

* 环境依赖说明 (Prerequisites)
* 项目安装步骤 (Installation)

---

感谢你的贡献！让我们一起构建更好的开源项目！ ❤️

