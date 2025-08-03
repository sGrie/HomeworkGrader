import streamlit as st
import ollama

#for now it will accept jpg but later this will need to be done with a pdf parser to make it machine readable
accepted_file_types = ["pdf", "docx", "jpg"]
llama_model = "qwen3:8b"
st.title("Llama Homework Grader")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]


### Write Message History
for msg in st.session_state.messages:
    if msg["role"] == "user":
        #msg["role"], avatar="🧑‍💻",
        prompt = st.chat_message(msg["role"]).write(msg["content"])
        st.write(prompt.text)
        # if prompt and prompt.text:
        #     st.write(prompt.text)
        # if prompt and prompt["files"]:
        #     st.image(prompt["files"][0])

    else:
        st.chat_message(msg["role"], avatar="🤖").write(msg["content"])



## Generator for Streaming Tokens
def generate_response():
    print(st.session_state.messages)
    response = ollama.chat(model=llama_model, stream=True, messages=st.session_state.messages)
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token

#, accept_file=True, file_type=accepted_file_types
prompting = st.chat_input("say something/attach a pdf or doc", accept_file=True, file_type=accepted_file_types)
if prompting:
    # if prompt and prompt.text:
    #    st.write(prompt.text)
    # if prompt and prompt["files"]:
    #    st.write(prompt["files"][0])
    st.session_state.messages.append({"role": "user", "content": prompting.text})
    #st.chat_message("user", avatar="🧑‍💻").write(prompting.text)
    #this only displays the writing
    st.chat_message("user", avatar="🧑‍💻").write(prompting.text)
    st.session_state["full_message"] = ""
    st.chat_message("assistant", avatar="🤖").write_stream(generate_response)
    st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})