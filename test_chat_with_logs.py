#!/usr/bin/env python3
"""
测试 Chat API 并查看详细日志
"""

import requests
import json
import sys

# API 基础 URL
BASE_URL = "http://localhost:8000"

def test_chat_with_logs():
    """
    测试 Chat API 并查看日志输出
    """
    print(f"\n{'='*60}")
    print(f"测试 Chat API - 查看详细日志")
    print(f"{'='*60}\n")
    
    url = f"{BASE_URL}/chat"
    
    # 测试请求数据
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "请搜索 FastAPI 的最新版本，然后搜索它的主要竞争对手"
            }
        ],
        "model": "gpt-5",
        "temperature": 0.7
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"📤 发送请求到: {url}")
        print(f"请求内容:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print(f"\n{'='*60}")
        print("注意：详细的工具调用日志会输出到运行 FastAPI 服务器的终端")
        print("请查看运行 'uvicorn main:app --reload' 的终端窗口")
        print(f"{'='*60}\n")
        
        response = requests.post(url, json=payload, headers=headers, timeout=180)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ 请求成功！")
        print(f"状态码: {response.status_code}")
        
        # 检查响应结构
        if "choices" in result and len(result["choices"]) > 0:
            choice = result["choices"][0]
            message = choice.get("message", {})
            content = message.get("content", "")
            tool_calls = message.get("tool_calls")
            
            print(f"\n📥 响应摘要:")
            print(f"模型: {result.get('model', 'N/A')}")
            print(f"完成原因: {choice.get('finish_reason', 'N/A')}")
            
            if tool_calls:
                print(f"\n🔧 检测到工具调用（在最终响应中）:")
                for tool_call in tool_calls:
                    func = tool_call.get("function", {})
                    print(f"  工具: {func.get('name', 'N/A')}")
            else:
                print(f"\n💬 AI 最终回复（前500字符）:")
                print(f"{content[:500]}...")
            
            # 显示使用统计
            if "usage" in result:
                usage = result["usage"]
                print(f"\n📊 Token 使用统计:")
                print(f"  输入 tokens: {usage.get('prompt_tokens', 'N/A')}")
                print(f"  输出 tokens: {usage.get('completion_tokens', 'N/A')}")
                print(f"  总计 tokens: {usage.get('total_tokens', 'N/A')}")
        
        print(f"\n{'='*60}")
        print("提示：查看运行 FastAPI 服务器的终端，可以看到详细的日志：")
        print("  - 每轮的开始和结束")
        print("  - 工具调用的详细信息（工具名称、参数）")
        print("  - 搜索结果的摘要")
        print(f"{'='*60}\n")
        
        return result
        
    except requests.exceptions.ConnectionError:
        print(f"❌ 连接错误：无法连接到 {BASE_URL}")
        print("请确保 FastAPI 应用正在运行（运行: uvicorn main:app --reload）")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 错误：{e}")
        print(f"状态码: {e.response.status_code}")
        try:
            error_body = e.response.json()
            print(f"错误详情:")
            print(json.dumps(error_body, indent=2, ensure_ascii=False))
        except:
            print(f"响应内容: {e.response.text}")
        return None
    except requests.exceptions.Timeout:
        print(f"❌ 请求超时：AI Builder 服务响应时间过长")
        return None
    except Exception as e:
        print(f"❌ 发生错误：{e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    test_chat_with_logs()

