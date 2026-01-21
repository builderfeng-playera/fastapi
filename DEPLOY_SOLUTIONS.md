# Vercel 部署解决方案

## 当前问题
- npm 全局安装权限错误
- npx 也可能有权限问题

## 最佳解决方案

### 方案 A：通过 GitHub + Vercel Dashboard（推荐）⭐⭐⭐⭐⭐

**无需安装任何 CLI 工具，最简单！**

#### 步骤 1：准备 Git 仓库

```bash
cd "/Users/shipeifeng/AI Architect"

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Ready for Vercel deployment"

# 创建 GitHub 仓库（在 GitHub 网站上创建），然后：
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

#### 步骤 2：在 Vercel Dashboard 部署

1. **访问 Vercel**
   - 打开 https://vercel.com
   - 如果没有账号，先注册（可以用 GitHub 账号登录）

2. **导入项目**
   - 点击 "Add New Project"
   - 选择 "Import Git Repository"
   - 选择你的 GitHub 仓库
   - 点击 "Import"

3. **配置项目**
   - Framework Preset: 选择 "Other" 或自动检测
   - Root Directory: `./`（默认）
   - Build Command: 留空（Python 不需要构建）
   - Output Directory: 留空
   - Install Command: 留空

4. **设置环境变量**
   - 在 "Environment Variables" 部分
   - 添加变量：
     - Name: `AI_BUILDER_TOKEN`
     - Value: `sk_e5ec71d9_a491add896e4e94da35be769927505a579f8`
   - 选择所有环境（Production, Preview, Development）

5. **部署**
   - 点击 "Deploy"
   - 等待部署完成（通常 1-2 分钟）

6. **访问**
   - 部署完成后会显示 URL
   - 例如：`https://your-project.vercel.app`

---

### 方案 B：修复 npm 权限后使用 CLI ⭐⭐⭐⭐

#### 修复 npm 权限

```bash
# 1. 创建 npm 全局目录
mkdir -p ~/.npm-global

# 2. 配置 npm
npm config set prefix '~/.npm-global'

# 3. 添加到 PATH
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc

# 4. 重新加载配置
source ~/.zshrc

# 5. 验证
npm config get prefix
# 应该显示: /Users/shipeifeng/.npm-global

# 6. 现在可以全局安装
npm install -g vercel

# 7. 验证安装
vercel --version
```

#### 然后部署

```bash
cd "/Users/shipeifeng/AI Architect"
vercel login
vercel
vercel env add AI_BUILDER_TOKEN
# 输入: sk_e5ec71d9_a491add896e4e94da35be769927505a579f8
vercel --prod
```

---

### 方案 C：使用本地安装 ⭐⭐⭐

在项目目录中安装：

```bash
cd "/Users/shipeifeng/AI Architect"

# 创建 package.json
cat > package.json << 'EOF'
{
  "name": "ai-architect",
  "version": "1.0.0",
  "scripts": {
    "deploy": "vercel",
    "deploy:prod": "vercel --prod"
  },
  "devDependencies": {
    "vercel": "^32.0.0"
  }
}
EOF

# 本地安装
npm install

# 使用
npm run deploy
```

---

## 推荐：使用 GitHub + Dashboard（最简单）

**优点**：
- ✅ 无需安装任何工具
- ✅ 无需修复权限
- ✅ 自动持续部署（每次 push 自动部署）
- ✅ 有图形界面，更容易管理

**步骤总结**：
1. 推送到 GitHub
2. 在 Vercel Dashboard 导入
3. 设置环境变量
4. 点击 Deploy

---

## 部署后检查清单

- [ ] 环境变量 `AI_BUILDER_TOKEN` 已设置
- [ ] 主页可以访问：`https://your-project.vercel.app/`
- [ ] API 文档可以访问：`https://your-project.vercel.app/docs`
- [ ] Chat API 可以调用：`https://your-project.vercel.app/chat`
- [ ] 静态文件（CSS/JS）可以加载

---

## 如果遇到问题

### 问题 1：环境变量未生效
- 检查环境变量名称是否正确（`AI_BUILDER_TOKEN`）
- 确保选择了所有环境（Production, Preview, Development）
- 重新部署

### 问题 2：静态文件 404
- 检查 `static/` 目录是否在项目中
- 检查 `vercel.json` 配置是否正确

### 问题 3：函数超时
- 检查 Vercel Dashboard 中的函数日志
- 可能需要优化代码或升级计划

---

## 快速命令参考

### GitHub 部署流程
```bash
# 1. 初始化 Git
git init
git add .
git commit -m "Initial commit"

# 2. 创建 GitHub 仓库（在网页上），然后：
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main

# 3. 在 Vercel Dashboard 导入并部署
```

### 本地测试 Vercel 配置
```bash
# 如果修复了 npm 权限，可以本地测试
npx vercel dev
```

---

## 需要帮助？

如果遇到其他问题：
1. 查看 Vercel Dashboard 的部署日志
2. 检查项目的 Functions 日志
3. 参考 Vercel 文档：https://vercel.com/docs
