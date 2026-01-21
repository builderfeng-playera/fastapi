# FastAPI Hello API

一个简单的 FastAPI 应用，提供 hello API 端点。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

```bash
uvicorn main:app --reload
```

应用将在 `http://localhost:8000` 启动。

## API 端点

### GET /hello

通过查询参数传递名字：

```bash
curl "http://localhost:8000/hello?name=张三"
```

响应：
```json
{
  "message": "hello, 张三"
}
```

如果不提供名字：
```bash
curl "http://localhost:8000/hello"
```

响应：
```json
{
  "message": "hello, 世界"
}
```

### POST /hello

也可以通过 POST 方法调用：

```bash
curl -X POST "http://localhost:8000/hello?name=李四"
```

## API 文档

启动应用后，访问以下地址查看自动生成的 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

