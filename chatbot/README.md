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

### Setup Instructions
1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_name>
2. Install the required packages:
    `pip install -r requirements.txt`

3. Set Up Environment Variables: Create a .env file in the root directory and add your Groq API key:
    `GROQ_API_KEY=your_groq_api_key`


### Run the Application
Run the application using: `streamlit run app.py`

This will start the chatbot application, which can be accessed in your browser at http://localhost:8501.