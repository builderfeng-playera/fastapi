from fastapi import FastAPI, Query, Body, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import requests
import os
import logging
import json as json_lib
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# AI Builder API 配置
AI_BUILDER_BASE_URL = "https://space.ai-builders.com/backend"
AI_BUILDER_API_KEY = os.getenv("AI_BUILDER_TOKEN")

# 如果环境变量中没有，尝试从文件读取
if not AI_BUILDER_API_KEY:
    try:
        with open("AI builder API key:", "r") as f:
            lines = f.readlines()
            if len(lines) >= 2:
                AI_BUILDER_API_KEY = lines[1].strip()
    except FileNotFoundError:
        pass

app = FastAPI(
    title="AI Chat with Agentic Loop",
    description="""
    ## 一个简单的 FastAPI Hello 应用
    
    这个 API 提供了以下功能：
    - Hello 端点：接收用户输入的名字并返回问候语
    - Chat 端点：实现 Agentic Loop，AI 可以自主决定是否使用搜索工具获取信息
    - Search 端点：转发搜索请求到 AI Builder 的搜索 API（使用 Tavily）
    
    ### 主要功能
    - 通过 GET 或 POST 方法调用 hello 端点
    - 支持通过查询参数传递名字
    - Chat API 实现 Agentic Loop：AI 可以自主决定是否调用搜索工具
    - 当 AI 决定搜索时，会自动执行搜索并将结果整合到最终回复中
    - Search API 转发到 AI Builder 的搜索 API，支持多关键词并发搜索
    - 自动生成 OpenAPI 文档
    
    ### 使用示例
    
    **Hello GET 请求示例：**
    ```
    GET /hello?name=YIGE
    响应: {"message": "hello, YIGE"}
    ```
    
    **Chat POST 请求示例：**
    ```json
    POST /chat
    {
        "messages": [
            {"role": "user", "content": "你好，请介绍一下你自己"}
        ]
    }
    ```
    
    **Search POST 请求示例：**
    ```json
    POST /search
    {
        "keywords": ["FastAPI", "Python web framework"]
    }
    ```
    
    ### 访问文档
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc
    - OpenAPI JSON: http://localhost:8000/openapi.json
    """,
    version="1.0.0",
    contact={
        "name": "API 支持",
    },
    license_info={
        "name": "MIT",
    },
)

# 挂载静态文件
# 在 Vercel 上，静态文件通过 vercel.json 路由处理
# 本地开发时使用 mount
import os
if os.getenv("VERCEL") != "1":
    app.mount("/static", StaticFiles(directory="static"), name="static")


class HelloResponse(BaseModel):
    """Hello API 的响应模型"""
    message: str = Field(
        ...,
        description="问候消息",
        example="hello, YIGE"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "hello, YIGE"
            }
        }


class HelloRequest(BaseModel):
    """Hello API 的请求体模型（用于 POST 请求）"""
    name: Optional[str] = Field(
        None,
        description="用户输入的名字，可以是中文、英文或拼音",
        example="YIGE",
        min_length=1,
        max_length=100
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "YIGE"
            }
        }


@app.get(
    "/",
    tags=["基础"],
    summary="主页",
    description="返回聊天界面的 HTML 页面",
    response_class=FileResponse
)
async def root():
    """
    主页端点
    
    返回聊天界面的 HTML 页面。
    """
    # 在 Vercel 上，静态文件通过 vercel.json 路由处理
    # 这里直接返回文件内容
    static_path = "static/index.html"
    
    # 尝试多个可能的路径
    possible_paths = [
        static_path,
        os.path.join(os.path.dirname(__file__), static_path),
        os.path.join(os.getcwd(), static_path),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return FileResponse(path)
    
    # 如果找不到文件，尝试读取并返回 HTML 内容
    try:
        for path in possible_paths:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    from fastapi.responses import HTMLResponse
                    return HTMLResponse(content=f.read())
            except FileNotFoundError:
                continue
    except Exception as e:
        logger.error(f"Error loading static file: {e}")
    
    # 如果都失败了，返回一个简单的 HTML
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head><title>AI Chat</title></head>
    <body>
        <h1>AI Chat with Agentic Loop</h1>
        <p>Static files not found. Please check the deployment.</p>
        <p><a href="/docs">API Documentation</a></p>
    </body>
    </html>
    """)


@app.get(
    "/hello",
    response_model=HelloResponse,
    tags=["Hello"],
    summary="Hello 问候（GET）",
    description="""
    ## Hello 端点 - GET 方法
    
    通过 GET 请求获取问候消息。
    
    ### 参数说明
    - **name** (可选): 用户输入的名字
      - 可以是中文、英文或拼音
      - 如果不提供，默认返回 "hello, 世界"
      - 示例值: "YIGE", "张三", "Alice"
    
    ### 使用示例
    
    **带参数：**
    ```
    GET /hello?name=YIGE
    ```
    
    **不带参数：**
    ```
    GET /hello
    ```
    
    ### 响应示例
    
    **成功响应 (200):**
    ```json
    {
        "message": "hello, YIGE"
    }
    ```
    
    **无参数时的响应:**
    ```json
    {
        "message": "hello, 世界"
    }
    ```
    """,
    response_description="包含问候消息的响应对象",
    responses={
        200: {
            "description": "成功返回问候消息",
            "content": {
                "application/json": {
                    "examples": {
                        "with_name": {
                            "summary": "带名字的响应",
                            "value": {"message": "hello, YIGE"}
                        },
                        "without_name": {
                            "summary": "不带名字的响应",
                            "value": {"message": "hello, 世界"}
                        }
                    }
                }
            }
        },
        422: {
            "description": "参数验证错误",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["query", "name"],
                                "msg": "value is not a valid string",
                                "type": "type_error.string"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def hello(
    name: Optional[str] = Query(
        None,
        description="用户输入的名字（可选）。可以是中文、英文或拼音，例如：YIGE、张三、Alice",
        example="YIGE",
        min_length=1,
        max_length=100,
        title="名字",
        alias="name"
    )
):
    """
    Hello 端点 - GET 方法
    
    接收一个可选的名字参数，返回格式化的问候消息。
    
    **参数：**
    - name: 可选的名字参数，通过查询字符串传递
    
    **返回：**
    - 如果提供了名字，返回 "hello, [名字]"
    - 如果没有提供名字，返回 "hello, 世界"
    """
    if name:
        return HelloResponse(message=f"hello, {name}")
    else:
        return HelloResponse(message="hello, 世界")


@app.post(
    "/hello",
    response_model=HelloResponse,
    tags=["Hello"],
    summary="Hello 问候（POST）",
    description="""
    ## Hello 端点 - POST 方法
    
    通过 POST 请求获取问候消息。支持通过查询参数或请求体传递名字。
    
    ### 参数传递方式
    
    1. **查询参数方式：**
       ```
       POST /hello?name=YIGE
       ```
    
    2. **请求体方式：**
       ```json
       POST /hello
       {
           "name": "YIGE"
       }
       ```
    
    ### 参数说明
    - **name** (可选): 用户输入的名字
      - 可以通过查询参数或请求体传递
      - 可以是中文、英文或拼音
      - 如果不提供，默认返回 "hello, 世界"
      - 示例值: "YIGE", "张三", "Alice"
    
    ### 使用示例
    
    **使用查询参数：**
    ```bash
    curl -X POST "http://localhost:8000/hello?name=YIGE"
    ```
    
    **使用请求体：**
    ```bash
    curl -X POST "http://localhost:8000/hello" \\
         -H "Content-Type: application/json" \\
         -d '{"name": "YIGE"}'
    ```
    
    ### 响应示例
    
    **成功响应 (200):**
    ```json
    {
        "message": "hello, YIGE"
    }
    ```
    """,
    response_description="包含问候消息的响应对象",
    responses={
        200: {
            "description": "成功返回问候消息",
            "content": {
                "application/json": {
                    "example": {"message": "hello, YIGE"}
                }
            }
        },
        422: {
            "description": "参数验证错误"
        }
    }
)
async def hello_post(
    name: Optional[str] = Query(
        None,
        description="用户输入的名字（可选，通过查询参数传递）",
        example="YIGE",
        min_length=1,
        max_length=100
    ),
    body: Optional[HelloRequest] = Body(
        None,
        description="请求体，包含名字字段（可选）",
        example={"name": "YIGE"}
    )
):
    """
    Hello 端点 - POST 方法
    
    支持通过查询参数或请求体传递名字。
    如果同时提供了查询参数和请求体，优先使用查询参数。
    
    **参数：**
    - name: 可选的名字参数，通过查询字符串传递
    - body: 可选的名字参数，通过请求体传递
    
    **返回：**
    - 如果提供了名字，返回 "hello, [名字]"
    - 如果没有提供名字，返回 "hello, 世界"
    """
    # 优先使用查询参数，如果没有则使用请求体
    final_name = name or (body.name if body else None)
    
    if final_name:
        return HelloResponse(message=f"hello, {final_name}")
    else:
        return HelloResponse(message="hello, 世界")


# ==================== Chat API 模型定义 ====================

class ChatMessage(BaseModel):
    """聊天消息模型"""
    role: str = Field(
        ...,
        description="消息角色：'system', 'user', 'assistant'",
        example="user"
    )
    content: str = Field(
        ...,
        description="消息内容",
        example="你好，请介绍一下你自己"
    )


class ChatRequest(BaseModel):
    """Chat API 请求模型"""
    messages: List[ChatMessage] = Field(
        ...,
        description="对话消息列表",
        min_items=1,
        example=[
            {"role": "user", "content": "你好，请介绍一下你自己"}
        ]
    )
    model: str = Field(
        "gpt-5",
        description="要使用的模型，默认为 gpt-5",
        example="gpt-5"
    )
    temperature: Optional[float] = Field(
        None,
        description="生成文本的随机性（0-2），值越高越随机",
        ge=0.0,
        le=2.0,
        example=0.7
    )
    max_tokens: Optional[int] = Field(
        None,
        description="最大生成 token 数",
        ge=1,
        example=1000
    )
    stream: Optional[bool] = Field(
        False,
        description="是否使用流式响应",
        example=False
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {"role": "user", "content": "你好，请介绍一下你自己"}
                ],
                "model": "gpt-5",
                "temperature": 0.7,
                "max_tokens": 1000
            }
        }


class ChatChoice(BaseModel):
    """Chat API 响应中的选择项"""
    index: int = Field(..., description="选择项的索引")
    message: ChatMessage = Field(..., description="AI 返回的消息")
    finish_reason: Optional[str] = Field(None, description="完成原因")


class UsageInfo(BaseModel):
    """Token 使用信息"""
    prompt_tokens: int = Field(..., description="输入 token 数")
    completion_tokens: int = Field(..., description="输出 token 数")
    total_tokens: int = Field(..., description="总 token 数")


class ChatResponse(BaseModel):
    """Chat API 响应模型"""
    id: str = Field(..., description="响应 ID")
    object: str = Field("chat.completion", description="对象类型")
    created: int = Field(..., description="创建时间戳")
    model: str = Field(..., description="使用的模型")
    choices: List[ChatChoice] = Field(..., description="响应选择项列表")
    usage: Optional[UsageInfo] = Field(None, description="Token 使用信息")


# ==================== Agentic Loop 辅助函数 ====================

def get_search_tool_definition():
    """返回搜索工具的函数定义（OpenAI 格式）"""
    return {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "在网络上搜索信息。当你需要查找最新的信息、事实、新闻或任何需要实时网络数据的内容时，使用这个工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "搜索关键词列表。可以是一个或多个关键词，用于搜索相关信息。"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "每个关键词返回的最大结果数，范围 1-20，默认 6",
                        "minimum": 1,
                        "maximum": 20,
                        "default": 6
                    }
                },
                "required": ["keywords"]
            }
        }
    }


def execute_search(keywords: List[str], max_results: int = 6) -> Dict[str, Any]:
    """
    执行搜索并返回结果
    
    Args:
        keywords: 搜索关键词列表
        max_results: 最大结果数
    
    Returns:
        搜索结果字典
    """
    if not AI_BUILDER_API_KEY:
        return {"error": "AI Builder API token 未配置"}
    
    url = f"{AI_BUILDER_BASE_URL}/v1/search/"
    headers = {
        "Authorization": f"Bearer {AI_BUILDER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "keywords": keywords,
        "max_results": max_results
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"搜索失败: {str(e)}"}


def execute_single_tool_call(tool_call: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行单个工具调用
    
    Args:
        tool_call: 工具调用对象，包含 function 和 id
    
    Returns:
        包含 tool_call_id, result_text, success 的字典
    """
    function = tool_call.get("function", {})
    function_name = function.get("name")
    function_args_str = function.get("arguments", "{}")
    tool_call_id = tool_call.get("id")
    
    try:
        # 解析参数
        function_args = json_lib.loads(function_args_str)
    except Exception as e:
        logger.warning(f"工具调用 {tool_call_id} 参数解析失败: {e}")
        function_args = {}
    
    # 执行搜索
    if function_name == "search_web":
        keywords = function_args.get("keywords", [])
        max_results = function_args.get("max_results", 6)
        
        # 执行搜索
        search_result = execute_search(keywords, max_results)
        
        # 格式化搜索结果
        search_result_text = format_search_results_for_llm(search_result)
        
        return {
            "tool_call_id": tool_call_id,
            "function_name": function_name,
            "keywords": keywords,
            "result_text": search_result_text,
            "search_result": search_result,
            "success": "error" not in search_result
        }
    else:
        logger.warning(f"未知的工具: {function_name}")
        return {
            "tool_call_id": tool_call_id,
            "function_name": function_name,
            "result_text": f"未知的工具: {function_name}",
            "success": False
        }


def format_search_results_for_llm(search_result: Dict[str, Any]) -> str:
    """
    将搜索结果格式化为 LLM 可读的文本
    
    Args:
        search_result: 搜索结果字典
    
    Returns:
        格式化的文本字符串
    """
    if "error" in search_result:
        return f"搜索错误: {search_result['error']}"
    
    formatted_text = "搜索结果：\n\n"
    
    if "queries" in search_result:
        for query in search_result["queries"]:
            keyword = query.get("keyword", "未知")
            response_data = query.get("response", {})
            results = response_data.get("results", [])
            
            formatted_text += f"关键词: {keyword}\n"
            formatted_text += f"找到 {len(results)} 个结果：\n\n"
            
            for i, result in enumerate(results[:5], 1):  # 只取前5个结果
                title = result.get("title", "无标题")
                url = result.get("url", "")
                content = result.get("content", "")
                score = result.get("score", 0)
                
                formatted_text += f"{i}. {title} (相关性: {score:.2f})\n"
                formatted_text += f"   URL: {url}\n"
                formatted_text += f"   内容: {content[:200]}...\n\n"
            
            # 如果有摘要答案，也包含进去
            if response_data.get("answer"):
                formatted_text += f"摘要: {response_data['answer']}\n\n"
    
    # 如果有综合答案，也包含进去
    if search_result.get("combined_answer"):
        formatted_text += f"综合答案: {search_result['combined_answer']}\n"
    
    return formatted_text


# ==================== Chat API 端点 ====================

@app.post(
    "/chat",
    response_model=ChatResponse,
    tags=["Chat"],
    summary="Chat 对话（Agentic Loop with Search）",
    description="""
    ## Chat 端点 - Agentic Loop with Search Tool (最多四轮)
    
    这个端点实现了 Agentic Loop（代理循环），AI 可以自主决定是否使用搜索工具来获取信息。
    
    ### 工作流程
    1. **第一轮**：AI 接收用户输入，并可以选择调用 `search_web` 工具来搜索信息
    2. **工具执行**：如果 AI 决定调用工具，系统会执行搜索并获取结果
    3. **第二轮**：如果第一轮调用了工具，AI 可以继续调用工具进行更深入的搜索
    4. **第三轮**：如果前两轮调用了工具，AI 可以继续调用工具进行更深入的搜索
    5. **第四轮**：无论前面如何，第四轮不提供工具，强制生成最终答案
    6. **返回结果**：AI 基于所有搜索结果生成最终回复
    
    ### 特点
    - 最多支持四轮交互
    - 前3轮可以调用工具
    - 第4轮强制生成最终答案，避免无限循环
    
    ### 功能特点
    - AI 自主决定是否需要搜索
    - 支持单轮工具调用（只执行一次搜索）
    - 自动将搜索结果整合到最终回复中
    - 默认使用 GPT-5 模型
    - 支持完整的 OpenAI 兼容格式
    
    ### 请求参数
    
    - **messages** (必需): 对话消息列表
      - 每个消息包含 `role` (system/user/assistant) 和 `content`
      - 至少需要一条消息
    - **model** (可选): 模型名称，默认为 "gpt-5"
    - **temperature** (可选): 生成随机性，0-2 之间
    - **max_tokens** (可选): 最大生成 token 数
    - **stream** (可选): 是否流式响应，默认 false
    
    ### 使用示例
    
    **基本对话（不需要搜索）：**
    ```json
    POST /chat
    {
        "messages": [
            {"role": "user", "content": "你好，请介绍一下你自己"}
        ]
    }
    ```
    
    **需要搜索的对话（AI 会自动调用搜索工具）：**
    ```json
    POST /chat
    {
        "messages": [
            {"role": "user", "content": "FastAPI 的最新版本是什么？它有什么新特性？"}
        ]
    }
    ```
    
    在这个例子中：
    1. **第一轮**：AI 会判断需要搜索最新信息，自动调用 `search_web` 工具
    2. **工具执行**：系统执行搜索并获取结果
    3. **第二轮**：AI 可以继续调用工具进行更深入的搜索（如果需要）
    4. **第三轮**：AI 可以继续调用工具进行更深入的搜索（如果需要）
    5. **第四轮**：强制生成最终答案，整合所有搜索结果
    6. **返回结果**：包含最新信息的最终回复
    
    **带参数的高级请求：**
    ```json
    POST /chat
    {
        "messages": [
            {"role": "system", "content": "你是一个有用的助手，可以使用网络搜索获取最新信息"},
            {"role": "user", "content": "Python 3.12 有什么新特性？"}
        ],
        "model": "gpt-5",
        "temperature": 0.7,
        "max_tokens": 1000
    }
    ```
    
    **使用 curl：**
    ```bash
    curl -X POST "http://localhost:8000/chat" \\
         -H "Content-Type: application/json" \\
         -d '{
             "messages": [
                 {"role": "user", "content": "你好"}
             ]
         }'
    ```
    
    ### 响应示例
    
    **成功响应 (200):**
    ```json
    {
        "id": "chatcmpl-xxx",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "gpt-5",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "你好！我是 AI 助手..."
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }
    ```
    
    ### 错误处理
    
    - **401**: API token 未配置或无效
    - **422**: 请求参数验证错误
    - **500**: AI Builder 服务错误或网络错误
    """,
    response_description="AI Builder 返回的聊天完成响应",
    responses={
        200: {
            "description": "成功返回 AI 响应",
            "content": {
                "application/json": {
                    "example": {
                        "id": "chatcmpl-abc123",
                        "object": "chat.completion",
                        "created": 1234567890,
                        "model": "gpt-5",
                        "choices": [
                            {
                                "index": 0,
                                "message": {
                                    "role": "assistant",
                                    "content": "你好！我是 AI 助手，很高兴为你服务。"
                                },
                                "finish_reason": "stop"
                            }
                        ],
                        "usage": {
                            "prompt_tokens": 10,
                            "completion_tokens": 20,
                            "total_tokens": 30
                        }
                    }
                }
            }
        },
        401: {
            "description": "API token 未配置或无效",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "AI Builder API token 未配置"
                    }
                }
            }
        },
        422: {
            "description": "请求参数验证错误"
        },
        500: {
            "description": "AI Builder 服务错误",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "无法连接到 AI Builder 服务"
                    }
                }
            }
        }
    }
)
async def chat(request: ChatRequest):
    """
    Chat 端点 - Agentic Loop with Search (最多四轮)
    
    实现代理循环：AI 可以自主决定是否使用搜索工具，最多支持四轮交互。
    - 第一轮、第二轮和第三轮：可以提供工具
    - 第四轮：强制不提供工具，生成最终答案
    
    **参数：**
    - request: ChatRequest 对象，包含消息列表和可选参数
    
    **返回：**
    - ChatResponse 对象，包含 AI 的响应
    """
    # 检查 API token
    if not AI_BUILDER_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="AI Builder API token 未配置。请设置 AI_BUILDER_TOKEN 环境变量或确保 'AI builder API key:' 文件存在。"
        )
    
    url = f"{AI_BUILDER_BASE_URL}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {AI_BUILDER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 准备消息列表
    messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    
    # 最大轮数：4轮
    MAX_ROUNDS = 4
    
    try:
        logger.info("=" * 60)
        logger.info("开始 Agentic Loop - Chat API 请求")
        logger.info("=" * 60)
        logger.info(f"用户消息数量: {len(messages)}")
        logger.info(f"模型: {request.model}")
        logger.info(f"最大轮数: {MAX_ROUNDS}")
        
        # ========== 循环处理最多三轮 ==========
        for round_num in range(1, MAX_ROUNDS + 1):
            logger.info("")
            logger.info("-" * 60)
            logger.info(f"第 {round_num} 轮开始")
            logger.info("-" * 60)
            
            # 判断是否提供工具
            # 前3轮可以提供工具，第4轮不提供
            provide_tools = round_num < MAX_ROUNDS
            
            logger.info(f"是否提供工具: {provide_tools}")
            if provide_tools:
                logger.info("✓ 工具可用: search_web")
            else:
                logger.info(f"✗ 工具不可用（第{MAX_ROUNDS}轮，强制生成最终答案）")
            
            # 构建请求负载
            payload = {
                "model": request.model,
                "messages": messages
            }
            
            # 前3轮提供工具
            if provide_tools:
                payload["tools"] = [get_search_tool_definition()]
                payload["tool_choice"] = "auto"
            
            # 添加可选参数
            if request.temperature is not None:
                payload["temperature"] = request.temperature
            if request.max_tokens is not None:
                payload["max_tokens"] = request.max_tokens
            if request.stream is not None:
                payload["stream"] = request.stream
            
            logger.info(f"发送请求到 AI Builder...")
            logger.info(f"消息历史长度: {len(messages)}")
            
            # 发送请求
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            round_response = response.json()
            
            # 检查响应
            choices = round_response.get("choices", [])
            if not choices:
                logger.warning("响应中没有 choices，直接返回")
                return round_response
            
            choice = choices[0]
            message = choice.get("message", {})
            tool_calls = message.get("tool_calls")
            finish_reason = choice.get("finish_reason")
            usage = round_response.get("usage", {})
            
            logger.info(f"响应状态: finish_reason = {finish_reason}")
            logger.info(f"Token 使用: prompt={usage.get('prompt_tokens', 0)}, completion={usage.get('completion_tokens', 0)}, total={usage.get('total_tokens', 0)}")
            
            # 检查是否有工具调用
            if tool_calls:
                logger.info(f"✓ 检测到 {len(tool_calls)} 个工具调用")
            else:
                logger.info("✗ 没有工具调用")
                if message.get("content"):
                    content_preview = message.get("content", "")[:200]
                    logger.info(f"AI 回复预览: {content_preview}...")
            
            # 将 assistant 消息添加到消息历史
            assistant_message = {
                "role": "assistant",
                "content": message.get("content")
            }
            if tool_calls:
                assistant_message["tool_calls"] = tool_calls
            messages.append(assistant_message)
            
            # 如果没有工具调用，或者 finish_reason 是 "stop"，直接返回
            if not tool_calls or finish_reason == "stop":
                logger.info(f"第 {round_num} 轮结束：没有工具调用或已完成，返回响应")
                logger.info("=" * 60)
                return round_response
            
            # ========== 执行工具调用（并行执行）==========
            logger.info("")
            logger.info("执行工具调用（并行执行）:")
            
            # 先记录所有工具调用的信息
            for idx, tool_call in enumerate(tool_calls, 1):
                function = tool_call.get("function", {})
                function_name = function.get("name")
                function_args_str = function.get("arguments", "{}")
                tool_call_id = tool_call.get("id")
                
                logger.info(f"  工具调用 #{idx}:")
                logger.info(f"    ID: {tool_call_id}")
                logger.info(f"    工具名称: {function_name}")
                
                # 解析参数用于日志
                try:
                    function_args = json_lib.loads(function_args_str)
                    logger.info(f"    参数 (JSON): {json_lib.dumps(function_args, indent=6, ensure_ascii=False)}")
                    if function_name == "search_web":
                        keywords = function_args.get("keywords", [])
                        max_results = function_args.get("max_results", 6)
                        logger.info(f"      关键词: {keywords}")
                        logger.info(f"      最大结果数: {max_results}")
                except Exception as e:
                    logger.warning(f"    参数解析失败: {e}")
                    logger.info(f"    原始参数: {function_args_str}")
            
            # 并行执行所有工具调用
            logger.info("")
            logger.info("开始并行执行工具调用...")
            tool_results = []
            
            with ThreadPoolExecutor(max_workers=len(tool_calls)) as executor:
                # 提交所有任务
                future_to_tool_call = {
                    executor.submit(execute_single_tool_call, tool_call): tool_call 
                    for tool_call in tool_calls
                }
                
                # 收集结果（按完成顺序）
                for future in as_completed(future_to_tool_call):
                    tool_call = future_to_tool_call[future]
                    try:
                        result = future.result()
                        tool_results.append(result)
                        
                        # 记录结果
                        if result["success"]:
                            if result["function_name"] == "search_web":
                                search_result = result["search_result"]
                                queries = search_result.get("queries", [])
                                logger.info(f"  ✓ 工具调用 {result['tool_call_id']} 完成")
                                logger.info(f"    返回 {len(queries)} 个关键词的搜索结果")
                                
                                for query in queries:
                                    keyword = query.get("keyword", "未知")
                                    response_data = query.get("response", {})
                                    results = response_data.get("results", [])
                                    logger.info(f"      关键词 '{keyword}': {len(results)} 个结果")
                                    
                                    # 显示前2个结果的摘要
                                    for i, result_item in enumerate(results[:2], 1):
                                        title = result_item.get("title", "无标题")
                                        score = result_item.get("score", 0)
                                        logger.info(f"        [{i}] {title} (相关性: {score:.2f})")
                            else:
                                logger.info(f"  ✓ 工具调用 {result['tool_call_id']} 完成")
                        else:
                            logger.error(f"  ✗ 工具调用 {result['tool_call_id']} 失败")
                    except Exception as e:
                        logger.error(f"  ✗ 工具调用执行异常: {e}")
                        tool_results.append({
                            "tool_call_id": tool_call.get("id"),
                            "function_name": tool_call.get("function", {}).get("name", "unknown"),
                            "result_text": f"执行异常: {str(e)}",
                            "success": False
                        })
            
            # 按原始顺序添加结果到消息历史（保持工具调用顺序）
            tool_results_dict = {r["tool_call_id"]: r for r in tool_results}
            for tool_call in tool_calls:
                tool_call_id = tool_call.get("id")
                if tool_call_id in tool_results_dict:
                    result = tool_results_dict[tool_call_id]
                    messages.append({
                        "role": "tool",
                        "content": result["result_text"],
                        "tool_call_id": tool_call_id
                    })
                    logger.info(f"  ✓ 工具结果 {tool_call_id} 已添加到消息历史")
            
            logger.info(f"所有工具调用执行完成（共 {len(tool_calls)} 个）")
            
            logger.info(f"第 {round_num} 轮结束：已执行工具调用，准备下一轮")
            
            # 如果这是第4轮，已经执行完工具调用，下一轮循环会强制不提供工具
            # 如果这是前3轮，继续循环，下一轮仍然可以提供工具
        
        # 如果循环结束（理论上不应该到达这里，因为第4轮应该返回）
        # 返回最后一轮的响应
        logger.info("=" * 60)
        logger.info("Agentic Loop 完成")
        logger.info("=" * 60)
        return round_response
        
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=500,
            detail="请求超时，AI Builder 服务响应时间过长"
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=500,
            detail="无法连接到 AI Builder 服务，请检查网络连接"
        )
    except requests.exceptions.HTTPError as e:
        error_detail = f"AI Builder API 错误: {e.response.status_code}"
        try:
            error_body = e.response.json()
            if "detail" in error_body:
                error_detail = error_body["detail"]
            elif "message" in error_body:
                error_detail = error_body["message"]
        except:
            error_detail = e.response.text or error_detail
        
        raise HTTPException(
            status_code=e.response.status_code,
            detail=error_detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"处理请求时发生错误: {str(e)}"
        )


# ==================== Search API 模型定义 ====================

class SearchRequest(BaseModel):
    """Search API 请求模型"""
    keywords: List[str] = Field(
        ...,
        description="搜索关键词列表，支持多个关键词并发搜索",
        min_items=1,
        example=["FastAPI", "Python web framework"]
    )
    max_results: Optional[int] = Field(
        6,
        description="每个关键词返回的最大结果数，范围 1-20，默认 6",
        ge=1,
        le=20,
        example=6
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "keywords": ["FastAPI", "Python web framework"],
                "max_results": 6
            }
        }


class SearchError(BaseModel):
    """搜索错误信息"""
    keyword: str = Field(..., description="失败的关键词")
    error: str = Field(..., description="错误描述")


class SearchQueryResult(BaseModel):
    """单个关键词的搜索结果"""
    keyword: str = Field(..., description="搜索关键词")
    response: Dict[str, Any] = Field(..., description="Tavily API 返回的原始响应数据")


class SearchResponse(BaseModel):
    """Search API 响应模型"""
    queries: List[SearchQueryResult] = Field(
        ...,
        description="每个关键词的搜索结果列表"
    )
    combined_answer: Optional[str] = Field(
        None,
        description="所有关键词搜索结果的综合摘要（如果可用）"
    )
    errors: Optional[List[SearchError]] = Field(
        None,
        description="搜索失败的关键词列表（如果有）"
    )


# ==================== Search API 端点 ====================

@app.post(
    "/search",
    response_model=SearchResponse,
    tags=["Search"],
    summary="Web 搜索（转发到 AI Builder）",
    description="""
    ## Search 端点 - 转发到 AI Builder Tavily 搜索
    
    这个端点将你的搜索请求转发到 AI Builder 的搜索 API，使用 Tavily 搜索引擎进行网络搜索。
    
    ### 功能特点
    - 支持多个关键词并发搜索
    - 每个关键词独立查询，互不影响
    - 返回详细的搜索结果（标题、URL、内容、评分等）
    - 可选的综合摘要答案
    - 自动处理搜索错误
    
    ### 请求参数
    
    - **keywords** (必需): 搜索关键词列表
      - 至少需要一个关键词
      - 支持多个关键词，会并发搜索
      - 示例: `["FastAPI", "Python web framework"]`
    - **max_results** (可选): 每个关键词返回的最大结果数
      - 范围: 1-20
      - 默认值: 6
    
    ### 使用示例
    
    **单关键词搜索：**
    ```json
    POST /search
    {
        "keywords": ["FastAPI"]
    }
    ```
    
    **多关键词并发搜索：**
    ```json
    POST /search
    {
        "keywords": ["FastAPI", "Python web framework", "REST API"],
        "max_results": 10
    }
    ```
    
    **使用 curl：**
    ```bash
    curl -X POST "http://localhost:8000/search" \\
         -H "Content-Type: application/json" \\
         -d '{
             "keywords": ["FastAPI", "Python"]
         }'
    ```
    
    ### 响应示例
    
    **成功响应 (200):**
    ```json
    {
        "queries": [
            {
                "keyword": "FastAPI",
                "response": {
                    "results": [
                        {
                            "title": "FastAPI - Modern Python Web Framework",
                            "url": "https://fastapi.tiangolo.com",
                            "content": "FastAPI is a modern, fast web framework...",
                            "score": 0.95
                        }
                    ],
                    "answer": "FastAPI is a modern Python web framework..."
                }
            }
        ],
        "combined_answer": "FastAPI is a modern Python web framework...",
        "errors": null
    }
    ```
    
    ### 响应结构说明
    
    - **queries**: 每个关键词的搜索结果
      - `keyword`: 搜索的关键词
      - `response`: Tavily API 返回的完整响应，包含：
        - `results`: 搜索结果列表（标题、URL、内容、评分等）
        - `answer`: 可选的摘要答案
    - **combined_answer**: 所有关键词的综合摘要（如果可用）
    - **errors**: 搜索失败的关键词列表（如果有）
    
    ### 错误处理
    
    - **401**: API token 未配置或无效
    - **422**: 请求参数验证错误（如关键词列表为空）
    - **500**: AI Builder 服务错误或网络错误
    
    ### 注意事项
    
    - 支持多个关键词并发搜索，每个关键词独立处理
    - 如果某个关键词搜索失败，会在 `errors` 字段中返回，其他关键词的结果仍会正常返回
    - 搜索结果来自 Tavily 搜索引擎，包含实时网络内容
    """,
    response_description="AI Builder 返回的搜索结果",
    responses={
        200: {
            "description": "成功返回搜索结果",
            "content": {
                "application/json": {
                    "example": {
                        "queries": [
                            {
                                "keyword": "FastAPI",
                                "response": {
                                    "results": [
                                        {
                                            "title": "FastAPI Documentation",
                                            "url": "https://fastapi.tiangolo.com",
                                            "content": "FastAPI is a modern web framework...",
                                            "score": 0.95
                                        }
                                    ]
                                }
                            }
                        ],
                        "combined_answer": "FastAPI is a modern Python web framework...",
                        "errors": None
                    }
                }
            }
        },
        401: {
            "description": "API token 未配置或无效",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "AI Builder API token 未配置"
                    }
                }
            }
        },
        422: {
            "description": "请求参数验证错误"
        },
        500: {
            "description": "AI Builder 服务错误",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "无法连接到 AI Builder 服务"
                    }
                }
            }
        }
    }
)
async def search(request: SearchRequest):
    """
    Search 端点 - 转发请求到 AI Builder
    
    将搜索请求转发到 AI Builder 的搜索 API，使用 Tavily 搜索引擎。
    
    **参数：**
    - request: SearchRequest 对象，包含关键词列表和可选的最大结果数
    
    **返回：**
    - SearchResponse 对象，包含每个关键词的搜索结果
    """
    # 检查 API token
    if not AI_BUILDER_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="AI Builder API token 未配置。请设置 AI_BUILDER_TOKEN 环境变量或确保 'AI builder API key:' 文件存在。"
        )
    
    # 构建转发请求
    url = f"{AI_BUILDER_BASE_URL}/v1/search/"
    headers = {
        "Authorization": f"Bearer {AI_BUILDER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 构建请求体
    payload = {
        "keywords": request.keywords,
        "max_results": request.max_results
    }
    
    try:
        # 发送请求到 AI Builder
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        # 返回响应
        return response.json()
        
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=500,
            detail="请求超时，AI Builder 服务响应时间过长"
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=500,
            detail="无法连接到 AI Builder 服务，请检查网络连接"
        )
    except requests.exceptions.HTTPError as e:
        error_detail = f"AI Builder API 错误: {e.response.status_code}"
        try:
            error_body = e.response.json()
            if "detail" in error_body:
                error_detail = error_body["detail"]
            elif "message" in error_body:
                error_detail = error_body["message"]
        except:
            error_detail = e.response.text or error_detail
        
        raise HTTPException(
            status_code=e.response.status_code,
            detail=error_detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"处理请求时发生错误: {str(e)}"
        )

