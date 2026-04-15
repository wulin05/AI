from cffi import api
from openai import OpenAI
import os

# 获取Client对象：创建OpenAI类对象
api_key = os.getenv("CODING_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "Missing API key. Set CODING_API_KEY (preferred) or DASHSCOPE_API_KEY or OPENAI_API_KEY."
    )

client = OpenAI(
    api_key=api_key,
    base_url="https://coding.dashscope.aliyuncs.com/v1"
)

# 调用模型
response = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[
        # system角色：设定模型的行为和规则
        {"role": "system", "content": "你是一个Python编程专家，回答精确简练不说废话"},
        # assistant角色：设定模型的回答，由用户设定
        {"role": "assistant", "content": "好的，我是编程专家，并且话不多，你要问什么？"},
        # user角色：设定用户的提问
        {"role": "user", "content": "如何安装Python？并输出1~10的代码！"},
    ]
)

# 打印结果
print(response.choices[0].message.content)