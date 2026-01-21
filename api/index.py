"""
Vercel serverless function entry point for FastAPI
"""
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 确保可以导入 main
try:
    from main import app
except ImportError as e:
    # 如果导入失败，尝试直接添加路径
    import importlib.util
    main_path = os.path.join(project_root, "main.py")
    spec = importlib.util.spec_from_file_location("main", main_path)
    main_module = importlib.util.module_from_spec(spec)
    sys.modules["main"] = main_module
    spec.loader.exec_module(main_module)
    app = main_module.app

# Vercel Python runtime 需要这个导出
# FastAPI 应用本身就是 ASGI 应用，可以直接使用
handler = app
