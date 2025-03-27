import streamlit as st
import requests

# ✅ Streamlit App Configuration
st.set_page_config(page_title="DeepSeek R1 Chatbot", layout="centered")

# ✅ Define API endpoint
API_URL = "http://127.0.0.3:8080/chat"

# ✅ Streamlit UI
st.title("DeepSeek R1 Chatbot")
st.write("Chat with DeepSeek R1 1.5B via Ollama.")

# System Prompt
system_prompt = st.text_area("Define AI Behavior:", height=80, placeholder="Type system prompt here...")

# User Input
user_input = st.text_area("Enter your message:", height=150, placeholder="Type your message here...")

# ✅ Submit Button
if st.button("Send"):
    if user_input.strip():
        try:
            # ✅ Send API Request
            payload = {"messages": [user_input], "system_prompt": system_prompt}
            response = requests.post(API_URL, json=payload)

            # ✅ Handle Response
            if response.status_code == 200:
                response_data = response.json()
                if "error" in response_data:
                    st.error(response_data["error"])
                else:
                    ai_response = response_data["messages"][0]["content"]
                    st.subheader("AI Response:")
                    st.markdown(f"**{ai_response}**")
            else:
                st.error(f"Request failed with status code {response.status_code}.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a message before clicking 'Send'.")
