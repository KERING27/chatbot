import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 개인정보보호법 도우미")
st.write(
    "안녕하세요! 이 챗봇은 OpenAI의 GPT 모델을 활용하여 **개인정보 보호법**에 대한 궁금증을 해결해드립니다. "
    "개인정보 수집·이용, 제공, 파기, 정보주체의 권리 등 관련된 법률 및 실무 지식에 대해 질문해보세요.\n\n"
    "⚠️ 이 챗봇은 참고용이며, 법적 자문이 필요한 경우 전문 변호사와 상담하시기 바랍니다."
)
# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management

# OpenAI API 키 입력
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
   # 초기 시스템 메시지 설정 (선택사항)
        st.session_state.messages = [
            {
                "role": "system",
                "content": "당신은 한국의 개인정보보호법 전문가입니다. 사용자의 질문에 대해 친절하고 정확하게 설명하세요."
            }
        ]
 # 이전 메시지 표시
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("개인정보 보호법에 대해 궁금한 점을 물어보세요! 예: '동의 없이 개인정보를 수집하면 어떤 처벌을 받나요??"):

        # 사용자 메시지 저장 및 출력
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI 응답 생성
        stream = client.chat.completions.create(
            model="gpt-4o mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        
        # 응답 출력 및 저장
        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
