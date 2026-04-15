"""
ChatPromptTemplate: 聊天提示词模板
用于构建多轮对话的提示词模板
"""
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI
import os

# 创建聊天提示词模板
chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template("你是一个{role}，请用{tone}的语气回答问题"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)

# 创建模型实例
model = ChatOpenAI(
    model="kimi-k2.5",
    api_key=os.getenv("CODING_API_KEY") or os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://coding.dashscope.aliyuncs.com/v1"
)

# 构建 chain
chain = chat_prompt | model

try:
    # 调用时传入所有变量
    response = chain.invoke({
        "role": "语文老师",
        "tone": "温和耐心",
        "question": "如何快速提高写作水平？"
    })

    # 安全检查
    if hasattr(response, 'content') and response.content:
        print(f"✅ AI 回答：{response.content}")
    else:
        print(f"⚠️ 响应异常：{response}")

except Exception as e:
    print(f"❌ 错误：{type(e).__name__} - {e}")
