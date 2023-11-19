# Second
import streamlit as st 
from openai import OpenAI

PROMPT = """
Your name is 'Custom QA Bot', following is data provided by user you have to repond to user question accurately and according to user, try to give best results
"""

# set config
st.set_page_config(
    page_title="Custom Q&A With ChatGPT",
    page_icon="📝",
    menu_items={"About": "https://github.com/ArnavK-09"},
)

def cut_text_under_limit(input_text, max_tokens=3000):
    tokens = input_text.split()
    current_token_count = 0
    truncated_text = []

    for token in tokens:
        current_token_count += len(token)  # Adjust this based on your actual token definition
        if current_token_count <= max_tokens:
            truncated_text.append(token)
        else:
            break

    return ' '.join(truncated_text)

with st.sidebar:
    api_key = st.text_input("OpenAI API Key", key="file_qa_api_key", type="password", placeholder="Api Key Please :)")
    """
    # 🔐 It's Safe
    ## [Get Your Api Key Here](https://platform.openai.com)
    """

st.title("📝 Custom Q&A") 
file = st.file_uploader("Upload your text file", type=("txt", "md")) 
question = st.chat_input(
    placeholder="Provide me a short summary?",
    disabled=not file or not api_key,
    max_chars=500,
)

if "messages" not in st.session_state:
    st.session_state["messages"] = []
    st.chat_message("assistant").write("> Please enter your OpenAI API key in sidebar input to use this app!")

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if file and question and api_key:
    data = file.read().decode()
    data = cut_text_under_limit(data)
    data_msg = f"""## Data: \n\n{data}\n\n---\n## Question: {question}"""
    ai = OpenAI(api_key=api_key)
    st.session_state.messages.append({"role": "user", "content": data_msg})
    st.chat_message("human").write(data_msg)
    msgs = st.session_state.messages.copy()
    msg = msgs.insert(0, {"role": "user", "content": PROMPT})
    completion = ai.chat.completions.create(model="gpt-3.5-turbo", messages=msgs)
    msg = completion.choices[0].message.content
    st.session_state.messages.append({"role":"assistant","content": msg})
    st.chat_message("assistant").write(msg)