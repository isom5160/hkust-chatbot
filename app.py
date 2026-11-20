from openai import OpenAI, AuthenticationError
import streamlit as st

with st.sidebar:
    hkust_api_key = st.text_input("HKUST GenAI API Key", key="hkust_genai_api_key", type="password")
    st.caption("Enter your HKUST GenAI API key.")
    "[View the source code](https://github.com/1HD22/ISOM5160-Chatbot-Example)"

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by HKUST GenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not hkust_api_key:
        st.info("Please add your HKUST GenAI API key to continue.")
        st.stop()

    client = OpenAI(base_url="https://hkust.azure-api.net/hkust-genai/v1",
                    api_key=hkust_api_key,
                    default_headers={"api-key": hkust_api_key})
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    try:
        response = client.chat.completions.create(model="gpt-5.6-sol", messages=st.session_state.messages)
    except AuthenticationError:
        st.error("Invalid API key. Please check your HKUST GenAI API key.")
        st.stop()
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

