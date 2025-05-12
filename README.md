# 💬 Chat with Your SQL Database using LangChain, Streamlit & Groq

This project allows you to **chat with your SQL database (SQLite or MySQL)** using [LangChain](https://www.langchain.com/), [Groq’s Llama3](https://groq.com/), and [Streamlit](https://streamlit.io/). You can ask natural language questions and get insights directly from your tables.

---

## 🚀 Features

- ✅ Chat with **SQLite (`student.db`)** or any **MySQL** database
- ✅ Uses **Groq’s Llama3-8b-8192** for fast, intelligent SQL generation
- ✅ Streamlit UI with chat history and multi-turn interaction
- ✅ Auto-detects tables and schema
- ✅ Handles repetitive loops and iteration limits gracefully

---

## 🧠 Requirements

- Python 3.9 or newer
- A valid [Groq API Key](https://console.groq.com/)
- SQLite database (`student.db`) or access to a MySQL instance

---

## 🔧 Installation

```bash
git clone https://github.com/yourusername/sql-chat-agent.git
cd sql-chat-agent
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
sql-chat-agent/
│
├── app.py                # Main Streamlit app
├── student.db            # Sample SQLite database (optional)
├── README.md             # This file
└── requirements.txt      # Dependencies
```

---

## 🧪 Sample SQLite Schema (`student.db`)

If you're using the included SQLite DB, here's what it should contain:

```sql
CREATE TABLE STUDENT (
    id INTEGER PRIMARY KEY,
    name TEXT,
    marks INTEGER
);

INSERT INTO STUDENT (name, marks) VALUES
('Alice', 75),
('Bob', 55),
('Charlie', 90);
```

---

## 🔑 How to Get a Groq API Key

1. Go to [https://console.groq.com/keys](https://console.groq.com/keys)
2. Generate an API key
3. Paste it in the Streamlit sidebar

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Then open the app in your browser and choose:

- ✅ `Use SQLite Database - student.db`
- OR
- ✅ `Connect to MySQL Database` and provide credentials

Start chatting by asking questions like:

- `Show all students with marks > 60`
- `What is the average score?`
- `How many students scored below 50?`

---

## 🛠 Troubleshooting

### ❌ Agent stuck in loop?

- Make sure `student.db` file exists and is readable
- Use `SQLDatabase.from_uri()` instead of manual `creator` function
- Ensure the table name is correct (e.g., `STUDENT`)
- Limit max iterations on agent if needed (`max_iterations=5`)

---

## 📜 License

MIT License. Free to use and modify.

---
