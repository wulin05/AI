"""
LangChain 是「包装好的工具箱」，
openai SDK 是「原始零件」。 
工具箱好用但功能固定，原始零件麻烦但想怎么组装都行！
"""

from openai import OpenAI
import os

api_key = os.getenv("CODING_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "Missing API key. Set CODING_API_KEY (preferred) or DASHSCOPE_API_KEY or OPENAI_API_KEY."
    )

client = OpenAI(
    api_key=api_key,
    base_url="https://coding.dashscope.aliyuncs.com/v1",
)

messages = [{"role": "user", "content": "你是谁"}]
completion = client.chat.completions.create(
    model="qwen3.5-plus",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    extra_body={"enable_thinking": True},
    stream=True
)
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20)
for chunk in completion:
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20)
            is_answering = True
        print(delta.content, end="", flush=True)
