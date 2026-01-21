#!/bin/bash

# Git 仓库初始化脚本
# 用于准备推送到 GitHub 并部署到 Vercel

echo "🚀 初始化 Git 仓库..."

# 初始化 Git
git init

# 添加所有文件
echo "📦 添加文件..."
git add .

# 创建初始提交
echo "💾 创建提交..."
git commit -m "Initial commit: FastAPI with Agentic Loop and Web UI

- FastAPI application with Chat API supporting agentic loop (up to 4 rounds)
- Web UI with ChatGPT-like interface  
- Search API integration with AI Builder
- Parallel tool execution
- Markdown rendering support
- Ready for Vercel deployment"

echo ""
echo "✅ Git 仓库初始化完成！"
echo ""
echo "📝 下一步："
echo "1. 在 GitHub 创建新仓库：https://github.com/new"
echo "2. 然后运行以下命令："
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. 在 Vercel Dashboard 导入项目并部署"
echo ""
