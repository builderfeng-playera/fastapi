#!/usr/bin/env python3
"""
测试 Chat API Agentic Loop 的脚本
测试 AI 自动调用搜索工具的功能
"""

import requests
import json

# API 基础 URL
BASE_URL = "http://localhost:8000"

def test_chat_with_search():
    """
    测试需要搜索的对话（支持多轮工具调用）
    """
    print(f"\n{'='*50}")
    print(f"测试 Chat API - 多轮工具调用场景")
    print(f"{'='*50}")
    
    url = f"{BASE_URL}/chat"
    
    # 测试请求数据 - 需要搜索最新信息
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "FastAPI 的最新版本是什么？它有什么新特性？"
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
        print(f"\n💡 预期行为：")
        print(f"   - 第一轮：AI 会调用 search_web 工具搜索 FastAPI 最新版本")
        print(f"   - 第二轮：AI 可以继续调用工具进行更深入的搜索（如果需要）")
        print(f"   - 第三轮：AI 可以继续调用工具进行更深入的搜索（如果需要）")
        print(f"   - 第四轮：强制生成最终答案，整合所有搜索结果")
        print(f"   - 最多支持四轮工具调用")
        
        response = requests.post(url, json=payload, headers=headers, timeout=240)
        response.raise_for_status()
        
        result = response.json()
        print(f"\n✅ 请求成功！")
        print(f"状态码: {response.status_code}")
        
        # 检查响应结构
        if "choices" in result and len(result["choices"]) > 0:
            choice = result["choices"][0]
            message = choice.get("message", {})
            content = message.get("content", "")
            tool_calls = message.get("tool_calls")
            
            print(f"\n📥 响应内容:")
            print(f"模型: {result.get('model', 'N/A')}")
            print(f"完成原因: {choice.get('finish_reason', 'N/A')}")
            
            if tool_calls:
                print(f"\n🔧 检测到工具调用:")
                for tool_call in tool_calls:
                    func = tool_call.get("function", {})
                    print(f"  工具: {func.get('name', 'N/A')}")
                    args = func.get('arguments', '{}')
                    try:
                        args_dict = json.loads(args)
                        keywords = args_dict.get('keywords', [])
                        print(f"  关键词: {keywords}")
                    except:
                        print(f"  参数: {args[:100]}...")
                print(f"\n💬 最终回复（可能经过多轮工具调用）:")
            else:
                print(f"\n💬 AI 回复（未使用工具）:")
            
            print(f"{content}")
            
            # 显示使用统计
            if "usage" in result:
                usage = result["usage"]
                print(f"\n📊 Token 使用统计:")
                print(f"  输入 tokens: {usage.get('prompt_tokens', 'N/A')}")
                print(f"  输出 tokens: {usage.get('completion_tokens', 'N/A')}")
                print(f"  总计 tokens: {usage.get('total_tokens', 'N/A')}")
        else:
            print(f"\n📥 完整响应:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
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


def test_chat_without_search():
    """
    测试不需要搜索的对话
    """
    print(f"\n{'='*50}")
    print(f"测试 Chat API - 不需要搜索的场景")
    print(f"{'='*50}")
    
    url = f"{BASE_URL}/chat"
    
    # 测试请求数据 - 不需要搜索
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "你好，请用一句话介绍一下你自己"
            }
        ],
        "model": "gpt-5"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"\n📤 发送请求:")
        print(f"URL: {url}")
        print(f"Payload:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print(f"\n💡 预期行为：AI 应该直接回复，不需要调用搜索工具")
        
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        print(f"\n✅ 请求成功！")
        print(f"状态码: {response.status_code}")
        
        # 检查响应结构
        if "choices" in result and len(result["choices"]) > 0:
            choice = result["choices"][0]
            message = choice.get("message", {})
            content = message.get("content", "")
            tool_calls = message.get("tool_calls")
            
            if tool_calls:
                print(f"\n⚠️  意外：AI 调用了工具（可能不需要）")
            else:
                print(f"\n✅ 正确：AI 没有调用工具，直接回复")
            
            print(f"\n💬 AI 回复:")
            print(f"{content}")
        else:
            print(f"\n📥 完整响应:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        return result
        
    except requests.exceptions.ConnectionError:
        print(f"❌ 连接错误：无法连接到 {BASE_URL}")
        return None
    except Exception as e:
        print(f"❌ 发生错误：{e}")
        return None


def main():
    """主函数"""
    print("🚀 开始测试 Chat API Agentic Loop (最多四轮工具调用)")
    print(f"API 地址: {BASE_URL}")
    
    # 测试多轮工具调用场景
    test_chat_with_search()
    
    # 测试不需要搜索的场景
    test_chat_without_search()
    
    print(f"\n{'='*50}")
    print("测试完成！")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()

