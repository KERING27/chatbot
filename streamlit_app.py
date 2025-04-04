import streamlit as st
from openai import OpenAI

# 챗봇 제목 및 설명
st.title("개인정보보호법 상담 챗봇")
st.write(
    "이 챗봇은 한국의 개인정보보호법 관련 질문에 대해 빠르고 정확하게 답변해주는 도우미입니다. "
    "개인정보의 수집, 이용, 제3자 제공, 보관, 파기, 위탁, 정보주체 권리 등에 대해 궁금한 점을 자유롭게 질문하세요.\n\n"
    "※ 이 서비스는 참고용이며, 법적 분쟁이나 민감한 사안은 반드시 전문가의 자문을 받으시기 바랍니다."
)

# OpenAI API 키 입력
openai_api_key = st.text_input("OpenAI API Key 입력", type="password")
if not openai_api_key:
    st.info("API 키를 입력하시면 챗봇 이용이 가능합니다.")
else:
    client = OpenAI(api_key=openai_api_key)

    # 메시지 초기화 및 시스템 프롬프트 설정
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "당신은 한국의 개인정보보호법 전문가입니다. 사용자의 질문에 대해 법적 근거와 실무 예시를 포함하여 "
                    "명확하고 쉽게 설명하세요. 가능한 한 최신 법령과 가이드를 반영하고, 필요 시 관련 법 조항도 언급하세요."
                )
            }
        ]

    # 기존 대화 표시
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 사용자 질문 입력창
    if prompt := st.chat_input("질문을 입력하세요. 예: '마케팅 목적으로 개인정보를 수집할 수 있나요?'"):

        # 사용자 질문 저장 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT 응답 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 응답 표시 및 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
