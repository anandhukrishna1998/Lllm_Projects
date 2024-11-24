# RAG ChatBot

RAG (Retrieval-Augmented Generation) ChatBot is a conversational AI application built using **Streamlit** and **LangChain**. It allows users to upload or input data to create a custom knowledge base, enabling the chatbot to answer questions based on the provided content.

---

## Features

- **Multiple Data Input Options**:
  - Paste a URL to fetch content.
  - Upload a PDF document for processing.
  - Enter plain text directly.

- **Knowledge Base Creation**:
  - Automatically processes and stores document content using **FAISS** for fast retrieval.

- **Question Answering**:
  - Utilizes **LangChain**'s retrieval-augmented generation capabilities to answer queries with high accuracy.

- **Persistent Chat History**:
  - Keeps track of the conversation context, enabling seamless interaction.

---

## Requirements

### Python Packages
The following Python libraries are required:
- `streamlit`
- `langchain`
- `langchain_groq`
- `langchain_community`
- `PyPDF2`
- `python-dotenv`

Install them using:
```bash
pip install streamlit langchain langchain_groq langchain_community PyPDF2 python-dotenv
