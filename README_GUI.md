# AI Chat with Agentic Loop - Web GUI

这是一个带有 Web 界面的 AI 聊天应用，支持多轮工具调用的 Agentic Loop。

## 功能特点

- 🎨 **现代化 UI**：类似 ChatGPT 的聊天界面
- 💬 **实时对话**：支持与 AI 进行实时对话
- 🔍 **智能搜索**：AI 可以自主决定使用搜索工具获取最新信息
- 🔄 **多轮工具调用**：最多支持四轮工具调用
- 📝 **Markdown 渲染**：AI 回复支持 Markdown 格式，自动渲染为 HTML
- ⚡ **加载动画**：显示"正在思考"的动画效果
- 📱 **响应式设计**：支持桌面和移动设备

## 使用方法

### 1. 启动服务器

```bash
uvicorn main:app --reload
```

### 2. 访问网页

在浏览器中打开：
```
http://localhost:8000
```

### 3. 开始聊天

- 在输入框中输入你的问题
- 按 `Enter` 发送消息（`Shift+Enter` 换行）
- 或点击发送按钮
- AI 会自动处理你的请求，如果需要会调用搜索工具

## 界面说明

### 输入框
- **Enter**：发送消息
- **Shift+Enter**：换行
- 支持多行输入（最多 120px 高度）

### 消息显示
- **用户消息**：显示在右侧，紫色背景
- **AI 消息**：显示在左侧，白色背景
- **Markdown 支持**：代码块、列表、链接等会自动渲染

### 加载状态
- 发送消息后会显示"正在思考..."动画
- 等待 AI 响应时按钮会禁用

## API 端点

- `GET /` - 主页（聊天界面）
- `POST /chat` - Chat API（支持 Agentic Loop）
- `POST /search` - 搜索 API
- `GET /hello` - Hello API
- `GET /docs` - API 文档（Swagger UI）

## 技术栈

- **后端**：FastAPI
- **前端**：原生 HTML/CSS/JavaScript
- **Markdown 渲染**：Marked.js
- **样式**：自定义 CSS，渐变背景

## 文件结构

```
.
├── main.py              # FastAPI 应用
├── static/
│   ├── index.html       # 主页 HTML
│   ├── style.css        # 样式文件
│   └── script.js        # JavaScript 逻辑
└── README_GUI.md        # 本文件
```

## 注意事项

- 确保 FastAPI 服务器正在运行
- 需要配置 AI Builder API token
- 网络请求可能需要一些时间，请耐心等待

