from langchain_core.prompts import PromptTemplate
# from langchain_community.llms.tongyi import Tongyi
from langchain_openai import ChatOpenAI
import os

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}, 刚生了{gender}, 帮忙起名字,请简略回答。"
)   

# 变量注入，生成提示词文本
prompt_text = prompt_template.format(lastname="林", gender="女")


# model = Tongyi(model="qwen-max-2025-01-25")

api_key = os.getenv("CODING_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    raise RuntimeError(
        "Missing API key. Set CODING_API_KEY (preferred) or DASHSCOPE_API_KEY."
    )

# 想告诉的是，qwen3.5-plus是新的模型,需要用langchain_openai包！
model = ChatOpenAI(
    model="qwen3.5-plus",
    api_key=api_key,
    base_url="https://coding.dashscope.aliyuncs.com/v1"
)

print(f"提示词文本：{prompt_text}")

# 流式输出
res = ""
for chunk in model.stream(prompt_text):
    content = chunk.content
    print(content, end="", flush=True)
    res += content

print()  # 换行