import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

# Initialize Vertex AI and the generative model
project = "sample-gemini-427811"
vertexai.init(project=project)

config = generative_models.GenerationConfig(
    temperature=0.4
)

model = GenerativeModel(
    "gemini-pro",
    generation_config=config
)

chat = model.start_chat()

# Function to handle chat interactions
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": output
        }
    )

# Streamlit app starts here
st.title("Gemini Explorer")

# Initialize session state if not already initialized
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
query = st.chat_input("Gemini Explorer")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})
    llm_function(chat, query)

# Initial message based on whether user name is provided
if len(st.session_state.messages) == 0:
    user_name = st.text_input("Please enter your name")
    if user_name:
        initial_prompt = f"Hello {user_name}! I'm ReX, an assistant powered by Google Gemini. How can I assist you today?"
    else:
        initial_prompt = "Hello! I'm ReX, an assistant powered by Google Gemini. How can I assist you today?"
    llm_function(chat, initial_prompt)
