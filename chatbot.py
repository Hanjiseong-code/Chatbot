import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="GPT-4o-mini 챗봇", page_icon="🤖")
st.title("🤖 GPT-4o-mini 챗봇")

if "OPENAI_API_KEY" not in st.secrets:
    st.error("Secrets에 OPENAI_API_KEY가 설정되지 않았습니다. 앱 Settings → Secrets에서 추가해주세요.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

with st.sidebar:
    st.header("설정")
    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
