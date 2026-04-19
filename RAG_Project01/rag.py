from xml.dom.minidom import Document

from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from vector_stores import VectorStoreService
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableWithMessageHistory
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

import os

from file_history_store import get_history


class RagService(object):
    def __init__(self):
        # 向量服务
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name)
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主, 简洁和专业的回答用户问题。参考资料: {context}。"),
                ("system", "并且我提供用户的对话历史记录,如下:"),
                MessagesPlaceholder("history"),
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
        retriever = self.vector_service.get_retriever()      # 得到向量检索器

        def format_document(docs: list[Document]):
            if not docs:
                return "没有检索到相关信息"     
             
            formatted_str = "[\n"
            for doc in docs:
                formatted_str += f"文档片段: {doc.page_content}\n文档元数据: {doc.metadata}\n\n"
                formatted_str += "]"
            return formatted_str   
             
        # 自定义函数用来查询输入给prompt的是否有问题
        def print_prompt(prompt):
            print("="*30)
            print(prompt.to_string())
            print("="*30)
            return prompt

        def format_for_retriever(value: dict) -> str:
            # print("="*30, value)
            return value["input"]
        
        def format_for_prompt_template(value):
            # print("="*30, value)
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value

        bash_chain = (
            {
                "input": RunnablePassthrough(), 
                "context": RunnableLambda(format_for_retriever) | retriever | format_document
            } | RunnableLambda(format_for_prompt_template) | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        # 通过RunnableWithMessageHistory获取一个新的带有历史记录功能的增强对话chain
        conversation_chain = RunnableWithMessageHistory(
            bash_chain,       # 被附加历史消息的Runnable,通过是chain
            get_history,             # 获取指定会话ID的历史会话的函数: 这次不是InMemoryChatMessageHistory的类对象了,是
            input_messages_key="input",      # 声明用户输入消息在模板中的占位符
            history_messages_key="history",   # 声明历史消息在模板中的占位符
        )

        return conversation_chain
    
if __name__ == '__main__':
    # session_id的配置,具体查看Extend_21的代码
    session_config = {"configurable": {"session_id": "linwu01"}}

    # res = RagService().chain.invoke({"input": "我身高168cm,体重120斤,尺码推荐!"}, session_config)
    res = RagService().chain.invoke({"input": "我身高180cm,体重160斤,尺码推荐!"}, session_config)
    print(res)
