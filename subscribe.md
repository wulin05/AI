# 🚀 Project Name

> 简短描述：这个项目是做什么的（1~2句话）

---

## 📦 项目结构

```
project/
├── main.py
├── requirements.txt
├── README.md
└── .venv/
```

---

## 🧠 功能说明

* ✅ 功能1：xxx
* ✅ 功能2：xxx
* ✅ 功能3：调用大模型（GLM / Qwen / Kimi 等）

---

## ⚙️ 环境准备

### 1️⃣ 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate
```

---

### 2️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

如果没有 requirements.txt，可以先安装：

```bash
pip install langchain langchain-community langchain-ollama langchain-chroma dashscope chromadb
```

---

## 🔑 环境变量（API Key）

在运行前请设置 API Key，例如：

```bash
export DASHSCOPE_API_KEY="your_api_key"
```

或写入 `.env` 文件（推荐）：

```
DASHSCOPE_API_KEY=your_api_key
```

---

## ▶️ 运行项目

```bash
python main.py
```

---

## 💻 示例代码

```python
from openai import OpenAI

client = OpenAI(
    api_key="your_api_key",
    base_url="https://api.xxx.com/v1"
)

questions = ["文本1", "文本2"]

for q in questions:
    response = client.chat.completions.create(
        model="glm-5",
        messages=[
            {"role": "system", "content": "你是一个分类助手"},
            {"role": "user", "content": f"请分类: {q}"}
        ]
    )
    print(response.choices[0].message.content)
```

---

## 📄 requirements.txt 生成方式

```bash
pip freeze > requirements.txt
```

---

## 🧪 常见问题（FAQ）

### ❓ Q1：ModuleNotFoundError

👉 没激活虚拟环境：

```bash
source .venv/bin/activate
```

---

### ❓ Q2：API Key 无效

👉 检查：

* 是否设置环境变量
* key 是否过期

---

### ❓ Q3：模型报错

👉 确认：

* model 名称是否正确（如 `glm-5` / `qwen3.5-plus`）
* base_url 是否匹配

---

## 🧹 清理环境

删除虚拟环境：

```bash
rm -rf .venv
```

清理 pip 缓存：

```bash
rm -rf ~/.cache/pip
```

---

## 📌 Markdown 编写规范

### ✅ 代码块写法

```bash
pip install xxx
```

```python
print("hello")
```

---

### ❌ 错误示例（不要这样写）

```bash
(.venv) user@xxx$ pip install xxx
```

👉 会影响复制执行

---

### ✅ 行内代码

使用 `pip install` 安装依赖

---

## 📈 后续扩展

* 🔹 接入向量数据库（ChromaDB）
* 🔹 构建 RAG 系统
* 🔹 多模型对比（GLM vs Qwen vs Kimi）
* 🔹 并发请求优化

---

## 👤 作者

* Name: your_name
* Email: [xxx@example.com](mailto:xxx@example.com)

---

## 📜 License

MIT License

