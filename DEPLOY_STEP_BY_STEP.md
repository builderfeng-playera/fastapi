# Vercel 部署 - 完整步骤指南

## 🎯 推荐方法：GitHub + Vercel Dashboard（无需 CLI）

这是最简单的方法，不需要安装任何工具或修复权限问题。

---

## 步骤 1：初始化 Git 仓库

```bash
cd "/Users/shipeifeng/AI Architect"

# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: FastAPI with Agentic Loop"
```

---

## 步骤 2：创建 GitHub 仓库

### 方法 A：使用 GitHub 网页

1. 访问 https://github.com/new
2. 填写仓库信息：
   - Repository name: `ai-architect`（或你喜欢的名字）
   - Description: `AI Chat with Agentic Loop`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"
3. 点击 "Create repository"

### 方法 B：使用 GitHub CLI（如果已安装）

```bash
gh repo create ai-architect --public --source=. --remote=origin --push
```

---

## 步骤 3：推送到 GitHub

```bash
# 添加远程仓库（替换 YOUR_USERNAME 和 YOUR_REPO）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 或者使用 SSH（如果你配置了 SSH key）
# git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

**如果遇到认证问题**：
- 使用 Personal Access Token（推荐）
- 或者配置 SSH key

---

## 步骤 4：在 Vercel 部署

### 4.1 登录 Vercel

1. 访问 https://vercel.com
2. 点击 "Sign Up" 或 "Log In"
3. 选择 "Continue with GitHub"（推荐，自动连接 GitHub）

### 4.2 导入项目

1. 在 Dashboard 点击 **"Add New Project"**
2. 选择你的 GitHub 仓库（`ai-architect`）
3. 点击 **"Import"**

### 4.3 配置项目

**Framework Preset**: 
- 选择 **"Other"** 或让 Vercel 自动检测

**Root Directory**: 
- 留空（使用根目录）

**Build Command**: 
- 留空（Python 不需要构建）

**Output Directory**: 
- 留空

**Install Command**: 
- 留空

### 4.4 设置环境变量 ⚠️ 重要！

1. 在 **"Environment Variables"** 部分
2. 点击 **"Add"**
3. 添加变量：
   - **Name**: `AI_BUILDER_TOKEN`
   - **Value**: `sk_e5ec71d9_a491add896e4e94da35be769927505a579f8`
4. 选择所有环境：
   - ✅ Production
   - ✅ Preview  
   - ✅ Development
5. 点击 **"Add"**

### 4.5 部署

1. 点击 **"Deploy"** 按钮
2. 等待部署完成（通常 1-2 分钟）
3. 部署完成后会显示你的 URL：
   - 例如：`https://ai-architect.vercel.app`

---

## 步骤 5：验证部署

### 测试端点

1. **主页（聊天界面）**
   ```
   https://your-project.vercel.app/
   ```

2. **API 文档**
   ```
   https://your-project.vercel.app/docs
   ```

3. **Chat API**
   ```bash
   curl -X POST https://your-project.vercel.app/chat \
     -H "Content-Type: application/json" \
     -d '{"messages": [{"role": "user", "content": "你好"}]}'
   ```

---

## 持续部署

✅ **自动部署已启用！**

每次你推送到 GitHub 的 `main` 分支，Vercel 会自动：
1. 检测到新的推送
2. 重新部署项目
3. 更新生产环境

---

## 故障排除

### 问题 1：部署失败

**检查**：
- Vercel Dashboard → 项目 → Deployments → 查看日志
- 检查是否有错误信息

**常见原因**：
- 环境变量未设置
- `requirements.txt` 缺少依赖
- 代码语法错误

### 问题 2：环境变量未生效

**解决**：
1. 检查环境变量名称：`AI_BUILDER_TOKEN`（必须完全匹配）
2. 确保选择了所有环境（Production, Preview, Development）
3. 重新部署：在 Vercel Dashboard 点击 "Redeploy"

### 问题 3：静态文件 404

**检查**：
- `static/` 目录是否在项目中
- `vercel.json` 配置是否正确
- 文件路径是否正确

### 问题 4：函数超时

**解决**：
- 检查 Vercel Dashboard → Functions → 查看执行时间
- 如果超过 10 秒，可能需要升级到 Pro 计划
- 或者优化代码，减少执行时间

---

## 管理环境变量

### 在 Vercel Dashboard 中

1. 项目 → Settings → Environment Variables
2. 可以添加、编辑、删除环境变量
3. 可以为不同环境设置不同的值

### 更新环境变量后

需要重新部署才能生效：
- 在 Deployments 页面点击 "Redeploy"
- 或者推送新的代码

---

## 查看日志

### 在 Vercel Dashboard

1. 项目 → Deployments
2. 点击某个部署
3. 查看 "Function Logs" 或 "Build Logs"

### 实时日志

```bash
# 如果修复了 npm 权限，可以使用：
vercel logs
```

---

## 自定义域名（可选）

1. 项目 → Settings → Domains
2. 添加你的域名
3. 按照提示配置 DNS

---

## 回滚部署

如果新部署有问题：

1. 项目 → Deployments
2. 找到之前的成功部署
3. 点击 "..." → "Promote to Production"

---

## 总结

✅ **最简单的部署流程**：
1. 推送到 GitHub
2. 在 Vercel Dashboard 导入
3. 设置环境变量
4. 点击 Deploy

✅ **优势**：
- 无需安装 CLI
- 无需修复权限
- 自动持续部署
- 图形界面管理

---

## 需要帮助？

- Vercel 文档：https://vercel.com/docs
- Vercel 支持：https://vercel.com/support
- 查看部署日志：Vercel Dashboard → 项目 → Deployments
