# 🚀 Orion – Enterprise Multi-Agent AI Platform

## 📌 Overview

Orion is a Multi-Agent AI Platform built using LangGraph, LangChain, and Streamlit.

Instead of relying on a single AI assistant, Orion uses multiple specialized AI agents that collaborate to solve complex enterprise tasks. Each agent has a dedicated responsibility, while a Supervisor Agent coordinates the overall workflow.

This project demonstrates modern Agentic AI concepts such as planning, orchestration, delegation, tool calling, memory, and human-in-the-loop approval.

---

## 🎯 Project Objectives

- Build a working Multi-Agent AI application
- Demonstrate LangGraph orchestration
- Enable communication between specialized AI agents
- Showcase planning and delegation
- Demonstrate tool calling
- Maintain conversational memory
- Illustrate Human-in-the-Loop approval
- Demonstrate MCP integration
- Provide an intuitive Streamlit interface

---

## 🏗️ Architecture

```
                    User
                      │
                      ▼
             Streamlit Interface
                      │
                      ▼
            Supervisor Agent
                      │
                      ▼
              Planner Agent
      ┌──────────┼──────────┐
      ▼          ▼          ▼
Knowledge     SQL Agent   Report Agent
 Agent
      └──────────┼──────────┘
                 ▼
           Final Response
```

---

## 🤖 AI Agents

### Supervisor Agent
Receives user requests and coordinates the workflow.

### Planner Agent
Breaks a complex request into smaller tasks.

### Knowledge Agent
Searches enterprise documents and retrieves relevant information.

### SQL Agent
Queries structured enterprise data.

### Report Agent
Combines outputs from multiple agents into a single response.

---

## ✨ Features

- Multi-Agent Architecture
- LangGraph Orchestration
- Agent-to-Agent Communication
- Intelligent Task Planning
- Tool Calling
- Conversation Memory
- Human-in-the-Loop Approval
- MCP Integration
- Streamlit User Interface

---

## 🛠️ Technology Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| UI | Streamlit |
| AI Framework | LangChain |
| Orchestration | LangGraph |
| LLM | Ollama |
| Embeddings | all-MiniLM-L6-v2 |
| Vector Database | FAISS |
| Database | SQLite |
| IDE | VS Code |

---

## 📂 Project Structure

```
Orion/
│
├── app/
│   ├── agents/
│   ├── graph/
│   ├── tools/
│   ├── ui/
│   └── main.py
│
├── data/
├── screenshots/
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 🚀 Getting Started

### Clone the Repository

```bash
git clone <repository-url>
cd Orion
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

**Windows**

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app/main.py
```

---

## 💡 Sample Use Cases

- Summarize HR policies and employee information
- Retrieve structured and unstructured enterprise data
- Generate consolidated business reports
- Demonstrate collaborative AI agents

---

## 📚 AI Concepts Demonstrated

- Agentic AI
- Multi-Agent Systems
- LangGraph
- AI Orchestration
- Planning
- Delegation
- Tool Calling
- Memory
- Human-in-the-Loop
- MCP

---

## 📸 Screenshots

Screenshots will be added after implementation.

---

## 🔮 Future Enhancements

- Additional specialized agents
- Teams/Slack notifications
- REST API integration
- Advanced MCP servers
- Voice interface

---

## 👨‍💻 Author

Developed as part of an Enterprise AI Portfolio showcasing modern Agentic AI, Multi-Agent Systems, and AI Engineering concepts.