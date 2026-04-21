import time
import streamlit as st

from rag import RagService
import config_data as config

# 标题
st.title("智能客服")
st.divider()         # 分隔符

# 在页面最下方提供用户输入框
prompt = st.chat_input()

# 当没有这个session_state的话，页面就无法保存历史信息
if "msg" not in st.session_state:
    st.session_state["msg"] = [{"role": "assistant", "content": "你好,有什么可以帮您呀?"}]

# 同样将这个实例对象也放到session_state里,不然每次页面刷新或者元素变更都会重新创建RagService()实例, 会导致资源浪费,影响性能。
if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for msg in st.session_state["message"]:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt:

    #在页面显示用户的提问: write(prompt)输出用户的提问！
    st.chat_message("user").write(prompt)

    # 将用户的对话信息存入到session_state列表中：[{"role": "assistant", "content": "你好,有什么可以帮您呀?"}]
    st.session_state["msg"].append({"role": "user", "content": prompt})

    ai_res_list = []
    with st.spinner("AI思考中..."):
        # 下面这些测试页面效果用的
        # time.sleep(1)
        # st.chat_message("assistant").write("你也好呀")
        # st.session_state["messages"].append({"role": "assistant", "content": "你也好呀"})
        # # 假设当用户输入提问："你好呀", 那么这时候st.session_state["message"]结果为：
        # # [
        # #     {"role": "assistant", "content": "你好,有什么可以帮您呀?"},
        # #     {"role": "user", "content": "你好"},
        # #     {"role": "assistant", "content": "你也好呀"}
        # # ]

        # res = st.session_state["rag"].chain.invoke({"input": prompt}, config.session_config)
        # st.chat_message("assistant").write(res)
        # st.session_state["messages"].append({"role": "assistent", "content": res})

        res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)

        # yield
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        st.chat_message("assistant").write_stream(capture(res_stream, ai_res_list))
        st.session_state["msg"].append({"role": "assistent", "content": "".join(ai_res_list)})

        

       
