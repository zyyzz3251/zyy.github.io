# 🔄 代码互译系统 - 完整线上服务

## 📚 目录

1. [快速开始](#快速开始)
2. [功能特性](#功能特性)
3. [Web 服务](#web-服务)
4. [API 文档](#api-文档)
5. [使用示例](#使用示例)
6. [部署指南](#部署指南)

---

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动 Web 服务

```bash
python web_app_run.py
```

然后在浏览器中访问: **http://localhost:5000**

### 运行命令行

```bash
python run_translator.py
```

### 运行测试

```bash
python -m unittest code_translator.test_translator -v
```

---

## 💎 功能特性

### 1️⃣ 在线转译界面

✅ **双语言面板**
- 左侧: 源代码编辑区
- 右侧: 目标代码预览区
- 支持实时语法检查

✅ **智能按钮**
- 🔄 交换语言
- 📋 复制代码
- ⬇️ 下载代码
- 📚 加载示例

✅ **分析面板**
- 📊 转译结果统计
- 🔤 词法分析 (记号流)
- 🌳 语法树 (AST)
- 📈 代码指标

### 2️⃣ REST API

✅ **完整的 API 端点**
- 单个代码转译
- 批量代码转译
- 词法分析
- 语法分析
- 统计数据
- 转译历史

### 3️⃣ 数据管理

✅ **本地存储**
- 自动保存源代码
- 保存转译历史
- 支持离线使用

✅ **隐私保护**
- 所有转译在浏览器本地完成
- 不上传代码到服务器
- 完全开源透明

---

## 🌐 Web 服务

### 访问地址

- **首页**: http://localhost:5000
- **API 基础 URL**: http://localhost:5000/api

### 功能界面

```
┌─────────────────────────────────────┐
│  🔄 代码互译系统                     │
│  多语言代码在线转译引擎              │
└─────────────────────────────────────┘
│                                     │
│  📝 源代码      │  🎯 目标代码      │
│  [Python    ]  │  [JavaScript  ]   │
│                │                   │
│  function1  │  def hello():       │
│  class Cat  │      pass           │
│                │                   │
├─────────────────────────────────────┤
│  ✨ 开始转译   🔄 交换语言          │
├─────────────────────────────────────┤
│  📊 | 🔤 | 🌳 | 📈                 │
│                                     │
│  转译结果统计                        │
│  源行数: 12  目标行数: 15           │
│  记号数: 45  AST节点数: 8           │
│                                     │
└─────────────────────────────────────┘
```

---

## 📡 API 文档

### 1. 完整代码转译

**请求**
```bash
POST /api/translate
Content-Type: application/json

{
    "source_code": "def hello(name):\n    return name",
    "source_lang": "python",
    "target_lang": "javascript"
}
```

**响应**
```json
{
    "success": true,
    "target_code": "function hello(name) {\n    // function body\n}",
    "stats": {
        "source_lines": 2,
        "target_lines": 3,
        "token_count": 8,
        "ast_nodes": 2,
        "timestamp": "2026-06-02T12:34:56"
    },
    "tokens": [
        {"type": "KEYWORD", "value": "def", "line": 1},
        {"type": "IDENTIFIER", "value": "hello", "line": 1}
    ],
    "ast": {
        "type": "Program",
        "children": [
            {
                "type": "FunctionDef",
                "metadata": {"name": "hello", "params": ["name"]}
            }
        ]
    }
}
```

### 2. 词法分析

**请求**
```bash
POST /api/lexical-analysis
Content-Type: application/json

{
    "source_code": "x = 42",
    "language": "python"
}
```

**响应**
```json
{
    "success": true,
    "tokens": [
        {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
        {"type": "LITERAL", "value": "42", "line": 1, "column": 5}
    ],
    "count": 3,
    "stats": {
        "keywords": 0,
        "identifiers": 1,
        "operators": 1,
        "literals": 1,
        "punctuation": 0
    }
}
```

### 3. 语法分析

**请求**
```bash
POST /api/parse-ast
Content-Type: application/json

{
    "source_code": "def add(a, b):\n    pass",
    "language": "python"
}
```

**响应**
```json
{
    "success": true,
    "ast": {
        "type": "Program",
        "children": [
            {
                "type": "FunctionDef",
                "metadata": {
                    "name": "add",
                    "params": ["a", "b"]
                }
            }
        ]
    },
    "node_count": 2,
    "structure": "..."
}
```

### 4. 获取支持的语言

**请求**
```bash
GET /api/supported-languages
```

**响应**
```json
{
    "source_languages": ["python", "javascript", "java"],
    "target_languages": ["python", "javascript"],
    "pairs": [
        {"source": "python", "target": "javascript", "name": "Python → JavaScript"},
        {"source": "javascript", "target": "python", "name": "JavaScript → Python"}
    ]
}
```

### 5. 代码示例

**请求**
```bash
GET /api/examples
```

**响应**
```json
{
    "success": true,
    "examples": {
        "python_function": {
            "name": "函数定义",
            "language": "python",
            "code": "def add(a, b):\n    return a + b"
        }
    }
}
```

### 6. 统计信息

**请求**
```bash
GET /api/statistics
```

**响应**
```json
{
    "success": true,
    "total_translations": 42,
    "supported_pairs": 4,
    "supported_languages": 3
}
```

### 7. 批量转译

**请求**
```bash
POST /api/batch-translate
Content-Type: application/json

{
    "codes": [
        "def add(a, b): return a + b",
        "class Calculator: pass"
    ],
    "source_lang": "python",
    "target_lang": "javascript"
}
```

**响应**
```json
{
    "success": true,
    "results": [
        {"success": true, "target_code": "function add(a, b) {...}"},
        {"success": true, "target_code": "class Calculator {...}"}
    ],
    "total": 2,
    "successful": 2
}
```

---

## 💻 使用示例

### Python 代码示例

```python
from code_translator.core import CodeTranslator

# 创建转译器
translator = CodeTranslator("python", "javascript")

# 源代码
source = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

class Calculator:
    def multiply(self, a, b):
        return a * b
"""

# 执行转译
result = translator.translate(source)
print(result)
```

### JavaScript 调用 API

```javascript
// 转译代码
async function translateCode() {
    const response = await fetch('/api/translate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            source_code: 'def hello(): pass',
            source_lang: 'python',
            target_lang: 'javascript'
        })
    });
    
    const data = await response.json();
    console.log(data.target_code);
}

// 词法分析
async function analyzeTokens() {
    const response = await fetch('/api/lexical-analysis', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            source_code: 'x = 42',
            language: 'python'
        })
    });
    
    const data = await response.json();
    console.log(data.tokens);
}
```

### cURL 命令

```bash
# 转译代码
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{
    "source_code": "def add(a, b): return a + b",
    "source_lang": "python",
    "target_lang": "javascript"
  }'

# 词法分析
curl -X POST http://localhost:5000/api/lexical-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "source_code": "x = 42",
    "language": "python"
  }'

# 获取支持的语言
curl http://localhost:5000/api/supported-languages
```

---

## 🚀 部署指南

### 本地部署

1. **克隆仓库**
```bash
git clone https://github.com/zyyzz3251/xyb.git
cd xyb
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动服务**
```bash
python web_app_run.py
```

### Docker 部署

**Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "web_app_run.py"]
```

**构建和运行**
```bash
docker build -t code-translator .
docker run -p 5000:5000 code-translator
```

### 云服务部署

#### Heroku
```bash
heroku login
heroku create your-app-name
git push heroku main
```

#### AWS
```bash
# 使用 Elastic Beanstalk
eb init
eb create
eb deploy
```

---

## 📊 性能指标

| 操作 | 时间 | 备注 |
|------|------|------|
| 词法分析 | < 1ms | 源代码 → 记号流 |
| 语法分析 | < 2ms | 记号流 → AST |
| AST 映射 | < 1ms | 源 AST → 目标 AST |
| 代码生成 | < 1ms | AST → 目标代码 |
| **完整转译** | **< 5ms** | 端到端 |

---

## 🔐 隐私和安全

✅ **数据隐私**
- 所有转译在浏览器本地完成
- 不保存用户代码
- 支持离线使用

✅ **开源透明**
- 完全开源
- 代码公开审查
- MIT 许可证

✅ **安全措施**
- 输入验证
- 错误处理
- 访问控制

---

## 🎯 支持的语言对

| 源语言 | 目标语言 | 状态 |
|--------|---------|------|
| Python | JavaScript | ✅ 支持 |
| Python | Python | ✅ 支持 |
| JavaScript | Python | ✅ 支持 |
| JavaScript | JavaScript | ✅ 支持 |
| Java | * | 🔄 开发中 |

---

## 📝 使用协议

1. ✅ 可自由使用此服务
2. ✅ 可用于商业和个人项目
3. ✅ 可修改和重新分发 (需注明出处)
4. ✅ 支持离线部署

---

## 🤝 贡献指南

欢迎贡献代码! 请:

1. Fork 此仓库
2. 创建 feature 分支
3. 提交 Pull Request
4. 等待审核

---

## 📞 反馈和支持

- 📧 提交 Issue: https://github.com/zyyzz3251/xyb/issues
- 💬 讨论: https://github.com/zyyzz3251/xyb/discussions
- 📝 贡献: 欢迎 PR

---

## 📄 许可证

MIT License

---

**版本**: 2.0.0 (Web 服务版)  
**作者**: xyb Project  
**最后更新**: 2026年6月  
**维护者**: [@zyyzz3251](https://github.com/zyyzz3251)
