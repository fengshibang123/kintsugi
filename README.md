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

## 新仓库安装与使用方式（⚠️ 私有仓库鉴权提示）

> **🔐 权限说明**：`fengshibang123/war3game-skills` 为**私有仓库（Private Repository）**。请确保您的 GitHub 账号已被添加为协作者或拥有访问权限，并在本地配置好认证凭据。

### 1. SSH 克隆方式（推荐）
配置好 GitHub SSH Key 后直接克隆：
```bash
git clone git@github.com:fengshibang123/war3game-skills.git
```

### 2. GitHub CLI 克隆方式
已登录 `gh`（执行过 `gh auth login`）环境下：
```bash
gh repo clone fengshibang123/war3game-skills
```

### 3. HTTPS + Personal Access Token (PAT)
```bash
git clone https://<YOUR_GITHUB_PAT>@github.com/fengshibang123/war3game-skills.git
```

克隆后进入仓库执行：
```bash
cd war3game-skills
pnpm install
pnpm run sync    # 一键体检并同步至本地多智能体环境
```

## License

见 [LICENSE](LICENSE)。
