from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_community.chat_models.tongyi import ChatTongyi
import os

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个浪漫诗人,可以天马行空作诗"),
        MessagesPlaceholder("history"),
        ("human", "请再来一首古诗:"),
    ]
)

historr_data = [
    ("human", "你来个唐诗"),
    ("ai", "床前明月光,疑是地上霜,举头望明月,低头思故乡"),
    ("human", "好诗,再来一首"),
    ("ai", "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。")
]

# StringPromptValue
prompt_text = chat_prompt_template.invoke({"history": historr_data}).to_string()
# prompt_text = chat_prompt_template.invoke({"history": historr_data})

# print(prompt_text)

# model = ChatTongyi(mode="kimi-k2.5",temperature=0.7)  # 这个ok~
# model = ChatTongyi(model="qwen3.5-plus",temperature=0.7)   # 这个不行, qwen3.5-plus → 是新模型 → 只支持 OpenAI兼容接口
model = ChatTongyi(mode="qwen3-max",temperature=0.7)  # 这个ok~

# model = ChatOpenAI(model="qwen-max")   # 报错,由于我定义的key名称不是OPENAI_API_KEY,所以必须手动指定是用哪个key

# 推荐用：from langchain_openai import ChatOpenAI
# model = ChatOpenAI(
#     model="qwen3-max",
#     api_key=os.getenv("DASHSCOPE_API_KEY"),
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
# )

# 不知道为什么用这个非常慢
# model = ChatOpenAI(
#     model="qwen3.5-plus",
#     api_key=os.getenv("CODING_API_KEY"),
#     base_url="https://coding.dashscope.aliyuncs.com/v1"
# )

res = model.invoke(prompt_text)
print(res.content)




