import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="GPT-4o-mini 챗봇", page_icon="🤖")
st.title("🤖 GPT-4o-mini 챗봇")

# Streamlit Community Cloud secrets에서 API 키 로드
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 사이드바
with st.sidebar:
    st.header("설정")
    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 추가 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성 (스트리밍)
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
