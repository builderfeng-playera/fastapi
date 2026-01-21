#!/usr/bin/env python3
"""
测试 Search API 的脚本
测试转发到 AI Builder 的搜索 API
"""

import requests
import json

# API 基础 URL
BASE_URL = "http://localhost:8000"

def test_search_single_keyword():
    """
    测试单关键词搜索
    """
    print(f"\n{'='*50}")
    print(f"测试 POST /search 接口 - 单关键词")
    print(f"{'='*50}")
    
    url = f"{BASE_URL}/search"
    
    # 测试请求数据
    payload = {
        "keywords": ["FastAPI"],
        "max_results": 5
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
        
        # 显示搜索结果摘要
        if "queries" in result:
            print(f"\n🔍 搜索结果摘要:")
            for query in result["queries"]:
                keyword = query.get("keyword", "N/A")
                response_data = query.get("response", {})
                results = response_data.get("results", [])
                print(f"\n  关键词: {keyword}")
                print(f"  结果数量: {len(results)}")
                if results:
                    print(f"  第一个结果:")
                    first_result = results[0]
                    print(f"    标题: {first_result.get('title', 'N/A')}")
                    print(f"    URL: {first_result.get('url', 'N/A')}")
                    print(f"    评分: {first_result.get('score', 'N/A')}")
        
        # 显示综合答案
        if result.get("combined_answer"):
            print(f"\n📝 综合答案:")
            print(f"  {result['combined_answer']}")
        
        # 显示错误（如果有）
        if result.get("errors"):
            print(f"\n⚠️  搜索错误:")
            for error in result["errors"]:
                print(f"  关键词 '{error.get('keyword')}': {error.get('error')}")
        
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


def test_search_multiple_keywords():
    """
    测试多关键词并发搜索
    """
    print(f"\n{'='*50}")
    print(f"测试 POST /search 接口 - 多关键词")
    print(f"{'='*50}")
    
    url = f"{BASE_URL}/search"
    
    # 测试请求数据
    payload = {
        "keywords": ["FastAPI", "Python web framework", "REST API"],
        "max_results": 3
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
        
        # 显示搜索结果摘要
        if "queries" in result:
            print(f"\n🔍 搜索结果摘要:")
            for query in result["queries"]:
                keyword = query.get("keyword", "N/A")
                response_data = query.get("response", {})
                results = response_data.get("results", [])
                print(f"\n  关键词: {keyword}")
                print(f"  结果数量: {len(results)}")
                if results:
                    print(f"  前 2 个结果:")
                    for i, res in enumerate(results[:2], 1):
                        print(f"    {i}. {res.get('title', 'N/A')}")
                        print(f"       URL: {res.get('url', 'N/A')}")
        
        # 显示综合答案
        if result.get("combined_answer"):
            print(f"\n📝 综合答案:")
            print(f"  {result['combined_answer'][:200]}...")  # 只显示前200字符
        
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
    print("🚀 开始测试 Search API")
    print(f"API 地址: {BASE_URL}")
    
    # 测试单关键词搜索
    test_search_single_keyword()
    
    # 测试多关键词搜索
    test_search_multiple_keywords()
    
    print(f"\n{'='*50}")
    print("测试完成！")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()

