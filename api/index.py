"""
Vercel serverless function entry point for FastAPI
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Vercel Python runtime 需要这个导出
# FastAPI 应用本身就是 ASGI 应用，可以直接使用
handler = app
