# 快速部署到 Vercel

## 一键部署

### 步骤 1：安装 Vercel CLI
```bash
npm i -g vercel
```

### 步骤 2：登录 Vercel
```bash
vercel login
```

### 步骤 3：部署
```bash
cd "/Users/shipeifeng/AI Architect"
vercel
```

### 步骤 4：设置环境变量
```bash
vercel env add AI_BUILDER_TOKEN
# 输入: sk_e5ec71d9_a491add896e4e94da35be769927505a579f8
# 选择: Production, Preview, Development (全部)
```

### 步骤 5：生产环境部署
```bash
vercel --prod
```

## 或者通过 GitHub

1. **创建 GitHub 仓库并推送代码**
   ```bash
   git init
   git add .
   git commit -m "Ready for Vercel deployment"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **在 Vercel Dashboard 导入项目**
   - 访问 https://vercel.com/dashboard
   - 点击 "Add New Project"
   - 选择你的 GitHub 仓库
   - 添加环境变量 `AI_BUILDER_TOKEN`
   - 点击 Deploy

## 验证部署

部署完成后，访问你的 Vercel URL：
- 主页：`https://your-project.vercel.app/`
- API 文档：`https://your-project.vercel.app/docs`
- Chat API：`https://your-project.vercel.app/chat`

## 文件说明

- `vercel.json` - Vercel 配置文件
- `api/index.py` - Vercel serverless function 入口
- `.vercelignore` - 排除不需要部署的文件
- `.gitignore` - Git 忽略文件

## 注意事项

⚠️ **重要**：
1. 确保环境变量 `AI_BUILDER_TOKEN` 已设置
2. 不要在代码中硬编码 API token
3. 静态文件会自动通过 Vercel 的 CDN 提供

## 故障排除

如果遇到问题，查看：
- Vercel Dashboard → 项目 → Functions → 查看日志
- 检查环境变量是否正确设置
- 确认 `requirements.txt` 包含所有依赖
