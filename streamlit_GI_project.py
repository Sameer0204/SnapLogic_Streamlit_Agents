import streamlit as st
import requests

# Configure the Streamlit app
st.set_page_config(page_title="SnapLogic Customer Success Story Chatbot", page_icon="🤖", layout="centered")

# Title and intro
st.title("🤖 SnapLogic Customer Success Story Chatbot")
st.caption("Ask anything related to customer stories and digital EDI workflows.")

# Initialize session state to store messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hello! I’m your SnapLogic Agent. How can I help you today?"
        }
    ]

# API configuration
API_URL = "https://emea.snaplogic.com/api/1/rest/slsched/feed/ConnectFasterInc/snapLogic4snapLogic/Bootcamp_EMEA_June_2025/AgentDriver_Customer_story_Agent_GI_Trig_Task"
HEADERS = {
    "Authorization": "Bearer ij6UhQJJWE9a7vIDVJANBnzqZ1bEuZNk",
    "Content-Type": "application/json"
}

# Function to call the SnapLogic pipeline
def fetch_snaplogic_response(user_prompt):
    payload = [{"prompt": user_prompt}]
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "✅ Request successful, but no response content.")
        elif response.status_code == 500:
            return "🚨 Server Error 500: Something went wrong in the SnapLogic pipeline."
        else:
            return f"❌ Error {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"⚠️ Request failed: {str(e)}"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field at the bottom
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("SnapLogic Agent is thinking..."):
            response = fetch_snaplogic_response(user_input)
            st.markdown(response)

    # Append assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})
