#!/usr/bin/env python3
"""
测试 Chat API 的脚本
测试转发到 AI Builder 的 chat completion API
"""

import requests
import json

# API 基础 URL
BASE_URL = "http://localhost:8000"

def test_chat():
    """
    测试 POST /chat 接口
    """
    print(f"\n{'='*50}")
    print(f"测试 POST /chat 接口")
    print(f"{'='*50}")
    
    url = f"{BASE_URL}/chat"
    
    # 测试请求数据
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "你好，请用一句话介绍一下你自己"
            }
        ],
        "model": "gpt-5",
        "temperature": 0.7
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"\n📤 发送请求:")
        print(f"URL: {url}")
        print(f"Payload:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        print(f"\n✅ 请求成功！")
        print(f"状态码: {response.status_code}")
        print(f"\n📥 响应内容:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 提取 AI 回复
        if "choices" in result and len(result["choices"]) > 0:
            ai_message = result["choices"][0]["message"]["content"]
            print(f"\n🤖 AI 回复:")
            print(f"{ai_message}")
        
        # 显示使用统计
        if "usage" in result:
            usage = result["usage"]
            print(f"\n📊 Token 使用统计:")
            print(f"  输入 tokens: {usage.get('prompt_tokens', 'N/A')}")
            print(f"  输出 tokens: {usage.get('completion_tokens', 'N/A')}")
            print(f"  总计 tokens: {usage.get('total_tokens', 'N/A')}")
        
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


def main():
    """主函数"""
    print("🚀 开始测试 Chat API")
    print(f"API 地址: {BASE_URL}")
    
    # 测试 Chat API
    test_chat()
    
    print(f"\n{'='*50}")
    print("测试完成！")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()

