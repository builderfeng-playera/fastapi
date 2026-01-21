# 🚀 快速部署指南

## 一键设置 Git（在终端运行）

```bash
cd "/Users/shipeifeng/AI Architect"
./setup_git.sh
```

或者手动运行：

```bash
cd "/Users/shipeifeng/AI Architect"
git init
git add .
git commit -m "Initial commit: FastAPI with Agentic Loop"
```

---

## 然后推送到 GitHub

### 1. 在 GitHub 创建仓库

访问：https://github.com/new

- Repository name: `ai-architect`（或你喜欢的名字）
- 选择 Public 或 Private
- **不要**勾选 "Initialize with README"
- 点击 "Create repository"

### 2. 连接并推送

```bash
# 替换 YOUR_USERNAME 和 YOUR_REPO
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

**如果遇到认证问题**：
- 使用 Personal Access Token（推荐）
- 或者配置 SSH key

---

## 在 Vercel 部署

### 1. 登录 Vercel
- 访问 https://vercel.com
- 用 GitHub 账号登录

### 2. 导入项目
- 点击 "Add New Project"
- 选择你的 GitHub 仓库
- 点击 "Import"

### 3. 配置
- Framework: "Other"（或自动检测）
- Build/Install/Output: 全部留空

### 4. 环境变量 ⚠️ 重要！
添加环境变量：
- **Name**: `AI_BUILDER_TOKEN`
- **Value**: `sk_e5ec71d9_a491add896e4e94da35be769927505a579f8`
- 选择所有环境（Production, Preview, Development）

### 5. 部署
- 点击 "Deploy"
- 等待 1-2 分钟
- 完成！

---

## 验证

部署完成后访问：
- 主页：`https://your-project.vercel.app/`
- API 文档：`https://your-project.vercel.app/docs`

---

## 需要帮助？

查看详细文档：
- `DEPLOY_STEP_BY_STEP.md` - 完整步骤
- `DEPLOY_SOLUTIONS.md` - 其他方案
