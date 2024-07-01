import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# App title
st.title('Simple ChatBot')

# Sidebar for Hugging Face credentials
with st.sidebar:
    st.title('Login HugChat')
    hf_email = st.text_input('Enter E-mail:')
    hf_pass = st.text_input('Enter Password:', type='password')
    
    # Ensure both email and password are provided
    if not (hf_email and hf_pass):
        st.warning('Please enter your account!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')

# Store LLM generated responses in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function to generate response from HugChat
def generate_response(prompt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create ChatBot instance
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)

# Handle user input and display response
if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate and display response if last message is from the user
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt, hf_email, hf_pass) 
                st.write(response) 
        st.session_state.messages.append({"role": "assistant", "content": response})
