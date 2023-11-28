import streamlit as st
import random
import time
import requests
import re



def tsdGPTChatbot(message, user_id):
    data = {"user_id": user_id,"question": message}
    gpt_response = requests.post(url="http://localhost:8000/ask", json=data)
    res = gpt_response.json()
    return res['answer'],res['prompt_token'],res['ai_token']


st.sidebar.image("./datawars.png")
st.sidebar.header("LLM Code Optimization")
user_id = st.sidebar.text_input(label = "User ID")

st.sidebar.write("- Write your queries regularly and without leaving too many spaces,")
st.sidebar.write("- You left the comments,")

st.title("TSD Software Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can help you?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response,prompt_token,ai_token = tsdGPTChatbot(prompt,user_id)
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")

        # if "```python\n" in message_placeholder:
        #     codes = re.findall(rf"```python\n(.*?)\n```", assistant_response, re.DOTALL)
        #     for c in codes.split():
        #             full_response += c + " "
        #             time.sleep(0.05)
        #             # Add a blinking cursor to simulate typing
        #             message_placeholder.code(full_response + "▌")

        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})


col1,col2 = st.sidebar.columns(2)


user_token_count = 0
ai_token_count = 0
if prompt:
    col1.caption("User Token: ")
    user_token_count = prompt_token + user_token_count
    col2.text(user_token_count)

    col1.caption("AI Token: ")
    ai_token_count = ai_token + ai_token_count
    col2.text(ai_token_count)
