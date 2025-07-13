# 🤖 AI Curriculum Planner (Agentic RAG App)

An **agentic GenAI application** that builds personalized curriculum plans from a syllabus PDF using a team of AI **agents**, **Retrieval-Augmented Generation (RAG)**, and **Groq's LLaMA 3**. Powered by **Streamlit**, **ChromaDB**, and **Sentence Transformers** — this system gives each AI agent a focused role, enabling compositional intelligence and flexibility.

---

## 🧠 What Makes This App Unique?

This project is built using an **agentic architecture**, where each curriculum component (e.g., lesson plans, quizzes, resources) is created by a **dedicated AI agent**. These agents:

- Operate independently and only when invoked by the user
- Use shared context (retrieved via RAG) but focus on specific outputs
- Can be selectively combined and exported by the user

You’re not just generating one output — you’re coordinating a team of AI specialists!

---

## 🔧 Features (Modular Agentic Design)

✅ Upload a syllabus PDF (RAG knowledge base)  
✅ Extract text → Chunk → Embed → Store in **ChromaDB**  
✅ Enter any topic to generate a dynamic curriculum  

The following **agents** work in tandem:

| Agent                | Role                                                                 |
|---------------------|----------------------------------------------------------------------|
| 🧩 `topic_decomposer`     | Breaks down the topic into weekly subtopics using syllabus context |
| 📘 `lesson_planner`       | Creates a detailed week-by-week teaching plan                     |
| 📝 `quiz_generator`       | Generates 10+ questions per week (MCQ, short, long)               |
| 🔗 `resource_recommender` | Suggests public videos/articles for each week                     |
| 📝 `assignment_maker`     | Crafts 1–2 real-world assignments with objectives & rubrics       |
| 📤 `export_to_pdf`        | Combines all or selected agent outputs into a styled PDF          |

Each agent is only called when the user requests its output — reducing latency and enabling **selective generation**.

---

## ⚙️ Tech Stack

- 💬 **Groq API** (LLaMA 3 - lightning-fast LLM inference)
- 🧠 **Agentic Architecture** (modular, callable agents)
- 📚 **RAG Pipeline**: 
  - `sentence-transformers` for dense embeddings  
  - `chromadb` for fast local similarity search  
- 🖥️ **Streamlit** for interactive UI  
- 📄 **pdfkit + wkhtmltopdf** for PDF export  
- 💾 **DuckDB** backend (for Streamlit Cloud compatibility)

---

## 📁 Project Structure

