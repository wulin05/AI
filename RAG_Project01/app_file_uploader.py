"""
基于Streamlit完成WEB网页文件上传服务
pip install streamlit

Streamlit: 当WEB页面元素发生变化,则代码重新执行一遍,所以原生的保存状态是非常困难的
所以,Streamlit使用了session_state来解决这个问题

"""
import time

import streamlit as st
from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.title("知识库更新服务")

# 创建文件上传组件
uploaded_file = st.file_uploader(
    "选择一个文件进行上传", 
    type=["txt", "pdf", "docx"],
    accept_multiple_files=False   #False只允许上传单个文件,不接受多文件上传
)

# 通过注释知道,直接创建KnowledgeBaseService类对象的话,每次页面有更新(上传文件),就会重载,每次都在创建这个类对象,影响性能
# service = KnowledgeBaseService()
# 所以可以将该状态保存到session_state中
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

# session_state是一个字典,由用户自己决定存储的内容,比如上面的KnowledgeBaseService实例对象,或者下面的数值,都行。
# if "counter" not in st.session_state:
#     st.session_state["counter"] = 0

# 如果用户上传了文件
if uploaded_file is not None:
    file_name = uploaded_file.name
    file_type = uploaded_file.type
    file_size = uploaded_file.size / 1024  # 转换为KB

    st.subheader(f"文件名: {file_name}")
    st.write(f"文件类型: {file_type}")
    st.write(f"文件大小: {file_size:.2f} KB")

    # get_value()方法获取上传的文件对象，并返回文件内容的字节数组bytes -> decode("utf-8")将字节数据解码为字符串
    text = uploaded_file.getvalue().decode("utf-8")  # 获取文件内容并解码为字符串
    # st.write("文件内容预览: ")
    # st.write(text)

#     st.session_state["counter"] += 1

    # 为了更好的用户体验
    with st.spinner("载入知识库中..."):
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)



# print(f'上传了{st.session_state["counter"]}个文件')





    # # 读取文件内容（根据文件类型进行处理）
    # if uploaded_file.type == "text/plain":
    #     content = uploaded_file.read().decode("utf-8")
    #     st.text_area("文件内容预览", content, height=300)
    # elif uploaded_file.type == "application/pdf":
    #     st.warning("PDF文件预览功能尚未实现")
    # elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
    #     st.warning("Word文档预览功能尚未实现")