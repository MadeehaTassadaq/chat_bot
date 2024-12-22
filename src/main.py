import os
import json
import streamlit as st
from groq import Groq
work_dir = os.path.dirname(os.path.abspath(__file__))
# Load the data from the json file
with open(os.path.join(work_dir, "config.json"), "r") as file:
    data = json.load(file)
GROQ_API_KEY = data["GROQ_API_KEY"]
# save the API key to the environment variable
os.environ["GROQ_API_KEY"]  = data["GROQ_API_KEY"]
# stream page config
st.set_page_config(
    page_title="Medical Chatbot",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)
# Set the title of the web app
st.title("Medical Chatbot")

# create the instance of the Grog class
client=Groq()
# initialize the chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
# display the chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]): 
        st.markdown(message["content"]) 
# get the user input
user_input = st.chat_input("Ask me anything")

# get the response from the chatbot
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})
# send the user input to the chatbot
messages=[
    {"role":"assistant","content":"You are a helpful assistant"},
    *st.session_state.chat_history
    ]

response=client.chat.completions.create(    
        model="llama3-8b-8192",
         messages=messages,
    )

# display the response
assistant_response=response.choices[0].message.content
st.session_state.chat_history.append({"role":"assistant","content":assistant_response})
 
  # display the LLM's response
with st.chat_message("assistant"):
    st.markdown(assistant_response)
