import streamlit as st
import requests

# Set up the Streamlit app
st.title("Chatbot with Fact Generation")

# Chatbot Interaction Section
st.header("Chat with the Bot")

user_input = st.text_input("Enter your message:")

if st.button("Send"):
    if user_input:
        # Send user input to Flask backend
        response = requests.post("http://127.0.0.1:5000/chat", json={"input": user_input})
        if response.status_code == 200:
            bot_response = response.json().get('response', 'No response from the bot.')
            st.success(f"Bot: {bot_response}")
        else:
            st.error("Failed to get a response from the bot.")
    else:
        st.warning("Please enter a message.")

# Fact Generation Section
st.header("Generate Facts from Text")

input_text = st.text_area("Enter text for fact generation:")

if st.button("Generate Facts"):
    if input_text.strip():
        # Send text to Flask backend for fact generation
        response = requests.post("http://127.0.0.1:5000/generate-facts", json={"text": input_text})
        if response.status_code == 200:
            facts = response.json().get('facts', [])
            if facts:
                st.write("Extracted Facts:")
                for i, fact in enumerate(facts, start=1):
                    st.write(f"{i}. {fact}")
            else:
                st.info("No facts extracted.")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    else:
        st.warning("Please enter some text.")

# Run the Streamlit app by executing this file
