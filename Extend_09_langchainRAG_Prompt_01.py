"""
基于PromptTemplate类可以得到提示词模板，支持基于模板注入变量得到最终提示词
・zero-shot思想，可以基于PromptTemplate直接完成
・few-shot思想下,需要更换为FewShotPromptTemplate(后续内容)

PS：使用PromptTemplate还不如自己手动拼接字符串？
・使用Template模板构建提示词，在大型工程中更容易做标注化模板
・Template模板类，支持LangChain框架的链式调用(Runnable接口,后续内容)
  ・ PromptTemplate
  ・ FewShotPromptTemplate
  ・ ChatPromptTempalte
"""

from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}, 刚生了{gender}, 帮忙起名字,请简略回答。"
)

model = Tongyi(model="qwen-max-2025-01-25")

# 生成链
chain = prompt_template | model

# 基于链,调用模型获取结果
res = chain.invoke({"lastname": "林", "gender": "女"})

print(res)