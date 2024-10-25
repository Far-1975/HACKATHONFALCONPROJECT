import streamlit as st
import numpy as np
import random
import time
import streamlit as st
import requests
from requests.exceptions import RequestException
import random
from nltk.chat.util import Chat, reflections



API_KEY2 = "ai71-api-573ef5e3-71e1-471d-b8ed-68d6a69c492f"
API_URL = "https://api.ai71.ai/v1/chat/completions"


st.title("Medical Chatbot")

# Set a default model (if needed)
if "model_page_2" not in st.session_state:
    st.session_state["model_page_2"] = "tiiuae/falcon-180B-chat"

# Function to get response from the medical assistant API
def get_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY2}",
        "Content-Type": "application/json"
    }
    data = {
    "model": st.session_state["model_page_2"],  # Ensure valid model
    "messages": [
        {"role": "system", "content": "You are a doctor. Provide clear and accurate medical advice."},
        {"role": "user", "content": prompt}
    ],
    "max_tokens": 100  # Limit the response length
}

    try:
      response = requests.post(API_URL, headers=headers, json=data)
      response.raise_for_status()
      response_json = response.json()
      st.write(response_json)  # Log the full response
      return response_json["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as http_err:
     st.error(f"HTTP error occurred: {http_err}")
     st.error(f"Response content: {response.content}")  # Log the response content
     return None

# Initialize chat history
if "messages_page_2" not in st.session_state:
    st.session_state["messages_page_2"] = []

# Display chat messages from history on app rerun
for message in st.session_state["messages_page_2"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is your medical concern?"):
    # Add user message to chat history
    st.session_state["messages_page_2"].append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from the medical assistant API
    response = get_response(prompt)
    # Add assistant response to chat history
    st.session_state["messages_page_2"].append({"role": "assistant", "content": response})
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
pairs = [
    [
        r"(.*)health(.*)",
        ["Health is important. How are you feeling today?", ]
    ],
    [
        r"(.*)fever(.*)",
        ["It seems like you might have a fever. Have you checked your temperature?", ]
    ],
    [
        r"(.*)cough(.*)",
        ["Coughing can be a symptom of various conditions. Do you have any other symptoms?", ]
    ],
    [
        r"(.*)quit",
        ["Goodbye! Take care.", ]
    ]
]

def get_response(user_input):
    chatbot = Chat(pairs, reflections)
    return chatbot.respond(user_input)
def display_chatbot_ui():
    st.subheader("Ask the Chatbot")
    # Add chatbot-related fields and response sections here
    user_input = st.text_input("Type your question:")
    if user_input:
        st.write("Chatbot response here...")  # Replace with actual chatbot functionality
