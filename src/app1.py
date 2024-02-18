import time
import streamlit as st
from chains import Chains

# Custom image for the app icon and the assistant's avatar
company_logo = 'https://media.licdn.com/dms/image/D4E0BAQGh_NyvUObZJA/company-logo_200_200/0/1690556609027/meta_sense_fr_logo?e=1715212800&v=beta&t=um1p0g0fhqz2iHtCjyTR8wUATLfxbgHv8ysF9CqfftE'
# Configure Streamlit page
st.set_page_config(
    page_title="Metasense AI",
    page_icon=company_logo
)

openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    type="password",
)

st.header('Alogia Customer Representative', divider='rainbow')

if not openai_api_key:
    st.warning("Please enter your OpenAI API Key!", icon="⚠️")
    st.stop()

if "doc" not in st.session_state:
    doc_path = "services.txt"
    with open(doc_path) as f:
        st.session_state.doc = f.read()
    
    st.session_state.initial_advice = "Introduce yourself as Alogia Ergotherapy expert. Ask the user's needs and problems in an original way."
    st.session_state.history = ""
    st.session_state.lang = "french"
    # Initialize chat history
    st.session_state.messages = []
    Chains.setLlm(openai_api_key=openai_api_key)
    
    
# Display chat messages from history on app rerun
# Custom avatar for the assistant, default avatar for user
for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"], avatar=company_logo):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if 'messages' in st.session_state and len(st.session_state.messages) == 0:
    # Start with first message from assistant
    with st.spinner('Agent is being initialized...'):
        response, translated_response = Chains.reply(doc=st.session_state.doc, 
                                                     history=st.session_state.history, 
                                                     advice=st.session_state.initial_advice,
                                                     lang=st.session_state.lang)
    
    st.session_state.messages.append({"role": "assistant", 
                                        "content": translated_response})
    st.session_state.history = "Customer Rep: " + response
    with st.chat_message("assistant", avatar=company_logo):
        message_placeholder = st.empty()
        full_response = ""
        # Simulate stream of response with milliseconds delay
        for chunk in translated_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

# Chat logic
if query := st.chat_input("Type"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    translated_query, st.session_state.lang = Chains.translate(query)
    st.session_state.history += "\n\nCustomer:" + translated_query
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant", avatar=company_logo):
        message_placeholder = st.empty()
        # Send user's question to our chain
        with st.spinner('Thinking...'):
            response, translated_response = Chains.reply(doc=st.session_state.doc, 
                                                         history=st.session_state.history, 
                                                         lang=st.session_state.lang)            
        full_response = ""

        # Simulate stream of response with milliseconds delay
        for chunk in translated_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": translated_response})
    
    st.session_state.history += "\n\nCustomer Rep:" + response