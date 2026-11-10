# ⚠️ [DEPRECATED / 已废弃] 仓库已全面迁移至 war3game-skills

> **重要公告**：本项目（`fengshibang/kintsugi`）中的 **`war3-tester`** 与 War3 自动化测试及开发套件已全面并入新中枢仓库：
> 👉 **[fengshibang123/war3game-skills](https://github.com/fengshibang123/war3game-skills)**
>
> 核心测试能力已统一在 `war3game-skills` 的 `skills/war3-auto-test` 中持续维护与演进（四层测试体系、Named Pipe 管道桥接、34 项 MCP 工具、六大看门狗 Oracle、防作弊三盒纯度审计）。
> 本仓库已停止维护，后续请统一迁移至 **[fengshibang123/war3game-skills](https://github.com/fengshibang123/war3game-skills)** 使用。

---

# kintsugi — Claude Code 插件集合（旧版归档）

> 金缮（kintsugi）：用金漆修补破碎之处，让裂痕成为美的一部分。
>
> 本仓库已废弃归档。

## 迁移指引

| 原插件 | 现维护仓库与路径 | 状态 |
|------|------|------|
| **war3-tester** | 👉 **[fengshibang123/war3game-skills](https://github.com/fengshibang123/war3game-skills)** (`skills/war3-auto-test`) | **已迁移至新仓库持续维护** |
| **mentor-kit** | [plugins/mentor-kit/](plugins/mentor-kit/) | 归档 |

## 新仓库安装与使用方式

请直接使用新的通用技能中枢：

```bash
# 克隆新仓库
git clone https://github.com/fengshibang123/war3game-skills.git
```

在 Claude Code / Antigravity / Codex / DSH 中直接挂载使用 `war3game-skills`。

## License

见 [LICENSE](LICENSE)。
