import streamlit as st
import requests

# Streamlit page configuration
st.set_page_config(page_title="SnapLogic Retriever Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 SnapLogic Customer Story Retriever Chatbot")
st.write("Ask your questions to get insights from the SnapLogic Retriever Agent.")

# Initialize session state for conversation history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# API Configuration
API_URL = "https://emea.snaplogic.com/api/1/rest/slsched/feed/ConnectFasterInc/snapLogic4snapLogic/Bootcamp_EMEA_June_2025/Retriver_Customer_story_Agent_GI_Trig_Task"
API_HEADERS = {
    "Authorization": "Bearer kkHKBG3FiPc4Wfz2OB6qGcNnuHJbLVTL",
    "Content-Type": "application/json"
}

# Function to call API and get response
def get_api_response(question):
    payload = [{"Questions": question}]
    try:
        response = requests.post(API_URL, headers=API_HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and 'content' in data[0]:
            return data[0]['content']
        else:
            return "Unexpected response format from API."
    except requests.exceptions.RequestException as e:
        return f"API Error: {e}"

# Chat input box
user_input = st.text_input("You:", key="input")

if st.button("Send") and user_input.strip() != "":
    # Store user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get bot response from API
    bot_response = get_api_response(user_input)
    
    # Store bot's response
    st.session_state.messages.append({"role": "bot", "content": bot_response})

# Display conversation history
for message in st.session_state.messages:
    if message['role'] == 'user':
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Bot:** {message['content']}")

