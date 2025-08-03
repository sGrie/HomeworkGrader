import streamlit as st
import ollama

#for now it will accept jpg but later this will need to be done with a pdf parser to make it machine readable
accepted_file_types = ["pdf", "docx", "jpg"]
llama_model = "gemma3:12b"
st.title("Llama Homework Grader")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

### Write Message History
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"], avatar="🧑‍💻").write(msg["content"])
    else:
        st.chat_message(msg["role"], avatar="🤖").write(msg["content"])

## Generator for Streaming Tokens
def generate_response():
    response = ollama.chat(model=llama_model, stream=True, messages=st.session_state.messages)
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token

prompt = st.chat_input(placeholder="Your input here", accept_file=True, file_type=accepted_file_types)
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt.text, "files": prompt.files})
    #st.chat_message("user", avatar="🧑‍💻").write(prompt)
    st.chat_message("user", avatar="🧑‍💻").write(st.session_state.messages)
    st.session_state["full_message"] = ""
    st.chat_message("assistant", avatar="🤖").write_stream(generate_response)
    st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})