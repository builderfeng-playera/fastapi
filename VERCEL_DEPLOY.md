# 部署到 Vercel 指南

## 前置要求

1. **Vercel 账号**：如果没有，在 [vercel.com](https://vercel.com) 注册
2. **Vercel CLI**：安装 Vercel 命令行工具
   ```bash
   npm i -g vercel
   ```

## 部署步骤

### 方法 1：使用 Vercel CLI（推荐）

1. **登录 Vercel**
   ```bash
   vercel login
   ```

2. **在项目目录中部署**
   ```bash
   cd "/Users/shipeifeng/AI Architect"
   vercel
   ```

3. **按照提示操作**
   - 选择项目设置
   - 确认部署配置
   - 等待部署完成

4. **设置环境变量**
   ```bash
   vercel env add AI_BUILDER_TOKEN
   # 输入你的 API token: sk_e5ec71d9_a491add896e4e94da35be769927505a579f8
   ```

5. **重新部署以应用环境变量**
   ```bash
   vercel --prod
   ```

### 方法 2：通过 GitHub 部署（推荐用于持续部署）

1. **将代码推送到 GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **在 Vercel 中导入项目**
   - 访问 [vercel.com/dashboard](https://vercel.com/dashboard)
   - 点击 "Add New Project"
   - 选择你的 GitHub 仓库
   - 配置项目设置

3. **设置环境变量**
   - 在项目设置中添加环境变量：
     - `AI_BUILDER_TOKEN`: `sk_e5ec71d9_a491add896e4e94da35be769927505a579f8`

4. **部署**
   - Vercel 会自动检测到推送并部署

## 配置文件说明

### vercel.json
- 配置 Python runtime
- 设置路由规则
- 配置函数超时时间（60秒）

### .vercelignore
- 排除不需要部署的文件（测试文件、文档等）

## 重要注意事项

### 1. 环境变量
⚠️ **重要**：不要在代码中硬编码 API token！

在 Vercel 中设置环境变量：
- 项目设置 → Environment Variables
- 添加 `AI_BUILDER_TOKEN`

### 2. 静态文件
静态文件（HTML/CSS/JS）通过 Vercel 的静态文件服务提供。

### 3. 函数超时
- 默认超时：10秒
- 已配置：60秒（适合你的 agentic loop）
- 如果需要更长，可以升级到 Pro 计划

### 4. 日志和监控
- 在 Vercel Dashboard 中查看日志
- 监控函数执行时间和错误

## 测试部署

部署完成后，访问你的 Vercel URL：
```
https://your-project-name.vercel.app
```

测试端点：
- `GET /` - 主页（聊天界面）
- `POST /chat` - Chat API
- `POST /search` - Search API
- `GET /docs` - API 文档

## 常见问题

### 问题 1：静态文件 404
**解决方案**：确保 `static/` 目录在项目根目录，并且 `vercel.json` 配置正确。

### 问题 2：环境变量未生效
**解决方案**：
1. 检查环境变量名称是否正确（`AI_BUILDER_TOKEN`）
2. 重新部署：`vercel --prod`
3. 检查代码中是否正确读取环境变量

### 问题 3：函数超时
**解决方案**：
1. 检查 `vercel.json` 中的 `maxDuration` 设置
2. 优化代码，减少执行时间
3. 考虑升级到 Pro 计划（支持更长的超时）

### 问题 4：导入错误
**解决方案**：确保 `requirements.txt` 包含所有依赖。

## 持续部署

如果通过 GitHub 部署，每次推送到 main 分支都会自动触发部署。

## 本地测试 Vercel 环境

```bash
# 安装 Vercel CLI
npm i -g vercel

# 在项目目录运行
vercel dev
```

这会启动一个本地服务器，模拟 Vercel 环境。

## 生产环境检查清单

- [ ] 环境变量已设置
- [ ] API token 已配置
- [ ] 静态文件可以访问
- [ ] API 端点正常工作
- [ ] 日志可以查看
- [ ] 错误处理正常

## 性能优化建议

1. **缓存静态文件**：Vercel 自动缓存静态文件
2. **优化 API 响应**：减少不必要的计算
3. **监控使用量**：关注 Vercel 的使用限制

## 支持

如果遇到问题：
1. 查看 Vercel Dashboard 的日志
2. 检查 [Vercel 文档](https://vercel.com/docs)
3. 查看项目的 GitHub Issues
