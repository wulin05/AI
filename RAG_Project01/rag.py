from xml.dom.minidom import Document

from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from vector_stores import VectorStoreService
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

import os


class RagService(object):
    def __init__(self):
        # 向量服务
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name)
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主, 简洁和专业的回答用户问题。参考资料: {context}。"),
                ("user", "请回答用户提问: {input}")
            ]
        )

        self.chat_model = ChatOpenAI(
            model = config.chat_model_name,
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

        self.chain = self.__get_chain()

    # 定义私有方法__get_chain()
    def __get_chain(self):
        """获取最终的执行链"""
        retriever = self.vector_service.get_retriever()

        def format_func(docs: list[Document]) -> str:
            if not docs:
                return "没有检索到相关信息"      
            formatted_str = "[\n"
            for doc in docs:
                formatted_str += f"文档片段: {doc.page_content}\n文档元数据: {doc.metadata}\n\n"
                formatted_str += "]"
            return formatted_str        

        def print_prompt(prompt):
            print(prompt.to_string()) 
            print("="*30)
            return prompt

        chain = (
            {
                "input": RunnablePassthrough(), 
                "context": retriever | format_func
            } | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        return chain
    
if __name__ == '__main__':
    res = RagService().chain.invoke("我身高168cm,体重120斤,尺码推荐!")
    print(res)
