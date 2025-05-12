import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

# Set up page
st.set_page_config(page_title="LangChain: Chat with SQL DB")
st.title("LangChain: Chat with SQL DB")

# Sidebar DB options
radio_opt = ["Use SQLite Database - student.db", "Connect to MySQL Database"]
selected_opt = st.sidebar.radio("Choose the database you want to chat with", options=radio_opt)

# DB credentials input
if selected_opt == radio_opt[1]:
    db_uri = "MYSQL"
    mysql_host = st.sidebar.text_input("MySQL Hostname")
    mysql_user = st.sidebar.text_input("MySQL User")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database Name")
else:
    db_uri = "SQLITE"

# Groq API Key
api_key = st.sidebar.text_input("Groq API Key", type="password")
if not api_key:
    st.warning("Please enter your Groq API Key.")
    st.stop()

# Load Groq LLM
llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

# Cached database configuration
@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == "SQLITE":
        db_path = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite://", creator=creator))
    elif db_uri == "MYSQL":
        if not all([mysql_host, mysql_user, mysql_password, mysql_db]):
            st.error("Please provide all MySQL credentials.")
            st.stop()
        engine = create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}")
        return SQLDatabase(engine)
    else:
        st.error("Unsupported DB type.")
        st.stop()

# Initialize DB
if db_uri == "MYSQL":
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_uri)

# Create SQL Agent Toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Correct agent setup (no need for AgentExecutor separately)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Chat history
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
user_query = st.chat_input("Ask anything from the database...")

if user_query:
    st.session_state["messages"].append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        try:
            response = agent.run(user_query, callbacks=[streamlit_callback])
        except Exception as e:
            response = f"❌ Error: {str(e)}"
        st.session_state["messages"].append({"role": "assistant", "content": response})
        st.write(response)
