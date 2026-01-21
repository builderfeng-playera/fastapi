#!/usr/bin/env python3
"""
测试 Hello API 的脚本
使用 "yage" 作为名字来测试 hello 接口
"""

import requests
import json

# API 基础 URL
BASE_URL = "http://localhost:8000"

def test_hello_get(name="yage"):
    """
    测试 GET /hello 接口
    
    Args:
        name: 要测试的名字，默认为 "yage"
    """
    print(f"\n{'='*50}")
    print(f"测试 GET /hello 接口，名字: {name}")
    print(f"{'='*50}")
    
    url = f"{BASE_URL}/hello"
    params = {"name": name}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果状态码不是 200，会抛出异常
        
        result = response.json()
        print(f"✅ 请求成功！")
        print(f"状态码: {response.status_code}")
        print(f"响应内容:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"\n完整响应: {result['message']}")
        
        return result
        
    except requests.exceptions.ConnectionError:
        print(f"❌ 连接错误：无法连接到 {BASE_URL}")
        print("请确保 FastAPI 应用正在运行（运行: uvicorn main:app --reload）")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 错误：{e}")
        print(f"响应内容: {response.text}")
        return None
    except Exception as e:
        print(f"❌ 发生错误：{e}")
        return None


def test_hello_post(name="yage"):
    """
    测试 POST /hello 接口
    
    Args:
        name: 要测试的名字，默认为 "yage"
    """
    print(f"\n{'='*50}")
    print(f"测试 POST /hello 接口，名字: {name}")
    print(f"{'='*50}")
    
    url = f"{BASE_URL}/hello"
    params = {"name": name}
    
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ 请求成功！")
        print(f"状态码: {response.status_code}")
        print(f"响应内容:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"\n完整响应: {result['message']}")
        
        return result
        
    except requests.exceptions.ConnectionError:
        print(f"❌ 连接错误：无法连接到 {BASE_URL}")
        print("请确保 FastAPI 应用正在运行（运行: uvicorn main:app --reload）")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 错误：{e}")
        print(f"响应内容: {response.text}")
        return None
    except Exception as e:
        print(f"❌ 发生错误：{e}")
        return None


def main():
    """主函数"""
    print("🚀 开始测试 Hello API")
    print(f"API 地址: {BASE_URL}")
    
    # 测试名字
    test_name = "yage"
    
    # 测试 GET 方法
    test_hello_get(test_name)
    
    # 测试 POST 方法
    test_hello_post(test_name)
    
    print(f"\n{'='*50}")
    print("测试完成！")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()

