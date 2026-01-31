import streamlit as st
import requests
import json

# ---------------- CONFIG ----------------
API_URL = "https://emea.snaplogic.com/api/1/rest/slsched/feed/ConnectFasterInc/snapLogic4snapLogic/Sameer%20Shaikh/SL_Pipeline_Doc_Generation_V2_trig_Task"
HEADERS = {
    "Authorization": "Bearer mpsLPYJiboML00hEctZyJgBI5Mh7eD4T",
    "Content-Type": "application/json"
}
# ----------------------------------------

st.set_page_config(page_title="SnapLogic Pipeline Doc Bot", page_icon="🤖")

st.title("🤖 SnapLogic Pipeline Documentation Chatbot")

# ----------- SESSION MANAGEMENT ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------- USER INPUT ----------------
user_input = st.chat_input("Enter RUUID to generate pipeline report...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare API payload
    payload = [{
        "ruuid": user_input.strip()
    }]

    try:
        with st.spinner("Generating pipeline documentation from SnapLogic..."):
            response = requests.post(
                API_URL,
                headers=HEADERS,
                data=json.dumps(payload),
                timeout=120
            )

        if response.status_code == 200:
            api_result = response.json()
            bot_reply = api_result.get("response", "No response from API.")

        else:
            bot_reply = f"❌ API Error: {response.status_code}\n{response.text}"

    except Exception as e:
        bot_reply = f"⚠️ Error calling API:\n{str(e)}"

    # Add bot response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
