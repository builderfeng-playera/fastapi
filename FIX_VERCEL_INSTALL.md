# 解决 Vercel CLI 安装权限问题

## 问题
```
npm error code EACCES
npm error Error: EACCES: permission denied
```

## 解决方案（按推荐顺序）

### 方案 1：使用 npx（推荐，无需安装）⭐⭐⭐⭐⭐

**最简单的方法**，不需要全局安装：

```bash
# 直接使用 npx 运行 vercel
npx vercel login
npx vercel
```

每次使用 `npx vercel` 即可，不需要安装。

---

### 方案 2：使用本地安装 ⭐⭐⭐⭐

在项目目录中本地安装：

```bash
cd "/Users/shipeifeng/AI Architect"

# 初始化 package.json（如果还没有）
npm init -y

# 本地安装 vercel
npm install vercel --save-dev

# 使用本地安装的 vercel
npx vercel login
npx vercel
```

或者添加到 package.json 的 scripts：
```json
{
  "scripts": {
    "deploy": "vercel",
    "deploy:prod": "vercel --prod"
  }
}
```

然后运行：
```bash
npm run deploy
```

---

### 方案 3：修复 npm 权限（最佳实践）⭐⭐⭐⭐

**一次性设置，以后都可以全局安装**：

```bash
# 创建 npm 全局目录
mkdir ~/.npm-global

# 配置 npm 使用新目录
npm config set prefix '~/.npm-global'

# 添加到 PATH（添加到 ~/.zshrc）
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc

# 现在可以全局安装了
npm install -g vercel
```

---

### 方案 4：使用 sudo（不推荐）⭐⭐

**快速但不安全**：

```bash
sudo npm install -g vercel
```

⚠️ **注意**：使用 sudo 安装 npm 包可能导致安全问题。

---

## 推荐流程

### 使用 npx（最简单）

```bash
# 1. 登录（首次使用）
npx vercel login

# 2. 部署
cd "/Users/shipeifeng/AI Architect"
npx vercel

# 3. 设置环境变量
npx vercel env add AI_BUILDER_TOKEN
# 输入: sk_e5ec71d9_a491add896e4e94da35be769927505a579f8

# 4. 生产环境部署
npx vercel --prod
```

---

## 或者通过 GitHub 部署（无需 CLI）

如果不想使用 CLI，可以直接通过 GitHub：

1. **创建 GitHub 仓库**
   ```bash
   git init
   git add .
   git commit -m "Ready for deployment"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **在 Vercel Dashboard 部署**
   - 访问 https://vercel.com/dashboard
   - 点击 "Add New Project"
   - 选择你的 GitHub 仓库
   - 添加环境变量 `AI_BUILDER_TOKEN`
   - 点击 Deploy

---

## 验证安装

```bash
# 检查 vercel 是否可用
npx vercel --version
```

应该显示版本号，如：`vercel@32.x.x`
