import time
import streamlit as st
import re
import json
from chains import Chains

Chains.setLlm()

# Custom image for the app icon and the assistant's avatar
company_logo = 'https://media.licdn.com/dms/image/D4E0BAQGh_NyvUObZJA/company-logo_200_200/0/1690556609027/meta_sense_fr_logo?e=1715212800&v=beta&t=um1p0g0fhqz2iHtCjyTR8wUATLfxbgHv8ysF9CqfftE'
# Configure Streamlit page
st.set_page_config(
    page_title="Metasense AI",
    page_icon=company_logo
)

def getServicesDoc():
    return "\n\n".join([k + "\n" + v + "\n" for k,v in st.session_state.services.items()])

st.header('Alogia Customer Representative', divider='rainbow')

if "services" not in st.session_state:
    doc_path = "/home/melih/Desktop/personal/clients/metasense/metasense/services.txt"
    with open(doc_path) as f:
        st.session_state.doc = f.read()
        
    with open("tree_based_data.json") as f:
        tree_based_data = json.load(f)
        category_data = "Categories:\n\n"
        for category, data in tree_based_data.items():
            category_data += f"Category Name: {category}\n"
            category_data += f"Category Description: {data['generated_description']}\n"
            category_data += "\n"*2 + "#"*50+"\n"*2
        st.session_state.category_data = category_data
        
    pattern = r"Service Title: (.*?)\n\n(.*?)(?=\n\nService Title: |\Z)"
    matches = re.findall(pattern, st.session_state.doc, flags=re.DOTALL)
    st.session_state.services = {match[0]: match[1].strip() for match in matches}
    st.session_state.questioning = True
    
# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []
# Display chat messages from history on app rerun
# Custom avatar for the assistant, default avatar for user
for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"], avatar=company_logo):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if 'messages' in st.session_state and len(st.session_state['messages']) == 0:
    st.session_state.message = []
    # Start with first message from assistant
    st.session_state['messages'] = [{"role": "assistant", 
                                  "content": "Hey there! I'm your Alogia Ergotherapy expert. Need advice or have questions about our services? I'm here to chat. What can I do for you today?"}]
    
    with st.chat_message("assistant", avatar=company_logo):
        message_placeholder = st.empty()
        full_response = ""
        # Simulate stream of response with milliseconds delay
        for chunk in st.session_state['messages'][0]["content"].split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
            
    first_customer_message = "Hi, I want to use Alogia but I don't know which service to use."
    st.session_state["history"] = f"Customer Rep:{st.session_state['messages'][0]['content']}\n\nCustomer:{first_customer_message}\n\nCustomer Rep:"
    #with st.spinner('Assistant is thinking...'):
    st.session_state.question = Chains.generateQuestion(doc=getServicesDoc(),
                                        history = st.session_state["history"])
    with st.chat_message("assistant", avatar=company_logo):
        message_placeholder = st.empty()
        full_response = ""
        # Simulate stream of response with milliseconds delay
        for chunk in st.session_state.question.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state['messages'].append({"role": "assistant", "content": st.session_state.question})
    st.session_state["history"] += "\n\n" + st.session_state.question +"\n\nCustomer:"

# Chat logic
if query := st.chat_input("Ask me anything"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state["history"] += "\n\n" + query +"\n\nCustomer Rep:"
    st.session_state.response = query
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant", avatar=company_logo):
        message_placeholder = st.empty()
        # Send user's question to our chain
        with st.spinner('Thinking...'):
            if st.session_state.questioning:
                response = Chains.generateQuestion(doc=getServicesDoc(),    
                                                   history = st.session_state["history"])
            else:
                services = Chains.eliminateServices(doc=getServicesDoc(),
                                                    question = st.session_state.question,
                                                    response = st.session_state.response)
                st.info(f"Remaining services count: {len(services)}")
                st.session_state.services = {k:st.session_state.services[k] for k in services}
                
                response = Chains.generateQuestion(doc=getServicesDoc(),
                                                   history = st.session_state["history"])
            
                
        full_response = ""

        # Simulate stream of response with milliseconds delay
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
        full_response += "\n"
        for service in st.session_state.services.keys():
            full_response += "- " + service + "\n"

        st.markdown(full_response)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.session_state["history"] += "\n\n" + st.session_state.question +"\n\nCustomer:"
    
    st.session_state.questioning = not st.session_state.questioning