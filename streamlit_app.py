        # 사용자 입력
        if prompt := st.chat_input("질문을 입력하세요. 예: '마케팅 목적으로 개인정보를 수집할 수 있나요?'"):

            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            normalized_prompt = prompt.strip().lower()

            # 1. 인사말 처리
            if normalized_prompt in ["안녕", "안녕하세요", "hi", "hello"]:
                greeting_response = (
                    "안녕하세요! 개인정보보호법 상담 챗봇입니다.\n"
                    "개인정보 수집·이용, 제3자 제공, 파기 절차, 정보주체 권리 등 궁금한 내용을 자유롭게 질문해주세요."
                )
                with st.chat_message("assistant"):
                    st.markdown(greeting_response)
                st.session_state.messages.append({"role": "assistant", "content": greeting_response})

            # 2. "강조하여 표기" 관련 질문 처리
            elif "강조하여 표기" in normalized_prompt or "명확히 강조" in normalized_prompt:
                emphasize_response = (
                    "**개인정보 수집·이용 동의서**에는 다음 항목들을 **명확히 강조하여 표기**해야 합니다 "
                    "(개인정보 보호법 시행령 제17조 제1항 기준):\n\n"
                    "- **개인정보 수집·이용 목적**\n"
                    "- **수집하는 개인정보 항목**\n"
                    "- **보유 및 이용 기간**\n"
                    "- **동의를 거부할 권리와 그에 따른 불이익 내용**\n\n"
                    "이 항목들은 **굵은 글씨, 색상, 밑줄 등 시각적으로 눈에 띄도록** 표시해야 하며, "
                    "정보주체가 내용을 명확히 인식하고 동의할 수 있도록 구성해야 합니다."
                )
                with st.chat_message("assistant"):
                    st.markdown(emphasize_response)
                st.session_state.messages.append({"role": "assistant", "content": emphasize_response})

            # 3. 일반 질문은 OpenAI GPT 처리
            else:
                stream = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )

                with st.chat_message("assistant"):
                    response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
