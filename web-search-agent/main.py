import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import os


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# main agent, used Groq API key
web_scrape_agent = Agent(
    name="Web Searching Agent",
    description="An agent that searches any query over the web.",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions="""
    ## Instructions
    - Answer clearly and concisely in markdown format. 
    - Use headings (###) for sections 
    - Use **bold** and *italics* for emphasis 
    - Use bullet points or numbered lists for clarity 
    - Add emojis where relevant to make the response engaging 
    - Always include the sources at the end
    """,
    show_tool_calls=False,
    markdown=True,
    debug_mode=False
)

# streamlit defaults UI
st.set_page_config(page_title="Web Scrape Agent", layout="centered")
st.title("Web Scrape Agent")
st.caption("Ask me anything, I'll search the web and give you a clear answer! *Developed By Sheryar*")

# stores history(kabhi kabhi, karta hai, will fix it)
if "history" not in st.session_state:
    st.session_state["history"] = []

user_input=st.chat_input("Type your question here...")

if user_input:
    # INput
    st.session_state["history"].append({"role": "user", "content": user_input})

    # Will give Line by lIne response like chatGPT
    with st.chat_message("assistant"):
        placeholder = st.empty()
        collected_text = ""

        for chunk in web_scrape_agent.run(user_input, stream=True):
            if hasattr(chunk,"content"):
                collected_text+=chunk.content
            else:
                collected_text+= str(chunk)
            placeholder.markdown(collected_text, unsafe_allow_html=True)


        st.session_state["history"].append({"role": "agent", "content": collected_text})

# Checks the history
for chat in st.session_state["history"]:
    if chat["role"]=="user":
        with st.chat_message("user"):
            st.markdown(chat["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(chat["content"], unsafe_allow_html=True)
