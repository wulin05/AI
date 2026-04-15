from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}, 刚生了{gender}, 帮忙起名字,请简略回答。"
)   

# 变量注入，生成提示词文本
prompt_text = prompt_template.format(lastname="林", gender="女")

model = Tongyi(model="qwen-max-2025-01-25")

res = model.invoke(prompt_text)

print(f"提示词文本：{prompt_text}")
print(f"模型输出：{res}")
