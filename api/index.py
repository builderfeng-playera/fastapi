"""
Vercel serverless function entry point for FastAPI
"""
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 导入 FastAPI 应用
from main import app

# Vercel Python runtime 需要导出 app 变量（不是 handler）
# FastAPI 应用会自动被识别为 ASGI 应用
# 注意：直接导出 app，不要使用 handler
